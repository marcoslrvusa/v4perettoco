import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [CC] MT Queue Gateway
// Nodes   : 5  |  Connections: 4
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────────────
// Property name           Node type (short)         Flags
// Webhook                 webhook
// EnqueueJob              code
// DedupeCheck             if
// InsertJob               supabase                  [creds]
// Respond                  respondToWebhook
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────────────
// Webhook → EnqueueJob → DedupeCheck
//   ├── true (novo)  → InsertJob → Respond (202 with jobId)
//   └── false (dup)  → Respond  (200 with existing jobId)
// </workflow-map>

// =====================================================================
// [CC] MT Queue Gateway
// =====================================================================
// Proposito: Enfileira requisicoes MarTech como jobs assincronos.
//            NUNCA processa payload no webhook — grava na fila e responde
//            ACK imediato para absorver picos sem travar a instancia.
//
// CONFIGURE: Webhook path por fila (ex: /mt/crm-sync) e rotas de destino
//            (poller worker a cada 15s).
// =====================================================================

@workflow({
  name: '[CC] MT Queue Gateway',
  active: false,
  settings: {
    executionOrder: 'v1',
    errorWorkflow: '',
    timezone: 'America/Sao_Paulo',
    saveDataErrorExecution: 'all',
    saveDataSuccessExecution: 'all',
  },
})
export class MtQueueGatewayWorkflow {
  @node({
    name: 'Webhook',
    type: 'n8n-nodes-base.webhook',
    version: 2,
    position: [0, 400],
    webhookId: 'mt-gateway',
  })
  Webhook = {
    httpMethod: 'POST',
    path: 'mt/gateway',
    responseMode: 'responseNode',
    options: {
      ignoreNoWebhookMatch: false,
    },
  };

  @node({
    name: 'Serialize Job',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [220, 400],
  })
  SerializeJob = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
// =====================================================================
// Serialize Job — MT Queue Gateway
// =====================================================================
// Converte a request em um job da fila mt_jobs.
// Job leve: payload com referencias; dados pesados via mt_job_progress
// ou mount storage.
// =====================================================================

const body = $input.first().json.body || $input.first().json;

const queue = body.queue || 'default';
const rawKey = body.jobKey || [
  queue,
  (body.object || 'unknown'),
  (body.id || new Date().toISOString()),
].join(':');

// Job key estavel (idempotencia): hash simples do rawKey
const jobKey = (() => {
  let h = 0;
  for (let i = 0; i < rawKey.length; i++) {
    h = ((h << 5) - h) + rawKey.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h).toString(36) + '-' + rawKey.slice(0, 60);
})();

return [{
  json: {
    queue,
    jobKey,
    priority: typeof body.priority === 'number' ? body.priority : 0,
    payload: {
      client: body.client || null,
      object: body.object || 'generic',
      integration: body.integration || null,
      ref: body.ref || null,
      meta: body.meta || null,
    },
    requestedAt: new Date().toISOString(),
    _raw: body,
  },
}];
`,
  };

  @node({
    name: 'Check Duplicate',
    type: 'n8n-nodes-base.supabase',
    version: 1,
    position: [440, 400],
    credentials: {
      supabaseApi: {
        id: 'nRJEEi2QwVVKIAHY',
        name: 'Command Center Supabase',
      },
    },
  })
  CheckDuplicate = {
    resource: 'row',
    operation: 'getAll',
    tableId: 'mt_jobs',
    returnAll: true,
    filterType: 'manual',
    matchType: 'allFilters',
    filters: {
      conditions: [
        {
          keyName: 'job_key',
          condition: 'eq',
          keyValue: '={{ $json.jobKey }}',
        },
      ],
    },
  };

  @node({
    name: 'Has Duplicate?',
    type: 'n8n-nodes-base.if',
    version: 2.3,
    position: [660, 400],
  })
  HasDuplicate = {
    conditions: {
      conditions: [
        {
          id: 'dup-check',
          leftValue: '={{ $json.length }}',
          rightValue: '0',
          operator: {
            type: 'number',
            operation: 'gt',
          },
        },
      ],
      combinator: 'and',
      options: {
        caseSensitive: true,
        typeValidation: 'strict',
      },
    },
    options: [],
  };

  @node({
    name: 'Insert Job',
    type: 'n8n-nodes-base.supabase',
    version: 1,
    position: [700, 220],
    credentials: {
      supabaseApi: {
        id: 'nRJEEi2QwVVKIAHY',
        name: 'Command Center Supabase',
      },
    },
  })
  InsertJob = {
    resource: 'row',
    operation: 'create',
    tableId: 'mt_jobs',
    useCustomSchema: false,
    schema: 'public',
    dataToSend: 'defineBelow',
    fieldsUi: {
      fieldValues: [
        { fieldId: 'job_key', fieldValue: '={{ $json.jobKey }}' },
        { fieldId: 'queue', fieldValue: '={{ $json.queue }}' },
        { fieldId: 'status', fieldValue: 'queued' },
        { fieldId: 'priority', fieldValue: '={{ $json.priority }}' },
        { fieldId: 'payload', fieldValue: '={{ JSON.stringify($json.payload) }}' },
        { fieldId: 'retry_at', fieldValue: '={{ new Date().toISOString() }}' },
      ],
    },
  };

  @node({
    name: 'Respond 202',
    type: 'n8n-nodes-base.respondToWebhook',
    version: 1.1,
    position: [920, 220],
  })
  Respond202 = {
    respondWith: 'json',
    responseBody: `={{
      JSON.stringify({
        accepted: true,
        status: 'queued',
        jobKey: $json.jobKey
      })
    }}`,
    options: {
      responseCode: 202,
    },
  };

  // path elimination (duplicate) — respond 200 with existing
  @node({
    name: 'Respond Duplicate',
    type: 'n8n-nodes-base.respondToWebhook',
    version: 1.1,
    position: [700, 580],
  })
  RespondDuplicate = {
    respondWith: 'json',
    responseBody: `={{
      JSON.stringify({
        accepted: false,
        status: 'duplicate',
        jobKey: $json.jobKey
      })
    }}`,
    options: {
      responseCode: 200,
    },
  };

  @links()
  defineRouting() {
    this.Webhook.out(0).to(this.SerializeJob.in(0));
    this.SerializeJob.out(0).to(this.CheckDuplicate.in(0));
    this.CheckDuplicate.out(0).to(this.HasDuplicate.in(0));

    this.HasDuplicate.out(0).to(this.InsertJob.in(0));
    this.InsertJob.out(0).to(this.Respond202.in(0));

    this.HasDuplicate.out(1).to(this.RespondDuplicate.in(0));
  }
}