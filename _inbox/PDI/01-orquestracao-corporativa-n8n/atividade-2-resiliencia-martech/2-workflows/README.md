# Workflows — PDI-MARTECH (resiliencia MarTech)

Workflows n8n desenvolvidos para a segunda atividade do PDI. **Nao publicar em
producao ainda** — aguardando homologacao da apresentacao.

## Componentes

| # | Workflow | Tipo | Proposito |
|---|----------|------|-----------|
| 1 | `[CC] MT Queue Gateway` | Webhook | Recebe requests MarTech e enfileira em `mt_jobs` (ACK imediato, idempotencia por job_key) |
| 2 | `[CC] MT - Queue Worker` | Schedule (15s) | Consome a fila respeitando semaforo `mt_concurrency`, delega ao Heavy Payload Processor |
| 3 | `[CC] MT - Heavy Payload Processor` | Sub-workflow (executeWorkflow) | Processa payload pesado: normalizacao JS, progresso em `mt_job_progress`, enriquecimento Python |
| 4 | `[CC] MT - CRM Sync Observabilidade` | Webhook (`/mt/crm-sync`) | Loga syncs de CRM, calcula drift, alimenta `mt_sync_log` + `mt_crm_health` + `mt_sync_delta` |

## Arquitetura

```
Requisicao MarTech (pico)
      │
      ▼
[1] Queue Gateway ──ACK 202──▶ mt_jobs (queued)
      │
      ▼
[2] Queue Worker (15s) ──slot mt_concurrency──▶ running
      │
      ▼
[3] Heavy Payload Processor ──mt_job_progress──▶ done/failed
      │
      ▼
[4] CRM Sync Observabilidade ──mt_sync_log + health + delta──▶ drift
```

## Dependencias

- Schema v3.0 aplicado (veja `../3-supabase/`)
- Credencial `Command Center Supabase` (`nRJEEi2QwVVKIAHY`) nos nodes Supabase
- **Antes de publicar:** trocar `MT_HEAVY_PAYLOAD_PROCESSOR_ID` no worker pelo ID real
  do sub-workflow `[CC] MT - Heavy Payload Processor` criado no n8n
- O Heavy Payload Processor NÃO tem trigger proprio — e invocado pelo Execute Workflow
  (n8n injeta a entrada direto no primeiro node)

## Como usar (quando autorizado a publicar)

1. `npx --yes n8nac push "2-workflows/[CC] MT Queue Gateway.workflow.ts"` (e demais)
2. No n8n UI: copiar o ID do Heavy Payload Processor e colar em `ExecuteHeavyPayload`
3. Ativar Gateway, Worker e Observabilidade
4. Testar: POST para `https://n8n.fvmarketing.com.br/webhook/mt/gateway` com payload de teste

> **Status: NÃO publicado.** Workflows validados com n8nac (`Workflow is valid`).
> Implementar/conectar somente apos homologacao da apresentacao.

## Configuracao

| Parametro | Valor default | Onde |
|-----------|--------------|------|
| Intervalo do Worker | 15s | Schedule Trigger do Worker |
| Limite por fila | 5 slots | Tabela `mt_concurrency` (`max_concurrency`) |
| Chunk size payload | 100 itens | Node `Unpack Input` (Heavy Processor) |
| Tolerancia de drift | 5% | Node `Decode Sync Envelope` (Observabilidade) |