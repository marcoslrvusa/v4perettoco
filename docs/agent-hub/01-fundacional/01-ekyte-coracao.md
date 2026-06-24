# Ekyte como Coração da Arquitetura

**Documento:** Fundacional
**Propósito:** Estabelecer o Ekyte como o sistema central de registro, tarefas, gestão e automação — e como cada componente da stack se conecta a ele.

---

## 1. Por que o Ekyte é o Centro

O Ekyte não é mais uma ferramenta no ecossistema — ele é o **sistema de registro** (source of truth) de toda a operação. Tudo que acontece passa por ele:

| O Que | Como | Onde |
|---|---|---|
| **Tarefas** | Criação, atualização, fases, responsáveis, prazos | Ekyte |
| **Projetos** | Cronogramas, compartilhamento com cliente, milestones | Ekyte |
| **Tickets** | Chamados, suporte, flags, alertas | Ekyte |
| **Registro de horas** | Apontamento por tarefa/projeto | Ekyte |
| **Comentários** | Histórico de decisões, contexto, aprovações | Ekyte |
| **Artefatos** | Upload de arquivos vinculados a tarefas | Ekyte |
| **Workflows** | Fluxos de aprovação, tipos de tarefa, automações | Ekyte |
| **Squads e usuários** | Quem faz parte, perfis de acesso | Ekyte |

Quando os agentes do OpenCode precisam **ler** ou **escrever** algo operacional, o destino é o Ekyte.

---

## 2. Arquitetura: Ekyte no Centro

```
                         ┌──────────────────────┐
                         │       OpenCode       │
                         │    (agentes IA)      │
                         │                      │
                         │  @account-checkin    │
                         │  @copy-content       │
                         │  @analista-dados     │
                         │  @csm-orquestrador   │
                         └──────────┬───────────┘
                                    │
                                    │ MCP (65 tools)
                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │                      EKYTE                                │   │
│   │                                                           │   │
│   │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │   │
│   │   │ Tarefas  │  │ Projetos │  │ Tickets  │  │ Horas  │  │   │
│   │   └──────────┘  └──────────┘  └──────────┘  └────────┘  │   │
│   │                                                           │   │
│   │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │   │
│   │   │ Quadros  │  │ Workflows│  │ Artefatos│  │ Squads │  │   │
│   │   └──────────┘  └──────────┘  └──────────┘  └────────┘  │   │
│   └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
           │                        │                    │
           │                        │                    │
           ▼                        ▼                    ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│    Google Drive   │    │    LiteLLM       │    │       n8n        │
│   (documentos,    │    │   (modelos)      │    │  (automações)    │
│    briefings,     │    │   Agente envia   │    │                  │
│    relatórios)    │    │   prompt →       │    │  Webhooks do     │
│                   │    │   modelo         │    │  Ekyte disparam  │
│  Drive MCP lê     │    │   responde       │    │  workflows       │
│  docs para        │    │                  │    │                  │
│  alimentar        │    │  LiteLLM com     │    │  n8n também      │
│  contexto do      │    │  chaves por      │    │  escreve de      │
│  agente           │    │  squad           │    │  volta no Ekyte  │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

## 3. Fluxo Básico: Tudo Começa e Termina no Ekyte

```
USUÁRIO                            AGENTE                              EKYTE
   │                                  │                                  │
   │  "Cria tarefa no Ekyte"          │                                  │
   │─────────────────────────────────>│                                  │
   │                                  │  ekyte/create_task()             │
   │                                  │─────────────────────────────────>│
   │                                  │                           Task criada!
   │                                  │<─────────────────────────────────│
   │                                  │                                  │
   │                                  │  "Precisa de um briefing"        │
   │                                  │  Drive MCP → search_files()      │
   │                                  │  → lê documento                 │
   │                                  │                                  │
   │                                  │  "Analisa com IA"                │
   │                                  │  LiteLLM → modelo → resposta    │
   │                                  │                                  │
   │                                  │  "Salva resultado no Drive"     │
   │                                  │  Drive MCP → create_file()      │
   │                                  │                                  │
   │                                  │  "Atualiza a task no Ekyte"     │
   │                                  │  ekyte/update_task()            │
   │                                  │  + ekyte/create_task_comment()  │
   │                                  │─────────────────────────────────>│
   │                                  │                           Task atualizada!
   │  "Pronto! Link: ..."             │<─────────────────────────────────│
   │<─────────────────────────────────│                                  │
```

## 4. O Que Cada Componente Puxa do Ekyte

| Componente | Lê do Ekyte | Escreve no Ekyte |
|---|---|---|
| **OpenCode (agentes)** | Tarefas, projetos, tickets, squads, usuários, workspaces, quadros, notas, apontamentos | Tarefas, comentários, tickets, projetos, notas, artefatos |
| **n8n** | Tarefas (via webhook), tickets | Tarefas, projetos, tickets, comentários |
| **Google Drive** | — (não se comunicam diretamente) | — |
| **LiteLLM** | — (não se comunicam diretamente) | — |

> Ekyte e Drive **não se comunicam diretamente** — a ponte entre eles é o **agente OpenCode** ou o **n8n**. O agente lê um documento no Drive e cria uma tarefa no Ekyte. O n8n ouve um evento no Ekyte e salva um arquivo no Drive.

## 5. Automações n8n que Integram Ekyte

| Automação | Gatilho | Ação |
|---|---|---|
| **Notificar Slack** | Tarefa criada no Ekyte | Mensagem no canal do squad |
| **Criar pasta no Drive** | Projeto criado no Ekyte | Estrutura de pastas do cliente |
| **Alerta de atraso** | Tarefa vencendo em 24h | Ticket de alerta no Ekyte + notificação |
| **Relatório semanal** | Cron + tarefas concluídas | Gera PDF e salva no Drive |
| **Flag CSM** | OKR fora da meta | Ticket automático no Ekyte |

## 6. Ekyte MCP — 65 Tools em Detalhe

Ver documento específico: [02-componentes/04-ekyte-mcp.md](../02-componentes/04-ekyte-mcp.md)

---

**Documento relacionado:** [fluxograma-ekyte-central.html](../fluxograma-ekyte-central.html) — Diagrama visual da arquitetura.
