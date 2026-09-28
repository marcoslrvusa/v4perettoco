# Deck PDI: APIs Modulares de Missão Crítica (FastAPI) com Paginação, Cache e Rate Limiting

Área: Arquitetura Full Stack

## Slide 1: Resumo Executivo
API modular FastAPI para dados de missão crítica, com paginação cursor-based, cache Redis com invalidação e rate limiting por chave. Entrego o padrão e uma implementação real.
Foco em corretude sob carga: uma API de leads não pode vazar memória nem derrubar o banco em pico.
## Slide 2: Contexto de Produção
Endpoints internos servem 3-5 sistemas.
Listas de 5k-80k sem paginação estouravam memória.
Sem rate limit: 2k req/min derrubava o Postgres.
## Slide 3: O Problema e o Blast Radius
| Sintoma | Hoje | Alvo |
| --- | --- | --- |
| Paginação | offset | cursor-based |
| Cache | nenhum | Redis + invalidação |
| Rate limit | ausente | por api_key |
| Erro 5xx | stack cru | envelope |
## Slide 4: Diagnóstico
Offset em tabelas grandes = full scan.
Conexões não pooladas -> esgotamento.
Sem distinção 4xx vs 5xx.
## Slide 5: Decisão Arquitetural (ADR)
ADR-032: API Modular
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| FastAPI + Redis + slowapi | async, maduro | mais deps | ESCOLHIDA |
| Flask manual | simples | menos perf | rejeitada |
> Nota: Cursor-based para estabilidade; cache por chave com invalidação no write.
## Slide 6: Entregas desta Atividade
API-STANDARD.md.
main_api.py.
requirements.txt.
## Slide 7: Validação
Carga com k6: 200 req/s por 5 min.
Rate limit: estourar quota -> 429.
Cache: 2o hit vem do Redis.
## Slide 8: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| p95 (lista) | < 200 ms cache hit |
| Rate limit | 100/min/key |
| Disponibilidade | >= 99.5% |
## Slide 9: Riscos
| Risco | Mitigação |
| --- | --- |
| Cache stale | TTL + invalidar no write |
| Redis down | fallback DB |
## Slide 10: Próximos Passos
Gateway com OAuth2.
Tracing OTel.