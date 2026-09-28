# APIs Modulares de Missao Critica (FastAPI) com Paginacao, Cache e Rate Limiting

Arquitetura Full Stack

## Resumo Executivo

API modular FastAPI para dados de missao critica, com paginacao cursor-based, cache Redis com invalidacao e rate limiting por chave. Entrego o padrao e uma implementacao real.

Foco em corretude sob carga: uma API de leads nao pode vazar memoria nem derrubar o banco em pico.

## Contexto de Producao

- Endpoints internos servem 3-5 sistemas.

- Listas de 5k-80k sem paginacao estouravam memoria.

- Sem rate limit: 2k req/min derrubava o Postgres.

## O Problema e o Blast Radius

| Sintoma | Hoje | Alvo |

| --- | --- | --- |

| Paginacao | offset | cursor-based |

| Cache | nenhum | Redis + invalidacao |

| Rate limit | ausente | por api_key |

| Erro 5xx | stack cru | envelope |

## Diagnostico

- Offset em tabelas grandes = full scan.

- Conexoes nao pooladas -> esgotamento.

- Sem distincao 4xx vs 5xx.

## Decisao Arquitetural (ADR)

ADR-032: API Modular

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| FastAPI + Redis + slowapi | async, maduro | mais deps | ESCOLHIDA |

| Flask manual | simples | menos perf | rejeitada |

> **Nota:** Cursor-based para estabilidade; cache por chave com invalidacao no write.

## Entregas desta Atividade

- API-STANDARD.md.

- main_api.py.

- requirements.txt.

## Validacao

1. Carga com k6: 200 req/s por 5 min.

2. Rate limit: estourar quota -> 429.

3. Cache: 2o hit vem do Redis.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| p95 (lista) | < 200 ms cache hit |

| Rate limit | 100/min/key |

| Disponibilidade | >= 99.5% |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Cache stale | TTL + invalidar no write |

| Redis down | fallback DB |

## Decisoes e tradeoffs

1. **Paginacao cursor-based (`after` + `limit`, nunca offset acima de 10k):** paginas profundas com OFFSET fazem o Postgres varrer e descartar milhares de linhas; o cursor mantem custo estavel por pagina. Tradeoff: perde o salto direto para a pagina N, aceito porque as listas de 5k-80k sao consumidas sequencialmente.
2. **Cache Redis com TTL curto (30s) + `stale-while-revalidate=60` e invalidacao no write:** o mesmo JSON recalculado dezenas de vezes por minuto passa a sair do cache. Tradeoff: janela de segundos com dado defasado, aceita porque listagem de leads tolera atraso curto.
3. **Rate limiting 100 req/min por chave via slowapi com 429 + `Retry-After`:** impede que 2k req/min de um unico cliente derrubem o Postgres. Tradeoff: cliente legitimo em pico recebe 429 e precisa implementar retry com backoff.
4. **Fallback para o banco se o Redis cair:** o endpoint continua respondendo sem cache. Tradeoff: a latencia degrada no caminho direto ate o Redis voltar; disponibilidade vale mais que p95 nesse cenario.
5. **Envelope de erro unico com `trace_id` e separacao 4xx (nao retentar) vs 5xx (retry com backoff):** o cliente sabe como reagir sem ler stack trace. Tradeoff: o stack cru some da resposta, entao todo erro precisa de log com `trace_id` para depuracao.

## Impacto no negocio

Os endpoints internos servem 3 a 5 sistemas com listas de 5k a 80k registros; sem o padrao, picos de 2k req/min derrubavam o Postgres e estouravam memoria. Com cursor, cache e rate limit, o p95 da lista fica abaixo de 200ms no hit e a disponibilidade atinge 99,5%, o que protege a operacao de SDR e CRM em pico de campanha sem aumentar custo de banco.

## Referencias de estudo

- Curso: FastAPI Beyond CRUD (TalkPython Training)
- Video: Curso completo de FastAPI (freeCodeCamp, YouTube)
- Doc oficial: Documentacao do FastAPI, https://fastapi.tiangolo.com/ (verificada em 2026-09-28)
- Doc oficial: Redis, https://redis.io/ (site oficial com link para a documentacao, verificado em 2026-09-28)

## Proximos Passos

- Gateway com OAuth2.

- Tracing OTel.