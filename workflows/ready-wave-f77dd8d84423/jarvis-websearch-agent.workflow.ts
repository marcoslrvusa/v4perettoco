import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Peretto AI Ops - Search
// Nodes   : 5  |  Connections: 4
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// Webhook                            webhook
// SetQuery                           set
// HttpRequestTavily                  httpRequest
// FormatResponse                     code
// RespondToWebhook                   respondToWebhook
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// Webhook
//    → SetQuery
//      → HttpRequestTavily
//        → FormatResponse
//          → RespondToWebhook
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: '0rqMgaLLfOUiyFzG',
    name: 'Peretto AI Ops - Search',
    active: true,
    isArchived: false,
    projectId: 'u3W65WbPCWTXrdjF',
    settings: { executionOrder: 'v1' },
})
export class PerettoAiOpsSearchWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: '489c201c-82a0-448b-8603-9d2febd8e0e4',
        webhookId: 'c0c87a29-c08c-433b-a9ab-7f5aec905164',
        name: 'Webhook',
        type: 'n8n-nodes-base.webhook',
        version: 2.1,
        position: [250, 300],
    })
    Webhook = {
        httpMethod: 'POST',
        path: 'peretto-search',
        authentication: 'none',
        responseMode: 'onReceived',
        responseCode: 200,
        responseData: 'firstEntryJson',
        options: {},
    };

    @node({
        id: 'ebe4a62c-cd33-4ff9-ab2e-c8674e1113e9',
        name: 'Set Query',
        type: 'n8n-nodes-base.set',
        version: 3.1,
        position: [520, 300],
    })
    SetQuery = {
        mode: 'manual',
        assignments: {
            assignments: [
                {
                    id: 'query',
                    name: 'query',
                    value: '={{ $json.body.query || $json.query }}',
                    type: 'string',
                },
            ],
        },
        options: {},
    };

    @node({
        id: '141173ea-0131-4d92-bd2f-b6c8752d6da7',
        name: 'HTTP Request - Tavily',
        type: 'n8n-nodes-base.httpRequest',
        version: 4.2,
        position: [790, 300],
    })
    HttpRequestTavily = {
        method: 'POST',
        url: 'https://api.tavily.com/search',
        authentication: 'none',
        sendHeaders: true,
        specifyHeaders: 'keypair',
        headerParameters: {
            parameters: [
                {
                    name: 'Authorization',
                    value: 'Bearer {{ $json.tavilyApiKey }}',
                },
                {
                    name: 'Content-Type',
                    value: 'application/json',
                },
            ],
        },
        sendBody: true,
        specifyBody: 'json',
        jsonBody: '={"query":"={{ $json.query }}","search_depth":"basic","include_answer":true,"max_results":5}',
        options: {},
    };

    @node({
        id: 'aea88cca-3017-415e-938d-7fd712ba1299',
        name: 'Format Response',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1060, 300],
    })
    FormatResponse = {
        jsCode: `// Formatar resposta da busca
const results = $input.all();
const searchData = results[0].json;

// Tavily retorna: answer, results[], query, response_time
let formatted = '';

if (searchData.answer) {
  formatted += '## Resumo da Busca\\n\\n';
  formatted += searchData.answer + '\\n\\n';
}

if (searchData.results && searchData.results.length > 0) {
  formatted += '## Resultados\\n\\n';
  for (const r of searchData.results) {
    formatted += \`### \${r.title}\\n\`;
    formatted += \`\${r.content}\\n\`;
    formatted += \`Fonte: \${r.url}\\n\\n\`;
  }
}

return [{ json: { result: formatted, raw: searchData } }];`,
    };

    @node({
        id: '83354cf1-1978-4198-a8a3-911888f710fa',
        name: 'Respond to Webhook',
        type: 'n8n-nodes-base.respondToWebhook',
        version: 1.5,
        position: [1330, 300],
    })
    RespondToWebhook = {
        respondWith: 'json',
        responseBody: {},
        options: {},
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.Webhook.out(0).to(this.SetQuery.in(0));
        this.SetQuery.out(0).to(this.HttpRequestTavily.in(0));
        this.HttpRequestTavily.out(0).to(this.FormatResponse.in(0));
        this.FormatResponse.out(0).to(this.RespondToWebhook.in(0));
    }
}
