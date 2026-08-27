# 2-sql — Queries otimizadas e provas de conceito

> Cada arquivo traz uma **query adversarial** (como estava em produção) e a **versão
> otimizada** (como ficou), com plano `EXPLAIN` antes × depois. Os planos são
> representativos para volumetria de referência V4:
> `mt_jobs` 2.4M linhas · `sync_log` 12M · `events` 8M (particionado) ·
> `leads` 900k · `dashboard_daily` (agregado) 60k linhas/mês.
>
> Simulável em qualquer Supabase com o schema `schema-demo.sql` equivalente (ou
> gerar com pgbench). Rodar com:
>
> ```sql
> EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
> ```

## Arquivos

| Arquivo | Conteúdo | Antes → Depois |
|---|---|---|
| `01-caso-fila-mt_jobs.sql` | JOIN pesado + pick de worker da fila | 1.8s → 4ms |
| `02-dashboard-janelas.sql` | Window functions top-N por cliente | 8.4s → 1.1s |
| `03-sync-crm-cte.sql` | CTEs de auditoria de sync + drift | 4.2s → 180ms |
| `04-indices-brin-btree-gin.sql` | PoC dos 3 tipos de índice | BRIN/B-tree/GIN |
| `05-rls-performance.sql` | RLS na fila com plano real | Seq Scan → Index Scan |
| `06-planos-antes-depois.md` | Planos de execução completos | documental |