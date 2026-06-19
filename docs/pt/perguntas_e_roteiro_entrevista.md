# Perguntas e Roteiro de Entrevista

## Como usar este arquivo

Use este material para treinar respostas curtas, organizar a fala e preparar a defesa técnica do case.

## Resumo curto para abrir a conversa

Eu construí uma API em FastAPI que recebe eventos linha a linha, persiste os dados em SQL, agrega o histórico de forma confiável e recomenda a alocação de tráfego do próximo dia usando Thompson Sampling. A solução foi desenhada para suportar múltiplas variantes, manter rastreabilidade e ser fácil de explicar em entrevista.

## Por que usei SQL + Thompson Sampling

- Usei SQL porque o problema é temporal, precisa de auditoria e exige agregação confiável.
- Usei Thompson Sampling porque o objetivo é decidir alocação de tráfego, não só medir desempenho.
- A combinação funciona bem para CTR, múltiplas variantes e atualização diária da recomendação.

## Roteiro de 2 minutos

1. O desafio pede uma API para receber eventos de um experimento e recomendar a alocação do próximo dia.
2. Eu tratei o problema como uma solução de produto e não como um notebook isolado.
3. A API recebe eventos linha a linha e grava o dado bruto em SQL.
4. Em paralelo, o sistema atualiza um agregado diário para facilitar consulta e auditoria.
5. Para a decisão, usei Thompson Sampling com distribuição Beta, que é natural para CTR.
6. A solução já nasce com suporte a múltiplas variantes.
7. O resultado final é uma recomendação percentual para controle e variantes.

## Roteiro de 5 minutos

1. Eu comecei modelando o fluxo completo: evento bruto, persistência, agregação e recomendação.
2. Separei o dado bruto do dado agregado para garantir rastreabilidade e eficiência.
3. Usei FastAPI porque o contrato da API fica claro e a validação dos dados é simples e forte.
4. Usei PostgreSQL porque o desafio pede SQL real e o banco é central para agregações e histórico.
5. Para a decisão, escolhi Thompson Sampling porque ele equilibra exploração e exploração de forma estatística.
6. Como o desafio pede múltiplas variantes, a arquitetura já foi feita para N variantes.
7. A recomendação é gerada com base em CTR, usando clique como sucesso e impressão sem clique como falha.
8. Também deixei a recomendação registrada para auditoria e comparação futura.
9. A documentação está em português, com espelho em inglês, para facilitar leitura e apresentação.
10. A solução mostra engenharia, ciência de dados e clareza de produto ao mesmo tempo.

## Perguntas difíceis e respostas curtas

### Por que não usar só A/B test?

Porque A/B fixo mantém tráfego em variantes piores por mais tempo. Thompson Sampling adapta a alocação conforme os dados chegam.

### Por que usar SQL nesse caso?

Porque o problema exige persistência temporal, rastreabilidade e agregação confiável.

### Por que guardar evento bruto e agregado?

O bruto permite auditoria e reprocessamento. O agregado acelera a consulta para a recomendação.

### Como a solução lida com novas variantes?

A API aceita eventos com novo `nome_variante` para o mesmo experimento e passa a considerar a variante automaticamente.

### O que você faria para produção?

Eu adicionaria fila de ingestão, monitoramento, particionamento por data e testes de carga.

### Por que Thompson Sampling e não UCB?

Thompson Sampling é mais intuitivo para CTR e fácil de defender em um case com múltiplas variantes.

### Como garantir reprodutibilidade?

Com Docker Compose, schema SQL versionado, seed fixa nos testes e documentação clara.

## Frases que ajudam na entrevista

- Eu separei dado bruto, agregado e recomendação porque cada camada resolve um problema diferente.
- O objetivo não era só analisar dados, mas transformar dados em decisão de alocação.
- A solução foi pensada para ser explicável, reproduzível e extensível.
- Thompson Sampling é uma escolha natural quando o problema é CTR com múltiplas variantes.

## Fechamento sugerido

A proposta entrega uma solução simples de operar, fácil de explicar e forte tecnicamente, com foco em dados confiáveis, decisão estatística e reprodutibilidade.

