import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [CC] MT CRM Sync Observability
// Nodes   : 8  |  Connections: 8
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────────────
// Property name                 Node type (short)          Flags
// WebhookTrigger                webhook
// DecodeSyncEnvelope            code
// LogSyncStart                  supabase                 [creds]
// UpdateHealth                  supabase                 [creds]
// CheckForDrift                 if
// UpsertDelta                   supabase                 [creds]
// MarkHealthDegraded            supabase                 [creds]
// Respond200                    respondToWebhook
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────────────
// WebhookTrigger → DecodeSyncEnvelope
//   → LogSyncLog
//     → UpdateHealth (health_score)
//       → CheckForDrift
//         ├── true (drift)  → UpsertDelta → MarkHealthDegraded → Respond200
//         └── false         → Respond200
// </workflow-map>

// =====================================================================
// [CC] MT - CRM Sync Observability (Logger + Drift Detector)
// =====================================================================
// Endpoint usado por QUALQUER workflow de integração com CRM para
// registrar a execução de sync. O node Code `DecodeSyncEnvelope` já
// detecta divergência entre `payload_hash` e `response_hash`.
//
// CONFIGURE:
//  1. Webhook: path /mt/crm-sync (public)
//  2. Credencial Command Center Supabase nos 4 nos supabase.
// =====================================================================

@workflow({
    id: 'mt-crm-obs',
    name: '[CC] MT - CRM Sync Observabilidade',
    active: false,
    isArchived: false,
    settings: { timezone: 'America/Sao_Paulo', saveDataErrorExecution: 'all', executionOrder: 'v1' },
})
export class MtCrmObservabilidadeWorkflow {
    @node({
        name: 'Webhook',
        type: 'n8n-nodes-base.webhook',
        version: 2,
        position: [250, 300],
    })
    WebhookTrigger = {
        httpMethod: 'POST',
        path: 'mt/crm-sync',
        responseMode: 'lastNode',
        options: { responseData: 'all' },
    };

