from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EstatisticaVariante:
    nome_variante: str
    impressos: int
    cliques: int

    @property
    def falhas(self) -> int:
        return max(self.impressos - self.cliques_validos, 0)

    @property
    def cliques_validos(self) -> int:
        return min(self.cliques, self.impressos)

    @property
    def alpha(self) -> int:
        return self.cliques_validos + 1

    @property
    def beta(self) -> int:
        return self.falhas + 1

    @property
    def ctr_estimado(self) -> float:
        return self.cliques_validos / self.impressos if self.impressos else 0.0


@dataclass(slots=True)
class AlocacaoVariante:
    nome_variante: str
    percentual_trafego: float
    probabilidade_vitoria: float
    impressos: int
    cliques: int
    ctr_estimado: float
