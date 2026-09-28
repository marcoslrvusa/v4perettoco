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

A janela (`LIMIT :window`) é parte do padrão: em vez de tentar esvaziar a fila
inteira em um único ciclo, o poller consome no máximo `window` jobs por execução,
o que mantém cada execução do Worker curta e evita que um lote gigante segure o
event loop do n8n.

## 4.1 Backoff exponencial com jitter

Backoff determinístico agrupa todas as retentativas no mesmo instante e gera um
segundo pico (efeito "thundering herd"). O padrão usa backoff exponencial com
jitter uniforme de até 20%:

```js
// Tenta 1: 30s, tentativa 2: 60s, tentativa 3: 120s, sempre com jitter
const BASE_MS = [30_000, 60_000, 120_000];

function retryDelay(attempt) {
  const index = Math.min(Math.max(attempt - 1, 0), BASE_MS.length - 1);
  const base = BASE_MS[index];
  const jitter = Math.floor(Math.random() * 0.2 * base);
  return base + jitter;
}

return { retry_at: new Date(Date.now() + retryDelay(job.attempts)) };
```

**Exemplo numérico:** três jobs que falharam juntos no instante `T` viram
retentativas em `T+30s`, `T+36s` e `T+42s` em vez de todas em `T+30s`,
diluindo o pico em três ciclos do poller (15s cada).

Decisão de arquitetura: o backoff é calculado no Worker e gravado em `retry_at`,
não no cliente, de modo que qualquer Worker que pegue a fila enxergue a mesma
política. `retry_at` nulo significa "pode processar agora", o que mantém a query
do poller única e indexável.

### 4.1.1 Escolha do cancelamento e da prioridade

| Situação | Decisão |
|----------|---------|
| Job com mais de 3 tentativas | Vai para `failed` e entra no `error_dlq` da atividade 1 |
| Job cujo cliente desistiu (webhook cancelado) | Status `failed` com `error_message = cancelado pelo cliente`, nunca `done` |
| Dois jobs do mesmo `job_key` chegando ao mesmo tempo | `ON CONFLICT (job_key, queue) DO NOTHING`, o segundo vira ACK do primeiro |
| Fila `import` lotada e chegando job de `crm-sync` | Filas independentes: cada uma tem seu `max_concurrency`, não há bloqueio cruzado |

## 5. Limites de Concorrência por Entidade

| Recurso | Limite Default |
|----------|----------------|
| Execuções simultâneas por fila | 5 |
| Payloads pesados em paralelo | 2 por fila |
| Timeout de job | 10 min |
| Max tentativas por job | 3 |

**Exemplo numérico:** três filas (`crm-sync`, `campaign`, `import`) com 5 slots
cada dão 15 execuções simultâneas no pior caso, contra o cenário anterior de
concorrência ilimitada em que 200 webhooks simultâneos geravam 200 execuções.
A redução é de 200 para 15, ou 13,3x menos pressão sobre a instância.

Como chegar ao limite: medir o tempo médio de processamento (`W`) de uma semana
e a chegada média por fila (`λ`), aplicar $L = \lambda W$ e arredondar para cima
com folga de 25%. Se o resultado maior que 10 slots por fila, o gargalo está no
tempo de processamento e não na concorrência: primeiro reduzir `W` com chunking,
depois aumentar slot.

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

## 8. Telemetria e Alerta

| Métrica | Fonte | Cardinalidade | Alerta |
|---------|-------|---------------|--------|
| `queued_total` por fila | `vw_mt_queue_backlog` | 1 por fila | `stale_queued > 0` por 10 min |
| `slot_usage_pct` | `vw_mt_slots` | 1 por fila | > 90% por 5 min |
| `attempts_avg` | `mt_jobs` | 1 global | > 1,5 em 1 h (meta) |
| `reaper_reclaims` | contagem de devoluções | 1 global | > 5 em 10 min (meta) |
| Latência p95 do ACK | log do Gateway | 1 global | > 2 s |

Regra de cardinalidade: nenhuma métrica carrega `job_key` ou `sync_id` como
label. Isso evita séries com milhares de séries distintas e mantém o custo do
coletor constante mesmo em pico. Identificador de job só entra em log, nunca em
métrica.

## 9. Plano de Teste e Critérios de Aceite

| Caso | Passo | Esperado | Critério de falha |
|------|-------|----------|-------------------|
| ACK rápido | 200 POSTs em rajada de 1 s no Gateway | Todos respondem 202 em < 2 s | Alguma resposta acima de 2 s ou erro 5xx |
| Idempotência | Mesmo `job_key` enviado 3 vezes | 1 linha em `mt_jobs`, 3 ACKs | 2 ou mais linhas |
| Limite de slots | Inserir 50 jobs com 5 slots | Nunca mais que 5 em `running` | `in_use > max_concurrency` |
| Retomada de Worker | Matar o Worker com job em `running` | Reaper devolve para `queued` em 1 min | Job preso por mais de 2 min |
| Backoff | Simular 3 falhas seguidas | `retry_at` em ~30s, 60s, 120s com jitter | Retentativa imediata ou igual |
| DLQ | 4 falhas no mesmo job | `status = failed` e linha no `error_dlq` | Job tentando para sempre |
| Prioridade | Enfileirar `campaign` depois de `crm-sync` | Ordem respeitada por `priority DESC` | Fila sem ordenação |

Critério de aceite global: os sete casos passam duas vezes seguidas, com as
consultas de `5-monitoring/DASHBOARD-QUERIES.md` mostrando os números esperados
durante a execução.

## 10. Checklist de Adesão

- [ ] Todo webhook de entrada só grava em `mt_jobs` e responde 202.
- [ ] `job_key` é estável e determinístico (não usa timestamp aleatório).
- [ ] Existe `UNIQUE (job_key, queue)` com `ON CONFLICT DO NOTHING`.
- [ ] Todo Worker atualiza `heartbeat_at` a cada 30 s.
- [ ] Reaper roda a cada 1 min e devolve job sem heartbeat de 2 min.
- [ ] `max_attempts` é 3 e a exaustão vai para `failed` + `error_dlq`.
- [ ] Backoff usa jitter e é gravado em `retry_at`.
- [ ] `max_concurrency` é declarado por fila em `mt_concurrency`.
- [ ] Nenhuma query de poller varre a tabela inteira (janela com `LIMIT`).
- [ ] Métricas não carregam identificador de job como label.
- [ ] Payload nunca trafega completo na linha do job.
- [ ] Rollback documentado: desativar Gateway e Worker sem perder jobs.