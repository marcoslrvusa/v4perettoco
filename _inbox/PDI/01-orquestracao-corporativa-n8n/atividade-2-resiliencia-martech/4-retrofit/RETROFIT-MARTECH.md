# RETROFIT: Como adaptar workflows MarTech existentes ao padrão PDI-MARTECH

> Objetivo: transformar workflows síncronos frágeis em pipelines assincronos
> resilientes SEM reescrever a lógica de negócio existente.

## 1. Workflows MarTech comuns que precisam de retrofit

| Workflow atual | Problema | Mudança |
|----------------|----------|---------|
| Importação de pedidos (SPA → CRM) | Síncrono, trava em payload grande | Gateway + Worker + Heavy Payload |
| Sincronização de contatos (CRM push) | Falha some, cliente descobre | Envelope padrão → Observabilidade |
| Enriquecimento de leads (API externa) | Rate limit derruba a execução | Fila com backoff + circuit |
| Exportação de relatórios (grandes) | Timeout do webhook | Job assíncrono + status polling |

## 2. Passo a passo genérico

### 2.1 Queue Gateway

```ts
// Antes (workflow atual)
Webhook → [lógica pesada 1] → [lógica pesada 2] → Respond

// Depois
Webhook → [CC] MT Queue Gateway  (enfileira + ACK 202)
        → [CC] MT - Queue Worker  (delega)
        → [CC] MT - Heavy Payload Processor (lógica pesada)
```

### 2.2 Camada de observabilidade

O workflow que fala com o CRM passa a chamar o webhook `/mt/crm-sync`
ao FINAL, com o envelope padrão:

```json
{
  "syncId": "job-123",
  "object": "order",
  "direction": "push",
  "client": "genics",
  "expected": 120,
  "synced": 118,
  "http_status": 200,
  "execution_url": "https://n8n.../executions/...",
  "payload": "<opcional>",
  "response": "<opcional>"
}
```

O Observabilidade calcula hash, drift e atualiza `mt_crm_health`.

## 3. Regras de retrofit

1. **Não mudar a lógica de negócio** no retrofit: só o transporte.
2. **Job keys estáveis**: `queue:object:id` para idempotência.
3. **Checkpoint em jobs > 5 min**: `mt_job_progress` com chunk_index.
4. **Sempre enviar envelope** ao Observabilidade (mesmo em erro).
5. **Backoff exponencial** no retry (30s → 1m → 2m), max 3 tentativas.
6. **Circuit breaker** (atividade 1) protege a integração externa.

## 4. Checklist por workflow retrofitado

- [ ] Fluxo passa pelo Gateway (ACK 202)
- [ ] Payload > 100 itens usa chunks com progresso
- [ ] Envelope de sync enviado ao `/mt/crm-sync`
- [ ] `mt_sync_log` registra done/error
- [ ] Drift detectado gera `mt_sync_delta`
- [ ] Erros entram no Error Handler Central (atividade 1)
- [ ] Workflow continua ativo com mesmo trigger

## 5. Exemplo completo (Sincronização de pedidos Kommo)

```
Kommo Webhook (novo pedido)
  → [retrofit] Envelope padrão montado no Code node
  → [CC] MT Queue Gateway      (job: pedido:sync:123, ACK 202)
  → [CC] MT - Queue Worker     (slot 1/5, running)
  → [CC] MT - Heavy Payload    (normaliza itens, enriquece, progresso)
  → Kommo API (push)           (circuit protegido)
  → [CC] MT - CRM Sync Obs     (mt_sync_log done, health +1)
  └── drift? → mt_sync_delta → alerta 15 min (antecipando cliente)
```