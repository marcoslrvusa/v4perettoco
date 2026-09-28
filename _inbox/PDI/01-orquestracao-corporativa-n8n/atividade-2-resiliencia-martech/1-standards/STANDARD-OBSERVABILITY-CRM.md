# Padrão de Observabilidade de Sincronização com CRM: n8n Enterprise V4

> **Versão:** 1.0 | **Status:** Pronto para homologação | **Última revisão:** 2026-08-05

## 1. Problema

Integrações com CRMs terceiros (Kommo, HubSpot, RD Station, Pipedrive) acontecem em
workflows que sincronizam contatos, pedidos, conversas e propriedades. Quando o CRM
recusa payload, muda schema, aplica rate limit ou cai, o workflow falha: mas a
falha **só chega ao time quando o cliente reclama**. Não existe trilha do que foi
sincronizado, quando, com qual payload e que erro retornou.

## 2. Solução: Sincronização Auditada + Detector de Divergência

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
saído**. Divergências viram um registro em `mt_sync_delta` (não um erro que se
perde), e um workflow de alerta decide se a divergência já impacta o cliente.

## 3. Tabela de Trilha (mt_sync_log)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | PK |
| `sync_id` | TEXT | Correlation id do job |
| `object` | TEXT | `contact`, `order`, `conversation`, `product` |
| `direction` | TEXT | `push` (n8n → CRM), `pull` (CRM → n8n) |
| `source` | TEXT | Integração (Kommo API, HubSpot, etc) |
| `client` | TEXT | Cliente afetado |
| `payload_hash` | TEXT | Hash do payload enviado (consistência) |
| `response_hash` | TEXT | Hash do que foi retornado pelo CRM |
| `status` | TEXT | `in_progress` \| `done` \| `error` |
| `http_status` | INT | Resposta HTTP do CRM |
| `error_class` | TEXT | Classe mapeada para o padrão de erros |
| `error_message` | TEXT | Mensagem resumida |
| `attempts` | INT | Tentativas |
| `execution_url` | TEXT | Link da execução no n8n |
| `drift` | INT | Divergências percebidas pelo detector |
| `created_at`, `finished_at` | TIMESTAMPTZ | Timeline |

## 4. Health por Entidade (mt_crm_health)

A cada sync concluído, o handler atualiza um agregado por `object + direction`:

```
company, object, direction, total, success, failed,
error_class_count (JSONB), last_sync_at, drift_count,
min_health, updated_at
```

- `health_score = success / total` na janela (default 1h, computado na view).
- A view `vw_crm_health` devolve todos os healths abaixo do `min_health` config.

## 5. Detector de Divergência: "antes de afetar o cliente"

1. O workflow que faz o sync grava o **esperado**: quantos registros deveriam
   existir (ex: `total = 1200` após a importação).
2. Depois do sync, o CRM confirma o contador real; se a diferença > tolerância,
   um registro `mt_sync_delta` grava a divergência.
3. `mt_sync_delta` alimenta a view `vw_crm_drivabertos` que um workflow de
   alerta (ScheduleTrigger a cada 15 min) consulta.

```
esperado (before) - confirmado (after) / esperado > 5% = drift_flag
```

- Sem divergência: `drift = 0`, health atualiza +1 sucesso.
- Com divergência: grava delta e **não marca o job como concluído** até revisão.

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
- O alerta usa **grupo por objeto windows** para evitar ruído em picos esperados
  (ex: importação programada que sempre gera diferença conhecida).

## 6. Métricas de Exportação

O padrão define estas métricas para o dashboard de observabilidade:

| Métrica | Consulta |
|---------|----------|
| Volume de syncs (24h) | `select count(*) from mt_sync_log where created_at > now() - interval '24 hours'` |
| Taxa de sucesso (24h) | sucesso / total por `object` |
| Divergências abertas | `select * from vw_crm_drift_abertos` |
| Health baixo | `select * from vw_crm_health` |
| Latência média | `avg(finished_at - created_at)` |

## 7. Envelope de Sync Padrão

Todo workflow de sync que produz registros envia para o padrão um envelope:

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
| Sincronização sem log | Não se sabe o que aconteceu |
| Log somente na falha | Não se vê tendência de saúde |
| Payload inteiro no log | Sensível/grande demais; usar hashes |
| Alerta por falha isolada (ruído) | Time ignora; agrupar por drift |
| Sem campo "esperado" | Não da para medir divergência |
| Tratar drift como erro normal | Melhor revisão que verificação |
| Sem hash de resposta | Não sabe se o CRM salvou igual |
| Confiar só no status HTTP | HTTP 200 não significa dados corretos |