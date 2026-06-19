# Decisoes Arquiteturais

## Objetivo

Documentar as decisoes principais da solucao para facilitar defesa tecnica em entrevista e orientar evolucoes futuras.

## 1. FastAPI

Escolhido por combinar rapidez de entrega, validacao forte, documentação automatica e tipagem clara.

### Ganho

- contrato bem definido;
- baixo atrito para demonstrar o caso;
- leitura facil para avaliador tecnico.

## 2. PostgreSQL

Escolhido como banco principal por ser o padrao natural para SQL analitico e historico temporal.

### Ganho

- joins e agregacoes simples;
- integridade referencial;
- facilidade para evoluir o schema.

## 3. Eventos brutos + agregados

A solucao guarda as duas camadas porque cada uma resolve um problema diferente.

### Evento bruto

- rastreabilidade;
- auditoria;
- reprocessamento futuro.

### Agregado diario

- consulta mais rapida;
- calculo de recomendacao mais simples;
- menor custo de leitura.

## 4. Thompson Sampling

Foi escolhido por ser mais aderente ao problema do que um A/B test estatico.

### Motivos

- funciona bem com CTR;
- trata incerteza de forma estatistica;
- suporta multiplas variantes;
- tem narrativa forte para negocio e engenharia.

## 5. Multiplas variantes desde o inicio

Isso evita retrabalho se a entrevista pedir extensao alem de A/B.

### Ganho

- arquitetura mais generica;
- algoritmo ja preparado para N variantes;
- argumento de senioridade mais forte.

## 6. Nomes em portugues

A solucao usa portugues em codigo, docs e pastas para maximizar clareza no seu contexto de apresentacao.

### Ganho

- leitura mais rapida para voce;
- narrativa consistente na entrevista;
- maior facilidade para explicar a solucao de ponta a ponta.

## 7. Idempotencia simples

O campo `id_evento_externo` foi previsto para evitar duplicidade quando o produtor de eventos tiver um identificador confiavel.

### Ganho

- mais robustez na ingestao;
- bom argumento de engenharia;
- base para evolucao futura.

## 8. Janela analitica configuravel

A recomendacao usa uma janela configuravel de analise.

### Ganho

- permite adaptar sensibilidade temporal;
- facilita explicar a escolha durante a entrevista;
- evita rigidez desnecessaria.

## 9. Docker Compose

Foi adotado para tornar a reproducao da solucao simples no ambiente do avaliador.

### Ganho

- mesma infraestrutura local para qualquer pessoa;
- menos dependencia do ambiente da maquina;
- entrega com cara de produto.

## 10. O que foi evitado de proposito

- Kubernetes;
- cloud provider especifico;
- streaming distribuido complexo;
- microservicos;
- excesso de observabilidade para este escopo.

### Motivo

O desafio pede clareza, reproducibilidade e decisao estatistica. Complexidade extra sem ganho direto atrapalharia a avaliacao.
