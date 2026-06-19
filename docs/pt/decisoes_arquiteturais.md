# Decisões Arquiteturais

## Objetivo

Documentar as decisões principais da solução para facilitar a defesa técnica em entrevista e orientar evoluções futuras.

## 1. FastAPI

Escolhido por combinar rapidez de entrega, validação forte, documentação automática e tipagem clara.

### Ganho

- contrato bem definido;
- baixo atrito para demonstrar o caso;
- leitura fácil para avaliador técnico.

## 2. PostgreSQL

Escolhido como banco principal por ser o padrão natural para SQL analítico e histórico temporal.

### Ganho

- joins e agregações simples;
- integridade referencial;
- facilidade para evoluir o schema.

## 3. Eventos brutos + agregados

A solução guarda as duas camadas porque cada uma resolve um problema diferente.

### Evento bruto

- rastreabilidade;
- auditoria;
- reprocessamento futuro.

### Agregado diário

- consulta mais rápida;
- cálculo de recomendação mais simples;
- menor custo de leitura.

## 4. Thompson Sampling

Foi escolhido por ser mais aderente ao problema do que um A/B test estático.

### Motivos

- funciona bem com CTR;
- trata incerteza de forma estatística;
- suporta múltiplas variantes;
- tem narrativa forte para negócio e engenharia.

## 5. Múltiplas variantes desde o início

Isso evita retrabalho se a entrevista pedir extensão além de A/B.

### Ganho

- arquitetura mais genérica;
- algoritmo já preparado para N variantes;
- argumento de senioridade mais forte.

## 6. Nomes em português

A solução usa português em código, docs e pastas para maximizar clareza no seu contexto de apresentação.

### Ganho

- leitura mais rápida para você;
- narrativa consistente na entrevista;
- maior facilidade para explicar a solução de ponta a ponta.

## 7. Idempotência simples

O campo `id_evento_externo` foi previsto para evitar duplicidade quando o produtor de eventos tiver um identificador confiável.

### Ganho

- mais robustez na ingestão;
- bom argumento de engenharia;
- base para evolução futura.

## 8. Janela analítica configurável

A recomendação usa uma janela configurável de análise.

### Ganho

- permite adaptar sensibilidade temporal;
- facilita explicar a escolha durante a entrevista;
- evita rigidez desnecessária.

## 9. Docker Compose

Foi adotado para tornar a reprodução da solução simples no ambiente do avaliador.

### Ganho

- mesma infraestrutura local para qualquer pessoa;
- menos dependência do ambiente da máquina;
- entrega com cara de produto.

## 10. O que foi evitado de propósito

- Kubernetes;
- cloud provider específico;
- streaming distribuído complexo;
- microserviços;
- excesso de observabilidade para este escopo.

### Motivo

O desafio pede clareza, reprodutibilidade e decisão estatística. Complexidade extra sem ganho direto atrapalharia a avaliação.