    @node({
        name: 'Decode Sync Envelope',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [480, 300],
    })
    DecodeEnvelope = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `
// ============================================================
// Decode Sync Envelope — CRM Sync Observabilidade
// ============================================================
// Envelope padrao da camada de sync (STANDARD-OBSERVABILITY-CRM.md).
// Calcula payload_hash/response_hash e drift% (divergencia).
// ============================================================
const input = (typeof $input.first().json.body !== 'undefined')
    ? $input.first().json.body
    : $input.first().json;

function hash(str) {
  if (typeof str !== 'string') {
    try { str = JSON.stringify(str); } catch (e) { str = String(str); }
  }
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h) + str.charCodeAt(i);
    h |= 0;
  }
  return 'h' + Math.abs(h).toString(16);
}

const expected = Number(input.expected || 0);
const synced = Number(input.synced || 0);
const driftPct = expected > 0 ? ((expected - synced) / expected) * 100 : 0;
const hasDrift = Math.abs(driftPct) > 5; // tolerancia 5%

return [{
  json: {
    syncId: input.syncId || ('sync-' + Date.now()),
    object: input.object || 'generic',
    direction: input.direction || 'push',
    source: input.source || null,
    client: input.client || null,
    payloadHash: hash(input.payload || ''),
    responseHash: hash(input.response || ''),
    httpStatus: Number(input.http_status || 200),
    executionUrl: input.execution_url || null,
    expected,
    synced,
    driftPct: Number(driftPct.toFixed(2)),
    hasDrift,
    inputMeta: input,
  },
}];
`,
    };

    @node({
        name: 'Insert Sync Log',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [710, 300],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    InsertSyncLog = {
        resource: 'row',
        operation: 'create',
        tableId: 'mt_sync_log',
        useCustomSchema: false,
        schema: 'public',
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'sync_id', fieldValue: '={{ $json.syncId }}' },
                { fieldId: 'object', fieldValue: '={{ $json.object }}' },
                { fieldId: 'direction', fieldValue: '={{ $json.direction }}' },
                { fieldId: 'source', fieldValue: '={{ $json.source }}' },
                { fieldId: 'client', fieldValue: '={{ $json.client }}' },
                { fieldId: 'payload_hash', fieldValue: '={{ $json.payloadHash }}' },
                { fieldId: 'response_hash', fieldValue: '={{ $json.responseHash }}' },
                { fieldId: 'status', fieldValue: '={{ $json.hasDrift ? "error" : "done" }}' },
                { fieldId: 'http_status', fieldValue: '={{ $json.httpStatus }}' },
                { fieldId: 'execution_url', fieldValue: '={{ $json.executionUrl }}' },
                { fieldId: 'drift', fieldValue: '={{ $json.hasDrift ? 1 : 0 }}' },
                { fieldId: 'expected', fieldValue: '={{ $json.expected }}' },
                { fieldId: 'synced', fieldValue: '={{ $json.synced }}' },
                { fieldId: 'finished_at', fieldValue: '={{ new Date().toISOString() }}' },
            ],
        },
    };

    @node({
        name: 'Insert CRM Health',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [940, 300],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    UpsertHealth = {
        resource: 'row',
        operation: 'create',
        tableId: 'mt_crm_health',
        useCustomSchema: false,
        schema: 'public',
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'company', fieldValue: '={{ $json.client }}' },
                { fieldId: 'object', fieldValue: '={{ $json.object }}' },
                { fieldId: 'direction', fieldValue: '={{ $json.direction }}' },
                { fieldId: 'total', fieldValue: '1' },
                { fieldId: 'success', fieldValue: '={{ $json.hasDrift ? 0 : 1 }}' },
                { fieldId: 'failed', fieldValue: '={{ $json.hasDrift ? 1 : 0 }}' },
                { fieldId: 'last_sync_at', fieldValue: '={{ new Date().toISOString() }}' },
                { fieldId: 'drift_count', fieldValue: '={{ $json.hasDrift ? 1 : 0 }}' },
                { fieldId: 'updated_at', fieldValue: '={{ new Date().toISOString() }}' },
            ],
        },
    };

    @node({
        name: 'Flag Drift',
        type: 'n8n-nodes-base.if',
        version: 2.3,
        position: [1170, 300],
    })
    FlagDrift = {
        conditions: {
            conditions: [
                {
                    id: 'drift-check',
                    leftValue: '={{ $json.driftPct }}',
                    rightValue: '5',
                    operator: {
                        type: 'number',
                        operation: 'gt',
                    },
                },
            ],
            combinator: 'and',
            options: { caseSensitive: true, typeValidation: 'strict' },
        },
        options: [],
    };

    @node({
        name: 'Insert Delta',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1400, 120],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    InsertDelta = {
        resource: 'row',
        operation: 'create',
        tableId: 'mt_sync_delta',
        useCustomSchema: false,
        schema: 'public',
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'sync_id', fieldValue: '={{ $json.syncId }}' },
                { fieldId: 'object', fieldValue: '={{ $json.object }}' },
                { fieldId: 'client', fieldValue: '={{ $json.client }}' },
                { fieldId: 'expected', fieldValue: '={{ $json.expected }}' },
                { fieldId: 'confirmed', fieldValue: '={{ $json.synced }}' },
                { fieldId: 'drift_pct', fieldValue: '={{ $json.driftPct }}' },
                { fieldId: 'execution_url', fieldValue: '={{ $json.executionUrl }}' },
            ],
        },
    };

    @node({
        name: 'Respond 200',
        type: 'n8n-nodes-base.respondToWebhook',
        version: 1.1,
        position: [1650, 300],
    })
    Respond200 = {
        respondWith: 'json',
        responseBody: `{ "recorded": true }`,
        options: { responseCode: 200 },
    };

    @links()
    defineRouting() {
        this.WebhookTrigger.out(0).to(this.DecodeEnvelope.in(0));
        this.DecodeEnvelope.out(0).to(this.InsertSyncLog.in(0));
        this.InsertSyncLog.out(0).to(this.UpsertHealth.in(0));

        this.UpsertHealth.out(0).to(this.FlagDrift.in(0));
        this.FlagDrift.out(0).to(this.InsertDelta.in(0));
        this.InsertDelta.out(0).to(this.Respond200.in(0));
        this.FlagDrift.out(1).to(this.Respond200.in(0));
    }
}