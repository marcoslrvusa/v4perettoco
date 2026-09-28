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

## Pré-checklist antes de rodar

1. Backup/exportação recente do schema `public` (mesmo sendo aditivo).
2. Nenhum workflow em execução escrevendo em `mt_*` (a v3.0 ainda não está em
   produção, então este item vale principalmente para reexecuções).
3. SQL Editor aberto em transação: rodar o script inteiro de uma vez, não por
   pedaços, para que views que dependem de tabelas não fiquem quebradas no meio.
4. Anotar a contagem atual de objetos `mt_*` antes (deve ser zero na primeira
   aplicação):

```sql
SELECT COUNT(*) AS objetos_mt FROM information_schema.tables
WHERE table_schema = 'public' AND table_name LIKE 'mt_%';
```

## Índices que a fila depende

A fila só mantém o poller barato se existirem os índices abaixo. Sem eles, cada
ciclo de 15 s vira um scan em uma tabela que cresce a cada job:

| Índice | Colunas | Por quê |
|--------|---------|---------|
| `mt_jobs_poll` | `(status, priority DESC, created_at)` | A query do poller é exatamente esse predicado |
| `mt_jobs_retry` | `(status, retry_at)` | Filtra jobs que já podem voltar para a fila |
| `mt_jobs_heartbeat` | `(status, heartbeat_at)` | O Reaper varre `running` com heartbeat antigo |
| `mt_sync_log_window` | `(created_at)` | As consultas de dashboard sempre filtram janela |
| `mt_job_progress_job` | `(job_id, chunk_index)` | Retomada e progresso por job |

Verificação pós-migração dos índices:

```sql
SELECT tablename, indexname FROM pg_indexes
WHERE schemaname = 'public' AND tablename LIKE 'mt_%'
ORDER BY tablename, indexname;
```

**Exemplo numérico:** com 200.000 linhas em `mt_jobs` e um índice em
`(status, priority DESC, created_at)`, o poller lê apenas as linhas `queued`,
que numa fila saudável são dezenas; sem o índice, o planner varre as 200.000
linhas a cada 15 s, ou 1,33 milhão de linhas lidas por minuto sem necessidade
alguma.

## Observações de compatibilidade

- As tabelas `error_*` da atividade 1 continuam sendo escritas pelos workflows já
  homologados: nenhum `ALTER` ou `DROP` as toca.
- As views novas usam prefixo `vw_mt_` para não colidir com `vw_crm_health` nem
  `vw_crm_drift_abertos` citadas nos padrões (as views efetivas do schema são as
  `vw_mt_*`; os padrões usam o nome curto como atalho de leitura).
- Schema `public` no Supabase é o mesmo usado pela credencial `Peretto` já
  existente, então nenhum ajuste de credencial é necessário na migração.
- A migração é idempotente no sentido operacional: rodar duas vezes não duplica
  objetos, pois `CREATE TABLE IF NOT EXISTS` e `CREATE OR REPLACE VIEW` são a
  base do script.