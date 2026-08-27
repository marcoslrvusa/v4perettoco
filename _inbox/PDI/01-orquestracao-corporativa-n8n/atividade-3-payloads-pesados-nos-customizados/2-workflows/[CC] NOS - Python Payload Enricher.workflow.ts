import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [CC] NOS - Python Payload Enricher
// Nodes   : 4  |  Connections: 3
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────────────
// Property name                    Node type (short)   Flags
// Webhook                           webhook
// ParsePayload                     code (python — decodifica 1x + dedupe)
// EnrichPython                    code (python — agrega com stdlib)
// ReturnSummary                    code (js — resume o resultado)
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────────────
// Webhook
//   → ParsePayload
//     → EnrichPython
//       → ReturnSummary
// </workflow-map>

// =====================================================================
// [CC] NOS - Python Payload Enricher
// =====================================================================
// Proposito: enriquecimento e agregacao de payload pesado em Python,
// apenas stdlib (collections). Recebe via webhook, dedupe O(n) com set,
// agrega com Counter/defaultdict. Exemplo de "no customizado" Python.
//
// CONFIGURE:
//  1. Nada de credencial — apenas nos Code (Python/JS).
// =====================================================================

@workflow({
  name: '[CC] NOS - Python Payload Enricher',
  active: false,
  settings: {
    executionOrder: 'v1',
    timezone: 'America/Sao_Paulo',
    saveDataErrorExecution: 'all',
    saveDataSuccessExecution: 'all',
  },
})
export class PythonPayloadEnricherWorkflow {
  @node({
    name: 'Webhook',
    type: 'n8n-nodes-base.webhook',
    version: 2.1,
    position: [250, 300],
  })
  Webhook = {
    httpMethod: 'POST',
    path: 'nos/python-enricher',
    responseMode: 'onReceived',
    responseData: 'allEntries',
    options: {},
  };

  @node({
    name: 'Parse Payload',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [520, 300],
  })
  ParsePayload = {
    mode: 'runOnceForAllItems',
    language: 'pythonNative',
    pythonCode: `
# ============================================================
# Parse Payload — decodifica 1x, nunca dentro do loop
# ============================================================
import json

data = _input[0]['json']
payload = data.get('payload', [])

if isinstance(payload, str):
    try:
        payload = json.loads(payload)
    except Exception:
        payload = []

rows = payload if isinstance(payload, list) else []

return [{'json': {'totalItems': len(rows), 'rows': rows}}]
`,
  };

  @node({
    name: 'Enrich Python',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [790, 300],
  })
  EnrichPython = {
    mode: 'runOnceForAllItems',
    language: 'pythonNative',
    pythonCode: `
# ============================================================
# Enrich Python — dedupe O(n) + agregacao com stdlib
# ============================================================
from collections import Counter, defaultdict

data = _input[0]['json']
rows = data.get('rows', [])

# 1) dedupe por chave primitiva (O(n))
seen = set()
result = []
for row in rows:
    key = row.get('id')
    if key in seen:
        continue
    seen.add(key)
    result.append(row)

# 2) agregacao com Counter/defaultdict (O(n), nunca O(n²))
by_tipo = Counter(r.get('tipo', 'sem_tipo') for r in result)
soma_score = defaultdict(float)
for r in result:
    try:
        soma_score[r.get('tipo', 'sem_tipo')] += float(r.get('score') or 0)
    except (TypeError, ValueError):
        pass

return [{'json': {
    'totalItems': data.get('totalItems'),
    'processedItems': len(result),
    'deduped': data.get('totalItems', 0) - len(result),
    'by_tipo': dict(by_tipo),
    'soma_score': dict(soma_score),
    'enriched_at': __import__('datetime').datetime.utcnow().isoformat(),
}}]
`,
  };

  @node({
    name: 'Return Summary',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [1060, 300],
  })
  ReturnSummary = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
// Resume o resultado do enriquecimento Python para resposta.
const data = $input.first().json;
return [{
  json: {
    success: true,
    processedItems: data.processedItems,
    deduped: data.deduped,
    byTipo: data.by_tipo,
    somaScore: data.soma_score,
    ref: data.enriched_at,
  },
}];
`,
  };

  @links()
  defineRouting() {
    this.Webhook.out(0).to(this.ParsePayload.in(0));
    this.ParsePayload.out(0).to(this.EnrichPython.in(0));
    this.EnrichPython.out(0).to(this.ReturnSummary.in(0));
  }
}