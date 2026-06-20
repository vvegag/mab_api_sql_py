# Payloads

## POST /eventos

Campos principais:

- `codigo_experimento`
- `nome_experimento`
- `nome_variante`
- `tipo_evento`
- `timestamp_evento`
- `usuario_id`
- `contexto`
- `id_evento_externo`

### Regras principais

- `codigo_experimento` deve identificar o experimento de forma estável;
- `nome_variante` não pode estar vazio;
- `tipo_evento` aceita `impressao` ou `clique`;
- `timestamp_evento` é opcional, mas não pode estar no futuro;
- `contexto` é livre e pode carregar dados adicionais do evento;
- `id_evento_externo` pode ser usado para idempotência.

## GET /recomendacao/{codigo_experimento}

Retorna:

- código do experimento;
- janela analisada;
- método utilizado;
- lista de variantes com percentual de tráfego.
