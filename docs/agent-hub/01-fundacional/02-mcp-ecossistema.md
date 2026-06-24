# Ecossistema MCP Integrado

**Propósito:** Mapear como os diferentes MCPs se relacionam e como os agentes os combinam em um fluxo único.

---

## 1. Os 5 MCPs da Operação

```
                    ┌──────────────────────────────────────┐
                    │          AGENTE OpenCode             │
                    │                                      │
                    │   @account-checkin  @copy-content    │
                    │   @analista-dados   @csm             │
                    └──────────┬──────────┬───────────────┘
                               │          │
          ┌────────────────────┼──────────┼────────────────────┐
          │                    │          │                    │
          ▼                    ▼          ▼                    ▼
   ┌──────────┐         ┌──────────┐  ┌──────────┐      ┌──────────┐
   │  Ekyte   │         │ Drive    │  │ People   │      │ Calendar │
   │  MCP     │         │ MCP      │  │ MCP      │      │ MCP      │
   │  65 tools│         │ 8 tools  │  │ 3 tools  │      │ 8 tools  │
   └──────────┘         └──────────┘  └──────────┘      └──────────┘
```

## 2. Matriz de Combinação de MCPs

Os agentes **combinam múltiplos MCPs** em um único fluxo. Abaixo, as combinações mais comuns:

| Fluxo | MCPs Usados | O Que Acontece |
|---|---|---|
| **Criar tarefa pós-reunião** | Drive + Ekyte | Lê transcript do Drive → extrai combinados → cria tasks no Ekyte |
| **Onboarding de cliente** | People + Drive + Ekyte | Busca perfil do cliente → busca template → cria projeto + tarefas |
| **Relatório com dados do time** | Ekyte + Calendar + Drive | Busca tasks concluídas → verifica prazos → gera documento |
| **Ticket de suporte** | People + Ekyte | Busca contato do cliente → abre ticket com dados completos |
| **Planejamento de campanha** | Drive + Ekyte + Calendar | Lê briefing → cria tarefas no cronograma → cria eventos marco |

## 3. Exemplo Completo: Combinando 3 MCPs

```
Agente: @account-orchestrator
Tarefa: "Processar handoff do novo cliente X"

Passo 1 — People MCP:
  → search_directory_people(query: "cliente X")
  → Retorna: contato, email, telefone, cargo

Passo 2 — Drive MCP:
  → search_files(query: "briefing cliente X")
  → read_file_content(fileId: "...")
  → Retorna: documento de briefing completo

Passo 3 — Ekyte MCP:
  → create_project(name: "Cliente X", ...)
  → create_task(projectId: "...", title: "Revisar briefing", ...)
  → create_task(projectId: "...", title: "Kickoff com cliente", ...)
  → create_task_comment(taskId: "...", text: "Cliente indicado por...")
  → Retorna: projeto e tarefas criados

Resultado final para o usuário:
  "Cliente X onboarded. Projeto criado, 2 tarefas geradas.
   Contato: joao@email.com. Briefing lido e vinculado."
```

## 4. MCPs como Camadas

| Camada | MCP | Função | Ferramentas |
|---|---|---|---|
| **Registro** | Ekyte MCP | Onde tudo é registrado (source of truth operacional) | 65 tools |
| **Conhecimento** | Google Drive MCP | Onde os documentos vivem (briefings, relatórios) | 8 tools |
| **Contato** | Google People MCP | Quem são as pessoas (clientes, contatos) | 3 tools |
| **Tempo** | Google Calendar MCP | Quando as coisas acontecem (prazos, eventos) | 8 tools |

## 5. Adicionando Novos MCPs

O ecossistema é extensível. Para adicionar um MCP futuro:

```bash
# Exemplo: adicionar MCP do Slack
opencode mcp add slack \
  --type remote \
  --url "https://slackmcp.googleapis.com/mcp/v1" \
  --oauth-client-id "$SLACK_CLIENT_ID" \
  --oauth-client-secret "$SLACK_CLIENT_SECRET"
```

Ao adicionar, atualizar: [docs/agent-hub/index.md](../index.md)

---

**Documento relacionado:** [fluxograma-ekyte-central.html](../fluxograma-ekyte-central.html)
