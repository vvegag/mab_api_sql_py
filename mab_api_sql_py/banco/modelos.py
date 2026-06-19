from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Experimento(Base):
    __tablename__ = "experimentos"

    id_experimento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_experimento: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    nome_experimento: Mapped[str] = mapped_column(String(255), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    variantes: Mapped[list["Variante"]] = relationship(back_populates="experimento", cascade="all, delete-orphan")


class Variante(Base):
    __tablename__ = "variantes"
    __table_args__ = (UniqueConstraint("id_experimento", "nome_variante", name="uq_variante_experimento_nome"),)

    id_variante: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_experimento: Mapped[int] = mapped_column(ForeignKey("experimentos.id_experimento"), nullable=False, index=True)
    nome_variante: Mapped[str] = mapped_column(String(120), nullable=False)
    eh_controle: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    metadata_variante: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    experimento: Mapped["Experimento"] = relationship(back_populates="variantes")


class EventoBruto(Base):
    __tablename__ = "eventos_brutos"

    id_evento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_experimento: Mapped[int] = mapped_column(ForeignKey("experimentos.id_experimento"), nullable=False, index=True)
    id_variante: Mapped[int] = mapped_column(ForeignKey("variantes.id_variante"), nullable=False, index=True)
    tipo_evento: Mapped[str] = mapped_column(String(30), nullable=False)
    timestamp_evento: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    usuario_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contexto: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    id_evento_externo: Mapped[str | None] = mapped_column(String(120), nullable=True, unique=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class AgregadoDiario(Base):
    __tablename__ = "agregados_diarios"
    __table_args__ = (UniqueConstraint("id_experimento", "id_variante", "data_referencia", name="uq_agregado_diario"),)

    id_agregado: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_experimento: Mapped[int] = mapped_column(ForeignKey("experimentos.id_experimento"), nullable=False, index=True)
    id_variante: Mapped[int] = mapped_column(ForeignKey("variantes.id_variante"), nullable=False, index=True)
    data_referencia: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    impressos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cliques: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class RecomendacaoDiaria(Base):
    __tablename__ = "recomendacoes_diarias"

    id_recomendacao: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_experimento: Mapped[int] = mapped_column(ForeignKey("experimentos.id_experimento"), nullable=False, index=True)
    data_referencia: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    metodo: Mapped[str] = mapped_column(String(120), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
