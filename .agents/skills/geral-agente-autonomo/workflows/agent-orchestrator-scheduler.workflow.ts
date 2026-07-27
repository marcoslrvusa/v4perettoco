import { workflow, node } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Agent Orchestra - Scheduler
// Nodes   : 4  |  Connections: 3
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// ScheduleTrigger     scheduleTrigger
// CheckQueue          code
// DequeueProcess      executeCommand
// NotifyEmpty         noOp
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// ScheduleTrigger
//    → CheckQueue (code)
//      → DequeueProcess (executeCommand) [se houver pendentes]
//      → NotifyEmpty (noOp) [se fila vazia]
// </workflow-map>

@workflow({
    id: 'agent_orchestra_scheduler_001',
    name: 'Agent Orchestra - Scheduler',
    active: true,
    isArchived: false,
    settings: { executionOrder: 'v1' },
    tags: ['agent-orchestra', 'scheduler'],
})
export class AgentOrchestraScheduler {
    @node({
        id: 'aos_trigger',
        name: 'Schedule Trigger',
        type: 'n8n-nodes-base.scheduleTrigger',
        version: 1.3,
        position: [250, 300],
    })
    ScheduleTrigger = {
        rule: {
            interval: [
                {
                    field: 'minutes',
                    minutesInterval: 15,
                },
            ],
        },
    };

    @node({
        id: 'aos_check',
        name: 'Check Queue',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [450, 300],
    })
    CheckQueue = {
        jsCode:
`const https = require('https');
const url = process.env.SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_KEY;

if (!url || !key) {
  throw new Error('SUPABASE_URL e SUPABASE_SERVICE_KEY são obrigatórios');
}

function supabaseGet(path) {
  return new Promise((resolve, reject) => {
    const u = new URL(path, url);
    const opt = {
      hostname: u.hostname,
      path: u.pathname + u.search,
      method: 'GET',
      headers: {
        apikey: key,
        Authorization: 'Bearer ' + key,
      },
    };
    const req = https.request(opt, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { reject(new Error('Falha ao parsear resposta: ' + data)); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

const pending = await supabaseGet('/rest/v1/agent_queue?status=eq.pending&order=priority.desc,created_at.asc&limit=5');
return pending.length > 0 ? pending : [{ empty: true, message: 'Fila vazia' }];`,
    };

    @node({
        id: 'aos_dequeue',
        name: 'Dequeue & Process',
        type: 'n8n-nodes-base.executeCommand',
        version: 1,
        position: [650, 300],
    })
    DequeueProcess = {
        command: 'python3',
        parameters: `/workspace/agent-orchestrator.py process`,
    };

    @node({
        id: 'aos_noop',
        name: 'Queue Empty',
        type: 'n8n-nodes-base.noOp',
        version: 1,
        position: [650, 500],
    })
    NotifyEmpty = {};
}
