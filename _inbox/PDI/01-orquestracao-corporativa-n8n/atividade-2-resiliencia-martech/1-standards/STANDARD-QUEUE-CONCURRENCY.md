# Padrão de Filas e Concorrência: n8n Enterprise V4

> **Versão:** 1.0 | **Status:** Pronto para homologação | **Última revisão:** 2026-08-05

## 1. Problema

Workflows MarTech processam requisições em linha reta (síncrono). Em picos de
requisição (campanha, black friday, importação em massa), cada requisição HTTP
dispara uma execução que:

- compete pela memória e event loop do n8n;
- estoura o limite de execuções simultâneas;
- trava payloads pesados (JSON com dezenas de MB) em um único no.

Resultado: a instância degrada, execuções ficam empilhadas na fila interna do n8n
e o SLA de resposta ao cliente quebra.

## 2. Solução: Fila Assíncrona + Semafaro de Concorrência

```
┌────────────────────────────────────────────────────────────┐
│ GATEWAY DE ENTRADA (Webhook / auto)                         │
│  → enfileira job na tabela mt_queue (status = queued)       │
│  → responde ACK imediato (nunca processa no request)        │
├──────────────────────────────────────────────────────────────┤
│ POLLER (ScheduleTrigger a cada 15s)                          │
│  → SELECT jobs queued por prioridade                        │
│  → adquire slot (semafaro distribuido)                      │
│  → status = running, atualiza heartbeat                    │
├──────────────────────────────────────────────────────────────┤
│ WORKER (sub-workflow assincrono por job)                     │
│  → processa payload (chunking: ver Padrão Payload Pesado)  │
│  → integra CRM / envia email / atualiza documentos         │
│  → status = done | error com retry programado              │
├──────────────────────────────────────────────────────────────┤
│ REAPER (ScheduleTrigger a cada 1 min)                        │
│  → jobs running sem heartbeat recente → de volta para fila  │
│  → jobs com retry_at <= now → de volta para queued         │
└──────────────────────────────────────────────────────────────┘
```

### 2.1 Fila de Mensagens

Fila baseada na tabela `mt_jobs` no Supabase. Cada requisição vira um job:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `job_key` | TEXT UNIQUE | Chave de idempotência (evita duplicidade) |
| `queue` | TEXT | Nome da fila (`crm-sync`, `campaign`, `import`) |
| `status` | TEXT | `queued` \| `running` \| `done` \| `failed` |
| `priority` | INT | Maior = mais prioritário |
| `payload` | JSONB | Payload leve do job (as referências carregadas depois) |
| `attempts` | INT | Tentativas executadas |
| `max_attempts` | INT | Limite (default 3) |
| `created_at`, `picked_at`, `finished_at` | TIMESTAMPTZ | Timeline |
| `heartbeat_at` | TIMESTAMPTZ | Último sinal do worker |
| `retry_at` | TIMESTAMPTZ | Libera job de novo após backoff |
| `error_message` | TEXT | Último erro |

Regras:
- **Idempotência:** deduplica por `job_key + queue` antes de inserir.
- **Retry:** worker que falha incrementa `attempts` e agenda `retry_at` com backoff.
- **Dead letter:** após `max_attempts`, status = `failed` e o job entra no error_dlq
  (Padrão Universal de Tratamento de Erros).

### 2.2 Semafaro de Concorrência

O n8n mantém uma fila interna de execuções, mas **não limita concorrência por fila**.
Usamos uma tabela de slots (`mt_concurrency`) como semafaro distribuído:

```
-- worker só avança se o número de slots ativos da fila for < limite
```

- Cada fila tem `max_concurrency` configurado (default 5).
- O worker verifica os slots antes de processar. Se estiver no limite, o job
  volte para a fila (não bloqueia a execução do n8n).
- A tomada do slot é atômica via `UPDATE ... SET status='running', picked_at=now()
  WHERE id = :id AND status='queued'`: apenas uma execução vence o race.

### 2.3 Heartbeat e Reaper

- Worker atualiza `heartbeat_at` a cada 30s.
- Reaper (1 min) devolve para `queued` jobs em `running` com heartbeat antigo
  (> 2 min): sinais de processamento morto.
- Reaper também re-enfileira jobs com `retry_at <= now()`.

## 3. Sub-workflows Assincronos

O modelo assíncrono real do padrão:

**Gateway (webhook) só enfileira e responde ACK imediato**: o processamento
pesado nunca acontece no request de entrada. O Poller (ScheduleTrigger) pega os
jobs enfileirados, adquire o slot e chama um **sub-workflow por job** via nó
`Execute Workflow` (mode `sync`, limitado pela concorrência da fila).

```
Webhook entrada → mt_jobs (queued) → ACK 202
Poller (15s)   → token slot → Execute Workflow: <Workflow Worker> (sync)
Worker         → processa payload → mt_jobs (done) + mt_sync_log
```

Se o processamento ultrapassar alguns minutos, o job simplesmente fica `running`
com heartbeat e é retomado pelo Reaper em nova execução (idempotência garante
segurança).

## 4. Prioridades

Fila priorizada (valor alto primeiro):

```sql
SELECT * FROM mt_jobs q
WHERE q.status = 'queued' AND q.retry_at <= now()
ORDER BY q.priority DESC, q.created_at ASC
LIMIT :window;
```

## 5. Limites de Concorrência por Entidade

| Recurso | Limite Default |
|----------|----------------|
| Execuções simultâneas por fila | 5 |
| Payloads pesados em paralelo | 2 por fila |
| Timeout de job | 10 min |
| Max tentativas por job | 3 |

## 6. Vias de Escala

- O semafaro + batch window limitam a pressão sobre a instância single.
- Para volume 50x: mover a fila para Redis (n8n já tem credenciais Redis) usando
  um List + bloqueio. O código do worker muda pouco (conector).
- Credenciais de integrações ficam no n8n (Secretvault), nunca no payload.

## 7. Anti-Patterns de Fila

| Anti-pattern | Problema |
|--------------|----------|
| Processar payload pesado no webhook de entrada | Bloqueia a instância e perde ACK rápido |
| Concorrência ilimitada no schedule | Derruba o n8n |
| Retry infinito | Fila enche; usa DLQ |
| Heartbeat errado | Reaper devolve job ainda processando (duplica) |
| Sem idempotência | Mesmo dado carregado 3x |
| Payload inteiro na linha do job | Fila pesada; guarda payload separado |
| Sync sem trilha | Não da para saber quando o cliente foi afetado |