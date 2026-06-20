from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class EventoEntrada(BaseModel):
    codigo_experimento: str = Field(..., min_length=3, description="Código estável do experimento")
    nome_experimento: str | None = None
    nome_variante: str = Field(..., min_length=1, description="Nome legível da variante")
    tipo_evento: str = Field(..., pattern="^(impressao|clique)$", description="Tipo do evento bruto")
    timestamp_evento: datetime | None = None
    usuario_id: str | None = None
    contexto: dict[str, Any] | None = None
    id_evento_externo: str | None = None

    @field_validator("codigo_experimento", "nome_experimento", "nome_variante", "usuario_id", "id_evento_externo", mode="before")
    @classmethod
    def remover_espacos_e_normalizar_vazios(cls, valor: Any):
        """Remove espaços desnecessários e converte strings vazias em `None` nos campos opcionais."""
        if valor is None:
            return None
        if isinstance(valor, str):
            texto = valor.strip()
            if texto == "":
                return None
            return texto
        return valor

    @model_validator(mode="after")
    def validar_timestamp(self):
        """Rejeita timestamps muito à frente do horário atual para evitar dados incoerentes."""
        if self.timestamp_evento is None:
            return self
        limite_futuro = datetime.now(tz=timezone.utc).replace(microsecond=0)
        if self.timestamp_evento.tzinfo is None:
            timestamp = self.timestamp_evento.replace(tzinfo=timezone.utc)
        else:
            timestamp = self.timestamp_evento.astimezone(timezone.utc)
        if timestamp > limite_futuro:
            raise ValueError("timestamp_evento não pode estar no futuro.")
        return self


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
