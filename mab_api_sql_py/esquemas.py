from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EventoEntrada(BaseModel):
    codigo_experimento: str = Field(..., min_length=3)
    nome_experimento: str | None = None
    nome_variante: str = Field(..., min_length=1)
    tipo_evento: str = Field(..., pattern="^(impressao|clique)$")
    timestamp_evento: datetime | None = None
    usuario_id: str | None = None
    contexto: dict[str, Any] | None = None
    id_evento_externo: str | None = None


class RespostaSaude(BaseModel):
    status: str
    banco: str


class VarianteRecomendacao(BaseModel):
    nome_variante: str
    percentual_trafego: float
    probabilidade_vitoria: float
    impressos: int
    cliques: int
    ctr_estimado: float


class RespostaRecomendacao(BaseModel):
    codigo_experimento: str
    janela_analise_dias: int
    metodo: str
    variantes: list[VarianteRecomendacao]

