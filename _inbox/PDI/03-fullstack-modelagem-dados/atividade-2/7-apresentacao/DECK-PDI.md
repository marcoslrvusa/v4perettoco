# Deck PDI — APIs Modulares de Missao Critica (FastAPI) com Paginacao, Cache e Rate Limiting

Area: Arquitetura Full Stack

## Slide 1: Resumo Executivo
API modular FastAPI para dados de missao critica, com paginacao cursor-based, cache Redis com invalidacao e rate limiting por chave. Entrego o padrao e uma implementacao real.
Foco em corretude sob carga: uma API de leads nao pode vazar memoria nem derrubar o banco em pico.
## Slide 2: Contexto de Producao
Endpoints internos servem 3-5 sistemas.
Listas de 5k-80k sem paginacao estouravam memoria.
Sem rate limit: 2k req/min derrubava o Postgres.
## Slide 3: O Problema e o Blast Radius
| Sintoma | Hoje | Alvo |
| --- | --- | --- |
| Paginacao | offset | cursor-based |
| Cache | nenhum | Redis + invalidacao |
| Rate limit | ausente | por api_key |
| Erro 5xx | stack cru | envelope |
## Slide 4: Diagnostico
Offset em tabelas grandes = full scan.
Conexoes nao pooladas -> esgotamento.
Sem distincao 4xx vs 5xx.
## Slide 5: Decisao Arquitetural (ADR)
ADR-032 — API Modular
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| FastAPI + Redis + slowapi | async, maduro | mais deps | ESCOLHIDA |
| Flask manual | simples | menos perf | rejeitada |
> Nota: Cursor-based para estabilidade; cache por chave com invalidacao no write.
## Slide 6: Entregas desta Atividade
API-STANDARD.md.
main_api.py.
requirements.txt.
## Slide 7: Validacao
Carga com k6: 200 req/s por 5 min.
Rate limit: estourar quota -> 429.
Cache: 2o hit vem do Redis.
## Slide 8: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| p95 (lista) | < 200 ms cache hit |
| Rate limit | 100/min/key |
| Disponibilidade | >= 99.5% |
## Slide 9: Riscos
| Risco | Mitigacao |
| --- | --- |
| Cache stale | TTL + invalidar no write |
| Redis down | fallback DB |
## Slide 10: Proximos Passos
Gateway com OAuth2.
Tracing OTel.