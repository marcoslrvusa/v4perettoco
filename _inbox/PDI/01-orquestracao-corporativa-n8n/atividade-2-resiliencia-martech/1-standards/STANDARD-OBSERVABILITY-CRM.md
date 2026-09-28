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

Implementação canônica do cálculo (Code node do Observabilidade):

```js
const EPSILON = 0.0001; // evita divisão por zero quando expected = 0

function computeDrift(expected, confirmed) {
  if (!Number.isFinite(expected) || expected <= 0) {
    return { drift_pct: 0, drift_flag: false, reason: 'sem_base_de_comparacao' };
  }
  const diff = Math.abs(expected - confirmed);
  const drift_pct = diff / Math.max(expected, EPSILON);
  return { drift_pct, drift_flag: drift_pct > 0.05, reason: null };
}

// Exemplo numérico: expected 1000, confirmed 860 → 140/1000 = 0,14 = 14%
```

Regra de negócio importante: `expected = 0` **não** é divergência, é ausência de
base. Tratar `0/0` como 100% de drift geraria alerta falso a cada criação de
entidade nova. O retorno explícito `sem_base_de_comparacao` deixa a decisão
auditável em vez de escondê-la em um `if`.

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

## 9. Semântica dos hashes

`payload_hash` e `response_hash` são SHA-256 truncado (32 hex) do conteúdo
canonizado, e não do JSON cru, porque a ordem das chaves varia entre versões da
API do CRM e produziria falso positivo:

```js
const crypto = require('crypto');

function canon(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(canon).join(',') + ']';
  return '{' + Object.keys(value).sort()
    .map((k) => JSON.stringify(k) + ':' + canon(value[k]))
    .join(',') + '}';
}

function payloadHash(value) {
  return crypto.createHash('sha256').update(canon(value)).digest('hex').slice(0, 32);
}
```

Nunca gravar o payload inteiro: o hash responde "mudou ou não mudou" com 32
caracteres, enquanto 10 MB de JSON em `mt_sync_log` transformaria a auditoria no
próprio gargalo que o padrão quer evitar. Quando a investigação exige o corpo, o
envelope opcional `payload` (já previsto no formato padrão) é armazenado separado
e com retenção curta.

## 10. Telemetria e Alerta

| Métrica | Fonte | Cardinalidade | Alerta |
|---------|-------|---------------|--------|
| `sync_total` por objeto | `mt_sync_log` | objeto + direção | queda de 50% em 24 h (meta) |
| `sync_error_rate` | view de resumo | objeto | > 10% por 15 min |
| `drift_abertos` | `vw_mt_drift_abertos` | cliente | qualquer linha com mais de 4 h |
| `health_score` mínimo | `vw_mt_crm_health` | empresa + objeto | abaixo de `min_health` (0,90) |
| Latência sync (`finished_at - created_at`) | `mt_sync_log` | global | p95 acima do orçamento da fila |

Alerta por agrupamento, nunca por evento: uma importação de 10 mil registros com
20 falhas isoladas vira **um** aviso agregado, não 20. O agrupamento é por
`object + client + janela de 15 min`, que é a granularidade em que o time consegue
decidir uma ação.

## 11. Plano de Teste e Critérios de Aceite

| Caso | Passo | Esperado | Critério de falha |
|------|-------|----------|-------------------|
| Sync limpo | Enviar envelope `expected=120, synced=120` | `drift = 0`, health +1 | Linha em `mt_sync_delta` |
| Drift dentro do limiar | `expected=120, synced=118` (1,7%) | Sem delta, health +1 | Alerta emitido |
| Drift fora do limiar | `expected=1000, synced=860` (14%) | Delta aberto e job não concluído | Job marcado `done` |
| Base nula | `expected=0` | `sem_base_de_comparacao` | Alerta de 100% de drift |
| Falha do CRM | HTTP 500 na chamada | `status=error` com `error_class` | Linha ausente em `mt_sync_log` |
| Resposta idêntica | Mesmo corpo em duas chamadas | Mesmo `response_hash` | Hashs diferentes |
| Resposta diferente | Corpo alterado pelo CRM | `response_hash` diferente | Hashs idênticos |
| Ausência de trilha | Sync sem chamar o Observabilidade | Falha de validação do retrofit | Registro ausente silenciosamente |

Critério de aceite global: os oito casos passam e o alerta de drift chega ao time
em menos de 15 min (meta) após a abertura do `mt_sync_delta`.

## 12. Checklist de Adesão

- [ ] Todo workflow de CRM envia o envelope ao final, inclusive em erro.
- [ ] `expected` é preenchido obrigatoriamente no `push`.
- [ ] Hash calculado sobre conteúdo canonizado, não sobre JSON cru.
- [ ] Nenhum payload completo gravado em `mt_sync_log`.
- [ ] `error_class` segue o mapeamento do Padrão Universal de Erros (atividade 1).
- [ ] Tolerância de drift configurada em um único lugar (5%).
- [ ] Job com drift acima do limiar não é concluído automaticamente.
- [ ] Alerta agrupado por `object + client + janela`.
- [ ] `execution_url` presente em todo registro para investigação.
- [ ] Health calculado por `object + direction`, não agregado global.
- [ ] Retenção do `mt_sync_log` definida (a tabela cresce a cada sync).
- [ ] Consultas de dashboard batem com os nomes reais das views.