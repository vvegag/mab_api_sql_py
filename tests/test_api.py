from __future__ import annotations

from fastapi.testclient import TestClient

from main import criar_app


def test_fluxo_basico_api():
    app = criar_app()
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

    resposta_payload_invalido = cliente.post(
        "/eventos",
        json={
            "codigo_experimento": "   ",
            "nome_experimento": "Teste CTR",
            "nome_variante": "controle",
            "tipo_evento": "impressao",
        },
    )
    assert resposta_payload_invalido.status_code == 422

    resposta_timestamp_futuro = cliente.post(
        "/eventos",
        json={
            "codigo_experimento": "experimento_teste",
            "nome_experimento": "Teste CTR",
            "nome_variante": "controle",
            "tipo_evento": "impressao",
            "timestamp_evento": "2999-01-01T00:00:00Z",
        },
    )
    assert resposta_timestamp_futuro.status_code == 422

    resposta = cliente.get("/recomendacao/experimento_teste")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["codigo_experimento"] == "experimento_teste"
    assert len(corpo["variantes"]) >= 1
