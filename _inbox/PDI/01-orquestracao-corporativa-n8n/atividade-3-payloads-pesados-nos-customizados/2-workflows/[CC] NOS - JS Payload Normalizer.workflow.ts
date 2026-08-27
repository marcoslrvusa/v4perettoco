import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [CC] NOS - JS Payload Normalizer
// Nodes   : 4  |  Connections: 3
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────────────
// Property name                    Node type (short)   Flags
// Webhook                           webhook
// ParseAndChunk                    code  (JS — stream + chunk + dedupe)
// NormalizeInOnePass               code  (JS — O(n), copia minima)
// ReturnMetrics                    code  (JS — metricas de performance)
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────────────
// Webhook
//   → ParseAndChunk
//     → NormalizeInOnePass
//       → ReturnMetrics
// </workflow-map>

// =====================================================================
// [CC] NOS - JS Payload Normalizer
// =====================================================================
// Proposito: recebe payload pesado via webhook, faz parsing 1x, chunking
// streaming, dedupe por chave e normalizacao em UMA passada (O(n)).
// Entrega itens normalizados + metricas de performance.
//
// CONFIGURE:
//  1. Nada de credencial — apenas nos Code (JS).
//  2. ChunkSize no node ParseAndChunk (default 1000).
// =====================================================================

@workflow({
  name: '[CC] NOS - JS Payload Normalizer',
  active: false,
  settings: {
    executionOrder: 'v1',
    timezone: 'America/Sao_Paulo',
    saveDataErrorExecution: 'all',
    saveDataSuccessExecution: 'all',
  },
})
export class JsPayloadNormalizerWorkflow {
  @node({
    name: 'Webhook',
    type: 'n8n-nodes-base.webhook',
    version: 2.1,
    position: [250, 300],
  })
  Webhook = {
    httpMethod: 'POST',
    path: 'nos/js-normalizer',
    responseMode: 'onReceived',
    responseData: 'allEntries',
    options: {},
  };

  @node({
    name: 'Parse and Chunk',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [520, 300],
  })
  ParseAndChunk = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
// ============================================================
// Parse and Chunk — payload pesado (JS)
// ============================================================
// 1) Recebe { payload: "JSON string" | array }.
// 2) Parse 1x (nunca dentro do loop).
// 3) Quebra em chunks e agrupa por chunk para dedupe O(n).
// ============================================================

const raw = $input.first().json;
let rows = raw.payload;

if (typeof rows === 'string') {
  try { rows = JSON.parse(rows); } catch (e) { rows = []; }
}
if (!Array.isArray(rows)) rows = rows && rows.rows ? rows.rows : [];

const chunkSize = Number(raw.chunk_size || 1000);
const chunks = [];
for (let i = 0; i < rows.length; i += chunkSize) {
  chunks.push(rows.slice(i, i + chunkSize));
}

return [{
  json: {
    totalItems: rows.length,
    chunkSize,
    totalChunks: chunks.length,
    chunks,
    startedAt: Date.now(),
  },
}];
`,
  };

  @node({
    name: 'Normalize in One Pass',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [790, 300],
  })
  NormalizeInOnePass = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
// ============================================================
// Normalize in One Pass — O(n), copia minima, dedupe por chave
// ============================================================
// Filtra + dedupe + transforma no MESMO loop. Sem map().filter()
// encadeado, sem busca por item, sem spread gigante por item.
// ============================================================

const ctx = $input.first().json;
const seen = new Set();
const out = [];

for (const chunk of ctx.chunks) {
  for (const row of chunk) {
    // 1) filtro barato primeiro
    if (!row || !row.id) continue;

    // 2) dedupe por chave primitiva
    const key = String(row.id);
    if (seen.has(key)) continue;
    seen.add(key);

    // 3) transformacao minima (evita copiar campos inuteis)
    out.push({
      json: {
        id: row.id,
        name: String(row.name || '').toUpperCase(),
        score: Number(row.score || 0),
      },
    });
  }
}

return [{
  json: {
    totalItems: ctx.totalItems,
    processedItems: out.length,
    deduped: ctx.totalItems - out.length,
    normalizedAt: new Date().toISOString(),
    items: out,
  },
}];
`,
  };

  @node({
    name: 'Return Metrics',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [1060, 300],
  })
  ReturnMetrics = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
// ============================================================
// Return Metrics — diagnostico de performance do pipeline
// ============================================================
const data = $input.first().json;
const durationMs = Date.now() - (data.startedAt || Date.now());

return [{
  json: {
    success: true,
    processedItems: data.processedItems,
    deduped: data.deduped,
    durationMs,
    itemsPerSecond: data.processedItems
      ? Math.round(data.processedItems / (durationMs / 1000))
      : 0,
    resultRef: data.normalizedAt,
  },
}];
`,
  };

  @links()
  defineRouting() {
    this.Webhook.out(0).to(this.ParseAndChunk.in(0));
    this.ParseAndChunk.out(0).to(this.NormalizeInOnePass.in(0));
    this.NormalizeInOnePass.out(0).to(this.ReturnMetrics.in(0));
  }
}