# Padrao de Observabilidade de Sincronizacao com CRM — n8n Enterprise V4

> **Versao:** 1.0 | **Status:** Pronto para homologacao | **Ultima revisao:** 2026-08-05

## 1. Problema

Integracoes com CRMs terceiros (Kommo, HubSpot, RD Station, Pipedrive) acontecem em
workflows que sincronizam contatos, pedidos, conversas e propriedades. Quando o CRM
recusa payload, muda schema, aplica rate limit ou cai, o workflow falha — mas a
falha **so chega ao time quando o cliente reclama**. Nao existe trilha do que foi
sincronizado, quando, com qual payload e que erro retornou.

## 2. Solucao: Sincronizacao Auditada + Detector de Divergencia

```
┌────────────────────────────────────────────────────────────┐
│ CAMADA 1: Audit Log (mt_sync_log)                           │
│  Todo sync inicia: status = in_progress                    │
│  Sucesso → done | Falha → error (+ error_class)            │
│  payload_hash para comparacao futura                      │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 2: Health por Entidade (mt_crm_health)               │
│   Resumo de erros/sucesso por object + janela              │
│   Taxa de erro global e drift window gerenciado            │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 3: Detector de Divergencia (mt_sync_delta)           │
│   Compara o esperado vs o que o CRM retornou                │
│   Amplitude com diferenca acima do limite → alerta          │
└──────────────────────────────────────────────────────────────┘
```

Filosofia: **nunca confie no retorno; compare o que saiu com o que deveria ter
saido**. Divergencias viram um registro em `mt_sync_delta` (nao um erro que se
perde), e um workflow de alerta decide se a divergencia ja impacta o cliente.

## 3. Tabela de Trilha (mt_sync_log)

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `id` | UUID | PK |
| `sync_id` | TEXT | Correlation id do job |
| `object` | TEXT | `contact`, `order`, `conversation`, `product` |
| `direction` | TEXT | `push` (n8n → CRM), `pull` (CRM → n8n) |
| `source` | TEXT | Integracao (Kommo API, HubSpot, etc) |
| `client` | TEXT | Cliente afetado |
| `payload_hash` | TEXT | Hash do payload enviado (consistencia) |
| `response_hash` | TEXT | Hash do que foi retornado pelo CRM |
| `status` | TEXT | `in_progress` \| `done` \| `error` |
| `http_status` | INT | Resposta HTTP do CRM |
| `error_class` | TEXT | Classe mapeada para o padrao de erros |
| `error_message` | TEXT | Mensagem resumida |
| `attempts` | INT | Tentativas |
| `execution_url` | TEXT | Link da execucao no n8n |
| `drift` | INT | Divergencias percebidas pelo detector |
| `created_at`, `finished_at` | TIMESTAMPTZ | Timeline |

## 4. Health por Entidade (mt_crm_health)

A cada sync concluido, o handler atualiza um agregado por `object + direction`:

```
company, object, direction, total, success, failed,
error_class_count (JSONB), last_sync_at, drift_count,
min_health, updated_at
```

- `health_score = success / total` na janela (default 1h, computado na view).
- A view `vw_crm_health` devolve todos os healths abaixo do `min_health` config.

## 5. Detector de Divergencia — "antes de afetar o cliente"

1. O workflow que faz o sync grava o **esperado**: quantos registros deveriam
   existir (ex: `total = 1200` apos a importacao).
2. Depois do sync, o CRM confirma o contador real; se a diferenca > tolerancia,
   um registro `mt_sync_delta` grava a divergencia.
3. `mt_sync_delta` alimenta a view `vw_crm_drivabertos` que um workflow de
   alerta (ScheduleTrigger a cada 15 min) consulta.

```
esperado (before) - confirmado (after) / esperado > 5% = drift_flag
```

- Sem divergencia: `drift = 0`, health atualiza +1 sucesso.
- Com divergencia: grava delta e **nao marca o job como concluido** ate revisao.

### 5.1 Fluxo do Detector

```
Worker sync → mt_sync_log (done)
  → Code: comparar esperado vs confirmado
    → IF: |delta| > tolerancia
       ├── YES → INSERT mt_sync_delta → alerta (15 min)
       └── NO  → mt_crm_health atualiza health_score (+1 sucesso)
```

### 5.2 Alertas

- Workflow `[CC] CRM Drift Alert` (ScheduleTrigger 15 min): consulta
  `vw_crm_drift_abertos`. Se houver drift, notifica (email/WhatsApp/ Slack) com
  `object`, `client`, `esperado`, `confirmado` e `execution_url`.
- O alerta usa **grupo por objeto windows** para evitar ruido em picos esperados
  (ex: importacão programada que sempre gera diferenca conhecida).

## 6. Metricas de Exportacao

O padrao define estas metricas para o dashboard de observabilidade:

| Metrica | Consulta |
|---------|----------|
| Volume de syncs (24h) | `select count(*) from mt_sync_log where created_at > now() - interval '24 hours'` |
| Taxa de sucesso (24h) | sucesso / total por `object` |
| Divergencias abertas | `select * from vw_crm_drift_abertos` |
| Health baixo | `select * from vw_crm_health` |
| Latencia media | `avg(finished_at - created_at)` |

## 7. Envelope de Sync Padrao

Todo workflow de sync que produz registros envia para o padrao um envelope:

```json
{
  "syncId": "job-123",
  "object": "contact",
  "direction": "push",
  "client": "genics",
  "expected": 120,
  "synced": 118,
  "http_status": 200,
  "execution_url": "https://n8n...",
  "timestamp": "2026-08-05T10:30:00Z"
}
```

## 8. Anti-Patterns de Observabilidade

| Anti-pattern | Problema |
|--------------|----------|
| Sincronizacao sem log | Nao se sabe o que aconteceu |
| Log somente na falha | Nao se ve tendencia de saude |
| Payload inteiro no log | Sensivel/grande demais; usar hashes |
| Alerta por falha isolada (ruido) | Time ignora; agrupar por drift |
| Sem campo "esperado" | Nao da para medir divergencia |
| Tratar drift como erro normal | Melhor revisao que verificacao |
| Sem hash de resposta | Nao sabe se o CRM salvou igual |
| Confiar so no status HTTP | HTTP 200 nao significa dados corretos |