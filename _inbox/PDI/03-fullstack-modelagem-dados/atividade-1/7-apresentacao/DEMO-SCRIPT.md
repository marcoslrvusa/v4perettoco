# Roteiro de Demo: Queries Complexas e Indexação no Supabase (PostgreSQL)

Abra o deck e percorra os slides na ordem. Tempo sugerido: 10 min.

1. Slides 2 a 4 (3 min): abra com o problema de negócio. Fila `mt_jobs` com 2,4M linhas, dashboards de 8s e 3 timeouts de webhook por dia. Mostre a tabela dos 3 casos.
2. Slides 5 a 8 (4 min): rode ao vivo `EXPLAIN (ANALYZE, BUFFERS)` do pick da fila antes e depois. Aponte o Seq Scan com 2,38M linhas removidas, depois o Index Scan de 4ms. Repita o raciocínio para sync CRM e dashboard.
3. Slides 9 e 10 (2 min): defenda o padrão de índices por acesso e o particionamento com TTL. Reforce CONCURRENTLY fora de pico.
4. Slides 12 a 14 (1 min): feche com metas (pick abaixo de 10ms, sync abaixo de 250ms, dashboard abaixo de 1,5s) e o aviso de que nada foi aplicado em produção.

Material de apoio: pdi-fullstack-modelagem-dados-a1.pdf (dossiê completo) + 2-sql/06-planos-antes-depois.md (planos para reproduzir no staging).
