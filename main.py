from __future__ import annotations

from dataclasses import replace

from fastapi import FastAPI

from mab_api_sql_py.api.rotas import roteador_api
from mab_api_sql_py.banco.conexao import FabricaBanco
from mab_api_sql_py.configuracao import carregar_configuracao
from mab_api_sql_py.seed import garantir_dados_iniciais


def criar_app(database_url: str | None = None) -> FastAPI:
    """Cria a aplicação FastAPI já com banco e rotas configurados."""
    configuracao = carregar_configuracao()
    if database_url is not None:
        # Permite sobrescrever o banco em testes locais sem mexer no .env.
        configuracao = replace(configuracao, database_url=database_url)
    fabrica_banco = FabricaBanco(configuracao.database_url)
    fabrica_banco.criar_tabelas()

    app = FastAPI(
        title="API de Otimizacao Multi-Armed Bandit",
        version="1.0.0",
        description="API para ingestao de eventos, agregacao SQL e recomendacao de trafego via Thompson Sampling.",
    )
    app.state.fabrica_banco = fabrica_banco
    app.state.configuracao = configuracao

    # Injeta dados iniciais para que a API suba pronta para demonstração.
    garantir_dados_iniciais(app)
    app.include_router(roteador_api)
    return app


app = criar_app()
