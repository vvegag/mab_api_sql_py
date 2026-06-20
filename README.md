# API de Otimização Multi-Armed Bandit com SQL

Esta solução foi desenhada como um case de entrevista para receber eventos linha a linha, persistir os dados em SQL, consolidar histórico e recomendar a alocação de tráfego do próximo dia com Thompson Sampling.

## O que esta entrega mostra

- API REST com FastAPI;
- persistência em PostgreSQL;
- eventos brutos e agregados diários;
- suporte a múltiplas variantes desde o início;
- recomendação estatística para o dia seguinte;
- validação de entrada para evitar dados ruins;
- documentação em português.

## Estrutura de alto nível

- `POST /eventos`: ingestão de eventos;
- `GET /recomendacao/{codigo_experimento}`: recomenda a alocação do próximo dia;
- `GET /saude`: health check.

## Principais decisões

- evento bruto para auditoria e rastreabilidade;
- agregado diário para consulta eficiente;
- Thompson Sampling com distribuição Beta para CTR;
- Docker Compose para reprodução simples;
- nomes e documentação em português para facilitar a explicação.

## Arquivos de apoio técnico

- `docs/pt/arquitetura.md`
- `docs/pt/decisoes_arquiteturais.md`
- `docs/pt/payloads.md`

## Materiais pessoais

Materiais de preparação pessoal para entrevista e estudo ficam fora do repositório público.

## Como executar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

## Como executar com Docker

```powershell
docker compose up --build
```

## Como testar

```powershell
pytest -q
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

## Fluxo da solução

1. o evento chega na API;
2. o payload é validado;
3. o evento bruto é salvo no banco;
4. o agregado diário é atualizado;
5. a recomendação consulta o histórico recente;
6. Thompson Sampling calcula a alocação sugerida;
7. a API retorna os percentuais recomendados.

## Como evoluir o projeto

- incluir dashboards de monitoramento;
- adicionar particionamento por data;
- ampliar para receita e eCPM;
- adicionar fila para ingestão assíncrona;
- medir drift e performance do modelo ao longo do tempo;
- incluir observabilidade com métricas e alertas;
- publicar uma versão de demonstração em ambiente controlado.

## Observação

O foco aqui foi manter a solução clara, reproduzível e fácil de explicar. A arquitetura está pronta para evoluir sem reescrever o fluxo central.
