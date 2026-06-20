# Arquitetura

## Objetivo

Receber eventos de experimentação linha a linha, validar a entrada, registrar em SQL, consolidar o histórico e recomendar a distribuição de tráfego para o dia seguinte.

## Fluxo

1. A API recebe um evento.
2. O payload é validado.
3. O evento bruto é salvo no banco.
4. O agregado diário é atualizado.
5. A consulta de recomendação busca o histórico recente.
6. Thompson Sampling calcula a probabilidade de vitória de cada variante.
7. A API retorna os percentuais recomendados.

## Camadas da solução

### API

Responsável por receber eventos e expor a recomendação do experimento.

### Banco

Responsável por persistir:

- experimentos;
- variantes;
- eventos brutos;
- agregados diários;
- recomendações geradas.

### Serviço de recomendação

Responsável por consultar o histórico recente, preparar as estatísticas e calcular a distribuição de tráfego do próximo dia.

## Escolha do algoritmo

Thompson Sampling foi escolhido porque:

- lida bem com exploração versus exploração;
- funciona naturalmente com CTR;
- escala para múltiplas variantes;
- tem explicação estatística simples para entrevista.

## Como adicionar variantes

Não é necessário mudar o código do algoritmo.

O sistema reconhece novas variantes a partir dos eventos recebidos e passa a incluí-las na recomendação.

## Como o histórico é usado

- o dado bruto garante rastreabilidade;
- o agregado diário melhora a leitura operacional;
- a recomendação usa uma janela temporal configurável para equilibrar sensibilidade e estabilidade.
