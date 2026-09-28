# Script de Demonstração: Resiliência MarTech n8n Enterprise (PDI-MARTECH)

> Homologação simulada. NENHUM passo publica em produção.

## Setup

```bash
npx n8nac env status --json

tree _inbox/PDI-MARTECH/
```

## Passo 1: Validar Workflows (n8nac, sem push)

```bash
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT Queue Gateway.workflow.ts"
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT - Queue Worker.workflow.ts"
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT - Heavy Payload Processor.workflow.ts"
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT - CRM Sync Observabilidade.workflow.ts"
# Todos devem acusar: ✅ Workflow is valid
```

## Passo 2: Schema Supabase (v3.0)

Mostrar `3-supabase/supabase-schema-v3.sql`:

- Tabelas: `mt_jobs` · `mt_concurrency` · `mt_job_progress` · `mt_sync_log` · `mt_crm_health` · `mt_sync_delta`
- Views: `vw_mt_queue_backlog` · `vw_mt_slots` · `vw_mt_sync_summary_24h` · `vw_mt_drift_abertos` · `vw_mt_crm_health`
- **Aditivo**: não altera o schema v2.x (`error_*`)

## Passo 3: Mock do fluxo completo

> Para a demo, usar um Supabase local/de teste: não o de produção.

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

## Passo 4: Detectar drift

```bash
# Esperado 120, syncou 118 → drift ~1.7% (dentro da tolerância de 5%) → sem delta grave.
# Agora simular divergência real:
#  expected=1000, synced=860 → drift=14% > 5% → mt_sync_delta aberto

SELECT * FROM vw_mt_drift_abertos;      -- divergências abertas
SELECT * FROM vw_mt_sync_summary_24h;    -- resumo de sync por objeto
SELECT * FROM vw_mt_crm_health;          -- health abaixo do mínimo
```

## Passo 5: Limite de concorrência (semáforo)

```sql
INSERT INTO mt_concurrency (queue, max_concurrency) VALUES ('crm-sync', 5)
ON CONFLICT (queue) DO UPDATE SET max_concurrency = 5;

-- Uso em tempo real (in_use nunca ultrapassa max_concurrency)
SELECT * FROM vw_mt_slots;
```

## Passo 6: Retomada de payload pesado

```bash
# Simular falha no chunk 4 de 10

SELECT * FROM mt_job_progress WHERE job_id = 'demo-1';
# → chunk_index=4/10, status=running

# Re-enfileirar e mostrar retomada do chunk 4 (checkpoint), não do zero
```

## Passo 7: Alertas de monitoramento

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

## Passo 8: Idempotência do Gateway

```bash
# Enviar o MESMO job três vezes em sequência
for i in 1 2 3; do
  curl -s -X POST http://localhost:5678/webhook/mt/gateway \
    -H 'Content-Type: application/json' \
    -d '{"queue":"crm-sync","object":"order","id":"demo-dup","client":"genics"}'
done

SELECT COUNT(*) FROM mt_jobs WHERE job_key LIKE '%demo-dup%';
```

- **Saída esperada:** três ACKs 202 e `COUNT = 1`.
- **Falha:** `COUNT > 1` (idempotência quebrada, `job_key` ou `UNIQUE` ausente).
- **Se falhar:** conferir o `ON CONFLICT (job_key, queue) DO NOTHING` no Gateway.

## Passo 9: Prioridade da fila

```sql
-- Fila com um job urgente atrás de um normal
INSERT INTO mt_jobs (job_key, queue, status, priority, payload)
VALUES ('demo-prio-low', 'import', 'queued', 10, '{}'),
       ('demo-prio-high', 'crm-sync', 'queued', 300, '{}')
ON CONFLICT DO NOTHING;

SELECT job_key, priority FROM mt_jobs
WHERE status = 'queued' ORDER BY priority DESC, created_at ASC;
```

