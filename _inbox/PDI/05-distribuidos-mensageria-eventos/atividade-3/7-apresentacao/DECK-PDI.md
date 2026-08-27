# Deck PDI — Resiliencia com Circuit Breaker e Retry/Backoff

Area: Sistemas Distribuidos

## Slide 1: Resumo Executivo
Padrao de resiliencia para chamadas a servicos externos (LLM, CRM): Circuit Breaker + retry com backoff e jitter, fallback. Entrego o padrao e uma implementacao funcional.
Sem breaker, 1 API lenta vira fila que derruba o proprio servico.
## Slide 2: Contexto de Producao
LLM/CRM lentos travavam o worker.
Retry sem backoff multiplicava a carga.
Sem fallback: erro virou 5xx.
## Slide 3: Diagnostico
| Hoje | Alvo |
| --- | --- |
| retry imediato | backoff + jitter |
| sem protecao | breaker |
| 5xx seco | fallback |
## Slide 4: Decisao Arquitetural (ADR)
ADR-053 — Resiliencia
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| CB + backoff + fallback | protege cascata | estado | ESCOLHIDA |
| retry infinito | simples | piora outage | rejeitada |
> Nota: Closed -> Open apos N falhas; Half-Open testa; fallback em Open.
## Slide 5: Entregas
RESILIENCIA.md.
circuit_breaker.py.
retry.py.
## Slide 6: Validacao
Simular API lenta; breaker abre apos limite.
Fallback em Open (sem 5xx).
API volta -> Half-Open reabilita.
## Slide 7: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Breaker abre em | <= 5 falhas |
| Fallback em outage | 100% |
## Slide 8: Riscos
| Risco | Mitigacao |
| --- | --- |
| Mal calibrado | tunar |
| Fallback mentiroso | explicito |
## Slide 9: Proximos Passos
Aplicar em todas as saidas.
Metricas de breaker.