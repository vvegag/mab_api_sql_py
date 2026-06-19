from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from mab_api_sql_py.banco.modelos import Experimento
from mab_api_sql_py.banco.repositorio import (
    obter_ou_criar_experimento,
    obter_ou_criar_variante,
    registrar_evento_bruto,
    atualizar_agregado_diario,
)
from mab_api_sql_py.esquemas import EventoEntrada, RespostaRecomendacao, RespostaSaude, VarianteRecomendacao
from mab_api_sql_py.servicos.recomendacao import gerar_recomendacao
from mab_api_sql_py.utils.datas import normalizar_utc
from mab_api_sql_py.utils.constantes import TIPO_EVENTO_CLIQUE, TIPO_EVENTO_IMPRESSAO

roteador_api = APIRouter()


def obter_sessao(request: Request):
    with request.app.state.fabrica_banco.obter_sessao() as sessao:
        yield sessao


@roteador_api.get("/saude", response_model=RespostaSaude)
def saude(request: Request):
    return RespostaSaude(status="ok", banco=request.app.state.configuracao.database_url)


@roteador_api.post("/eventos")
def registrar_evento(evento: EventoEntrada, sessao: Session = Depends(obter_sessao)):
    timestamp_evento = normalizar_utc(evento.timestamp_evento or datetime.now(tz=timezone.utc))
    experimento = obter_ou_criar_experimento(sessao, evento.codigo_experimento, evento.nome_experimento)
    variante = obter_ou_criar_variante(sessao, experimento.id_experimento, evento.nome_variante)
    evento_bruto = registrar_evento_bruto(
        sessao=sessao,
        id_experimento=experimento.id_experimento,
        id_variante=variante.id_variante,
        tipo_evento=evento.tipo_evento,
        timestamp_evento=timestamp_evento,
        usuario_id=evento.usuario_id,
        contexto=evento.contexto,
        id_evento_externo=evento.id_evento_externo,
    )
    agregado = atualizar_agregado_diario(
        sessao=sessao,
        id_experimento=experimento.id_experimento,
        id_variante=variante.id_variante,
        timestamp_evento=timestamp_evento,
        tipo_evento=evento.tipo_evento,
    )
    return {
        "status": "registrado",
        "id_evento": evento_bruto.id_evento,
        "id_experimento": experimento.id_experimento,
        "id_variante": variante.id_variante,
        "agregado_diario": {
            "impressos": agregado.impressos,
            "cliques": agregado.cliques,
            "data_referencia": agregado.data_referencia.isoformat(),
        },
    }


@roteador_api.get("/recomendacao/{codigo_experimento}", response_model=RespostaRecomendacao)
def recomendacao(
    codigo_experimento: str,
    request: Request,
    sessao: Session = Depends(obter_sessao),
):
    experimento = sessao.scalar(select(Experimento).where(Experimento.codigo_experimento == codigo_experimento))
    if experimento is None:
        return RespostaRecomendacao(codigo_experimento=codigo_experimento, janela_analise_dias=request.app.state.configuracao.janela_analise_dias, metodo="thompson_sampling", variantes=[])

    payload = gerar_recomendacao(
        sessao=sessao,
        id_experimento=experimento.id_experimento,
        codigo_experimento=experimento.codigo_experimento,
        janela_dias=request.app.state.configuracao.janela_analise_dias,
        numero_amostras=request.app.state.configuracao.numero_amostras_thompson,
        alocacao_minima_variante=request.app.state.configuracao.alocacao_minima_variante,
        seed=request.app.state.configuracao.seed_reprodutibilidade,
    )
    return payload
