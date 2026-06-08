import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Peretto AI Ops - Content
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
    id: 'zJSwihRdvEkhxsam',
    name: 'Peretto AI Ops - Content',
    active: true,
    isArchived: false,
    projectId: 'u3W65WbPCWTXrdjF',
    settings: { executionOrder: 'v1' },
})
export class PerettoAiOpsContentWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: '11e86d61-8b46-4bdc-ab4c-944c0d7ffc0e',
        webhookId: '47f168e2-7905-4be0-85cc-e7eda35b8e6f',
        name: 'Webhook',
        type: 'n8n-nodes-base.webhook',
        version: 2.1,
        position: [250, 300],
    })
    Webhook = {
        httpMethod: 'POST',
        path: 'peretto-content',
        authentication: 'none',
        responseMode: 'onReceived',
        responseCode: 200,
        responseData: 'firstEntryJson',
        options: {},
    };

    @node({
        id: 'e768fbf3-4d03-4cca-a24f-5f1f3489b0ac',
        name: 'AI Agent',
        type: '@n8n/n8n-nodes-langchain.agent',
        version: 3.1,
        position: [520, 300],
    })
    AiAgent = {
        promptType: 'define',
        text: `Você é o Peretto AI Ops - Content, especializado em criar conteúdo.

Capacidades:
1. Escrever posts para redes sociais (LinkedIn, Twitter/X, Instagram)
2. Criar newsletters e emails marketing
3. Gerar artigos e blog posts
4. Resumir conteúdos
5. Adaptar tom e estilo conforme solicitado

Sempre retorne o conteúdo formatado e pronto para uso.

Solicitação: {{ $json.body.query || $json.query }}`,
        hasOutputParser: false,
        needsFallback: false,
        options: {},
    };

    @node({
        id: '1c84f22e-8731-41d1-b743-3d086b5d43c5',
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
        id: '4a6945ef-c480-47aa-b075-19bc20d8cea7',
        name: 'Simple Memory',
        type: '@n8n/n8n-nodes-langchain.memoryBufferWindow',
        version: 1.4,
        position: [520, 700],
    })
    SimpleMemory = {
        sessionKey: 'jarvis-content-session',
        sessionIdType: 'fromInput',
        contextWindowLength: 5,
    };

    @node({
        id: '9118e921-0233-4072-9557-ea1f559d7944',
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
