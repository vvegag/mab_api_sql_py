from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from main import criar_app


def test_fluxo_basico_api():
    database_path = Path(__file__).resolve().parents[1] / "teste_mabandit.db"
    if database_path.exists():
        database_path.unlink()
    database_url = f"sqlite:///{database_path}"
    app = criar_app(database_url=database_url)
    cliente = TestClient(app)

    resposta_saude = cliente.get("/saude")
    assert resposta_saude.status_code == 200
    assert resposta_saude.json()["status"] == "ok"

    payload_impressao = {
        "codigo_experimento": "experimento_teste",
        "nome_experimento": "Teste CTR",
        "nome_variante": "controle",
        "tipo_evento": "impressao",
    }
    payload_clique = {
        "codigo_experimento": "experimento_teste",
        "nome_experimento": "Teste CTR",
        "nome_variante": "controle",
        "tipo_evento": "clique",
    }
    cliente.post("/eventos", json=payload_impressao)
    cliente.post("/eventos", json=payload_clique)
    cliente.post(
        "/eventos",
        json={
            "codigo_experimento": "experimento_teste",
            "nome_experimento": "Teste CTR",
            "nome_variante": "variante_a",
            "tipo_evento": "impressao",
        },
    )

    resposta = cliente.get("/recomendacao/experimento_teste")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["codigo_experimento"] == "experimento_teste"
    assert len(corpo["variantes"]) >= 1
