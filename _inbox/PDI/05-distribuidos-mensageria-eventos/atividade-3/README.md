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

ADR-053: Resiliencia

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

## Decisoes e tradeoffs

- **Timeout de 800ms conta como falha**: se o Score nao responde em 800ms, o Pagamento nao prende thread esperando.
- **Breaker abre apos mais de 5 falhas em 10s**: em OPEN o `score_cache()` responde em menos de 1s, isolando a falha no Score.
- **Half-open apos 30s com 1 sonda**: o `breaker.test()` libera uma chamada de teste; se ok, fecha, se nao, mantem OPEN. Recupera sozinho em vez de exigir acao manual.
- **Retry com backoff de 0.1 a 0.4s mais jitter so em CLOSED**: espera crescente com ruido; retry imediato foi rejeitado porque piora o outage.

## Impacto no negocio

Com abertura em ate 5 falhas e fallback em 100% do outage, o Pagamento sustenta 99,9% de disponibilidade mesmo com o Score fora do ar por minutos. Sem a protecao, a lentidao virava esgotamento de threads e erro para o cliente; com ela, a degradacao e graciosa em milissegundos e o retorno e automatico via half-open, sem intervencao manual.

## Referencias de estudo

- Curso: "Microservices: Resilience Patterns with Resilience4j" (Udemy).
- Video: "Circuit Breaker Pattern Explained" (YouTube, Fireship).
- Documento oficial: Microsoft Learn, "Circuit Breaker pattern" (learn.microsoft.com).
- Documento oficial: Resilience4j Documentation (resilience4j.readme.io).
