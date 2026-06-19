# Payloads

## POST /eventos

Main fields:

- `codigo_experimento`
- `nome_experimento`
- `nome_variante`
- `tipo_evento`
- `timestamp_evento`
- `usuario_id`
- `contexto`
- `id_evento_externo`

## GET /recomendacao/{codigo_experimento}

Returns:

- experiment code
- analysis window
- method used
- variant allocation list

