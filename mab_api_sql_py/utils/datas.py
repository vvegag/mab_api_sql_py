from __future__ import annotations

from datetime import UTC, datetime, timedelta


def agora_utc() -> datetime:
    return datetime.now(tz=UTC)


def inicio_janela(data_base: datetime, dias: int) -> datetime:
    return data_base - timedelta(days=dias)


def normalizar_utc(data: datetime) -> datetime:
    if data.tzinfo is None:
        return data.replace(tzinfo=UTC)
    return data.astimezone(UTC)
