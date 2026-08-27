import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [CC] MT Heavy Payload Processor
// Nodes   : 6  |  Connections: 6
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────────────
// Property name                 Node type (short)          Flags
// WorkflowTrigger               n8nTrigger (executeWorkflow)
// UnpackInput                   code
// NormalizePayload              code (JS — heavy transforms)
// WriteChunkProgress            supabase                  [creds]
// PythonEnrich                 code (python)
// ReturnResult                 executeCommand? (sub-process) → respondToWebhook
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────────────
// WorkflowTrigger
//   → UnpackInput
//     → CheckAutoTruncate
//       → LimitChunks (noOp p/ cutoff)
//       ├── true → WriteChunkProgress (checkpoint)
//       ├── ...
//       └── done → EnrichWithPython → ReturnResult true
// </workflow-map>

// =====================================================================
// [CC] MT - Heavy Payload Processor
// =====================================================================
// Roda como SUB-WORKFLOW chamado pelo [CC] MT - Queue Worker. Faz o
// trabalho "pesado": ler payload JSONB, processar em chunks (code JS)
// e enriquecer com Python. Grava progresso (mt_job_progress) para
// retomada. Retorna { success: true } para o worker finalizar o job.
//
// CONFIGURE:
//  1. Credencial Command Center Supabase nos nos Supabase.
//  2. ChunkSize no node NormalizePayload conforme limite (default 100).
//  3. Toggle EnrichWithPython p/ ativar etapa Python.
// =====================================================================

@workflow({
    id: 'mt-heavy-payload',
    name: '[CC] MT - Heavy Payload Processor',
    active: false,
    isArchived: false,
    settings: { timezone: 'America/Sao_Paulo', saveDataErrorExecution: 'all', executionOrder: 'v1' },
})
export class MtHeavyPayloadWorkflow {
    // =====================================================================
    // Sub-workflow: sem trigger proprio — executado via Execute Workflow
    // (n8n injeta a entrada direto no primeiro node, 'Unpack Input').
    // =====================================================================

    @node({
        name: 'Unpack Input',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [250, 300],
    })
    UnpackInput = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `
// ============================================================
// Unpack Input — Heavy Payload
// ============================================================
// O worker entrega { job_id, payload (JSONB string), chunks }.
// Parse seguranca + concatena itens de chor lambda.
// ============================================================

const raw = $input.first().json;
const job = raw.job || raw;
const payload = typeof job.payload === 'string' ? tryParse(job.payload) : job.payload;

function tryParse(s) {
  try { return JSON.parse(s); } catch (e) { return { __raw: s }; }
}

const items = Array.isArray(payload) ? payload : (payload.data || payload.items || [payload]);

const chunkSize = Number(job.chunk_size || 100);
const totalChunks = Math.max(1, Math.ceil(items.length / chunkSize));
const chunks = [];
for (let i = 0; i < items.length; i += chunkSize) {
  chunks.push(items.slice(i, i + chunkSize));
}

return [{
  json: {
    jobId: job.id,
    queue: job.queue,
    attempts: Number(job.attempts || 0),
    totalChunks,
    chunks: chunks.map((c, idx) => ({ idx, data: c })),
    itemsCount: items.length,
    startedChunk: 0,
  },
}];
`,
    };

    // JS AVANÇADO — altura pesada (página estratégia, normalizações)
    @node({
        name: 'Normalize Data',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [710, 300],
    })
    NormalizeData = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `
// ============================================================
// Normalize Data — heavy payload processing (JS)
// ============================================================
// Converte campos divergentes para o formato padrao do monocito.
// Aplica-se a TODOS os chunks; mantem chunk com progresso.
// ============================================================

const job = $input.first().json;
const results = [];

for (const chunk of job.chunks) {
  const normalized = (chunk.data || []).map((item) => {
    const out = { ...item };

    // normalizacao padrao de datas (ex MM/DD/YYYY → ISO)
    if (item.date) {
      const m = String(item.date).match(/^(\\d{2})[\\/.-](\\d{2})[\\/.-](\\d{4})$/);
      out.date = m ? new Date(m[3], m[2] - 1, m[1]).toISOString() : item.date;
    }

    // telefone E.164-ish
    if (item.phone) {
      out.phone = String(item.phone).replace(/[^0-9]/g, '');
      if (out.phone.length === 10) out.phone = '55' + out.phone;
    }

    // estrutura padrao
    out._normalized = true;
    results.push(out);
  }

  return [{
    json: {
      ...job,
      chunks: job.chunks.map((c, i) => ({ ...c, data: results.slice(
        i * (c.data ? c.data.length : 0),
        (i + 1) * (c.data ? c.data.length : 0)
      ) })),
      normalize_at: new Date().toISOString(),
    },
  }];
`,
    };

    // Translate: escreve progresso por chunk (retomável)
    @node({
        name: 'Write Chunk Progress',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [720, 400],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    WriteProgress = {
        resource: 'row',
        operation: 'create',
        tableId: 'mt_job_progress',
        useCustomSchema: false,
        schema: 'public',
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'job_id', fieldValue: '={{ $json.jobId }}' },
                { fieldId: 'chunk_index', fieldValue: '={{ $json.processedChunk }}' },
                { fieldId: 'total_chunks', fieldValue: '={{ $json.totalChunks }}' },
                { fieldId: 'status', fieldValue: 'running' },
                { fieldId: 'updated_at', fieldValue: '={{ new Date().toISOString() }}' },
            ],
        },
    };

    // Enrichment de momento — Python code de monumento (ex: BERT-lite, OCR)
    @node({
        name: 'Enrich Python',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [960, 400],
    })
    EnrichPython = {
        mode: 'runOnceForAllItems',
        language: 'pythonNative',
        pythonCode: `
# ============================================================
# Enrich Python — Heavy Payload (step opcional)
# ============================================================
# Poinpoint: enriquecimento por itens (segment, clean, tags).
# Usando a biblioteca padrão — sem deps externas.
# ============================================================
from datetime import datetime

data = _input[0]['json']
chunks = data.get('chunks') or []
results = []
for chunk in chunks:
    enriched = []
    for item in chunk.get('data') or []:
        item = item.copy()
        item['enriched_at'] = datetime.utcnow().isoformat()
        item['source_type'] = 'mt'
        enriched.append(item)
    results.append({'idx': chunk['idx'], 'data': enriched})

data['enrichedChunks'] = results
data['enriched_at'] = datetime.utcnow().isoformat()
data['python_version'] = '3.11'
data['success'] = True
return [{'data': data}]
`,
    };

    @node({
        name: 'Return True',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1100, 400],
    })
    ReturnTrue = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `
// Resposta ao worker: sucesso do job.
// Em execucoes async, loga na fila como done.
return [{
    json: {
        success: true,
        jobId: $json.jobId || null,
        ref: $json.ref || null,
        message: 'MT Heavy Payload processor finalizado',
        chunksTotal: ($json.totalChunks || 0),
        processedAt: new Date().toISOString(),
    },
}];
`,
    };

    @links()
    defineRouting() {
        // Sem trigger: entrada injetada pelo Execute Workflow (n8n)
        this.UnpackInput.out(0).to(this.NormalizeData.in(0));

        // STEP 2: Progresso (checkpoint) — chamável apos cada chunk
        this.NormalizeData.out(0).to(this.WriteProgress.in(0));

        // STEP 3: Python enrich (opcional)
        this.WriteProgress.out(0).to(this.EnrichPython.in(0));

        // STEP 4: Retorno ao worker
        this.EnrichPython.out(0).to(this.ReturnTrue.in(0));
    }
}