# CASO 1 — Gargalo: fila `mt_jobs` no pick do worker

## Sinais

- Worker SDR IA rodando polling a cada 15s começou a estourar o timeout do comando.
- `mt_jobs` quebrou 2.4M linhas; pódio do Grafana mostrava `Seq Scan on mt_jobs`.
- O pick de job, que rodava em ~50ms, degradou para **1.82s** quando a fila encheu
  numa campanha de pico (black friday) e o webhook de enfileitamento começou a 504.

## Diagnóstico

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT j.id, j.client_id, j.payload
FROM mt_jobs j
LEFT JOIN clients c ON c.id = j.client_id
WHERE j.status = 'queued' AND j.queue = 'crm-sync'
ORDER BY j.priority DESC, j.created_at ASC
LIMIT 1;
```

O plano mostrava:

- `Seq Scan on mt_jobs` com `Rows Removed by Filter: 2,381,450` — status/queue sem índice.
- `Nested Loop` no JOIN (FK `client_id` desindexada) — re-scan por linha.
- `Sort` em 2,1M linhas para pegar 1 — pobríssimo.

Duas causas-raiz: filtro da fila sem índice composto (**igualdade→range→ORDER BY**) e LEFT JOIN
que o pick nunca precisava (payload já trazia o que o worker usa).

## Correção

```sql
CREATE INDEX CONCURRENTLY idx_mt_jobs_pick
  ON mt_jobs (status, queue, scheduled_at->fim DESC? não);
-- versão final:
CREATE INDEX CONCURRENTLY idx_mt_jobs_pick
  ON mt_jobs (queue, status, scheduled_at);
CREATE INDEX CONCURRENTLY idx_mt_jobs_client ON mt_jobs (client_id);
```

Uso id segura: `FOR UPDATE SKIP LOCKED` no pick para 5 workers consumindo a mesma URL.

### Resultado

| Métrica | Antes | Depois |
|---|---|---|
| Execution Time | 1.82s | **4.1ms** |
| Estratégia | Seq Scan + Sort | Index Scan |
| Enqueue sob pico | 504 / fila cresce | processo continua |
| Read (buffers) | 94,400 | < 120 |

## Aplicação do padrão

- Toda classe de query de worker deve ter `EXPLAIN` no MR.
- Pick de fila sempre `FOR UPDATE SKIP LOCKED` + limite explícito (`LIMIT 5`).
- `update_status` em batch (CTE) — nunca editor linha a linha no loop.