# Fluxo Account — Check-in com Ekyte no Centro

**Propósito:** Mostrar como o Account usa o Ekyte como centro de tudo durante o ciclo de check-in com cliente.

---

## 1. Macro Fluxo

```
PRÉ-CALL                     CALL                      PÓS-CALL
   │                          │                          │
   ▼                          ▼                          ▼
Ler pauta no    ─────►   Rodar call    ─────►   Processar transcript
Drive + Ekyte            com cliente            no OpenCode
   │                          │                          │
   ▼                                                     ▼
Tasks do                    Drive MCP              OpenCode lê transcript
check-in                    lê pauta               Extrai combinados
                                                      │
                                                      ▼
                                                  Ekyte MCP cria:
                                                  ├── Tarefas dos combinados
                                                  ├── Comentários com contexto
                                                  ├── Atualiza projeto do cliente
                                                  └── Ticket se tiver flag
```

## 2. Passo a Passo com o Agente

### Pré-Call: @account-checkin-roleplay

```
Usuário: "@account-checkin-roleplay, vou ter check-in com
         o cliente X amanhã. Me prepara."

Agente:
1. Ekyte → list_tasks(filtro: "cliente X", status: aberto)
           → tasks pendentes do cliente
2. Drive → search_files("pauta check-in cliente X")
          → read_file_content → pauta anterior
3. Ekyte → list_tickets(filtro: "cliente X", status: aberto)
           → flags e pendências
4. Drive → search_files("mission-control cliente X")
          → situação atual do cliente
5. Gera resumo: pauta, tasks pendentes, tickets abertos,
   histórico de check-ins, perguntas sugeridas
```

### Pós-Call: @account-checkin-review

```
Usuário: "@account-checkin-review, processa o transcript
         da call que acabei com o cliente X"

Agente:
1. Lê o transcript (texto colado pelo usuário)
2. Extrai combinados, prazos, responsáveis, flags
3. Para cada combinado:
   → Ekyte → create_task(
       workspace: "Account",
       title: combinado,
       currentDueDate: prazo,
       responsibleUserId: responsável
     )
   → Ekyte → create_task_comment(
       taskId: task.id,
       text: "Combinado na call de 20/06 com cliente X"
     )
4. Se detectou flag (insatisfação, risco):
   → Ekyte → create_ticket(
       subject: "Flag detectada - cliente X",
       description: "...",
       priority: "alta"
     )
5. Drive → create_file(
     name: "checkin-2026-06-20-cliente-x.md",
     content: resumo da call + combinados
   )
6. Retorna:
   "3 tarefas criadas no Ekyte. 1 ticket de flag aberto.
    Resumo salvo no Drive. Links: ..."
```

## 3. Tabela de Tools Ekyte Usadas pelo Account

| Momento | Tool Ekyte | Para Quê |
|---|---|---|
| Pré-call | `list_tasks` | Tasks pendentes do cliente |
| Pré-call | `list_tickets` | Flags e pendências |
| Pré-call | `list_task_comments` | Histórico de decisões |
| Pós-call | `create_task` | Cada combinado vira tarefa |
| Pós-call | `create_task_comment` | Contexto do combinado |
| Pós-call | `update_task_phase` | Avançar tarefa existente |
| Pós-call | `create_ticket` | Flag de risco |
| Pós-call | `list_squads` | Confirmar squads envolvidos |
| Pós-call | `list_project_tasks` | Tasks vinculadas ao projeto |

## 4. Exemplo Prompt

```
"Acabei a call com o cliente X. Segue o transcript:
[COLAR TRANSCRIPT]
Processa e cria as tarefas no Ekyte.

Combinados identificados:
1. Entregar relatório Q2 até 30/06 — responsável: João
2. Reunião de alinhamento com equipe até 25/06 — responsável: Maria
3. Correção no layout da campanha até 28/06 — responsável: Ana
```

---

**Documentos relacionados:**
- [02-componentes/04-ekyte-mcp.md](../02-componentes/04-ekyte-mcp.md) — Tools do Ekyte
- [01-fundacional/01-ekyte-coracao.md](../01-fundacional/01-ekyte-coracao.md) — Ekyte como centro
