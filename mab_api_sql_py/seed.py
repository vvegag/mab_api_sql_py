from __future__ import annotations

from datetime import timezone

from fastapi import FastAPI
from sqlalchemy import select

from mab_api_sql_py.banco.modelos import Experimento
from mab_api_sql_py.banco.repositorio import obter_ou_criar_experimento, obter_ou_criar_variante
from mab_api_sql_py.utils.constantes import (
    CODIGO_EXPERIMENTO_PADRAO,
    NOME_EXPERIMENTO_PADRAO,
    NOME_VARIANTE_A,
    NOME_VARIANTE_B,
    NOME_VARIANTE_CONTROLE,
)


def garantir_dados_iniciais(app: FastAPI) -> None:
    fabrica_banco = app.state.fabrica_banco
    with fabrica_banco.obter_sessao() as sessao:
        existe = sessao.scalar(select(Experimento.id_experimento).limit(1))
        if existe is not None:
            return

        experimento = obter_ou_criar_experimento(sessao, CODIGO_EXPERIMENTO_PADRAO, NOME_EXPERIMENTO_PADRAO)
        obter_ou_criar_variante(sessao, experimento.id_experimento, NOME_VARIANTE_CONTROLE, eh_controle=True)
        obter_ou_criar_variante(sessao, experimento.id_experimento, NOME_VARIANTE_A, eh_controle=False)
        obter_ou_criar_variante(sessao, experimento.id_experimento, NOME_VARIANTE_B, eh_controle=False)

