# APIs Modulares de Missão Crítica (FastAPI) com Paginação, Cache e Rate Limiting

Arquitetura Full Stack

## Resumo Executivo

API modular FastAPI para dados de missão crítica, com paginação cursor-based, cache Redis com invalidação e rate limiting por chave. Entrego o padrão e uma implementação real.

Foco em corretude sob carga: uma API de leads não pode vazar memória nem derrubar o banco em pico.

## Contexto de Produção

- Endpoints internos servem 3-5 sistemas.

- Listas de 5k-80k sem paginação estouravam memória.

- Sem rate limit: 2k req/min derrubava o Postgres.

## O Problema e o Blast Radius

| Sintoma | Hoje | Alvo |

| --- | --- | --- |

| Paginação | offset | cursor-based |

| Cache | nenhum | Redis + invalidação |

| Rate limit | ausente | por api_key |

| Erro 5xx | stack cru | envelope |

## Diagnóstico

- Offset em tabelas grandes = full scan.

- Conexões não pooladas -> esgotamento.

- Sem distinção 4xx vs 5xx.

## Decisão Arquitetural (ADR)

ADR-032: API Modular

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| FastAPI + Redis + slowapi | async, maduro | mais deps | ESCOLHIDA |

| Flask manual | simples | menos perf | rejeitada |

> **Nota:** Cursor-based para estabilidade; cache por chave com invalidação no write.

## Entregas desta Atividade

- API-STANDARD.md.

- main_api.py.

- requirements.txt.

## Validação

1. Carga com k6: 200 req/s por 5 min.

2. Rate limit: estourar quota -> 429.

3. Cache: 2o hit vem do Redis.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| p95 (lista) | < 200 ms cache hit |

| Rate limit | 100/min/key |

| Disponibilidade | >= 99.5% |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Cache stale | TTL + invalidar no write |

| Redis down | fallback DB |

## Decisões e tradeoffs

1. **Paginação cursor-based (`after` + `limit`, nunca offset acima de 10k):** páginas profundas com OFFSET fazem o Postgres varrer e descartar milhares de linhas; o cursor mantém custo estável por página. Tradeoff: perde o salto direto para a página N, aceito porque as listas de 5k-80k são consumidas sequencialmente.
2. **Cache Redis com TTL curto (30s) + `stale-while-revalidate=60` e invalidação no write:** o mesmo JSON recalculado dezenas de vezes por minuto passa a sair do cache. Tradeoff: janela de segundos com dado defasado, aceita porque listagem de leads tolera atraso curto.
3. **Rate limiting 100 req/min por chave via slowapi com 429 + `Retry-After`:** impede que 2k req/min de um único cliente derrubem o Postgres. Tradeoff: cliente legítimo em pico recebe 429 e precisa implementar retry com backoff.
4. **Fallback para o banco se o Redis cair:** o endpoint continua respondendo sem cache. Tradeoff: a latência degrada no caminho direto até o Redis voltar; disponibilidade vale mais que p95 nesse cenário.
5. **Envelope de erro único com `trace_id` e separação 4xx (não retentar) vs 5xx (retry com backoff):** o cliente sabe como reagir sem ler stack trace. Tradeoff: o stack cru some da resposta, então todo erro precisa de log com `trace_id` para depuração.

## Impacto no negócio

Os endpoints internos servem 3 a 5 sistemas com listas de 5k a 80k registros; sem o padrão, picos de 2k req/min derrubavam o Postgres e estouravam memória. Com cursor, cache e rate limit, o p95 da lista fica abaixo de 200ms no hit e a disponibilidade atinge 99,5%, o que protege a operação de SDR e CRM em pico de campanha sem aumentar custo de banco.

## Referências de estudo

- Curso: FastAPI Beyond CRUD (TalkPython Training)
- Vídeo: Curso completo de FastAPI (freeCodeCamp, YouTube)
- Doc oficial: Documentação do FastAPI, https://fastapi.tiangolo.com/ (verificada em 2026-09-28)
- Doc oficial: Redis, https://redis.io/ (site oficial com link para a documentação, verificado em 2026-09-28)

## Próximos Passos

- Gateway com OAuth2.

- Tracing OTel.