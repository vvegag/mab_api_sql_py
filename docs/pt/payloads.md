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

## GET /recomendacao/{codigo_experimento}

Retorna:

- código do experimento
- janela analisada
- método utilizado
- lista de variantes com percentual de tráfego
