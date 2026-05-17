import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : JARVIS - Email Agent
// Nodes   : 6  |  Connections: 2
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// Webhook                            webhook
// AiAgent                            agent                      [AI]
// OpenaiChatModel                    lmChatOpenAi               [creds] [ai_languageModel]
// SimpleMemory                       memoryBufferWindow         [ai_memory]
// GmailTool                          gmailTool                  [ai_tool]
// RespondToWebhook                   respondToWebhook
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// Webhook
//    → AiAgent
//      → RespondToWebhook
//
// AI CONNECTIONS
// AiAgent.uses({ ai_languageModel: OpenaiChatModel, ai_memory: SimpleMemory, ai_tool: [GmailTool] })
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'HaHWMjK8BE8ZI0pp',
    name: 'JARVIS - Email Agent',
    active: false,
    isArchived: false,
    settings: { executionOrder: 'v1' },
})
export class JarvisEmailAgentWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: '1700328a-487e-40b2-ae72-8f6a6cd231e2',
        webhookId: 'adc0b24f-f200-40d1-b45b-5d6c1cf0f07b',
        name: 'Webhook',
        type: 'n8n-nodes-base.webhook',
        version: 2.1,
        position: [250, 300],
    })
    Webhook = {
        httpMethod: 'POST',
        path: 'jarvis-email-agent',
        authentication: 'none',
        responseMode: 'onReceived',
        responseCode: 200,
        responseData: 'firstEntryJson',
        options: {},
    };

    @node({
        id: '3f834911-a560-4fb8-a07f-b3bd1ee9ec1a',
        name: 'AI Agent',
        type: '@n8n/n8n-nodes-langchain.agent',
        version: 3.1,
        position: [520, 300],
    })
    AiAgent = {
        promptType: 'define',
        text: `Você é o Email Agent do JARVIS, um assistente especializado em gerenciamento de email.

Sua função é executar operações de email usando as ferramentas disponíveis:
- Buscar emails (caixa de entrada, não lidos, por remetente)
- Enviar emails
- Responder emails
- Organizar emails (marcar como lido, arquivar)

Operações suportadas:
1. "buscar" - Lista emails recentes ou não lidos
2. "enviar" - Envia um novo email
3. "responder" - Responde a um email existente
4. "arquivar" - Arquivar emails

Sempre confirme antes de executar ações destrutivas.

O usuário solicitou: {{ $json.body.query || $json.query }}`,
        hasOutputParser: false,
        needsFallback: false,
        options: {},
    };

    @node({
        id: '3051da18-ecf2-4f3b-bf0b-a4af6d271462',
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
        id: '19f25a33-cfbe-4c2a-ae2b-8c7ccc5bf888',
        name: 'Simple Memory',
        type: '@n8n/n8n-nodes-langchain.memoryBufferWindow',
        version: 1.4,
        position: [520, 700],
    })
    SimpleMemory = {
        sessionKey: 'jarvis-email-session',
        sessionIdType: 'fromInput',
        contextWindowLength: 10,
    };

    @node({
        id: '52a171c7-891a-46e2-82d8-0dcb5422d126',
        webhookId: '102c8f11-8606-4e79-905a-d7a02bb5baa9',
        name: 'Gmail Tool',
        type: 'n8n-nodes-base.gmailTool',
        version: 2.2,
        position: [790, 300],
    })
    GmailTool = {
        resource: 'message',
        operation: 'getAll',
        descriptionType: 'manual',
        toolDescription:
            'Gerencia emails do Gmail: buscar, enviar, responder, arquivar. Use para qualquer operação relacionada a email.',
    };

    @node({
        id: '54320968-4bae-467c-8baa-0bc70028a9fc',
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
            ai_tool: [this.GmailTool.output],
        });
    }
}
