# Guia de Migração: Schema v3.0 (MarTech Resilience)

> **Banco:** Supabase `gswzuzetverulcgzhynb` | **Schema:** `public`
> **Compatibilidade:** aditivo sobre v2.x (erro/circuit): nada e alterado

## O que este schema adiciona

| Tabela | Finalidade |
|--------|-----------|
| `mt_jobs` | Fila assíncrona de jobs MarTech |
| `mt_concurrency` | Limite de concorrência por fila |
| `mt_job_progress` | Checkpoint de payloads pesados |
| `mt_sync_log` | Auditoria de sincronização com CRM |
| `mt_crm_health` | Agregado de saúde por entidade |
| `mt_sync_delta` | Divergências detectadas (pre-cliente) |

| View | Finalidade |
|------|-----------|
| `vw_mt_queue_backlog` | Jobs aguardando pois fila |
| `vw_mt_slots` | Slots em uso vs limite |
| `vw_mt_sync_summary_24h` | Resumo de sync 24h |
| `vw_mt_drift_abertos` | Deltas não resolvidos |
| `vw_mt_crm_health` | Health abaixo do mínimo |

## Como aplicar

### Opção A: SQL Editor (dashboard)

1. Abrir `https://supabase.com/dashboard/project/gswzuzetverulcgzhynb/sql/editor`
2. Colar o conteúdo de `supabase-schema-v3.sql`
3. Rodar (Ctrl+Enter)

### Opção B: n8n (via credencial Postgres existente)

Já usado na migração v2.1: criar um workflow temporário com node Postgres
(credencial `Peretto`) com `operation: executeQuery` e o corpo do schema.

### Opção C: Script

```bash
bash ../6-automation/run-migration.sh
```

## Verificação após a migração

```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema='public' AND table_name LIKE 'mt_%'
ORDER BY table_name;

SELECT relname FROM pg_class
WHERE relkind='v' AND relname LIKE 'vw_mt_%' ORDER BY relname;
```

Resultado esperado:
- tabelas: `mt_concurrency`, `mt_crm_health`, `mt_job_progress`, `mt_jobs`,
  `mt_sync_delta`, `mt_sync_log`
- views: `vw_mt_crm_health`, `vw_mt_drift_abertos`, `vw_mt_queue_backlog`,
  `vw_mt_slots`, `vw_mt_sync_summary_24h`

## Rollback

```sql
DROP VIEW IF EXISTS vw_mt_crm_health, vw_mt_drift_abertos, vw_mt_queue_backlog,
  vw_mt_slots, vw_mt_sync_summary_24h;
DROP TABLE IF EXISTS mt_sync_delta, mt_crm_health, mt_sync_log,
  mt_job_progress, mt_concurrency, mt_jobs;
```

> Nenhuma tabela v2.x (error_dlq, error_circuit_breaker, error_retry_log,
> error_alert_config) e tocada por este schema.