# Roteiro de Apresentação do Case

## Como usar este documento

Este material serve como base para:
- slides no NotebookLM;
- roteiro de fala para entrevista;
- podcast de estudo;
- flashcards;
- mapa mental;
- revisão rápida antes da entrega.

## Mensagem central em uma frase

Eu desenhei uma API reproduzível que recebe eventos linha a linha, persiste dados em SQL, agrega informações de forma confiável e recomenda a alocação de tráfego do próximo dia usando Thompson Sampling com suporte a múltiplas variantes.

## Elevator pitch

O desafio pede uma API para otimizar a alocação de tráfego entre controle e variantes com base em dados temporais. Em vez de tratar isso como um notebook isolado, eu estruturei uma solução de produto: API REST, banco SQL, ingestão de eventos brutos, agregação diária, recomendação estatística e documentação bilíngue para facilitar reprodutibilidade e avaliação técnica.

## Problema de negócio

O objetivo é reduzir desperdício de tráfego em variantes inferiores e acelerar a descoberta das melhores variantes sem perder exploração estatística. O problema central é decidir quanto tráfego destinar a cada variante no dia seguinte a partir de evidências recentes.

## Premissas adotadas

- os eventos chegam linha a linha;
- o sistema precisa lidar com múltiplas variantes;
- CTR é a métrica principal do experimento;
- o avaliador precisa conseguir reproduzir a solução localmente;
- a explicação deve ser simples o bastante para negócio e precisa o bastante para engenharia.

## Escopo entregue

- `POST /eventos` para ingestão de eventos brutos;
- `GET /recomendacao/{codigo_experimento}` para gerar a alocação do dia seguinte;
- `GET /saude` para monitoramento básico;
- persistência em PostgreSQL;
- agregação diária em SQL;
- Thompson Sampling com distribuição Beta;
- suporte a múltiplas variantes;
- código e documentação em português.

## Arquitetura de alto nível

### Camada 1: API

A API foi feita em FastAPI porque entrega validação forte, tipagem clara e rapidez de desenvolvimento. Os endpoints estão separados por responsabilidade para deixar o fluxo entendível e fácil de testar.

### Camada 2: Persistência

O banco guarda duas visões do dado:
- evento bruto, linha a linha;
- agregado diário por experimento e variante.

Isso permite rastreabilidade e também leitura eficiente para recomendação.

### Camada 3: Algoritmo

Usei Thompson Sampling porque ele equilibra exploração e exploração de forma probabilística e natural para CTR. O modelo trata clique como sucesso e impressão sem clique como falha.

## Como os dados fluem

1. um evento chega na API;
2. a entrada é validada;
3. o evento bruto é persistido;
4. o agregado diário é atualizado;
5. a recomendação consulta o histórico recente;
6. Thompson Sampling calcula a chance de vitória de cada variante;
7. a API retorna os percentuais recomendados.

## Modelo de dados

### experimentos

Guarda o cadastro do experimento e o código de negócio usado pela API.

### variantes

Guarda as variantes do experimento e marca qual é o controle.

### eventos_brutos

Guarda cada evento recebido pela API, com timestamp, usuário e contexto opcional.

### agregados_diarios

Guarda a consolidação por dia e variante para consulta e auditoria.

### recomendacoes_diarias

Guarda o histórico das recomendações geradas pela API.

## Escolha do algoritmo

### Por que Thompson Sampling

- funciona muito bem para CTR;
- escala para múltiplas variantes;
- tem explicação estatística clara;
- é mais eficiente que A/B estático quando o objetivo é decidir alocação dinâmica.

### Fórmula de trabalho

- `alpha = cliques + 1`
- `beta = impressões - cliques + 1`

A cada variante eu amostro da distribuição Beta e converto a frequência de vitórias em percentual de tráfego.

## Por que não escolhi outras abordagens como principal

### A/B estático puro

Serve como baseline, mas mantém tráfego em variantes piores por mais tempo.

### Epsilon-greedy

É útil, mas a exploração é mais aleatória e menos elegante para justificar em um case de negócio.

### UCB

Também é válido, mas Thompson Sampling costuma ser mais intuitivo para esse tipo de experimento com CTR.

## Decisões de senioridade

- separar dado bruto de dado agregado;
- persistir recomendação gerada;
- usar idempotência via `id_evento_externo` quando existir;
- deixar a recomendação parametrizável por janela e número de amostras;
- manter a solução reproduzível com Docker e README claro;
- documentar em português e espelhar em inglês quando necessário.

## Pontos fortes para falar na entrevista

- a solução não é um notebook isolado, é uma API reproduzível;
- o banco é parte central da decisão, não só armazenamento;
- a agregação diária permite escalar a consulta de recomendação;
- a arquitetura suporta novas variantes sem reescrever a lógica;
- o design facilita testes, auditoria e evolução futura.

## Limites assumidos

- o desafio foi tratado como prova de arquitetura e raciocínio, não como plataforma de produção completa;
- a recomendação usa janela recente configurável, não um sistema de streaming em tempo real;
- a persistência foi mantida simples para maximizar clareza e velocidade de entrega.

## Evoluções futuras que eu mencionaria

- fila assíncrona para ingestão;
- particionamento por data;
- monitoramento de drift;
- testes de carga;
- dashboard operacional;
- suporte a métrica de receita além de CTR.

## Roteiro de fala de 3 a 5 minutos

1. abrir com o problema de negócio;
2. explicar que eventos chegam linha a linha;
3. destacar a separação entre evento bruto e agregado;
4. apresentar o motivo da escolha de Thompson Sampling;
5. mostrar que a API tem endpoints simples e claros;
6. fechar com reprodutibilidade, testes e capacidade de evolução.

## Perguntas que podem aparecer

- Por que não usar apenas A/B test?
- Como a solução lida com novas variantes?
- Por que gravar evento bruto e agregado?
- Como você justificaria o uso de SQL aqui?
- O que você faria para escalar isso em produção?

## Respostas curtas sugeridas

### Por que Thompson Sampling?

Porque ele equilibra exploração e exploração de forma estatística, e isso é muito adequado para CTR com múltiplas variantes.

### Por que SQL?

Porque o desafio pede persistência e análise temporal; SQL é ideal para agregação, auditabilidade e consulta de histórico.

### Por que eventos brutos e agregados?

Porque o bruto garante rastreabilidade e o agregado melhora a eficiência da consulta de recomendação.

### Como incluir novas variantes?

Basta enviar eventos com um novo `nome_variante` para o mesmo experimento. O sistema passa a considerar a variante automaticamente.

## Prompt sugerido para NotebookLM

Use este documento para gerar:
- slides de entrevista;
- roteiro de podcast;
- flashcards de revisão;
- mapa mental do case;
- perguntas e respostas técnicas;
- perguntas difíceis de entrevista com respostas objetivas.

## Frase de fechamento

A proposta entrega uma solução simples de operar, fácil de explicar e forte tecnicamente, com foco em dados confiáveis, decisão estatística e reprodutibilidade.
