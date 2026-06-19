from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracaoApp:
    database_url: str
    janela_analise_dias: int = 7
    numero_amostras_thompson: int = 5000
    alocacao_minima_variante: float = 0.05
    seed_reprodutibilidade: int = 42


def carregar_configuracao() -> ConfiguracaoApp:
    return ConfiguracaoApp(
        database_url=os.getenv("DATABASE_URL", "sqlite:///./mabandit.db"),
        janela_analise_dias=int(os.getenv("JANELA_ANALISE_DIAS", "7")),
        numero_amostras_thompson=int(os.getenv("NUMERO_AMOSTRAS_THOMPSON", "5000")),
        alocacao_minima_variante=float(os.getenv("ALOCACAO_MINIMA_VARIANTE", "0.05")),
        seed_reprodutibilidade=int(os.getenv("SEED_REPRODUTIBILIDADE", "42")),
    )

