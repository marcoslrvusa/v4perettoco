import { workflow, node } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Agent Orchestra - Queue Processor
// Nodes   : 5  |  Connections: 5
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// ManualTrigger       manualTrigger
// DequeueItem         executeCommand
// CheckResult         code
// HandleSuccess       code
// HandleFailure       code
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// ManualTrigger
//   → DequeueItem
//     → CheckResult
//       → HandleSuccess
//       → HandleFailure
// </workflow-map>

@workflow({
    id: 'agent_orchestra_processor_001',
    name: 'Agent Orchestra - Queue Processor',
    active: true,
    isArchived: false,
    settings: { executionOrder: 'v1' },
    tags: ['agent-orchestra', 'processor'],
})
export class AgentOrchestraProcessor {
    @node({
        id: 'aop_trigger',
        name: 'Manual Trigger',
        type: 'n8n-nodes-base.manualTrigger',
        version: 1,
        position: [250, 300],
    })
    ManualTrigger = {};

    @node({
        id: 'aop_dequeue',
        name: 'Dequeue & Classify',
        type: 'n8n-nodes-base.executeCommand',
        version: 1,
        position: [450, 300],
    })
    DequeueItem = {
        command: 'python3',
        parameters: '/workspace/agent-orchestrator.py process',
    };

    @node({
        id: 'aop_check',
        name: 'Check Result',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [650, 300],
    })
    CheckResult = {
        jsCode:
`const output = $input.first().json;
const stdout = (output.stdout || '').toString();
const stderr = (output.stderr || '').toString();

const hasError = stderr.includes('ERRO') || stderr.includes('Traceback') || stdout.includes('Nenhum item');
const mode = stdout.includes('AUTONOMO') ? 'autonomo'
  : stdout.includes('SEMI') ? 'semi'
  : stdout.includes('MANUAL') ? 'manual'
  : 'unknown';

return {
  raw_stdout: stdout,
  raw_stderr: stderr,
  has_error: hasError,
  mode: mode,
  requires_review: mode === 'semi' || mode === 'manual' || mode === 'unknown',
};`,
    };

    @node({
        id: 'aop_success',
        name: 'Handle Success',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [850, 200],
    })
    HandleSuccess = {
        jsCode:
`const result = $input.first().json;
return {
  status: 'processed',
  mode: result.mode,
  message: result.mode === 'autonomo'
    ? 'Demanda processada automaticamente'
    : 'Brief gerado. Aguardando revisão.',
  timestamp: new Date().toISOString(),
};`,
    };

    @node({
        id: 'aop_failure',
        name: 'Handle Failure',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [850, 400],
    })
    HandleFailure = {
        jsCode:
`const result = $input.first().json;
const https = require('https');
const url = process.env.SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_KEY;

// Notify on failure — log to agent_queue_log
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
        Prefer: 'return=minimal',
      },
    };
    const req = https.request(opt, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

try {
  await supabasePost('/rest/v1/agent_queue_log', {
    queue_id: 'unknown',
    event: 'processor_failure',
    detail: JSON.stringify({ error: result.raw_stderr, stdout: result.raw_stdout }),
  });
} catch (e) {
  // silent
}

return {
  status: 'failed',
  error: result.raw_stderr || 'Erro desconhecido no processamento',
  timestamp: new Date().toISOString(),
};`,
    };
}
