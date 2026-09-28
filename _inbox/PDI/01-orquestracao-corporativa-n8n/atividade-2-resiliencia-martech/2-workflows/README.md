# Workflows: PDI-MARTECH (resiliência MarTech)

Workflows n8n desenvolvidos para a segunda atividade do PDI. **Não publicar em
produção ainda**: aguardando homologação da apresentação.

## Componentes

| # | Workflow | Tipo | Propósito |
|---|----------|------|-----------|
| 1 | `[CC] MT Queue Gateway` | Webhook | Recebe requests MarTech e enfileira em `mt_jobs` (ACK imediato, idempotência por job_key) |
| 2 | `[CC] MT - Queue Worker` | Schedule (15s) | Consome a fila respeitando semáforo `mt_concurrency`, delega ao Heavy Payload Processor |
| 3 | `[CC] MT - Heavy Payload Processor` | Sub-workflow (executeWorkflow) | Processa payload pesado: normalização JS, progresso em `mt_job_progress`, enriquecimento Python |
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

## Dependências

- Schema v3.0 aplicado (veja `../3-supabase/`)
- Credencial `Command Center Supabase` (`nRJEEi2QwVVKIAHY`) nos nodes Supabase
- **Antes de publicar:** trocar `MT_HEAVY_PAYLOAD_PROCESSOR_ID` no worker pelo ID real
  do sub-workflow `[CC] MT - Heavy Payload Processor` criado no n8n
- O Heavy Payload Processor NÃO tem trigger próprio: e invocado pelo Execute Workflow
  (n8n injeta a entrada direto no primeiro node)

## Como usar (quando autorizado a publicar)

1. `npx --yes n8nac push "2-workflows/[CC] MT Queue Gateway.workflow.ts"` (e demais)
2. No n8n UI: copiar o ID do Heavy Payload Processor e colar em `ExecuteHeavyPayload`
3. Ativar Gateway, Worker e Observabilidade
4. Testar: POST para `https://n8n.fvmarketing.com.br/webhook/mt/gateway` com payload de teste

> **Status: NÃO publicado.** Workflows validados com n8nac (`Workflow is valid`).
> Implementar/conectar somente após homologação da apresentação.

## Configuração

| Parâmetro | Valor default | Onde |
|-----------|--------------|------|
| Intervalo do Worker | 15s | Schedule Trigger do Worker |
| Limite por fila | 5 slots | Tabela `mt_concurrency` (`max_concurrency`) |
| Chunk size payload | 100 itens | Node `Unpack Input` (Heavy Processor) |
| Tolerância de drift | 5% | Node `Decode Sync Envelope` (Observabilidade) |

Obs.: o chunk default do workflow (100 itens) é mais conservador que o limite do
standard (500 itens) porque o enriquecimento em Python por item custa mais que a
normalização em JS. O limite do standard continua valendo como teto; o workflow
pode ser apertado sem violar o padrão, nunca aliviado acima dele.

## Nó a nó (o que cada workflow faz)

**[1] MT Queue Gateway (Webhook)**

| Node | Papel |
|------|-------|
| Webhook (`mt/gateway`) | Entra com `responseMode: responseNode` para responder antes do fluxo seguir |
| Code `Build Job Key` | Monta `queue:object:id` e normaliza o corpo recebido |
| Supabase `Insert Job` | `INSERT ... ON CONFLICT (job_key, queue) DO NOTHING` |
| Respond to Webhook | 202 com `accepted`, `status` e `jobKey` |

Ponto crítico: se o `INSERT` falhar (banco indisponível), o Gateway responde 500
para o chamador tentar de novo. Ele **nunca** responde 202 sem gravar, porque 202
sem linha na fila é perda silenciosa de dado.

**[2] MT Queue Worker (Schedule 15s)**

| Node | Papel |
|------|-------|
| Schedule Trigger | 15 s fixo |
| Supabase `Fetch Queued` | `SELECT ... WHERE status='queued' AND retry_at <= now() ORDER BY priority DESC, created_at ASC LIMIT 10` |
| Code `Check Slots` | Compara em uso com `max_concurrency` e descarta o excedente sem erro |
| Supabase `Acquire` | `UPDATE ... SET status='running', picked_at=now(), owner=:exec WHERE id=:id AND status='queued'` |
| IF `Acquired?` | Só o vencedor do `UPDATE` segue; perdedor sai sem erro |
| Execute Workflow | Chama o Heavy Payload Processor com o job |

O `UPDATE` condicional é o que torna o semáforo correto: em execuções
concorrentes, só uma linha muda de estado, então a leitura de "quantos slots
livres" pode até estar defasada, a tomada de slot não.

**[3] MT Heavy Payload Processor (sub-workflow sem trigger)**

| Node | Papel |
|------|-------|
| Code `Unpack Input` | Extrai `payload.ref`, monta o array leve (chunk de 100) |
| SplitInBatches | Itera os lotes |
| Code `Process Chunk` | Kernel puro: normaliza e enriquece |
| Supabase `Checkpoint` | Grava `chunk_index` com `owner` |
| IF `Last Batch?` | Encerra a iteração e devolve o total |

Sem trigger próprio de propósito: ele só é alcançável pelo Execute Workflow, o
que impede que alguém o ative por acidente em produção com entrada arbitrária.

**[4] MT CRM Sync Observabilidade (Webhook `/mt/crm-sync`)**

| Node | Papel |
|------|-------|
| Webhook `mt/crm-sync` | Envelope padrão |
| Code `Decode Sync Envelope` | Canoniza, calcula os dois hashes e o drift |
| Supabase `Insert Sync Log` | Linha em `mt_sync_log` com status final |
| IF `Drift?` | `|expected - confirmed| / expected > 0,05` |
| Supabase `Insert Delta` | Só quando o IF é verdadeiro |
| Supabase `Upsert Health` | Atualiza `mt_crm_health` no ramo sem drift |

Fluxo de erro também entra por aqui: o workflow que falhou no CRM envia o
envelope com `http_status` de erro e `error_class`, de modo que a trilha registra
a falha em vez de sumir com ela.

## Homologação (critérios para liberar o push)

| # | Critério | Como verificar |
|---|----------|----------------|
| 1 | `n8nac validate` verde nos 4 workflows | Saída `Workflow is valid` |
| 2 | Schema v3.0 aplicado e verificado | Consultas de `3-supabase/MIGRATION-GUIDE.md` |
| 3 | ID real do Heavy Payload Processor no Worker | Campo `ExecuteHeavyPayload` preenchido |
| 4 | ACK 202 medido abaixo de 2 s | `curl -w '%{time_total}'` no Gateway |
| 5 | Semáforo observado em `vw_mt_slots` | `in_use` nunca acima de `max_concurrency` |
| 6 | Retomada de chunk demonstrada | `mt_job_progress.chunk_index` na falha |
| 7 | Drift de 14% gerando delta | `vw_mt_drift_abertos` com a linha |
| 8 | Rollback ensaiado | Desativar Gateway e Worker sem perder jobs |