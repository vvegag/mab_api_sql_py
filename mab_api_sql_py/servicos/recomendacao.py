from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from mab_api_sql_py.bandit.thompson_sampling import calcular_alocacao_thompson, serializar_alocacoes
from mab_api_sql_py.banco.repositorio import buscar_estatisticas_variantes, listar_variantes, salvar_recomendacao
from mab_api_sql_py.dominio.modelos import AlocacaoVariante


def gerar_recomendacao(
    sessao: Session,
    id_experimento: int,
    codigo_experimento: str,
    janela_dias: int,
    numero_amostras: int,
    alocacao_minima_variante: float,
    seed: int,
) -> dict:
    """Gera e persiste a recomendação do próximo dia para um experimento."""
    data_base = datetime.now(tz=timezone.utc)
    estatisticas = buscar_estatisticas_variantes(sessao, id_experimento=id_experimento, janela_dias=janela_dias, data_base=data_base)

    if not estatisticas:
        # Se ainda não houver histórico suficiente, distribuímos o tráfego de forma uniforme.
        variantes = listar_variantes(sessao, id_experimento)
        if not variantes:
            return {
                "codigo_experimento": codigo_experimento,
                "janela_analise_dias": janela_dias,
                "metodo": "thompson_sampling",
                "variantes": [],
            }
        quota = 1.0 / len(variantes)
        alocacoes = [
            AlocacaoVariante(
                nome_variante=variante.nome_variante,
                percentual_trafego=quota,
                probabilidade_vitoria=quota,
                impressos=0,
                cliques=0,
                ctr_estimado=0.0,
            )
            for variante in variantes
        ]
    else:
        alocacoes = calcular_alocacao_thompson(
            estatisticas=estatisticas,
            numero_amostras=numero_amostras,
            alocacao_minima_variante=alocacao_minima_variante,
            seed=seed,
        )

    payload = {
        "codigo_experimento": codigo_experimento,
        "janela_analise_dias": janela_dias,
        "metodo": "thompson_sampling",
        "variantes": serializar_alocacoes(alocacoes),
    }
    salvar_recomendacao(
        sessao=sessao,
        id_experimento=id_experimento,
        data_referencia=data_base,
        metodo="thompson_sampling",
        payload_json=payload,
    )
    return payload
