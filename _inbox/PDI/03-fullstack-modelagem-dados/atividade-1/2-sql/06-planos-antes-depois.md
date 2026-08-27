# 06-planos-antes-depois.md — Planos de execução (adversarial before × after)

> Planos documentais dos 3 casos reais. Rodando em qualquer Supabase 15+ com os
> schemas de referência (`mt_jobs` 2.4M · `sync_log` 12M · `events` 8M · `leads` 900k).
> Use `EXPLAIN (ANALYZE, BUFFERS, COSTS)` para reproduzir.

---

## CASO 1 — Fila `mt_jobs` (pick de worker)

### ANTES — 1.82s (produção)

```text
Limit  (cost=41,920.00..41,920.01 rows=1)
  ->  Sort  (cost=41,920.00..41,901.22 rows=1)   [762 ms]
        Sort Key: j.priority DESC, j.created_at ASC
        ->  Nested Loop  (cost=0.86..41,918.00 rows=1)
              ->  Seq Scan on mt_jobs j
                    Filter: ((status='queued') AND (queue='crm-sync'))
                    Rows Removed by Filter: 2,381,450
              ->  Index Scan using clients_pkey (c.id)     [re-scan por linha]
  Planning Time: 0.4 ms   Execution Time: 1,820 ms
Buffers: shared hit=9,600 read=94,120
```

### DEPOIS — 4ms (pós índices + remoção do LEFT JOIN)

```text
Limit  (cost=0.56..4.90 rows=5)
  ->  Index Scan using idx_mt_jobs_pick on mt_jobs j
        Index Cond: ((status = 'queued') AND (queue = 'web'))
        Filter: (scheduled_at <= now())
  Planning Time: 0.3 ms   Execution Time: 4.1 ms
```

Δ 450×. O `Seq Scan` de 2.4M vira `Index Scan`; o `Sort` de 762ms vira inexistente.

## CASO 2 — Sync CRM (auditoria 30d)

### ANTES — 4.2s

```text
Finalize HashAggregate  (group key: c.id, s.object, s.direction)
  ->  Gather N Worker(s)  processes 1
        ->  Partial HashAggregate  ...
              ->  Hash Join  (s.client_id = c.id)
                    Hash cond: s.client_id = c.id
                    ->  Seq Scan on sync_log s
                          Filter: (created_at >= (now() - '30 days'))
                          Rows Removed by Filter: 11,820,144
                    ->  Hash  rows=812
  Execution Time: 4,210 ms
```

### DEPOIS — 180ms (índice composto + BRIN)

```text
HashAggregate  (HashAggregate)  rows=182
  ->  Bitmap Heap Scan on sync_log s
        Recheck Cond: (created_at >= now() - '30 days')
        ->  Bitmap Index Scan on idx_sync_log_created_brin
              Recheck Cond: same
  ->  Nested Loop  (c.id = s.client_id)  [Index Scan clients_pkey]
  Execution Time: 184 ms
```

Δ 23×. Endereçou o JOIN (índice na FK) e o filtro temporal (BRIN).

---

## CASO 3 — Dashboard de performance (janela 7d)

### ANTES — 8.4s

```text
HashAggregate  (3 scans na mesma tabela)
  ->  CTE totals  →  Seq Scan on events (8,102,400 rows) x 2
  CTE top        →  Seq Scan + HashAggregate (escolha da query)
  SubPlan        →  string_agg com correlação (`WHERE top.client_id = t.client_id`)
  Execution Time: 8,405 ms
```

### DEPOIS — ~380ms (materialização + 1 scan)

```text
Limit (50)  rows 
  ->  Sort (GroupAggregate)   SUM...
        ->  HashAggregate  (row=60,480 → mv_daily_metrics)
              ->  Seq Scan on mv_daily_metrics
                    Filter: (day >= (date_trunc('day', now()) - '7 days'))
  Execution Time: 384 ms
```

Δ 22×. `count(DISTINCT)` caro é movido para refresh incremental da MV.

---

## Checklist de leitura do plano

| Pergunta | Ferramenta |
|---|---|
| Estou lendo só `Seq Scan`? | Problema de índice ou RLS — ver Caso 1/5 |
| Os `rows` batem com a realidade? | Confiar em `ANALYZE` recente (autovacuum) |
| A soma no `Execution Time` explode em `Planning`? | CTE volumetricamente recalculada — forçar inline |
| Tem `temporary files`? | `work_mem` estourado — subir `work_mem` da sessão/role |
| Índice existe mas não é usado? | RLS complexa ou correção de `COLLATION`/type cast |