# Ekyte MCP — 65 Tools para Agentes

**Propósito:** Referência completa de todas as ferramentas do Ekyte MCP que os agentes do OpenCode podem usar.

---

## 1. Conexão

```json
{
  "mcp": {
    "ekyte": {
      "type": "remote",
      "url": "https://api.ekyte.com/mcp?token={env:EKYTE_MCP_TOKEN}",
      "enabled": true
    }
  }
}
```

**Token:** Gerar em *Configurações > Usuário* no Ekyte. Cada usuário tem o próprio token — ações são registradas como executadas por ele.

## 2. Índice de Tools por Grupo

### 👥 Squads e Usuários
| Tool | O Que Faz | Quando Usar |
|---|---|---|
| `list_squads` | Lista todos os squads | "Quais squads existem?" |
| `list_admin_editors_users` | Usuários admin/editor | "Quem pode aprovar?" |
| `list_all_users_with_profile` | Todos os usuários + perfil | "Quem é quem na empresa?" |

### 📁 Workspaces
| Tool | O Que Faz |
|---|---|
| `list_short_workspaces` | Lista resumida de workspaces |
| `create_workspace` | Cria workspace (simples ou lote) |

### 📋 Tarefas (15 tools)

| Tool | O Que Faz | Fluxo Recomendado |
|---|---|---|
| `list_task_types_create_task` | Tipos de tarefa disponíveis | **Passo 1:** antes de criar, liste os tipos |
| `get_task_type_flow` | Fluxo do tipo de tarefa | **Passo 2:** veja as fases do tipo |
| `create_task` | Cria tarefa | **Passo 3:** crie com datas calculadas de trás pra frente |
| `create_recurring_task` | Próxima ocorrência de tarefa recorrente | Quando situação=30 e recurring=true |
| `list_tasks` | Lista tarefas (filtrado, max 200) | Consultas do dia a dia |
| `get_detailed_task` | Detalhes completos de uma tarefa | **SEMPRE** chame antes de update |
| `update_task` | Atualiza campos da tarefa | Depois de consultar o estado atual |
| `update_task_phase` | Avança/retrocede fase | Movimentação no workflow |
| `update_task_tags` | Substitui tags da tarefa | Re-categorização |
| `update_task_channels` | Substitui canais | Muda onde a tarefa aparece |
| `update_task_responsibles` | Substitui responsáveis | Reatribuição |
| `update_task_executor` | Altera executor da fase atual | Troca quem está executando |
| `update_task_recurring` | Altera configuração de recorrência | Muda frequência |
| `update_task_task_type` | Troca o tipo da tarefa | Migração de workflow |
| `list_task_flow_phases` | Etapas do fluxo da tarefa | "Em que fase está?" |

### 💬 Comentários em Tarefas
| Tool | O Que Faz |
|---|---|
| `create_task_comment` | Adiciona comentário |
| `list_task_comments` | Lista comentários |
| `list_task_forms` | Formulários vinculados |

### 📊 Projetos (8 tools)
| Tool | O Que Faz |
|---|---|
| `list_projects` | Lista projetos (max 75) |
| `get_detailed_project` | Detalhes completos |
| `create_project` | Cria novo projeto |
| `update_project` | Atualiza projeto |
| `update_project_tags` | Substitui tags |
| `update_project_shared_customers` | Compartilha cronograma com cliente |
| `generate_project_share_link` | Gera link público do cronograma |
| `send_project_email` | Envia cronograma por email |

### 🎫 Tickets (11 tools)
| Tool | O Que Faz |
|---|---|
| `list_tickets` | Lista tickets (max 200) |
| `create_ticket` | Abre novo ticket |
| `get_detailed_ticket` | Detalhes completos |
| `update_ticket` | Atualiza ticket |
| `update_ticket_phase` | Avança fase |
| `update_ticket_analyst` | Transfere responsável |
| `update_ticket_tags` | Substitui tags |
| `update_ticket_cc` | Altera cópia |
| `update_ticket_executor` | Troca executor da fase |
| `list_ticket_flow_phases` | Etapas do fluxo |
| `create_ticket_comment` | Comenta no ticket |

### 📌 Quadros (6 tools)
| Tool | O Que Faz |
|---|---|
| `list_boards` | Lista quadros |
| `get_detailed_board` | Detalhes + categorias + notas |
| `create_board` | Cria quadro |
| `update_board` | Atualiza quadro |
| `create_board_category` | Cria categoria |
| `update_board_category` | Renomeia/atualiza categoria |
| `create_board_note` | Cria nota |
| `get_detailed_note` | Detalhes da nota |
| `update_board_note` | Atualiza nota |

### 📎 Artefatos (4 tools)
| Tool | O Que Faz |
|---|---|
| `artifact_generate_upload_sas` | Inicia upload de arquivo |
| `artifact_confirm_upload` | Finaliza upload |
| `list_artifacts` | Lista arquivos da biblioteca |
| `get_detailed_artifact` | Detalhes do arquivo |

### ⏱ Apontamento
| Tool | O Que Faz |
|---|---|
| `list_time_trackings` | Apontamentos de horas (max 400) |

## 3. Regras para o Agente Usar o Ekyte MCP

### Regra 1: Sempre consultar antes de atualizar
```
ANTES de update_task / update_ticket / update_project:
  → Chame get_detailed_task / get_detailed_ticket / get_detailed_project
  → Capture o estado atual
  → Inclua campos existentes que não vão mudar junto com as alterações
```

### Regra 2: Criar tarefa seguindo o fluxo
```
1. list_task_types_create_task → tipos disponíveis
2. get_task_type_flow → fases e validações
3. create_task com datas calculadas de trás pra frente:
   currentDueDate - duração da fase N = data de início da fase N
4. Se necessário: create_task_comment com contexto
```

### Regra 3: Tags substituem (não adicionam)
```
update_task_tags e update_ticket_tags SUBSTITUEM.
Sempre inclua as tags atuais + as novas.
```

### Regra 4: Comentário após criação
```
Sempre que criar uma task/ticket, adicione um comment
explicando o contexto de origem da criação.
```

### Regra 5: Projeto com cronograma compartilhado
```
1. create_project
2. generate_project_share_link (antes de compartilhar)
3. update_project_shared_customers
4. send_project_email (opcional)
```

## 4. Exemplos de Prompts que Funcionam

```
"Crie uma tarefa no workspace Marketing do tipo 'Post de Redes Sociais'
 chamada 'Briefing campanha verão' com entrega para 30/07,
 responsável pela Ana, e adicione um comentário com o link do briefing."

"Liste meus tickets em aberto no workspace Suporte."

"Avance a tarefa 1234 para a próxima fase do fluxo."

"Crie um projeto chamado 'Campanha Q3' com início em 01/07,
 compartilhe o cronograma com o cliente de ID 88 e envie o link por email."

"Liste os apontamentos de horas dos últimos 7 dias do squad Account."
```

---

**Referência:** [Documentação oficial Ekyte MCP](https://developers.ekyte.com/docs/mcp)