- **Saída esperada:** `demo-prio-high` primeiro.
- **Falha:** ordem alfabética ou por data sem considerar `priority`.

## Passo 10: Backoff e limite de tentativas

```sql
-- Simular três falhas para ver o backoff
UPDATE mt_jobs
   SET attempts = 2,
       retry_at = now() + INTERVAL '2 minutes',
       error_message = 'HTTP 429 rate limit',
       status = 'queued'
 WHERE job_key = 'demo-dup';

SELECT attempts, retry_at, EXTRACT(EPOCH FROM (retry_at - now()))::INTEGER
  AS segundos_ate_retry FROM mt_jobs WHERE job_key = 'demo-dup';
```

- **Saída esperada:** valor próximo de 120 s (terceira tentativa: 2 min).
- **Falha:** `retry_at` nulo (retry imediato, thundering herd) ou job que já
  estourou `max_attempts` ainda em `queued`.
- **Se falhar:** verificar o cálculo de backoff com jitter no Worker.

## Passo 11: Latência do ACK medida

```bash
for i in $(seq 1 20); do
  curl -s -o /dev/null -w '%{http_code} %{time_total}\n' \
    -X POST http://localhost:5678/webhook/mt/gateway \
    -H 'Content-Type: application/json' \
    -d '{"queue":"import","object":"product","id":"ack-'$i'","client":"demo"}'
done
```

- **Saída esperada:** 20 todos com `202` e `time_total` abaixo de 0,5 s.
- **Falha:** qualquer 5xx ou tempo acima de 2 s.

## Passo 12: Erro do CRM vira trilha, não silêncio

```bash
curl -s -X POST http://localhost:5678/webhook/mt/crm-sync \
  -H 'Content-Type: application/json' \
  -d '{"syncId":"demo-err","object":"contact","direction":"push","client":"genics","expected":50,"synced":0,"http_status":429,"error_class":"rate_limit"}'

SELECT status, error_class, http_status FROM mt_sync_log
 WHERE sync_id = 'demo-err';
```

- **Saída esperada:** linha com `status=error` e `error_class=rate_limit`.
- **Falha:** nenhuma linha (trilha perdida no ramo de erro).

## Passo 13: Integridade do schema e dos índices

```sql
SELECT COUNT(*) FROM information_schema.tables
 WHERE table_schema='public' AND table_name LIKE 'mt_%';   -- 6

SELECT COUNT(*) FROM pg_indexes
 WHERE schemaname='public' AND tablename='mt_%';           -- >= 5
```

- **Saída esperada:** 6 tabelas e ao menos 5 índices de fila.
- **Falha:** número menor (migração parcial) ou tabela `error_*` alterada.

## Passo 14: Rollback ensaiado

```bash
# 1. Desativar Gateway e Worker no n8n (botão Active off)
# 2. Confirmar que nada mais escreve
SELECT COUNT(*) FROM mt_jobs WHERE created_at > now() - INTERVAL '1 minute';  -- 0
# 3. Jobs remanescentes ficam em queued, nenhum dado perdido
```

- **Saída esperada:** zero jobs novos após desligar e nenhum job sumido.
- **Falha:** job desaparecendo ou workflow legado afetado.

## Passo 15: Verificação final

```bash
npx -y n8nac skills validate "_inbox/PDI-MARTECH/2-workflows/[CC] MT Queue Worker.workflow.ts"
grep -rn '\{\{' _inbox/PDI-MARTECH --include='*.md' ;   # sem saída: nenhum placeholder
grep -rniE 'lorem|texto aqui' _inbox/PDI-MARTECH --include='*.md' ;   # sem saída
```

- **Saída esperada:** `Workflow is valid` e nenhuma ocorrência de travessão.
- **Falha:** validação vermelha ou caractere proibido no material.

## Observação

Nenhum workflow foi publicado no n8n. Publicação somente após homologação,
com confirmação explícita via `bash 6-automation/deploy-martech.sh`.