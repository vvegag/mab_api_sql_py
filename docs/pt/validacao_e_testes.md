# Validação e Testes da Solução

Este documento registra um roteiro prático para validar a API localmente e com Docker, além de demonstrar a auditoria dos dados e a recomendação gerada pelo algoritmo.

## Objetivo

Validar que a solução:

- sobe corretamente;
- recebe eventos linha a linha;
- persiste eventos brutos e agregados no banco;
- calcula recomendação com Thompson Sampling;
- pode ser auditada via SQL;
- funciona tanto no bash local quanto com Docker.

## 1. Execução local no bash

### 1.1 Ativar o ambiente virtual

```bash
source .venv/Scripts/activate
```

Se você estiver no PowerShell, o comando equivalente é:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 1.2 Subir a API

```bash
uvicorn main:app --reload
```

Resultado esperado:

- a API sobe em `http://127.0.0.1:8000`;
- a documentação Swagger fica disponível em `/docs`;
- o endpoint de saúde responde em `/saude`.

### 1.3 Testar a saúde da aplicação

```bash
curl http://127.0.0.1:8000/saude
```

Resultado esperado:

```json
{"status":"ok","banco":"..."}
```

### 1.4 Registrar um evento válido

```bash
curl -X POST "http://127.0.0.1:8000/eventos" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_experimento":"experimento_teste",
    "nome_experimento":"Teste CTR",
    "nome_variante":"controle",
    "tipo_evento":"impressao"
  }'
```

Resultado esperado:

- status de registro com sucesso;
- retorno do `id_evento`;
- atualização do agregado diário.

### 1.5 Registrar um clique para o mesmo experimento

```bash
curl -X POST "http://127.0.0.1:8000/eventos" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_experimento":"experimento_teste",
    "nome_experimento":"Teste CTR",
    "nome_variante":"controle",
    "tipo_evento":"clique"
  }'
```

Resultado esperado:

- o total de cliques sobe;
- o CTR estimado passa a refletir o novo evento.

### 1.6 Validar rejeição de entrada inválida

```bash
curl -X POST "http://127.0.0.1:8000/eventos" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_experimento":"   ",
    "nome_experimento":"Teste CTR",
    "nome_variante":"controle",
    "tipo_evento":"impressao"
  }'
```

Resultado esperado:

- resposta `422 Unprocessable Entity`;
- o payload inválido é rejeitado antes de chegar ao processamento.

### 1.7 Consultar a recomendação

```bash
curl http://127.0.0.1:8000/recomendacao/experimento_teste
```

Resultado esperado:

- retorno com o `codigo_experimento`;
- janela de análise;
- método `thompson_sampling`;
- lista de variantes com CTR estimado e percentual de tráfego.

## 2. Execução com Docker

### 2.1 Subir os serviços

```bash
docker compose up --build
```

Resultado esperado:

- container da API em execução;
- container do PostgreSQL em execução e saudável.

### 2.2 Verificar os containers

```bash
docker compose ps
```

Resultado esperado:

- um container para a API;
- um container para o banco.

### 2.3 Testar a saúde da API dentro do ambiente Docker

```bash
curl http://127.0.0.1:8000/saude
```

Resultado esperado:

```json
{"status":"ok","banco":"postgresql+psycopg2://..."}
```

## 3. Carga de exemplo com múltiplas variantes

Para simular um experimento maior, você pode registrar vários eventos com diferentes variantes.

### Exemplo conceitual

- `controle`
- `variante_a`
- `variante_b`

Depois de popular o banco com volume suficiente, consulte os agregados e a recomendação.

## 4. Auditoria via SQL

### 4.1 Consultar agregados diários

```sql
SELECT
    ex.codigo_experimento,
    v.nome_variante,
    a.data_referencia,
    a.impressos,
    a.cliques
FROM agregados_diarios a
JOIN experimentos ex ON ex.id_experimento = a.id_experimento
JOIN variantes v ON v.id_variante = a.id_variante
   AND v.id_experimento = a.id_experimento
WHERE ex.codigo_experimento = 'experimento_volume_5000'
ORDER BY v.nome_variante, a.data_referencia;
```

Resultado esperado:

- visão consolidada por variante;
- conferência de impressões e cliques por dia.

### 4.2 Consultar a última recomendação salva

```sql
SELECT
    r.metodo,
    r.payload_json
FROM recomendacoes_diarias r
JOIN experimentos ex ON ex.id_experimento = r.id_experimento
WHERE ex.codigo_experimento = 'experimento_volume_5000'
ORDER BY r.id_recomendacao DESC
LIMIT 1;
```

Resultado esperado:

- método usado na recomendação;
- JSON com a distribuição de tráfego sugerida.

### 4.3 Inspecionar eventos brutos

```sql
SELECT
    e.id_evento,
    ex.codigo_experimento,
    v.nome_variante,
    e.tipo_evento,
    e.timestamp_evento
FROM eventos_brutos e
JOIN experimentos ex ON ex.id_experimento = e.id_experimento
JOIN variantes v ON v.id_variante = e.id_variante
WHERE ex.codigo_experimento = 'experimento_teste'
ORDER BY e.id_evento;
```

Resultado esperado:

- trilha de auditoria linha a linha;
- confirmação de que o dado bruto foi persistido.

## 5. O que demonstrar na entrevista

### Fluxo mínimo

1. subir a API;
2. registrar eventos;
3. verificar persistência;
4. consultar recomendação;
5. auditar resultados via SQL.

### O que o avaliador deve perceber

- controle de entrada;
- persistência organizada;
- SQL usado para análise;
- algoritmo estatístico aplicado de forma prática;
- solução simples de executar e de explicar.

## 6. Resultado esperado da validação

Ao final da execução, espera-se:

- API funcionando;
- banco PostgreSQL ativo;
- eventos gravados;
- agregados atualizados;
- recomendação retornando percentuais;
- consultas SQL permitindo auditoria completa.

## 7. Observação final

Este roteiro foi desenhado para permitir validação rápida e objetiva, tanto por alguém experiente quanto por alguém que quer apenas confirmar que a solução funciona de ponta a ponta.
