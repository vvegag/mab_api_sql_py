# Decisões Arquiteturais

## Objetivo

Documentar as decisões principais da solução para facilitar a revisão técnica e orientar evoluções futuras.

## 1. FastAPI

Escolhido por combinar rapidez de entrega, validação forte, documentação automática e tipagem clara.

### Ganhos

- contrato bem definido;
- baixo atrito para demonstrar o caso;
- leitura fácil para avaliador técnico.

## 2. PostgreSQL

Escolhido como banco principal por ser um padrão natural para SQL analítico e histórico temporal.

### Ganhos

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

Isso evita retrabalho se a solução precisar ir além de A/B.

### Ganhos

- arquitetura mais genérica;
- algoritmo já preparado para N variantes;
- argumento técnico mais forte.

## 6. Nomes em português

A solução usa português em código, docs e pastas para maximizar clareza no contexto de apresentação.

### Ganhos

- leitura mais rápida;
- narrativa consistente;
- maior facilidade para explicar a solução de ponta a ponta.

## 7. Idempotência simples

O campo `id_evento_externo` foi previsto para evitar duplicidade quando o produtor de eventos tiver um identificador confiável.

### Ganhos

- mais robustez na ingestão;
- base para evolução futura;
- melhor controle de duplicidade.

## 8. Janela analítica configurável

A recomendação usa uma janela configurável de análise.

### Ganhos

- permite adaptar sensibilidade temporal;
- facilita explicar a escolha;
- evita rigidez desnecessária.

## 9. Docker Compose

Foi adotado para tornar a reprodução da solução simples no ambiente do avaliador.

### Ganhos

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
