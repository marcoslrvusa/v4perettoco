import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [CC] NOS - Expressions & Memo Playground
// Nodes   : 5  |  Connections: 4
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────────────
// Property name                    Node type (short)   Flags
// ManualTrigger                     manualTrigger
// GenerateSampleData                code  (JS — gera payload de teste)
// FilterHighScore                   if    (expressao JSONata/condicional)
// MemoizeReference                 code  (JS — $getWorkflowStaticData)
// OutputResult                     code  (JS — resume tudo)
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────────────
// ManualTrigger
//   → GenerateSampleData
//     → FilterHighScore
//       ├── true  → MemoizeReference → OutputResult
//       └── false → (fim)
// </workflow-map>

// =====================================================================
// [CC] NOS - Expressions & Memo Playground
// =====================================================================
// Proposito: demonstra expressoes avancadas + memoizacao entre execucoes
// ($getWorkflowStaticData). Gera dados de teste, filtra com IF (expressao
// condicional), usa JSONata-equivalente em JS e cache de valor estavel.
//
// CONFIGURE:
//  1. Nada de credencial.
//  2. Rode manualmente para ver as metricas de execucao.
// =====================================================================

@workflow({
  name: '[CC] NOS - Expressions & Memo Playground',
  active: false,
  settings: {
    executionOrder: 'v1',
    timezone: 'America/Sao_Paulo',
    saveDataErrorExecution: 'all',
    saveDataSuccessExecution: 'all',
  },
})
export class ExpressionsMemoPlaygroundWorkflow {
  @node({
    name: 'Manual Trigger',
    type: 'n8n-nodes-base.manualTrigger',
    version: 1,
    position: [250, 300],
  })
  ManualTrigger = {};

  @node({
    name: 'Generate Sample Data',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [520, 300],
  })
  GenerateSampleData = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
// Gera payload de teste: 500 leads com score aleatorio.
const rows = [];
for (let i = 0; i < 500; i++) {
  rows.push({
    id: i + 1,
    name: 'Lead ' + (i + 1),
    score: Math.floor(Math.random() * 100),
    tipo: i % 3 === 0 ? 'B2B' : i % 3 === 1 ? 'B2C' : 'Inbound',
  });
}
return [{ json: { rows, generatedAt: Date.now() } }];
`,
  };

  @node({
    name: 'Filter High Score',
    type: 'n8n-nodes-base.if',
    version: 2.3,
    position: [790, 300],
  })
  FilterHighScore = {
    conditions: {
      conditions: [
        {
          id: 'score-check',
          // Expressao avancada: referencia do proprio item ($json.score)
          leftValue: '={{ $json.score }}',
          rightValue: '={{ 70 }}',
          operator: {
            type: 'number',
            operation: 'gte',
          },
        },
      ],
      combinator: 'and',
      options: {
        caseSensitive: true,
        typeValidation: 'loose',
      },
    },
    options: [],
  };

  @node({
    name: 'Memoize Reference',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [1060, 200],
  })
  MemoizeReference = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
// ============================================================
// Memoize Reference — cache entre execucoes
// ============================================================
// Valores estaveis (limiar, taxa, config) sao cacheados no
// static data do workflow — calculados 1x e reutilizados.
// ============================================================

const staticData = $getWorkflowStaticData('global');
if (staticData.scoreThreshold === undefined) {
  // Simula uma busca cara feita apenas na 1a execucao
  staticData.scoreThreshold = 70;
  staticData.cachedAt = new Date().toISOString();
}

const item = $input.first().json;
return [{
  json: {
    ...item,
    scoreThreshold: staticData.scoreThreshold,
    cachedAt: staticData.cachedAt,
    memoized: true,
  },
}];
`,
  };

  @node({
    name: 'Output Result',
    type: 'n8n-nodes-base.code',
    version: 2,
    position: [1330, 200],
  })
  OutputResult = {
    mode: 'runOnceForAllItems',
    language: 'javaScript',
    jsCode: `
const data = $input.first().json;
const durationMs = Date.now() - (data.generatedAt || Date.now());
return [{
  json: {
    success: true,
    highScoreItems: data.rows ? data.rows.length : 0,
    scoreThreshold: data.scoreThreshold,
    memoized: data.memoized,
    cachedAt: data.cachedAt,
    durationMs,
  },
}];
`,
  };

  @links()
  defineRouting() {
    this.ManualTrigger.out(0).to(this.GenerateSampleData.in(0));
    this.GenerateSampleData.out(0).to(this.FilterHighScore.in(0));
    this.FilterHighScore.out(0).to(this.MemoizeReference.in(0));
    this.MemoizeReference.out(0).to(this.OutputResult.in(0));
  }
}