import { workflow, node } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Agent Orchestra - Webhook Receiver
// Nodes   : 3  |  Connections: 2
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// WebhookReceiver     webhook
// ValidatePayload     code
// EnqueueDemand       code
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// WebhookReceiver
//   → ValidatePayload
//     → EnqueueDemand
// </workflow-map>

@workflow({
    id: 'agent_orchestra_webhook_001',
    name: 'Agent Orchestra - Webhook Receiver',
    active: true,
    isArchived: false,
    settings: { executionOrder: 'v1' },
    tags: ['agent-orchestra', 'webhook'],
})
export class AgentOrchestraWebhook {
    @node({
        id: 'aow_webhook',
        name: 'Webhook Receiver',
        type: 'n8n-nodes-base.webhook',
        version: 1,
        position: [250, 300],
    })
    WebhookReceiver = {
        httpMethod: 'POST',
        path: 'agent-orchestra/enqueue',
        options: {},
        responseMode: 'onReceived',
        responseData: 'allEntries',
    };

    @node({
        id: 'aow_validate',
        name: 'Validate Payload',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [450, 300],
    })
    ValidatePayload = {
        jsCode:
`const payload = $input.first().json;

const validFunctions = ['aquisicao','conteudo','saude_cliente','receita','lancamento','operacao','lideranca','copy'];
const validUrgency = ['baixa','normal','alta','critica'];
const validTypes = ['flag','scheduled','manual','webhook'];

if (!payload.function || !validFunctions.includes(payload.function)) {
  throw new Error('function inválida. Use: ' + validFunctions.join(', '));
}

if (payload.urgency && !validUrgency.includes(payload.urgency)) {
  throw new Error('urgency inválida. Use: ' + validUrgency.join(', '));
}

if (!payload.demand_type || !validTypes.includes(payload.demand_type)) {
  payload.demand_type = 'webhook';
}

return {
  demand_type: payload.demand_type,
  source: payload.source || 'webhook',
  function: payload.function,
  urgency: payload.urgency || 'normal',
  scope: payload.scope || 'single',
  priority: payload.priority || 50,
  briefing: payload.briefing || {},
};`,
    };

    @node({
        id: 'aow_enqueue',
        name: 'Enqueue in Supabase',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [650, 300],
    })
    EnqueueDemand = {
        jsCode:
`const https = require('https');
const url = process.env.SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_KEY;
const data = $input.first().json;

function supabasePost(path, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(path, url);
    const payload = JSON.stringify(body);
    const opt = {
      hostname: u.hostname,
      path: u.pathname + u.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        apikey: key,
        Authorization: 'Bearer ' + key,
        Prefer: 'return=representation',
      },
    };
    const req = https.request(opt, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve(JSON.parse(d)); }
        catch { reject(new Error('Falha ao parsear: ' + d)); }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

const result = await supabasePost('/rest/v1/agent_queue', {
  demand_type: data.demand_type,
  source: data.source,
  function: data.function,
  urgency: data.urgency,
  scope: data.scope,
  priority: data.priority,
  briefing: JSON.stringify(data.briefing),
  status: 'pending',
});

return {
  success: true,
  queue_id: Array.isArray(result) ? result[0]?.id : result?.id,
  demand: data,
};`,
    };
}
