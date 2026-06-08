import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Peretto AI Ops - Chat
// Nodes   : 7  |  Connections: 1
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// ChatTrigger                        chatTrigger
// AiAgent                            agent                      [AI]
// OpenrouterChatModel                lmChatOpenAi               [creds] [ai_languageModel]
// SimpleMemory                       memoryBufferWindow         [ai_memory]
// WebSearchAgentTool                 toolWorkflow               [ai_tool]
// ContentAgentTool                   toolWorkflow               [ai_tool]
// ContactsAgentTool                  toolWorkflow               [ai_tool]
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// ChatTrigger
//    → AiAgent
//
// AI CONNECTIONS
// AiAgent.uses({ ai_languageModel: OpenrouterChatModel, ai_memory: SimpleMemory, ai_tool: [WebSearchAgentTool, ContentAgentTool, ContactsAgentTool] })
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'tdKTb1fcmKHkLxqH',
    name: 'Peretto AI Ops - Chat',
    active: true,
    isArchived: false,
    projectId: 'u3W65WbPCWTXrdjF',
    settings: { executionOrder: 'v1' },
})
export class PerettoAiOpsChatWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: '36f9b623-fe61-4d97-b7a0-0e2e06f2c2c2',
        webhookId: 'e679652b-69fb-423a-9ec4-676be9d2efca',
        name: 'Chat Trigger',
        type: '@n8n/n8n-nodes-langchain.chatTrigger',
        version: 1.4,
        position: [250, 300],
    })
    ChatTrigger = {
        public: true,
        mode: 'hostedChat',
        authentication: 'none',
        initialMessages: 'Bem-vindo ao Peretto AI Ops. Como posso ajudar hoje?',
        availableInChat: true,
        agentName: 'Peretto AI Ops',
        agentDescription: 'Assistente inteligente da V4 Company para automação e operações',
        agentIcon: {
            type: 'icon',
            value: 'bot',
        },
        suggestedPrompts: {
            prompts: [
                {
                    text: 'Pesquise sobre inteligência artificial em 2026',
                },
                {
                    text: 'Me ajude a escrever um post para o LinkedIn sobre produtividade',
                },
                {
                    text: 'Quais as últimas notícias de tecnologia?',
                },
                {
                    text: 'Crie uma newsletter semanal sobre marketing digital',
                },
            ],
        },
        options: {},
    };

    @node({
        id: '30825234-0fd0-4e39-b32b-54709d6df6a1',
        name: 'AI Agent',
        type: '@n8n/n8n-nodes-langchain.agent',
        version: 3.1,
        position: [520, 300],
    })
    AiAgent = {
        promptType: 'define',
        text: `Você é Peretto AI Ops — plataforma de automação inteligente da V4 Company.

## Personalidade
- Profissional, direto e eficiente
- Respostas concisas e em português brasileiro
- Foco em resolver com agilidade

## Capacidades
Você pode responder perguntas, pesquisar na web, criar conteúdo e gerenciar contatos.
Use as ferramentas disponíveis quando necessário.

## Regras
- Para perguntas simples, responda diretamente
- Use as ferramentas para buscar informações atualizadas ou executar ações
- Apresente os resultados de forma organizada
- Mantenha o contexto da conversa`,
        hasOutputParser: false,
        needsFallback: false,
        options: {},
    };

    @node({
        id: '959364b1-5291-4c6a-b90d-40976f3806a3',
        name: 'OpenRouter Chat Model',
        type: '@n8n/n8n-nodes-langchain.lmChatOpenAi',
        version: 1.3,
        position: [520, 500],
        credentials: { openAiApi: { id: 'SN4AwfKsQ1EMDELQ', name: 'OpenRouter' } },
    })
    OpenrouterChatModel = {
        model: {
            mode: 'id',
            value: 'openrouter/free',
        },
        options: {
            baseURL: 'https://openrouter.ai/api/v1',
        },
    };

    @node({
        id: '2d7d9556-0e43-4857-80d2-8ad862bb41cb',
        name: 'Simple Memory',
        type: '@n8n/n8n-nodes-langchain.memoryBufferWindow',
        version: 1.4,
        position: [520, 700],
    })
    SimpleMemory = {
        sessionKey: 'jarvis-chat-web',
        sessionIdType: 'customKey',
        contextWindowLength: 10,
    };

    @node({
        id: 'bf5926a0-a7d6-49dc-9ce2-9cd31705cc5d',
        name: 'Web Search Agent Tool',
        type: '@n8n/n8n-nodes-langchain.toolWorkflow',
        version: 2.2,
        position: [790, 300],
    })
    WebSearchAgentTool = {
        name: 'webSearchAgent',
        description:
            'Pesquisa na internet em tempo real. Use quando o usuário pedir para pesquisar, buscar notícias, informações atuais ou qualquer coisa que precise da web.',
        source: 'database',
        workflowId: '0rqMgaLLfOUiyFzG',
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
                        value: '={{ $json.chatInput || $json.input }}',
                    },
                ],
            },
        },
    };

    @node({
        id: '10079b1f-75ef-4367-a0ed-9b3d3a1c274d',
        name: 'Content Agent Tool',
        type: '@n8n/n8n-nodes-langchain.toolWorkflow',
        version: 2.2,
        position: [790, 500],
    })
    ContentAgentTool = {
        name: 'contentAgent',
        description:
            'Cria conteúdo: posts para redes sociais, artigos, newsletters, resumos. Use quando o usuário pedir para criar ou gerar conteúdo escrito.',
        source: 'database',
        workflowId: 'zJSwihRdvEkhxsam',
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
                        value: '={{ $json.chatInput || $json.input }}',
                    },
                ],
            },
        },
    };

    @node({
        id: '0e078add-df53-4400-bb5d-de5366614127',
        name: 'Contacts Agent Tool',
        type: '@n8n/n8n-nodes-langchain.toolWorkflow',
        version: 2.2,
        position: [790, 700],
    })
    ContactsAgentTool = {
        name: 'contactsAgent',
        description: 'Gerencia contatos: buscar, criar, atualizar, listar contatos.',
        source: 'database',
        workflowId: 'Hp2pmqu92vxLXvFH',
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
                        value: '={{ $json.chatInput || $json.input }}',
                    },
                ],
            },
        },
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.ChatTrigger.out(0).to(this.AiAgent.in(0));

        this.AiAgent.uses({
            ai_languageModel: this.OpenrouterChatModel.output,
            ai_memory: this.SimpleMemory.output,
            ai_tool: [this.WebSearchAgentTool.output, this.ContentAgentTool.output, this.ContactsAgentTool.output],
        });
    }
}
