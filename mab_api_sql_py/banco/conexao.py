from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from mab_api_sql_py.banco.modelos import Base


@dataclass
class FabricaBanco:
    database_url: str

    def __post_init__(self) -> None:
        kwargs = {"future": True, "pool_pre_ping": True}
        if self.database_url.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
        self.engine: Engine = create_engine(self.database_url, **kwargs)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, future=True)

    def criar_tabelas(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def obter_sessao(self):
        sessao = self.SessionLocal()
        try:
            yield sessao
            sessao.commit()
        except Exception:
            sessao.rollback()
            raise
        finally:
            sessao.close()

