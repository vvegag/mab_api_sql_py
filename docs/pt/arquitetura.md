# Arquitetura

## Objetivo

Receber eventos de experimentacao linha a linha, registrar em SQL, consolidar os dados e recomendar a distribuicao de trafego para o dia seguinte.

## Fluxo

1. A API recebe um evento.
2. O evento e validado.
3. O evento bruto e salvo no banco.
4. O agregado diario e atualizado.
5. A consulta de recomendacao busca o historico recente.
6. Thompson Sampling calcula a probabilidade de vitoria de cada variante.
7. A API retorna os percentuais recomendados.

## Escolha do algoritmo

Thompson Sampling foi escolhido porque:

- lida bem com exploration vs exploitation;
- funciona naturalmente com CTR;
- escala para multiplas variantes;
- tem explicacao estatistica simples para entrevista.

## Como adicionar variantes

Nao e necessario mudar o codigo do algoritmo.
O sistema reconhece novas variantes a partir dos eventos recebidos e passa a inclui-las na recomendacao.

