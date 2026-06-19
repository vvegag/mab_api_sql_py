# Roteiro de Apresentacao do Case

## Como usar este documento

Este material serve como base para:
- slides no NotebookLM;
- roteiro de fala para entrevista;
- podcast de estudo;
- flashcards;
- mapa mental;
- revisao rapida antes da entrega.

## Mensagem central em uma frase

Eu desenhei uma API reproduzivel que recebe eventos linha a linha, persiste dados em SQL, agrega informacoes de forma confiavel e recomenda a alocacao de trafego do proximo dia usando Thompson Sampling com suporte a multiplas variantes.

## Elevator pitch

O desafio pede uma API para otimizar a alocacao de trafego entre controle e variantes com base em dados temporais. Em vez de tratar isso como um notebook isolado, eu estruturei uma solucao de produto: API REST, banco SQL, ingestao de eventos brutos, agregacao diaria, recomendacao estatistica e documentacao bilinguue para facilitar reproducibilidade e avaliacao tecnica.

## Problema de negocio

O objetivo e reduzir desperdicio de trafego em variantes inferiores e acelerar a descoberta das melhores variantes sem perder exploracao estatistica. O problema central e decidir quanto trafego destinar a cada variante no dia seguinte a partir de evidencias recentes.

## Premissas adotadas

- os eventos chegam linha a linha;
- o sistema precisa lidar com multiplas variantes;
- CTR e a metrica principal do experimento;
- o avaliador precisa conseguir reproduzir a solucao localmente;
- a explicacao deve ser simples o bastante para negocio e precisa o bastante para engenharia.

## Escopo entregue

- `POST /eventos` para ingestao de eventos brutos;
- `GET /recomendacao/{codigo_experimento}` para gerar a alocacao do dia seguinte;
- `GET /saude` para monitoramento basico;
- persistencia em PostgreSQL;
- agregacao diaria em SQL;
- Thompson Sampling com distribuicao Beta;
- suporte a multiplas variantes;
- codigo e documentacao em portugues.

## Arquitetura de alto nivel

### Camada 1: API

A API foi feita em FastAPI porque entrega validacao forte, tipagem clara e rapidez de desenvolvimento. Os endpoints estao separados por responsabilidade para deixar o fluxo entendivel e facil de testar.

### Camada 2: Persistencia

O banco guarda duas visoes do dado:
- evento bruto, linha a linha;
- agregado diario por experimento e variante.

Isso permite rastreabilidade e tambem leitura eficiente para recomendacao.

### Camada 3: Algoritmo

Usei Thompson Sampling porque ele equilibra exploracao e exploracao de forma probabilistica e natural para CTR. O modelo trata clique como sucesso e impressao sem clique como fracasso.

## Como os dados fluem

1. um evento chega na API;
2. a entrada e validada;
3. o evento bruto e persistido;
4. o agregado diario e atualizado;
5. a recomendacao consulta o historico recente;
6. Thompson Sampling calcula a chance de vitoria de cada variante;
7. a API retorna os percentuais recomendados.

## Modelo de dados

### experimentos

Guarda o cadastro do experimento e o codigo de negocio usado pela API.

### variantes

Guarda as variantes do experimento e marca qual e o controle.

### eventos_brutos

Guarda cada evento recebido pela API, com timestamp, usuario e contexto opcional.

### agregados_diarios

Guarda a consolidacao por dia e variante para consulta e auditoria.

### recomendacoes_diarias

Guarda o historico das recomendacoes geradas pela API.

## Escolha do algoritmo

### Por que Thompson Sampling

- funciona muito bem para CTR;
- escala para multiplas variantes;
- tem explicacao estatistica clara;
- e mais eficiente que A/B estatico quando o objetivo e decidir alocacao dinamica.

### Formula de trabalho

- `alpha = cliques + 1`
- `beta = impressoes - cliques + 1`

A cada variante eu amostro da distribuicao Beta e converto a frequencia de vitorias em percentual de trafego.

## Por que nao escolhi outras abordagens como principal

### A/B estatico puro

Serve como baseline, mas mantem trafego em variantes piores por mais tempo.

### Epsilon-greedy

E util, mas a exploracao e mais aleatoria e menos elegante para justificar em um case de negocio.

### UCB

Tambem e valido, mas Thompson Sampling costuma ser mais intuitivo para esse tipo de experimento com CTR.

## Decisoes de senioridade

- separar dado bruto de dado agregado;
- persistir recomendacao gerada;
- usar idempotencia via `id_evento_externo` quando existir;
- deixar a recomendacao parametrizavel por janela e numero de amostras;
- manter a solucao reproduzivel com Docker e README claro;
- documentar em portugues e espelhar em ingles.

## Pontos fortes para falar na entrevista

- a solucao nao e um notebook isolado, e uma API reproduzivel;
- o banco e parte central da decisao, nao so armazenamento;
- a agregacao diaria permite escalar a consulta de recomendacao;
- a arquitetura suporta novas variantes sem reescrever a logica;
- o design facilita testes, auditoria e evolucao futura.

## Limites assumidos

- o desafio foi tratado como prova de arquitetura e raciocinio, nao como plataforma de producao completa;
- a recomendacao usa janela recente configuravel, nao um sistema de streaming em tempo real;
- a persistencia foi mantida simples para maximizar clareza e velocidade de entrega.

## Evolucoes futuras que eu mencionaria

- fila assicrona para ingestao;
- particionamento por data;
- monitoramento de drift;
- testes de carga;
- dashboard operacional;
- suporte a metrica de receita alem de CTR.

## Roteiro de fala de 3 a 5 minutos

1. abrir com o problema de negocio;
2. explicar que eventos chegam linha a linha;
3. destacar a separacao entre evento bruto e agregado;
4. apresentar o motivo da escolha de Thompson Sampling;
5. mostrar que a API tem endpoints simples e claros;
6. fechar com reproducibilidade, testes e capacidade de evolucao.

## Perguntas que podem aparecer

- Por que nao usar apenas A/B test?
- Como a solucao lida com novas variantes?
- Por que gravar evento bruto e agregado?
- Como voce justificaria o uso de SQL aqui?
- O que voce faria para escalar isso em producao?

## Respostas curtas sugeridas

### Por que Thompson Sampling?

Porque ele equilibra exploracao e exploracao de forma estatistica, e isso e muito adequado para CTR com multiplas variantes.

### Por que SQL?

Porque o desafio pede persistencia e analise temporal; SQL e ideal para agregacao, auditabilidade e consulta de historico.

### Por que eventos brutos e agregados?

Porque o bruto garante rastreabilidade e o agregado melhora a eficiencia da consulta de recomendacao.

### Como incluir novas variantes?

Basta enviar eventos com um novo `nome_variante` para o mesmo experimento. O sistema passa a considerar a variante automaticamente.

## Prompt sugerido para NotebookLM

Use este documento para gerar:
- slides de entrevista;
- roteiro de podcast;
- flashcards de revisao;
- mapa mental do case;
- perguntas e respostas tecnicas;
- perguntas dificeis de entrevista com respostas objetivas.

## Frase de fechamento

A proposta entrega uma solucao simples de operar, facil de explicar e forte tecnicamente, com foco em dados confiaveis, decisao estatistica e reproducibilidade.
