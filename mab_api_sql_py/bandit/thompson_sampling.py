from __future__ import annotations

from dataclasses import asdict

import numpy as np

from mab_api_sql_py.dominio.modelos import AlocacaoVariante, EstatisticaVariante


def calcular_alocacao_thompson(
    estatisticas: list[EstatisticaVariante],
    numero_amostras: int,
    alocacao_minima_variante: float,
    seed: int | None = None,
) -> list[AlocacaoVariante]:
    if not estatisticas:
        return []

    if len(estatisticas) == 1:
        unica = estatisticas[0]
        return [
            AlocacaoVariante(
                nome_variante=unica.nome_variante,
                percentual_trafego=1.0,
                probabilidade_vitoria=1.0,
                impressos=unica.impressos,
                cliques=unica.cliques,
                ctr_estimado=unica.ctr_estimado,
            )
        ]

    rng = np.random.default_rng(seed)
    amostras = np.vstack([rng.beta(item.alpha, item.beta, size=numero_amostras) for item in estatisticas])
    vencedores = np.argmax(amostras, axis=0)
    probabilidades_brutas = np.bincount(vencedores, minlength=len(estatisticas)) / float(numero_amostras)

    piso = min(max(alocacao_minima_variante, 0.0), 1.0 / len(estatisticas))
    probabilidades = np.maximum(probabilidades_brutas, piso)
    probabilidades = probabilidades / probabilidades.sum()

    resultados: list[AlocacaoVariante] = []
    for estatistica, probabilidade_bruta, probabilidade_final in zip(estatisticas, probabilidades_brutas, probabilidades, strict=True):
        resultados.append(
            AlocacaoVariante(
                nome_variante=estatistica.nome_variante,
                percentual_trafego=float(probabilidade_final),
                probabilidade_vitoria=float(probabilidade_bruta),
                impressos=estatistica.impressos,
                cliques=estatistica.cliques,
                ctr_estimado=estatistica.ctr_estimado,
            )
        )

    resultados.sort(key=lambda item: item.percentual_trafego, reverse=True)
    return resultados


def serializar_alocacoes(alocacoes: list[AlocacaoVariante]) -> list[dict]:
    return [asdict(item) for item in alocacoes]
