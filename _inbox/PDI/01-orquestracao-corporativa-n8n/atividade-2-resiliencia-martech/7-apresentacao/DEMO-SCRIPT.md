# Script de Demonstracao — Resiliencia MarTech n8n Enterprise (PDI-MARTECH)

> Homologacao simulada. NENHUM passo publica em produção.

## Setup

```bash
npx n8nac env status --json

tree _inbox/PDI-MARTECH/
```

## Passo 1 — Validar Workflows (n8nac, sem push)

```bash
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT Queue Gateway.workflow.ts"
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT - Queue Worker.workflow.ts"
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT - Heavy Payload Processor.workflow.ts"
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT - CRM Sync Observabilidade.workflow.ts"
# Todos devem acusar: ✅ Workflow is valid
```

## Passo 2 — Schema Supabase (v3.0)

Mostrar `3-supabase/supabase-schema-v3.sql`:

- Tabelas: `mt_jobs` · `mt_concurrency` · `mt_job_progress` · `mt_sync_log` · `mt_crm_health` · `mt_sync_delta`
- Views: `vw_mt_queue_backlog` · `vw_mt_slots` · `vw_mt_sync_summary_24h` · `vw_mt_drift_abertos` · `vw_mt_crm_health`
- **Aditivo** — não altera o schema v2.x (`error_*`)

## Passo 3 — Mock do fluxo completo

> Para a demo, usar um Supabase local/de teste — não o de produção.

```bash
# 1. Enfileirar job (simula o Gateway)
curl -X POST http://localhost:5678/webhook/mt/gateway \
  -H 'Content-Type: application/json' \
  -d '{"queue":"crm-sync","object":"order","id":"demo-1","client":"genics"}'
# → 202 {"accepted":true,"status":"queued","jobKey":"..."}

# 2. Verificar na fila
SELECT * FROM mt_jobs ORDER BY created_at DESC LIMIT 3;

# 3. Marcado running pelo Worker + progresso em mt_job_progress

# 4. Registrar envelope no Observabilidade
curl -X POST http://localhost:5678/webhook/mt/crm-sync \
  -H 'Content-Type: application/json' \
  -d '{"syncId":"demo-1","object":"order","direction":"push","client":"genics","expected":120,"synced":118,"http_status":200}'
```

## Passo 4 — Detectar drift

```bash
# Esperado 120, syncou 118 → drift ~1.7% (dentro da tolerância de 5%) → sem delta grave.
# Agora simular divergência real:
#  expected=1000, synced=860 → drift=14% > 5% → mt_sync_delta aberto

SELECT * FROM vw_mt_drift_abertos;      -- divergências abertas
SELECT * FROM vw_mt_sync_summary_24h;    -- resumo de sync por objeto
SELECT * FROM vw_mt_crm_health;          -- health abaixo do mínimo
```

## Passo 5 — Limite de concorrência (semáforo)

```sql
INSERT INTO mt_concurrency (queue, max_concurrency) VALUES ('crm-sync', 5)
ON CONFLICT (queue) DO UPDATE SET max_concurrency = 5;

-- Uso em tempo real (in_use nunca ultrapassa max_concurrency)
SELECT * FROM vw_mt_slots;
```

## Passo 6 — Retomada de payload pesado

```bash
# Simular falha no chunk 4 de 10

SELECT * FROM mt_job_progress WHERE job_id = 'demo-1';
# → chunk_index=4/10, status=running

# Re-enfileirar e mostrar retomada do chunk 4 (checkpoint), não do zero
```

## Passo 7 — Alertas de monitoramento

```sql
-- Worker travado? job parado há +10 min
SELECT * FROM vw_mt_queue_backlog WHERE stale_queued > 0;

-- Health below minimum alerta
SELECT * FROM vw_mt_crm_health WHERE below_min = true;
```

## Sucesso

- ✅ ACK 202 imediato (webhook não trava em pico)
- ✅ Concorrência controlada por fila (semáforo `mt_concurrency`)
- ✅ Payload pesado com checkpoint (retomada do chunk)
- ✅ Drift detectado antes de afetar o cliente
- ✅ Health por objeto no dashboard

## Observação

Nenhum workflow foi publicado no n8n. Publicação somente após homologação,
com confirmação explícita via `bash 6-automation/deploy-martech.sh`.