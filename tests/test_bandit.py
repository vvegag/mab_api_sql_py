from __future__ import annotations

from mab_api_sql_py.bandit.thompson_sampling import calcular_alocacao_thompson
from mab_api_sql_py.dominio.modelos import EstatisticaVariante


def test_thompson_sampling_retorna_alocacao_somando_um():
    estatisticas = [
        EstatisticaVariante(nome_variante="controle", impressos=100, cliques=4),
        EstatisticaVariante(nome_variante="variante_a", impressos=120, cliques=10),
        EstatisticaVariante(nome_variante="variante_b", impressos=80, cliques=6),
    ]
    alocacoes = calcular_alocacao_thompson(estatisticas, numero_amostras=2000, alocacao_minima_variante=0.05, seed=42)
    total = sum(item.percentual_trafego for item in alocacoes)
    assert len(alocacoes) == 3
    assert abs(total - 1.0) < 1e-9
    assert alocacoes[0].percentual_trafego >= alocacoes[-1].percentual_trafego

