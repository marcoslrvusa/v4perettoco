# Resiliência com Circuit Breaker e Retry/Backoff

Sistemas Distribuídos

## Resumo Executivo

Padrão de resiliência para chamadas a serviços externos (LLM, CRM): Circuit Breaker + retry com backoff e jitter, fallback. Entrego o padrão e uma implementação funcional.

Sem breaker, 1 API lenta vira fila que derruba o próprio serviço.

## Contexto de Produção

- LLM/CRM lentos travavam o worker.

- Retry sem backoff multiplicava a carga.

- Sem fallback: erro virou 5xx.

## Diagnóstico

| Hoje | Alvo |

| --- | --- |

| retry imediato | backoff + jitter |

| sem proteção | breaker |

| 5xx seco | fallback |

## Decisão Arquitetural (ADR)

ADR-053: Resiliência

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| CB + backoff + fallback | protege cascata | estado | ESCOLHIDA |

| retry infinito | simples | piora outage | rejeitada |

> **Nota:** Closed -> Open após N falhas; Half-Open testa; fallback em Open.

## Entregas

- RESILIENCIA.md.

- circuit_breaker.py.

- retry.py.

## Validação

1. Simular API lenta; breaker abre após limite.

2. Fallback em Open (sem 5xx).

3. API volta -> Half-Open reabilita.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Breaker abre em | <= 5 falhas |

| Fallback em outage | 100% |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Mal calibrado | tunar |

| Fallback mentiroso | explícito |

## Próximos Passos

- Aplicar em todas as saídas.

- Métricas de breaker.

## Decisões e tradeoffs

- **Timeout de 800ms conta como falha**: se o Score não responde em 800ms, o Pagamento não prende thread esperando.
- **Breaker abre após mais de 5 falhas em 10s**: em OPEN o `score_cache()` responde em menos de 1s, isolando a falha no Score.
- **Half-open após 30s com 1 sonda**: o `breaker.test()` libera uma chamada de teste; se ok, fecha, se não, mantém OPEN. Recupera sozinho em vez de exigir ação manual.
- **Retry com backoff de 0.1 a 0.4s mais jitter só em CLOSED**: espera crescente com ruído; retry imediato foi rejeitado porque piora o outage.

## Impacto no negócio

Com abertura em até 5 falhas e fallback em 100% do outage, o Pagamento sustenta 99,9% de disponibilidade mesmo com o Score fora do ar por minutos. Sem a proteção, a lentidão virava esgotamento de threads e erro para o cliente; com ela, a degradação e graciosa em milissegundos e o retorno e automático via half-open, sem intervenção manual.

## Referências de estudo

- Curso: "Microservices: Resilience Patterns with Resilience4j" (Udemy).
- Vídeo: "Circuit Breaker Pattern Explained" (YouTube, Fireship).
- Documento oficial: Microsoft Learn, "Circuit Breaker pattern" (learn.microsoft.com).
- Documento oficial: Resilience4j Documentation (resilience4j.readme.io).
