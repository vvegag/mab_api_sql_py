from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from mab_api_sql_py.banco.modelos import AgregadoDiario, EventoBruto, Experimento, Variante
from mab_api_sql_py.dominio.modelos import EstatisticaVariante
from mab_api_sql_py.utils.datas import normalizar_utc
from mab_api_sql_py.utils.constantes import TIPO_EVENTO_CLIQUE, TIPO_EVENTO_IMPRESSAO


def obter_ou_criar_experimento(sessao: Session, codigo_experimento: str, nome_experimento: str | None) -> Experimento:
    """Busca um experimento existente ou cria um novo registro base."""
    experimento = sessao.scalar(select(Experimento).where(Experimento.codigo_experimento == codigo_experimento))
    if experimento:
        return experimento
    experimento = Experimento(
        codigo_experimento=codigo_experimento,
        nome_experimento=nome_experimento or codigo_experimento,
    )
    sessao.add(experimento)
    sessao.flush()
    return experimento


def obter_ou_criar_variante(
    sessao: Session,
    id_experimento: int,
    nome_variante: str,
    eh_controle: bool = False,
) -> Variante:
    """Busca uma variante existente ou cria uma nova para o experimento."""
    variante = sessao.scalar(
        select(Variante).where(
            Variante.id_experimento == id_experimento,
            Variante.nome_variante == nome_variante,
        )
    )
    if variante:
        return variante
    variante = Variante(id_experimento=id_experimento, nome_variante=nome_variante, eh_controle=eh_controle)
    sessao.add(variante)
    sessao.flush()
    return variante


def registrar_evento_bruto(
    sessao: Session,
    id_experimento: int,
    id_variante: int,
    tipo_evento: str,
    timestamp_evento: datetime,
    usuario_id: str | None,
    contexto: dict | None,
    id_evento_externo: str | None,
) -> EventoBruto:
    """Persiste o evento linha a linha para manter rastreabilidade total."""
    evento = EventoBruto(
        id_experimento=id_experimento,
        id_variante=id_variante,
        tipo_evento=tipo_evento,
        timestamp_evento=timestamp_evento,
        usuario_id=usuario_id,
        contexto=contexto,
        id_evento_externo=id_evento_externo,
    )
    sessao.add(evento)
    sessao.flush()
    return evento


def atualizar_agregado_diario(
    sessao: Session,
    id_experimento: int,
    id_variante: int,
    timestamp_evento: datetime,
    tipo_evento: str,
) -> AgregadoDiario:
    """Atualiza o consolidado do dia para leitura eficiente do bandit."""
    timestamp_evento = normalizar_utc(timestamp_evento)
    data_referencia = timestamp_evento.replace(hour=0, minute=0, second=0, microsecond=0)
    agregado = sessao.scalar(
        select(AgregadoDiario).where(
            AgregadoDiario.id_experimento == id_experimento,
            AgregadoDiario.id_variante == id_variante,
            AgregadoDiario.data_referencia == data_referencia,
        )
    )
    if agregado is None:
        agregado = AgregadoDiario(
            id_experimento=id_experimento,
            id_variante=id_variante,
            data_referencia=data_referencia,
            impressos=0,
            cliques=0,
        )
        sessao.add(agregado)

    if tipo_evento == TIPO_EVENTO_IMPRESSAO:
        agregado.impressos += 1
    elif tipo_evento == TIPO_EVENTO_CLIQUE:
        agregado.cliques += 1
    agregado.atualizado_em = datetime.now(tz=timezone.utc)
    sessao.flush()
    return agregado


def buscar_estatisticas_variantes(
    sessao: Session,
    id_experimento: int,
    janela_dias: int,
    data_base: datetime,
) -> list[EstatisticaVariante]:
    """Agrupa cliques e impressões dentro da janela analítica configurada."""
    data_inicio = data_base - timedelta(days=janela_dias)
    # A query lê o histórico recente e converte os eventos em estatísticas por variante.
    query = text(
        """
        SELECT
            v.nome_variante AS nome_variante,
            COALESCE(SUM(CASE WHEN e.tipo_evento = :tipo_impressao THEN 1 ELSE 0 END), 0) AS impressos,
            COALESCE(SUM(CASE WHEN e.tipo_evento = :tipo_clique THEN 1 ELSE 0 END), 0) AS cliques
        FROM variantes v
        LEFT JOIN eventos_brutos e
            ON e.id_variante = v.id_variante
           AND e.id_experimento = v.id_experimento
           AND e.timestamp_evento >= :data_inicio
           AND e.timestamp_evento <= :data_base
        WHERE v.id_experimento = :id_experimento
        GROUP BY v.nome_variante
        ORDER BY v.nome_variante
        """
    )
    resultado = sessao.execute(
        query,
        {
            "id_experimento": id_experimento,
            "data_inicio": data_inicio,
            "data_base": data_base,
            "tipo_impressao": TIPO_EVENTO_IMPRESSAO,
            "tipo_clique": TIPO_EVENTO_CLIQUE,
        },
    )
    estatisticas: list[EstatisticaVariante] = []
    for linha in resultado.fetchall():
        estatisticas.append(
            EstatisticaVariante(
                nome_variante=linha.nome_variante,
                impressos=int(linha.impressos or 0),
                cliques=int(linha.cliques or 0),
            )
        )
    return estatisticas


def salvar_recomendacao(
    sessao: Session,
    id_experimento: int,
    data_referencia: datetime,
    metodo: str,
    payload_json: dict,
):
    """Grava a recomendação gerada para auditoria e comparação futura."""
    from mab_api_sql_py.banco.modelos import RecomendacaoDiaria

    recomendacao = RecomendacaoDiaria(
        id_experimento=id_experimento,
        data_referencia=data_referencia,
        metodo=metodo,
        payload_json=payload_json,
    )
    sessao.add(recomendacao)
    sessao.flush()
    return recomendacao


def listar_variantes(sessao: Session, id_experimento: int) -> list[Variante]:
    """Lista todas as variantes conhecidas para um experimento."""
    resultado = sessao.scalars(select(Variante).where(Variante.id_experimento == id_experimento).order_by(Variante.nome_variante))
    return list(resultado)
