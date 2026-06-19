# API de Otimizacao Multi-Armed Bandit com SQL

Esta solucao foi desenhada como um case de entrevista para receber eventos linha a linha, persistir os dados em SQL, consolidar historico e recomendar a alocacao de trafego do proximo dia com Thompson Sampling.

## O que esta entrega mostra

- API REST com FastAPI;
- persistencia em PostgreSQL;
- eventos brutos e agregados diarios;
- suporta multiplas variantes desde o inicio;
- recomendacao estatistica para o dia seguinte;
- documentacao em portugues com apoio em ingles.

## Estrutura de alto nivel

- `POST /eventos`: ingestao de eventos;
- `GET /recomendacao/{codigo_experimento}`: recomenda alocacao;
- `GET /saude`: health check.

## Principais decisoes

- evento bruto para auditoria e rastreabilidade;
- agregado diario para consulta eficiente;
- Thompson Sampling com Beta para CTR;
- Docker Compose para reproducao simples;
- nomes e documentacao em portugues para facilitar explicacao.

## Arquivos de apoio para a entrevista

- `docs/pt/roteiro_apresentacao_case.md`
- `docs/pt/decisoes_arquiteturais.md`
- `docs/pt/arquitetura.md`
- `docs/pt/payloads.md`
- `docs/en/architecture.md`
- `docs/en/payloads.md`

## Como executar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

## Com Docker

```powershell
docker compose up --build
```

## Exemplo de evento

```json
{
  "codigo_experimento": "experimento_ctr_homepage",
  "nome_experimento": "CTR homepage",
  "nome_variante": "controle",
  "tipo_evento": "impressao",
  "timestamp_evento": "2026-06-18T12:00:00Z",
  "usuario_id": "u_123",
  "contexto": {
    "pagina": "home",
    "dispositivo": "mobile"
  }
}
```

## Como evoluir o projeto

- incluir dashboards de monitoramento;
- adicionar particionamento por data;
- ampliar para receita e eCPM;
- adicionar fila para ingestao assicrona;
- medir drift e performance do modelo ao longo do tempo.

## Observacao

O foco aqui foi manter a solucao clara, reproduzivel e facil de explicar. A arquitetura esta pronta para evoluir sem precisar reescrever o fluxo central.
