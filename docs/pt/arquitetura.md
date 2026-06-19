# Arquitetura

## Objetivo

Receber eventos de experimentação linha a linha, registrar em SQL, consolidar os dados e recomendar a distribuição de tráfego para o dia seguinte.

## Fluxo

1. A API recebe um evento.
2. O evento é validado.
3. O evento bruto é salvo no banco.
4. O agregado diário é atualizado.
5. A consulta de recomendação busca o histórico recente.
6. Thompson Sampling calcula a probabilidade de vitória de cada variante.
7. A API retorna os percentuais recomendados.

## Escolha do algoritmo

Thompson Sampling foi escolhido porque:

- lida bem com exploração versus exploração;
- funciona naturalmente com CTR;
- escala para múltiplas variantes;
- tem explicação estatística simples para entrevista.

## Como adicionar variantes

Não é necessário mudar o código do algoritmo.
O sistema reconhece novas variantes a partir dos eventos recebidos e passa a incluí-las na recomendação.
