import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Peretto AI Ops - Contacts
// Nodes   : 5  |  Connections: 2
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// Webhook                            webhook
// AiAgent                            agent                      [AI]
// OpenaiChatModel                    lmChatOpenAi               [creds] [ai_languageModel]
// SimpleMemory                       memoryBufferWindow         [ai_memory]
// RespondToWebhook                   respondToWebhook
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// Webhook
//    → AiAgent
//      → RespondToWebhook
//
// AI CONNECTIONS
// AiAgent.uses({ ai_languageModel: OpenaiChatModel, ai_memory: SimpleMemory })
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'Hp2pmqu92vxLXvFH',
    name: 'Peretto AI Ops - Contacts',
    active: true,
    isArchived: false,
    projectId: 'u3W65WbPCWTXrdjF',
    settings: { executionOrder: 'v1' },
})
export class PerettoAiOpsContactsWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: '6e2ad1cc-1d5e-44bc-86e5-eab7d9e80498',
        webhookId: '93116089-eb5a-4293-aa3a-f040babdea92',
        name: 'Webhook',
        type: 'n8n-nodes-base.webhook',
        version: 2.1,
        position: [250, 300],
    })
    Webhook = {
        httpMethod: 'POST',
        path: 'peretto-contacts',
        authentication: 'none',
        responseMode: 'onReceived',
        responseCode: 200,
        responseData: 'firstEntryJson',
        options: {},
    };

    @node({
        id: '3603683e-0e82-4563-8bf3-3cd86bc03c57',
        name: 'AI Agent',
        type: '@n8n/n8n-nodes-langchain.agent',
        version: 3.1,
        position: [520, 300],
    })
    AiAgent = {
        promptType: 'define',
        text: `Você é o Peretto AI Ops - Contacts, especializado em gerenciar contatos.

Funções:
1. "buscar" - Buscar contato por nome/email
2. "criar" - Adicionar novo contato
3. "atualizar" - Atualizar dados de contato
4. "listar" - Listar todos os contatos

Use a ferramenta Google Sheets para acessar a planilha de contatos.
ID da planilha será fornecido quando configurado.

Consulta: {{ $json.body.query || $json.query }}`,
        hasOutputParser: false,
        needsFallback: false,
        options: {},
    };

    @node({
        id: 'bfb46240-c9ee-4f9b-9148-5d5f48121285',
        name: 'OpenAI Chat Model',
        type: '@n8n/n8n-nodes-langchain.lmChatOpenAi',
        version: 1.3,
        position: [520, 500],
        credentials: { openAiApi: { id: 'SN4AwfKsQ1EMDELQ', name: 'OpenRouter' } },
    })
    OpenaiChatModel = {
        model: {
            mode: 'id',
            value: 'openrouter/free',
        },
        options: {
            baseURL: 'https://openrouter.ai/api/v1',
        },
    };

    @node({
        id: '4fe549e0-d5f5-4080-83dc-e39738dcfd34',
        name: 'Simple Memory',
        type: '@n8n/n8n-nodes-langchain.memoryBufferWindow',
        version: 1.4,
        position: [520, 700],
    })
    SimpleMemory = {
        sessionKey: 'jarvis-contacts-session',
        sessionIdType: 'fromInput',
        contextWindowLength: 5,
    };

    @node({
        id: '932b958e-32fb-4022-bf39-24f18389731d',
        name: 'Respond to Webhook',
        type: 'n8n-nodes-base.respondToWebhook',
        version: 1.5,
        position: [790, 500],
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
        this.Webhook.out(0).to(this.AiAgent.in(0));
        this.AiAgent.out(0).to(this.RespondToWebhook.in(0));

        this.AiAgent.uses({
            ai_languageModel: this.OpenaiChatModel.output,
            ai_memory: this.SimpleMemory.output,
        });
    }
}
