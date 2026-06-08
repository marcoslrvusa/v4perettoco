import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Peretto AI Ops - WhatsApp
// Nodes   : 6  |  Connections: 5
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// Webhook                            webhook
// FormatInput                        code
// CallPerettoAiOps                   toolWorkflow
// FormatResponse                     code
// Whatsapp                           whatsApp                   [creds]
// RespondToWebhook                   respondToWebhook
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// Webhook
//    → FormatInput
//      → CallPerettoAiOps
//        → FormatResponse
//          → Whatsapp
//            → RespondToWebhook
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'zXmAorUdV3jQuBHx',
    name: 'Peretto AI Ops - WhatsApp',
    active: true,
    isArchived: false,
    projectId: 'u3W65WbPCWTXrdjF',
    settings: { executionOrder: 'v1' },
})
export class PerettoAiOpsWhatsappWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: 'a50cfdb7-7038-41e6-8281-d0af7c370816',
        webhookId: '3538dd66-f2bb-452b-9f35-30aeb6708f72',
        name: 'Webhook',
        type: 'n8n-nodes-base.webhook',
        version: 2.1,
        position: [250, 300],
    })
    Webhook = {
        httpMethod: 'POST',
        path: 'peretto-whatsapp',
        authentication: 'none',
        responseMode: 'responseNode',
        responseCode: 200,
        responseData: 'firstEntryJson',
        options: {},
    };

    @node({
        id: '906aa491-9ecd-437a-9eab-125dfd35bcd5',
        name: 'Format Input',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [520, 300],
    })
    FormatInput = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `// Extrair mensagem do webhook (Evolution API ou formato genérico)
const item = $input.first().json;

// Evolution API format
let message = '';
let sender = '';
let senderName = '';

if (item.data && item.data.message) {
  // Evolution API
  message = item.data.message.message || '';
  sender = item.data.message.key && item.data.message.key.remoteJid ? item.data.message.key.remoteJid.replace('@s.whatsapp.net', '') : '';
  senderName = item.data.message.pushName || sender;
} else if (item.body) {
  // Generic format
  message = item.body.message || item.body.text || item.body.query || '';
  sender = item.body.from || item.body.sender || '';
  senderName = item.body.senderName || sender;
} else if (item.message) {
  message = typeof item.message === 'string' ? item.message : item.message.text || '';
}

// Se veio audio transcrito
const transcribedText = item.body && item.body.transcribedText ? item.body.transcribedText : '';

const finalQuery = transcribedText || message;

return [{
  json: {
    query: finalQuery,
    sender: sender,
    senderName: senderName,
    source: 'whatsapp'
  }
}];`,
    };

    @node({
        id: '7844f323-0330-4fb2-9c59-5f98d6126030',
        name: 'Call Peretto AI Ops',
        type: '@n8n/n8n-nodes-langchain.toolWorkflow',
        version: 2.2,
        position: [790, 300],
    })
    CallPerettoAiOps = {
        name: 'perettoMain',
        description: 'Call the main Peretto AI Ops orchestrator',
        source: 'database',
        workflowId: 'MiT8fbGXxIxX6NKP',
        workflowInputs: {
            mappingMode: 'defineBelow',
            value: {
                schema: [
                    {
                        id: 'query',
                        displayName: 'query',
                        type: 'string',
                    },
                ],
                matchingColumns: ['query'],
                values: [
                    {
                        fieldName: 'query',
                        mappingMode: 'manual',
                        value: '={{ $json.query }}',
                    },
                ],
            },
        },
    };

    @node({
        id: '2a637d79-ed9c-4400-b0b8-9f7b9bc0bc38',
        name: 'Format Response',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1060, 300],
    })
    FormatResponse = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `        // Formatar resposta do Peretto AI Ops para WhatsApp
const result = $input.first().json;
let responseText = '';

// Extrair texto da resposta
if (result.result) {
  responseText = typeof result.result === 'string' ? result.result : result.result.text || JSON.stringify(result.result);
} else if (result.output) {
  responseText = typeof result.output === 'string' ? result.output : JSON.stringify(result.output);
} else if (result.response) {
  responseText = typeof result.response === 'string' ? result.response : JSON.stringify(result.response);
} else {
  responseText = JSON.stringify(result);
}

// Limitar tamanho para WhatsApp (limite ~4096 chars)
if (responseText.length > 4000) {
  responseText = responseText.substring(0, 3997) + '...';
}

return [{
  json: {
    response: responseText,
    sender: $json.sender,
    senderName: $json.senderName
  }
}];`,
    };

    @node({
        id: 'bf8bcfb4-1cfa-413f-8710-3ce5888e4514',
        webhookId: '82913059-80bb-4432-9740-e1c939e151d2',
        name: 'WhatsApp',
        type: 'n8n-nodes-base.whatsApp',
        version: 1.1,
        position: [1330, 300],
        credentials: { whatsAppApi: { id: 'CREDENTIAL_ID', name: 'WhatsApp API' } },
    })
    Whatsapp = {
        resource: 'message',
        operation: 'send',
        phoneNumberId: '{{ $json.phoneNumberId }}',
        recipientPhoneNumber: '={{ $json.sender }}',
        messageType: 'text',
        textBody: '={{ $json.response }}',
    };

    @node({
        id: 'a40f83d8-5b13-4943-bb40-2acd48383e4b',
        name: 'Respond to Webhook',
        type: 'n8n-nodes-base.respondToWebhook',
        version: 1.5,
        position: [1600, 300],
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
        this.Webhook.out(0).to(this.FormatInput.in(0));
        this.FormatInput.out(0).to(this.CallPerettoAiOps.in(0));
        this.CallPerettoAiOps.out(0).to(this.FormatResponse.in(0));
        this.FormatResponse.out(0).to(this.Whatsapp.in(0));
        this.Whatsapp.out(0).to(this.RespondToWebhook.in(0));
    }
}
