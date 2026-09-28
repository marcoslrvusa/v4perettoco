# Deck PDI: Resiliência com Circuit Breaker e Retry/Backoff

Área: Sistemas Distribuídos

## Slide 1: Resumo Executivo
Padrão de resiliência para chamadas a serviços externos (LLM, CRM): Circuit Breaker + retry com backoff e jitter, fallback. Entrego o padrão e uma implementação funcional.
Sem breaker, 1 API lenta vira fila que derruba o próprio serviço.
## Slide 2: Contexto de Produção
LLM/CRM lentos travavam o worker.
Retry sem backoff multiplicava a carga.
Sem fallback: erro virou 5xx.
## Slide 3: Diagnóstico
| Hoje | Alvo |
| --- | --- |
| retry imediato | backoff + jitter |
| sem proteção | breaker |
| 5xx seco | fallback |
## Slide 4: Decisão Arquitetural (ADR)
ADR-053: Resiliência
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| CB + backoff + fallback | protege cascata | estado | ESCOLHIDA |
| retry infinito | simples | piora outage | rejeitada |
> Nota: Closed -> Open após N falhas; Half-Open testa; fallback em Open.
## Slide 5: Entregas
RESILIENCIA.md.
circuit_breaker.py.
retry.py.
## Slide 6: Validação
Simular API lenta; breaker abre após limite.
Fallback em Open (sem 5xx).
API volta -> Half-Open reabilita.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Breaker abre em | <= 5 falhas |
| Fallback em outage | 100% |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Mal calibrado | tunar |
| Fallback mentiroso | explícito |
## Slide 9: Próximos Passos
Aplicar em todas as saídas.
Métricas de breaker.