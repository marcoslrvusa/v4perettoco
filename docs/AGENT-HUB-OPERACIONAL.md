# Agent Hub V4 — Manual Operacional

**Produto:** Infraestrutura de Agentes IA para Squads
**Versão:** 1.0 | Junho 2026
**Unidade:** Peretto & Co. / V4 Company
**Stack:** OpenCode + LiteLLM + Google Drive MCP + Ekyte MCP + n8n

---

## Índice

1. [Visão Geral do Sistema](#1-visão-geral-do-sistema)
2. [Arquitetura Multi-Usuário](#2-arquitetura-multi-usuário)
3. [LiteLLM — Gateway e Governança](#3-litellm--gateway-e-governança)
4. [Ecossistema MCP](#4-ecossistema-mcp)
5. [Google Drive como Knowledge Base](#5-google-drive-como-knowledge-base)
6. [Ekyte — Gestão de Projetos e Tarefas](#6-ekyte--gestão-de-projetos-e-tarefas)
7. [n8n — Motor de Automação](#7-n8n--motor-de-automação)
8. [Onboarding de Novo Membro](#8-onboarding-de-novo-membro)
9. [Fluxos Operacionais do Dia a Dia](#9-fluxos-operacionais-do-dia-a-dia)
10. [Segurança e Compliance](#10-segurança-e-compliance)
11. [Custos por Squad e Projeção de Escala](#11-custos-por-squad-e-projeção-de-escala)
12. [Procedimentos de Emergência](#12-procedimentos-de-emergência)
13. [Apêndices](#13-apêndices)

---

## 1. Visão Geral do Sistema

### 1.1 O que é

O **Agent Hub V4** é a infraestrutura compartilhada de agentes de IA da Peretto & Co. Ele roda na VPS Hostinger e permite que cada squad da operação tenha acesso a agentes especializados, modelos de IA via LiteLLM, dados do Google Drive em tempo real, gestão de tarefas no Ekyte e automações via n8n — tudo a partir de um browser.

### 1.2 Proposta de Valor

```
Para squads da Peretto & Co. que precisam de agentes de IA no dia a dia
sem depender de setups locais, chaves de API individuais ou silos de conhecimento,
o Agent Hub é a infraestrutura centralizada que
disponibiliza agentes, modelos e dados do Drive em um só lugar,
com governança de custos, auditoria de uso e onboarding zero-config para novos membros.
```

### 1.3 Componentes da Stack

| Componente | Função | Onde Roda |
|---|---|---|
| **OpenCode Web** | Interface de agentes via browser | VPS (Docker) |
| **LiteLLM** | Gateway de modelos, rate limit, chaves virtuais, custos | VPS (Docker) |
| **Google Drive MCP** | Acesso a documentos, planilhas e arquivos como ferramenta do agente | Remoto (Google MCP) |
| **Ekyte MCP** | Criação e gestão de tarefas, projetos, tickets | Remoto (Ekyte API) |
| **n8n** | Automações, pipelines de dados, integrações | VPS (Docker) |
| **Google People MCP** | Consulta de contatos e perfis | Remoto (Google MCP) |
| **Obsidian** | Knowledge base local com grafo de notas | Local (cada usuário) |

### 1.4 Como os Componentes se Relacionam

```
                    ┌──────────────────────────────────────────────┐
                    │              SQUADS (usuários)                │
                    │  browser → https://opencode.v4.company.com    │
                    └─────────────────────┬────────────────────────┘
                                          │
                    ┌─────────────────────▼────────────────────────┐
                    │            OpenCode Web (VPS)                 │
                    │                                               │
                    │  @analista-dados  @copy-content  @csm         │
                    │  agentes + skills do Builders Hub             │
                    └──────┬──────────────┬──────────────┬─────────┘
                           │              │              │
                    ┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
                    │  LiteLLM    │ │ MCPs      │ │   n8n       │
                    │  (modelos)  │ │ (Drive,   │ │ (automação) │
                    │  virtual    │ │  Ekyte,   │ │             │
                    │  keys,      │ │  People)  │ │             │
                    │  rate limit │ │           │ │             │
                    └──────┬──────┘ └─────┬─────┘ └──────┬──────┘
                           │              │              │
                    ┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
                    │  OpenAI     │ │ Google    │ │  Meta Ads   │
                    │  Anthropic  │ │ Drive     │ │  Google Ads │
                    │  DeepSeek   │ │ Ekyte     │ │  HubSpot    │
                    │  Gemini     │ │           │ │  APIs       │
                    └─────────────┘ └───────────┘ └─────────────┘
```

---

## 2. Arquitetura Multi-Usuário

### 2.1 Modelo de Acesso

Diferente de um SaaS multi-tenant, o OpenCode Web é monousuário por instância — uma sessão por browser. Para uma equipe, existem três modelos de escalabilidade:

| Modelo | Descrição | Prós | Contras |
|---|---|---|---|
| **A — OpenCode Web compartilhado** | Única instância na VPS, todos acessam pelo browser com senha mestra | Simples, zero configuração | Sessões concorrentes limitadas, sem isolamento |
| **B — OpenCode Web + n8n como backend** | Agentes no browser + workflows no n8n para tarefas headless | Escalável, tarefas em background | Depende de n8n para operações assíncronas |
| **C — Cada membro com OpenCode local** | Cada pessoa roda OpenCode local, aponta pro LiteLLM da VPS | Isolamento total, cada um com seu provider | Setup local necessário |

### 2.2 Modelo Recomendado (Híbrido)

```
Usuário 1 (Account)        Usuário 2 (GT)          Usuário 3 (Copy)
       │                        │                        │
       ▼                        ▼                        ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ OpenCode Web │       │ OpenCode Web │       │ OpenCode Web │
│  (browser)   │       │  (browser)   │       │  (browser)   │
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              │
                     ┌────────▼────────┐
                     │   LiteLLM       │
                     │  (VPS Docker)   │
                     │                 │
                     │  Chave virtual  │
                     │  squad-account  │
                     │  squad-gt       │
                     │  squad-copy     │
                     └────────┬────────┘
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │ OpenAI   │  │ DeepSeek │  │ Gemini   │
         │ Anthropic│  │ (Zen)    │  │ (Google) │
         └──────────┘  └──────────┘  └──────────┘
```

**Funcionamento:**

1. Cada squad acessa a mesma URL `https://opencode.v4.company.com` no browser
2. OpenCode Web mantém sessões independentes por aba/gupy
3. LiteLLM faz o roteamento com **chaves virtuais por squad** — cada um tem seu rate limit e teto de gastos
4. MCPs são remotos — Drive MCP pede OAuth individual na primeira conexão
5. n8n roda workflows em background (relatórios, flags, comitê) independentes de sessão

### 2.3 Sessões Compartilhadas

OpenCode Web oferece **session share links**:

```
1. Usuário A inicia sessão de análise
2. Gera link compartilhável: https://opencode.v4.company.com/session/<hash>
3. Envia para Usuário B
4. Usuário B vê o mesmo contexto em tempo real
```

Útil para:
- Pair review de análises
- Debug de workflow com supervisor
- Handoff entre turnos

### 2.4 Configuração de Acesso

```bash
# No servidor VPS
opencode web \
  --host 0.0.0.0 \
  --port 4096 \
  --password "${OPENCODE_SERVER_PASSWORD}"
```

Protegido por:
- **HTTPS** via Nginx reverse proxy + Let's Encrypt
- **Autenticação** via senha mestra (compartilhada pelo squad)
- **Rede interna** opcional via Tailscale (sem expor porta pública)

---

## 3. LiteLLM — Gateway e Governança

### 3.1 O que é e Por Que Usar

LiteLLM é um proxy open-source que unifica 100+ provedores de LLM em uma única API compatível com OpenAI. Na nossa stack, ele é a **camada de governança** entre os agentes e os modelos.

### 3.2 Funções na Stack

| Função | Problema que Resolve | Como Funciona |
|---|---|---|
| **Chaves virtuais** | Cada agente/squad teria acesso direto à API key mestra | LiteLLM gera chaves virtuais por squad com permissões específicas |
| **Rate limit por squad** | Um squad pode consumir o limite dos outros | Cada chave virtual tem rpm (requests per minute) próprio |
| **Teto de gastos** | Loops infinitos podem gerar custos imprevistos | Budget mensal/diário por chave virtual |
| **Fallback automático** | Modelo free pode cair ou ficar lento | Roteia para modelo alternativo automaticamente |
| **Auditoria** | Sem rastreabilidade de uso | Logs de todas as chamadas por squad, modelo, tokens |
| **Cache semântico** | Mesma pergunta várias vezes = tokens desperdiçados | Respostas similares servidas do cache (Redis) |

### 3.3 Configuração de Chaves Virtuais por Squad

```yaml
# litellm-config.yaml
model_list:
  - model_name: deepseek-v4-flash
    litellm_params:
      model: openrouter/deepseek/deepseek-v4-flash:free
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 10

  - model_name: claude-sonnet-4
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY
      rpm: 20

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      rpm: 30

  - model_name: gemini-2.5-flash
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: os.environ/GEMINI_API_KEY
      rpm: 30

  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: os.environ/OPENAI_API_KEY
      rpm: 60

router_settings:
  routing_strategy: "latency-based-routing"
  num_retries: 3
  fallback_strategy: "strict"
  cache:
    type: semantic
    similarity_threshold: 0.85
```

**Chaves virtuais** (criadas via API LiteLLM):

| Squad | Chave Virtual | Modelos Liberados | RPM | Budget Mensal |
|---|---|---|---|---|
| Account | `sk-account-xxxx` | gpt-4o-mini, gemini-2.5-flash | 30 | $20 |
| GT (Tráfego) | `sk-gt-xxxx` | gpt-4o-mini, deepseek-v4-flash | 30 | $20 |
| Copy | `sk-copy-xxxx` | claude-sonnet-4, gpt-4o | 20 | $40 |
| Design | `sk-design-xxxx` | gpt-4o, gemini-2.5-flash | 20 | $15 |
| CSM | `sk-csm-xxxx` | gpt-4o-mini, gemini-2.5-flash | 20 | $15 |
| Coordenação | `sk-coord-xxxx` | Todos | 50 | $50 |

### 3.4 OpenCode → LiteLLM

Cada squad configura no `opencode.json`:

```json
{
  "provider": {
    "litellm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LiteLLM V4",
      "options": {
        "baseURL": "http://litellm:4000/v1",
        "apiKey": "sk-account-xxxx"
      },
      "models": {
        "gpt-4o-mini": {},
        "gemini-2.5-flash": {}
      }
    }
  }
}
```

Se o LiteLLM estiver na mesma VPS (Docker), o nome do host é o nome do container (`litellm`). Se for remoto, usa o IP ou domínio.

### 3.5 Roteamento por Custo

| Agente | Modelo Primário | Custo | Fallback | Custo Fallback |
|---|---|---|---|---|
| @analista-dados | gpt-4o-mini | $0.15/1M in | deepseek-v4-flash | $0 |
| @copy-content | claude-sonnet-4 | $3/1M in | gpt-4o | $2.50/1M in |
| @criacao-design | gpt-4o | $2.50/1M in | gemini-2.5-flash | $0 |
| @flag-roi | deepseek-v4-flash | $0 | gpt-4o-mini | $0.15/1M in |
| @gerar-pdf | gpt-4o | $2.50/1M in | gemini-2.5-flash | $0 |

---

## 4. Ecossistema MCP

### 4.1 O que é MCP na Prática

MCP (Model Context Protocol) é o padrão que permite agentes OpenCode usarem ferramentas externas como se fossem nativas. Cada MCP expõe **tools** que o agente chama sob demanda.

### 4.2 Catálogo de MCPs da Operação

| MCP | Tools | O Que Permite ao Agente | Tipo |
|---|---|---|---|
| **Google Drive MCP** | search_files, read_file_content, create_file, download_file_content, list_recent_files, get_file_metadata, get_file_permissions, copy_file | Ler docs de cliente, buscar planilhas, criar arquivos | Remoto (Google) |
| **Google Docs MCP** | create_document, read_document, update_document | Editar documentos do Drive como texto | Remoto (Google) |
| **Google Sheets MCP** | read_range, update_range, append_rows | Ler/atualizar planilhas de dados | Remoto (Google) |
| **Ekyte MCP** | create_task, list_tasks, update_task, create_project, list_projects, create_ticket, list_tickets, list_squads, list_workspaces, list_time_trackings (65 tools) | Criar tarefas, abrir tickets, gerenciar projetos e apontar horas | Remoto (Ekyte) |
| **Google People MCP** | get_user_profile, search_contacts, search_directory_people | Buscar contatos e perfis de cliente | Remoto (Google) |
| **Google Calendar MCP** | list_events, create_event, get_event | Gerenciar agenda | Remoto (Google) |

### 4.3 Configuração Centralizada

As configurações de MCP ficam no `opencode.json` da VPS, disponíveis para todos os usuários:

```json
{
  "mcp": {
    "google-drive": {
      "type": "remote",
      "url": "https://drivemcp.googleapis.com/mcp/v1",
      "oauth": {
        "clientId": "{env:GOOGLE_MCP_CLIENT_ID}",
        "clientSecret": "{env:GOOGLE_MCP_CLIENT_SECRET}",
        "scope": "https://www.googleapis.com/auth/drive.readonly"
      }
    },
    "google-docs": {
      "type": "remote",
      "url": "https://docsmcp.googleapis.com/mcp/v1",
      "oauth": {
        "clientId": "{env:GOOGLE_MCP_CLIENT_ID}",
        "clientSecret": "{env:GOOGLE_MCP_CLIENT_SECRET}",
        "scope": "https://www.googleapis.com/auth/documents"
      }
    },
    "google-sheets": {
      "type": "remote",
      "url": "https://sheetsmcp.googleapis.com/mcp/v1",
      "oauth": {
        "clientId": "{env:GOOGLE_MCP_CLIENT_ID}",
        "clientSecret": "{env:GOOGLE_MCP_CLIENT_SECRET}",
        "scope": "https://www.googleapis.com/auth/spreadsheets"
      }
    },
    "ekyte": {
      "type": "remote",
      "url": "https://api.ekyte.com/mcp?token={env:EK YTE_MCP_TOKEN}",
      "enabled": true
    },
    "google-people": {
      "type": "remote",
      "url": "https://people.googleapis.com/mcp/v1",
      "oauth": {
        "clientId": "{env:GOOGLE_MCP_CLIENT_ID}",
        "clientSecret": "{env:GOOGLE_MCP_CLIENT_SECRET}",
        "scope": "https://www.googleapis.com/auth/contacts.readonly"
      }
    }
  }
}
```

### 4.4 Fluxo de Autenticação OAuth (Google MCPs)

```
1. OpenCode inicia, carrega MCPs do config
2. Usuário dá comando que usa tool do Drive
3. OpenCode detecta: precisa autenticar
4. Abre browser com tela de consentimento Google
5. Usuário autoriza
6. Token salvo em ~/.local/share/opencode/mcp-auth.json
7. Tool executa normalmente
```

O token fica no servidor (VPS), associado à sessão do OpenCode Web. Cada usuário precisa autorizar uma vez.

### 4.5 Adicionar Novo MCP no Futuro

O ecossistema MCP é extensível. Para adicionar:

```bash
# MCP local (stdio) — roda na VPS
opencode mcp add <nome> \
  --type local \
  --command "npx -y @us-all/google-drive-mcp"

# MCP remoto (URL) — serviço externo
opencode mcp add <nome> \
  --type remote \
  --url "https://api.exemplo.com/mcp"
```

Ou adiciona no `opencode.json`:

```json
{
  "mcp": {
    "novo-servico": {
      "type": "remote",
      "url": "https://api.exemplo.com/mcp/v1",
      "enabled": true
    }
  }
}
```

### 4.6 MCPs com Potencial para Incorporar

| MCP | O Que Faz | Prioridade |
|---|---|---|
| **Context7** | Documentação atualizada de bibliotecas/frameworks | 🟡 Média |
| **GitHub** | Issues, PRs, código do Builders Hub | 🟢 Alta |
| **Slack** | Mensagens, canais, notificações | 🟡 Média |
| **Web Search** | Pesquisa em tempo real (tendências, concorrência) | 🟢 Alta |
| **n8n MCP** | Disparar workflows do n8n como tools | 🟢 Alta |
| **Meta Ads MCP** | Dados de campanhas direto no agente | 🟡 Média |
| **Notion MCP** | Se migrarem para Notion no futuro | 🔴 Baixa |

---

## 5. Google Drive como Knowledge Base

### 5.1 Estrutura de Pastas no Drive

O Google Drive é a **fonte única de verdade** da operação. A estrutura de pastas espelha o Builders Hub:

```
📁 V4 Company Drive
├── 📁 Squads/
│   ├── 📁 [Squad]/
│   │   ├── 📁 Clientes/
│   │   │   ├── 📁 [Cliente]/
│   │   │   │   ├── 📄 Briefings/
│   │   │   │   ├── 📄 Documents/
│   │   │   │   ├── 📄 Relatórios/
│   │   │   │   └── 📄 Campanhas/
│   │   │   └── ...
│   │   ├── 📁 Operacional/
│   │   └── 📁 Reports/
│   └── ...
├── 📁 Bases/
│   ├── 📁 Dados/
│   ├── 📁 Referências/
│   └── 📁 Templates/
└── 📁 Compartilhado/
    ├── 📁 Modelos de Documento
    └── 📁 Playbooks
```

### 5.2 Como os Agentes Usam o Drive

Através do **Google Drive MCP**, os agentes têm 8 tools de manipulação:

| Tool MCP | O Que o Agente Pode Fazer | Exemplo de Uso |
|---|---|---|
| `search_files` | Buscar arquivos por nome, tipo, pasta | "Busque o briefing mais recente do cliente X" |
| `read_file_content` | Ler conteúdo de qualquer arquivo | "Leia a planilha de métricas do cliente Y" |
| `create_file` | Criar arquivos no Drive | "Crie um documento com o resumo da reunião" |
| `download_file_content` | Baixar conteúdo para processamento | "Baixe o PDF do relatório e analise" |
| `list_recent_files` | Ver arquivos recentes | "Quais documentos foram modificados hoje?" |
| `get_file_metadata` | Ver metadados (data, autor, tamanho) | "Quem criou este arquivo e quando?" |
| `get_file_permissions` | Ver permissões de acesso | "Quem tem acesso a esta pasta?" |
| `copy_file` | Duplicar arquivos | "Crie uma cópia do template para este cliente" |

### 5.3 Fluxo Completo: Agente Usa Drive

```
Usuário: "@copy-content, leia o briefing do cliente X no Drive
         e crie uma proposta de post para Instagram"

1. Agente abre sessão no OpenCode Web
2. Chama google-drive/search_files(query="briefing cliente X")
3. Google Drive MCP → retorna ID do arquivo
4. Agente chama google-drive/read_file_content(fileId="xxx")
5. Lê o briefing completo
6. Processa no contexto com o modelo (gpt-4o via LiteLLM)
7. Gera a proposta de post
8. Chama google-drive/create_file para salvar o resultado
9. Chama ekytte/create_task para criar tarefa no Ekyte
10. Responde ao usuário com o link do arquivo + tarefa
```

### 5.4 Cache Local vs Drive

A abordagem é **Drive-first**: o agente busca o documento quando precisa. Não há syncing em massa para o servidor. Isso garante que o dado está sempre fresco e evitamos duplicação.

Exceção: documentos de clientes ativos podem ser sincronizados via n8n para a pasta `squads/` local (para contexto rápido sem chamada MCP), mas a fonte original é sempre o Drive.

### 5.5 Modelos de Documento no Drive

Manter **templates** no Drive permite que os agentes gerem documentos padronizados:

- Template de briefing de campanha
- Template de relatório mensal
- Template de proposta comercial
- Template de pauta de check-in

O agente busca o template, preenche com dados do cliente e salva como novo documento.

---

## 6. Ekyte — Gestão de Projetos e Tarefas

### 6.1 O Ekyte na Operação

O Ekyte é o sistema de gestão de projetos e tarefas da operação. Com o **Ekyte MCP**, os agentes do OpenCode podem ler e escrever diretamente no Ekyte — criar tarefas, atualizar prazos, abrir tickets, gerenciar projetos, apontar horas.

### 6.2 65 Tools Disponíveis

O Ekyte MCP expõe 65 tools, organizadas em grupos funcionais:

| Grupo | Tools | O Que Permite |
|---|---|---|
| **Squads** | list_squads | Consultar squads da empresa |
| **Usuários** | list_all_users_with_profile, list_admin_editors_users | Quem é quem na operação |
| **Workspaces** | list_short_workspaces, create_workspace | Gestão de workspaces |
| **Tarefas** | create_task, list_tasks, update_task, get_detailed_task, create_task_comment, update_task_phase, update_task_tags, update_task_channels, update_task_responsibles, update_task_executor, update_task_recurring, list_task_flow_phases, list_task_forms, list_task_comments, list_project_tasks (15 tools) | Ciclo completo de tarefas |
| **Tipos de Tarefa** | list_task_types, list_task_types_create_task, get_task_type_flow, get_detailed_task_type, update_task_task_type | Workflows por tipo |
| **Workflows** | list_workflows, get_detailed_workflow | Fluxos de trabalho |
| **Tickets** | create_ticket, list_tickets, update_ticket, get_detailed_ticket, create_ticket_comment, update_ticket_analyst, update_ticket_tags, update_ticket_phase, update_ticket_cc, update_ticket_executor (11 tools) | Ciclo completo de tickets |
| **Projetos** | create_project, list_projects, get_detailed_project, update_project, update_project_tags, update_project_shared_customers, generate_project_share_link, send_project_email | Gestão de projetos com cronograma compartilhado |
| **Quadros** | create_board, list_boards, get_detailed_board, update_board | Kanban e quadros |
| **Categorias** | create_board_category, update_board_category | Categorias de quadro |
| **Notas** | create_board_note, get_detailed_note, update_board_note | Notas em quadros |
| **Artefatos** | artifact_generate_upload_sas, artifact_confirm_upload, list_artifacts, get_detailed_artifact | Upload e gestão de arquivos |
| **Apontamento** | list_time_trackings | Consulta de horas apontadas |

### 6.3 Fluxo: Agente Cria Tarefa a Partir de Reunião

```
Usuário: "@account-orchestrator, acabei a call com o cliente X.
         Crie as tarefas no Ekyte com base no transcript"

1. Agente lê o transcript do Google Drive (Drive MCP)
2. Extrai combinados, prazos e responsáveis
3. Para cada combinado:
   a. Chama ekyte/create_task(
        workspaceId: "marketing",
        title: "Entregar relatório Q2",
        currentDueDate: "2026-07-15",
        responsibleUserId: "joao",
        description: "Combinado na call de 20/06..."
      )
4. Chama ekyte/create_task_comment para registrar contexto
5. Responde: "3 tarefas criadas no Ekyte. Links: ..."
```

### 6.4 Automação Ekyte + n8n

O n8n pode **ouvir eventos do Ekyte** via webhook e disparar ações:

| Evento | Ação n8n | Gatilho |
|---|---|---|
| Tarefa criada | Notificar squad no Slack | Webhook Ekyte |
| Tarefa atrasada | Alertar coordenador | Cron semanal |
| Ticket aberto | Criar documento no Drive com resumo | Webhook Ekyte |
| Projeto concluído | Gerar relatório e salvar no Drive | Webhook Ekyte |
| Comentário adicionado | Log no mission-control do cliente | Webhook Ekyte |

---

## 7. n8n — Motor de Automação

### 7.1 Papel na Stack

O n8n é o **backend de automação** da operação. Enquanto o OpenCode executa agentes sob demanda (síncrono, com humano no loop), o n8n executa workflows programados ou disparados por eventos (assíncrono, headless).

### 7.2 Trabalho em Conjunto: OpenCode + n8n

```
          SOLICITAÇÃO                     AUTOMAÇÃO
     ┌──────────────────┐          ┌──────────────────┐
     │   OpenCode Web   │          │       n8n        │
     │   (agente sob    │          │  (workflow em    │
     │    demanda)      │          │   background)    │
     └────────┬─────────┘          └────────┬─────────┘
              │                             │
              │ "Puxa dados do              │ Cron: toda segunda 8h
              │  Meta Ads p/                │ → Puxa dados de todos
              │  relatório semanal"         │   os clientes
              │                             │ → Gera relatório
              │                             │ → Salva no Drive
              ▼                             ▼
     ┌──────────────────┐          ┌──────────────────┐
     │   Chama n8n      │          │   Workflow n8n   │
     │   webhook p/     │          │   processa e     │
     │   disparar       │          │   entrega        │
     │   workflow       │          │   (autônomo)     │
     └──────────────────┘          └──────────────────┘
```

### 7.3 Catálogo de Workflows

| Workflow | Disparo | O Que Faz | Saída |
|---|---|---|---|
| **Relatório de Tráfego Semanal** | Cron (segunda 8h) | Puxa Meta Ads + Google Ads, consolida, analisa | HTML + Drive |
| **Briefing do Comitê** | Cron (domingo 20h) | Puxa OKRs, sprints, FCAs de todos os clientes | Markdown + email |
| **Flags CSM** | Cron (quinta 7h) | Verifica NPS, CSAT, ROAS, OKRs contra meta | Alerta no Slack |
| **Sync Drive → Local** | Webhook (ao alterar pasta) | Sincroniza docs de cliente ativo para `squads/` local | Arquivos locais |
| **Handoff Vendas → Account** | Webhook (ticket criado) | Cria pasta de cliente, estrutura inicial, notifica account | KB inicial |
| **Criação de Cliente no Ekyte** | Webhook (novo-cliente) | Cria workspace, projeto e tarefas iniciais | Ekyte |
| **Notificação de Atraso** | Cron (diário 9h) | Verifica tarefas vencidas no Ekyte | Slack + email |

### 7.4 OpenCode Chamando n8n

O agente pode disparar workflows do n8n via webhook:

```
Usuário: "@analista-dados, quero o relatório semanal do cliente X"

Agente: 
1. Verifica se já existe relatório recente no Drive
2. Se não, chama webhook do n8n:
   POST https://n8n.v4.company.com/webhook/relatorio-semanal
   Body: { "cliente": "X", "periodo": "2026-06-15 a 2026-06-21" }
3. n8n dispara o workflow em background
4. Agente informa: "Relatório sendo gerado. Deve ficar pronto em 2 min."
```

### 7.5 n8n MCP (Opcional)

Com o **n8n MCP**, o agente pode listar, disparar e monitorar workflows diretamente como tools:

```json
{
  "mcp": {
    "n8n": {
      "type": "remote",
      "url": "https://n8n.v4.company.com/mcp",
      "headers": {
        "Authorization": "Bearer {env:N8N_MCP_TOKEN}"
      }
    }
  }
}
```

Tools que o agente ganha: `list_workflows`, `execute_workflow`, `get_execution_status`, `list_executions`.

---

## 8. Onboarding de Novo Membro

### 8.1 Checklist de 30 Minutos

```
┌──────────────────────────────────────────────────────────┐
│                 ONBOARDING — NOVO MEMBRO                  │
│                    (30 minutos)                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  □ 1. Acesso ao VPS                                      │
│     → Coordenação cria usuário Linux no servidor         │
│     → Chave SSH gerada e configurada                     │
│     → Acesso via: ssh <nome>@v4.company.com              │
│                                                          │
│  □ 2. OpenCode Web                                       │
│     → URL: https://opencode.v4.company.com               │
│     → Senha mestra do squad (via coordenador)            │
│     → Primeiro acesso: autentica Google OAuth p/ MCPs    │
│                                                          │
│  □ 3. Google Drive MCP                                   │
│     → Na primeira tool do Drive: browser abre OAuth      │
│     → Autoriza acesso aos documentos do squad            │
│     → Pronto: agente lê Drive como se fosse local        │
│                                                          │
│  □ 4. LiteLLM (chave virtual)                            │
│     → Coordenação gera chave virtual no LiteLLM          │
│     → Modelos liberados conforme papel do membro         │
│     → Budget mensal definido                             │
│                                                          │
│  □ 5. Ekyte MCP                                          │
│     → Token MCP gerado em Configurações > Usuário        │
│     → Token configurado no .env da VPS                   │
│     → Agente cria tarefas como o usuário                 │
│                                                          │
│  □ 6. Builders Hub (Git)                                 │
│     → git clone do repositório                           │
│     → Skills e agentes disponíveis localmente            │
│     → Fluxo de compartilhamento (sync-hub, PRs)          │
│                                                          │
│  □ 7. n8n (se aplicável)                                 │
│     → URL: https://n8n.v4.company.com                    │
│     → Acesso aos workflows do squad                      │
│                                                          │
│  □ 8. Teste Rápido                                       │
│     → "Quais são as tarefas do meu squad no Ekyte?"      │
│     → "Busque o último briefing do cliente X no Drive"   │
│     → "Crie uma tarefa de teste no workspace Y"          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 8.2 Responsabilidades por Papel

| Papel | Responsável por Onboarding |
|---|---|
| Coordenador do squad | Acesso ao VPS, LiteLLM, Ekyte, senhas |
| DevOps (quem configurou) | Manutenção da stack, troubleshooting |
| Novo membro | Seguir checklist, testar integrações |

### 8.3 Primeiros Comandos do Novo Membro

```bash
# Testar conexão com LiteLLM
curl http://litellm:4000/v1/models \
  -H "Authorization: Bearer sk-account-xxxx"

# Testar OpenCode Web
# → Abrir https://opencode.v4.company.com no browser
# → Digitar: "Quais MCPs estão configurados?"
# → O agente lista todas as tools disponíveis

# Testar Drive MCP
# → "Busque o arquivo mais recente na pasta do squad"
# → Na primeira vez, autoriza OAuth no browser

# Testar Ekyte MCP
# → "Liste minhas tarefas no Ekyte para hoje"

# Testar fluxo completo
# → "Leia o briefing do cliente X no Drive e crie
#    uma tarefa no Ekyte para revisar o briefing"
```

---

## 9. Fluxos Operacionais do Dia a Dia

### 9.1 Account — Pós-Reunião de Check-in

```
1. Usuário abre https://opencode.v4.company.com
2. Cola o transcript da call do Google Meet
3. Digita: "@account-checkin-review, processa este transcript"
4. Agente:
   a. Lê o transcript
   b. Chama Drive MCP → busca mission-control do cliente
   c. Chama Ekyte MCP → cria tarefas dos combinados
   d. Chama Drive MCP → atualiza documento de combinados
   e. Retorna resumo com links para as tarefas criadas
```

### 9.2 Copy — Criação de Conteúdo

```
1. Usuário: "@copy-content, preciso de um post para Instagram
             do cliente X sobre o lançamento da campanha Y"
2. Agente:
   a. Busca briefing no Drive (search_files)
   b. Lê o documento de briefing (read_file_content)
   c. Busca tom de voz do cliente no Drive
   d. Verifica campanhas anteriores no Ekyte (list_project_tasks)
   e. Gera 3 opções de copy no contexto do modelo
   f. Cria documento no Drive com as opções (create_file)
   g. Cria tarefa no Ekyte para aprovação (create_task)
   h. Retorna: "3 opções prontas. Link: ... Tarefa criada no Ekyte."
```

### 9.3 GT — Análise de Performance

```
1. Usuário: "@analista-dados, como foi o ROAS do cliente X
             na última semana vs a anterior?"
2. Agente:
   a. Chama n8n webhook → dispara workflow que puxa Meta Ads
   b. Workflow n8n salva resultado no Drive (planilha)
   c. Agente lê a planilha (read_file_content via Sheets MCP)
   d. Analisa no modelo (gpt-4o-mini via LiteLLM)
   e. Gera relatório com comparação, tendência e alertas
   f. Salva relatório no Drive
   g. Se ROAS abaixo da meta: cria flag no Ekyte (create_ticket)
   h. Retorna análise completa
```

### 9.4 CSM — Diagnóstico de Cliente

```
1. Usuário: "@csm-orquestrador, diagnóstico completo do cliente X"
2. Agente:
   a. Busca mission-control no Drive
   b. Busca histórico de check-ins (pastas do Drive)
   c. Chama Ekyte MCP → busca tarefas abertas do cliente
   d. Analisa NPS/CSAT (se disponível)
   e. Verifica flags ativas (n8n pode ter disparado alguma)
   f. Gera diagnóstico: saude da relação, riscos, recomendações
   g. Cria documento no Drive
   h. Se risco detectado: cria ticket de alerta no Ekyte
```

### 9.5 Coordenação — Comitê de P&EG

```
1. Workflow n8n (cron: domingo 20h) dispara:
   a. Puxa OKRs de todos os clientes (Drive/planilha)
   b. Puxa tasks do Ekyte por squad
   c. Puxa FCAs (se houver)
   d. Salva dados consolidados no Drive
2. Coordenador abre OpenCode Web:
3. Digita: "@executor-comite, gera o briefing do comitê"
4. Agente:
   a. Lê dados consolidados do Drive
   b. Invoca @analista-dados para cada cliente
   c. @revisor valida cada análise
   d. Consolida em briefing markdown + HTML
   e. Salva no Drive e envia por email (via n8n)
```

---

## 10. Segurança e Compliance

### 10.1 Matriz de Acesso

| Recurso | Quem Acessa | Como |
|---|---|---|
| OpenCode Web (URL) | Todos os squads | HTTPS + senha |
| LiteLLM (API) | OpenCode Web (indireto) | Rede interna Docker |
| Google Drive | Cada usuário (OAuth individual) | MCP remoto |
| Ekyte | Cada usuário (token individual) | MCP remoto |
| n8n UI | Coordenação + devs | HTTPS + senha |
| VPS (SSH) | Coordenação + devs | Chave SSH + IP restrito |
| Builders Hub (Git) | Todos os squads | GitHub (repo público/privado) |

### 10.2 Dados de Cliente

```
Regra fundamental: dado de cliente NÃO TRAFEGA pelo LiteLLM
para modelos externos sem autorização.

Fluxo seguro:
1. Drive MCP lê documento do cliente → agente OpenCode
2. Agente envia contexto para LiteLLM → modelo
3. LiteLLM NÃO armazena prompts (config stateless)
4. Resposta do modelo → agente → resultado para o usuário
5. Nada persiste em servidores terceiros além do modelo escolhido
```

### 10.3 Controle de Modelos por Dado

| Tipo de Dado | Modelos Permitidos | Motivo |
|---|---|---|
| Dados públicos (briefing, artigo) | Todos | Sem restrição |
| Dados internos (relatórios, OKRs) | gpt-4o-mini, deepseek | Modelos com política de não-treinamento |
| Dados sensíveis (financeiro, estratégico) | deepseek, gemini | Modelos que não retreinam com dados de produção |
| Dados de cliente (nome, contato) | deepseek, gemini | Máximo controle |

### 10.4 Política de Chaves e Tokens

| Segredo | Onde Fica | Quem Tem Acesso | Rotação |
|---|---|---|---|
| Chave mestra LiteLLM | `.env` na VPS | 1 pessoa (dev) | A cada 90 dias |
| Chaves virtuais (squad) | `opencode.json` de cada squad | Squad | A cada 90 dias |
| Token Ekyte | `.env` na VPS | Cada usuário (token próprio) | A cada 180 dias |
| OAuth Google (MCP) | `mcp-auth.json` no servidor | Individual | Revogável a qualquer momento |
| API keys (OpenAI, Anthropic) | LiteLLM (nunca expostas) | 0 pessoas (só o LiteLLM) | A cada 90 dias |

### 10.5 Auditoria

```
O QUE é auditado                ONDE fica
──────────────────────────────────────────────────
Todas as chamadas de LLM        Logs do LiteLLM (PostgreSQL)
Todas as tools MCP chamadas     Logs do OpenCode
Todas as execuções n8n          Histórico do n8n
Todas as ações no Ekyte        Audit log do Ekyte
Acessos SSH ao VPS             /var/log/auth.log
```

---

## 11. Custos por Squad e Projeção de Escala

### 11.1 Custos Fixos (Infraestrutura Compartilhada)

| Item | Custo Mensal | Rateado por Squad |
|---|---|---|
| VPS Hostinger (4 vCPU, 16GB RAM) | ~$15/mês | ~$2-3/squad (5 squads) |
| Domínio + SSL | ~$10/mês | ~$2/squad |
| Docker Compose (OpenCode + LiteLLM + n8n) | $0 | $0 |
| **Total fixo por squad** | | **~$4-5/mês** |

### 11.2 Custos Variáveis (Modelos)

**Cenário Free (hoje):**

| Squad | Modelo Principal | Custo |
|---|---|---|
| Account | Gemini 2.5 Flash (Google free) | $0 |
| GT | DeepSeek V4 Flash (Zen free) | $0 |
| Copy | DeepSeek V4 Flash (Zen free) | $0 |
| Design | Gemini 2.5 Flash (Google free) | $0 |
| CSM | DeepSeek V4 Flash (Zen free) | $0 |
| Coordenação | Misto (free) | $0 |
| **Total** | | **$0/mês** |

**Cenário Misto (recomendado para produção):**

| Squad | Modelo Pago Principal | Estimativa |
|---|---|---|
| Account | gpt-4o-mini ($0.15/1M in) | ~$5/mês |
| GT | gpt-4o-mini ($0.15/1M in) | ~$5/mês |
| Copy | claude-sonnet-4 ($3/1M in) | ~$15/mês |
| Design | gpt-4o ($2.50/1M in) | ~$10/mês |
| CSM | gpt-4o-mini ($0.15/1M in) | ~$3/mês |
| Coordenação | gpt-4o + claude | ~$10/mês |
| **Total estimado** | | **~$48/mês** |

### 11.3 Projeção por Tamanho de Equipe

| Métrica | 5 pessoas | 15 pessoas | 30 pessoas |
|---|---|---|---|
| Squads | 2 | 5 | 8 |
| VPS necessária | 1 (atual) | 1 (upgrade 8 vCPU) | 2 (escala horizontal) |
| Custo VPS | $15/mês | $25/mês | $50/mês |
| Custo APIs (misto) | $15/mês | $48/mês | $90/mês |
| **Total/mês** | **~$30** | **~$73** | **~$140** |
| **Custo por pessoa** | **$6** | **$4.80** | **$4.60** |

### 11.4 O Que o Custo por Pessoa Cobre

```
$4-6/pessoa/mês → acesso a:
├── 5+ modelos de IA (GPT, Claude, Gemini, DeepSeek)
├── 65+ tools do Ekyte (tarefas, projetos, tickets)
├── 8+ tools do Google Drive (documentos, planilhas)
├── Acesso ao Drive em tempo real via MCP
├── Workflows de automação n8n
├── 35+ agentes especializados
├── 100+ skills do Builders Hub
└── Manutenção zero (infra gerenciada pela coordenação)

Comparação:
  ChatGPT Team: $25/pessoa/mês
  Claude Pro: $20/pessoa/mês
  Agent Hub V4: $4-6/pessoa/mês ← 4-6x mais barato
```

---

## 12. Procedimentos de Emergência

### 12.1 LiteLLM Fora do Ar

```bash
# 1. Verificar status
docker ps | grep litellm

# 2. Ver logs
docker logs v4-litellm --tail 30

# 3. Reiniciar
docker restart v4-litellm

# 4. Se não resolver, conferir API keys no .env
docker exec v4-litellm env | grep API_KEY

# 5. Fallback: configurar OpenCode direto (sem proxy)
# → Remover provider.litellm do opencode.json
# → Adicionar provider.openrouter direto
```

### 12.2 OpenCode Web Fora do Ar

```bash
# 1. Verificar status
docker ps | grep opencode

# 2. Ver logs
docker logs v4-opencode --tail 50 -f

# 3. Reiniciar
docker restart v4-opencode

# 4. Verificar healthcheck
curl -I https://opencode.v4.company.com
```

### 12.3 Google Drive MCP Desconectado

```
1. Sintoma: agente tenta usar tool do Drive e recebe erro de auth
2. Causa: token OAuth expirou ou foi revogado
3. Solução: reautenticar
   opencode mcp auth google-drive
4. Browser abre → autorizar novamente
5. Testar: "Busque um arquivo no Drive"
```

### 12.4 Ekyte MCP Fora do Ar

```bash
# 1. Testar conexão
curl -I "https://api.ekyte.com/mcp?token=$EKYTE_MCP_TOKEN"

# 2. Verificar se token expirou
# → Gerar novo em Configurações > Usuário no Ekyte

# 3. Atualizar .env na VPS
nano /data/v4-repo/.env
# → Atualizar EKYTE_MCP_TOKEN

# 4. Reiniciar OpenCode
docker restart v4-opencode
```

### 12.5 Rate Limit Atingido

```
1. Sintoma: agente para de responder ou recebe erro 429
2. Causa: rpm excedido no LiteLLM ou no modelo free
3. Solução imediata:
   - Esperar 1-2 minutos
   - Trocar para modelo alternativo manualmente
4. Solução definitiva:
   - Aumentar rpm no LiteLLM (se plano pago)
   - Distribuir carga entre mais modelos
   - Ativar cache semântico para reduzir chamadas repetidas
```

### 12.6 Estouro de Budget

```
1. LiteLLM bloqueia automaticamente quando teto é atingido
2. Squad afetado: agentes param de funcionar
3. Coordenador:
   a. Avalia se foi uso legítimo ou loop
   b. Se legítimo: aumenta budget no LiteLLM
   c. Se loop: revisa agente que causou, ajusta permissões
4. Restaura acesso: atualiza budget da chave virtual
```

---

## 13. Apêndices

### A. Comandos Úteis no Servidor

```bash
# Status da stack
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Logs em tempo real
docker logs -f v4-litellm
docker logs -f v4-opencode
docker logs -f v4-n8n

# Recursos
docker stats --no-stream

# Testar LiteLLM
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer $LITELLM_API_KEY" | jq .

# Listar chaves virtuais do LiteLLM
curl http://localhost:4000/v1/key/list \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" | jq .

# Backup do .env
cp /data/v4-repo/.env /data/v4-repo/.env.backup.$(date +%Y%m%d)

# Atualizar repositório (skills, agentes)
cd /data/v4-repo && git pull && docker restart v4-opencode
```

### B. Arquivo .env da VPS

```bash
# ─── LiteLLM ───
LITELLM_MASTER_KEY=sk-master-xxxx
LITELLM_SALT_KEY=salt-xxxx

# ─── API Keys ───
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
OPENROUTER_API_KEY=sk-or-...

# ─── Google MCP OAuth ───
GOOGLE_MCP_CLIENT_ID=xxxx.apps.googleusercontent.com
GOOGLE_MCP_CLIENT_SECRET=GOCSPX-...

# ─── Ekyte MCP ─── (tokens individuais por squad)
EKYTE_MCP_TOKEN_ACCOUNT=ekyte_mcp_token_do_usuario_account
EKYTE_MCP_TOKEN_GT=ekyte_mcp_token_do_usuario_gt
EKYTE_MCP_TOKEN_COPY=ekyte_mcp_token_do_usuario_copy
EKYTE_MCP_TOKEN_DESIGN=ekyte_mcp_token_do_usuario_design
EKYTE_MCP_TOKEN_CSM=ekyte_mcp_token_do_usuario_csm
EKYTE_MCP_TOKEN_COORD=ekyte_mcp_token_do_usuario_coord

# ─── OpenCode Web ───
OPENCODE_SERVER_PASSWORD=senha-compartilhada-do-squad

# ─── n8n ───
N8N_ENCRYPTION_KEY=...

# ─── Postgres ───
POSTGRES_PASSWORD=...
```

### C. Glossário

| Termo | Definição |
|---|---|
| **MCP** | Model Context Protocol — padrão para conectar agentes a ferramentas externas |
| **LiteLLM** | Proxy que unifica múltiplos provedores de LLM em uma API |
| **Chave Virtual** | Chave API gerada pelo LiteLLM com permissões e limites específicos |
| **Tool** | Função exposta por um MCP que o agente pode chamar |
| **Squad** | Time da operação (Account, GT, Copy, Design, CSM, Coordenação) |
| **Builders Hub** | Repositório Git com skills e agentes compartilhados |
| **OpenCode Web** | Interface browser do OpenCode rodando no servidor |

### D. Referências

1. [OpenCode MCP Documentation](https://opencode.ai/docs/mcp-servers)
2. [LiteLLM Documentation](https://docs.litellm.ai)
3. [Google Workspace MCP Guide](https://developers.google.com/workspace/guides/configure-mcp-servers)
4. [Ekyte MCP Documentation](https://developers.ekyte.com/docs/mcp)
5. [n8n Documentation](https://docs.n8n.io)
6. [OpenCode Providers Guide](https://opencode.ai/docs/providers)
7. [SkillKit — Package Manager for AI Skills](https://skillkit.sh)
8. [INFRAESTRUTURA-AI.md](./INFRAESTRUTURA-AI.md) — Documento base de infraestrutura
9. [AGENTS.md](../AGENTS.md) — Regras do Builders Hub

---

*Documento gerado em junho/2026. Mantido em `docs/AGENT-HUB-OPERACIONAL.md` no Builders Hub.
Atualizar sempre que novos MCPs forem adicionados ou a estrutura de squads mudar.*
