# Resiliencia com Circuit Breaker e Retry/Backoff

Sistemas Distribuidos

## Resumo Executivo

Padrao de resiliencia para chamadas a servicos externos (LLM, CRM): Circuit Breaker + retry com backoff e jitter, fallback. Entrego o padrao e uma implementacao funcional.

Sem breaker, 1 API lenta vira fila que derruba o proprio servico.

## Contexto de Producao

- LLM/CRM lentos travavam o worker.

- Retry sem backoff multiplicava a carga.

- Sem fallback: erro virou 5xx.

## Diagnostico

| Hoje | Alvo |

| --- | --- |

| retry imediato | backoff + jitter |

| sem protecao | breaker |

| 5xx seco | fallback |

## Decisao Arquitetural (ADR)

ADR-053 — Resiliencia

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| CB + backoff + fallback | protege cascata | estado | ESCOLHIDA |

| retry infinito | simples | piora outage | rejeitada |

> **Nota:** Closed -> Open apos N falhas; Half-Open testa; fallback em Open.

## Entregas

- RESILIENCIA.md.

- circuit_breaker.py.

- retry.py.

## Validacao

1. Simular API lenta; breaker abre apos limite.

2. Fallback em Open (sem 5xx).

3. API volta -> Half-Open reabilita.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Breaker abre em | <= 5 falhas |

| Fallback em outage | 100% |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Mal calibrado | tunar |

| Fallback mentiroso | explicito |

## Proximos Passos

- Aplicar em todas as saidas.

- Metricas de breaker.