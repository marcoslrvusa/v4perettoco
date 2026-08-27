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

ADR-032 — API Modular

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

## Proximos Passos

- Gateway com OAuth2.

- Tracing OTel.