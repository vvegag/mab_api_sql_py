# API de Otimização Multi-Armed Bandit com SQL

Esta solução foi desenhada como um case de entrevista para receber eventos linha a linha, persistir os dados em SQL, consolidar histórico e recomendar a alocação de tráfego do próximo dia com Thompson Sampling.

## O que esta entrega mostra

- API REST com FastAPI;
- persistência em PostgreSQL;
- eventos brutos e agregados diários;
- suporte a múltiplas variantes desde o início;
- recomendação estatística para o dia seguinte;
- documentação em português.

## Estrutura de alto nível

- `POST /eventos`: ingestão de eventos;
- `GET /recomendacao/{codigo_experimento}`: recomenda a alocação;
- `GET /saude`: health check.

## Principais decisões

- evento bruto para auditoria e rastreabilidade;
- agregado diário para consulta eficiente;
- Thompson Sampling com Beta para CTR;
- Docker Compose para reprodução simples;
- nomes e documentação em português para facilitar explicação.

## Arquivos de apoio para a entrevista

- `docs/pt/roteiro_apresentacao_case.md`
- `docs/pt/decisoes_arquiteturais.md`
- `docs/pt/arquitetura.md`
- `docs/pt/payloads.md`
- `docs/pt/perguntas_e_roteiro_entrevista.md`
- `docs/pt/prompt_notebooklm.md`

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
- adicionar fila para ingestão assíncrona;
- medir drift e performance do modelo ao longo do tempo.

## Observação

O foco aqui foi manter a solução clara, reproduzível e fácil de explicar. A arquitetura está pronta para evoluir sem precisar reescrever o fluxo central.
