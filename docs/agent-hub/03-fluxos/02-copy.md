# Fluxo Copy — Conteúdo com Ekyte no Centro

**Propósito:** Mostrar como o squad Copy usa o Ekyte como centro durante o ciclo de produção de conteúdo — do briefing à aprovação.

---

## 1. Macro Fluxo

```
BRIEFING                          PRODUÇÃO                    APROVAÇÃO
   │                                │                            │
   ▼                                ▼                            ▼
Account cria task no         Copy lê task no              Copy publica link
Ekyte: "Produzir LP         Ekyte com briefing           no Ekyte + Drive
Campanha Verão"              pendente                      │
   │                                │                            │
   ▼                                ▼                            ▼
Task no Ekyte:              Agente @copy-content:        Account revisa:
- Tipo: "LP"                → Lê briefing do Drive       → Comenta na task
- Fase: "briefing"          → Gera rascunho              → Avança fase
- Responsável: copy        → Salva no Drive             → "aprovado"
- Prazo: calculado          → Atualiza task no Ekyte     → Fase = "concluido"
  de trás pra frente         → Comenta: "rascunho pronto"   │
   │                                │                            │
   ▼                                ▼                            ▼
                         Ciclo de revisão:                n8n dispara:
                         copy → account → copy →          → Notifica Slack
                         até aprovação                    → Atualiza kanban
```

## 2. Passo a Passo com o Agente

### Briefing Chegou

```
Usuário: "@copy-content, peguei a task #5678 de LP da
         Campanha Verão. Me ajuda a produzir."

Agente:
1. Ekyte → get_detailed_task(taskId: 5678)
           → lê título, descrição, fase, responsável, prazo
2. Drive → search_files("campanha-verao-briefing")
           → read_file_content → briefing completo
3. Drive → search_files("campanha-verao-links")
           → read_file_content → links de referência
4. Drive → search_files("cliente-X-mission-control")
           → read_file_content → tom de voz, personas
5. Gera rascunho da LP
6. Drive → create_file(
     name: "lp-campanha-verao-rascunho-v1.md",
     content: rascunho,
     parentFolder: pasta da campanha
   )
7. Ekyte → create_task_comment(
     taskId: 5678,
     text: "Rascunho v1 gerado. Link: [Drive URL]"
   )
8. Ekyte → update_task_phase(taskId: 5678, phase: "revisao")
9. Retorna: "Rascunho v1 salvo no Drive e task avançada para revisão."
```

### Ciclo de Revisão

```
Usuário: "@copy-content, pediram alterações na LP. Segue o
         feedback: [colar feedback]. Atualiza."

Agente:
1. Ekyte → get_detailed_task(5678) → task ainda em "revisao"
2. Drive → search_files("lp-campanha-verao-rascunho-v1")
           → lê rascunho atual
3. Aplica alterações solicitadas
4. Drive → create_file(
     name: "lp-campanha-verao-rascunho-v2.md",
     content: rascunho atualizado
   )
5. Ekyte → create_task_comment(
     taskId: 5678,
     text: "Alterações aplicadas na v2. Link: [Drive URL]"
   )
6. Se for a última revisão:
   Ekyte → update_task_phase(taskId: 5678, phase: "aprovado")
7. Ekyte → update_task(taskId: 5678, { status: "concluida" })
```

## 3. Agentes Envolvidos

| Agente | Papel | Modelo |
|---|---|---|
| **@content-studio** | Orquestra produção de conteúdo, coordena pesquisa, copy e design | `deepseek-v4-flash-free` |
| **@copy-content** | Escreve LPs, emails, anúncios, redes sociais | `gpt-4o-mini` |
| **@pipeline-conteudo** | Calendário editorial, blog, email marketing, fluxo de aprovação | `gemini-2.5-flash-free` |
| **@pesquisador** | Pesquisa profunda de cliente/mercado (acionado por account antes) | `deepseek-v4-flash-free` |
| **@criacao-design** | Cria visuais, imagens, vídeos para acompanhar o conteúdo | `claude-sonnet-4` |

## 4. Tabela de Tools Ekyte Usadas pelo Copy

| Momento | Tool Ekyte | Para Quê |
|---|---|---|
| Iniciar produção | `get_detailed_task` | Ler briefing da task |
| Iniciar produção | `list_task_types_create_task` | Verificar tipo correto |
| Entregar rascunho | `create_task_comment` | Avisar que rascunho está pronto |
| Entregar rascunho | `update_task_phase` | Avançar para revisão |
| Ciclo de revisão | `get_detailed_task` | Verificar feedback e fase atual |
| Ciclo de revisão | `list_task_comments` | Ler histórico de revisões |
| Finalizar | `update_task_phase` | Avançar para aprovado |
| Finalizar | `update_task` | Marcar como concluída |
| Finalizar | `create_task_comment` | Link final do artefato |
| Emergência | `create_ticket` | Reportar bloqueio |

## 5. Exemplo Prompt Completo

```
"Task #5678 — Produzir LP Campanha Verão

Briefing no Drive: /Clientes/ClienteX/Campanhas/verao/briefing.md
Links: /Clientes/ClienteX/Campanhas/verao/links.md
Tom de voz: /Clientes/ClienteX/mission-control.md

Prazos:
- Rascunho v1: 25/06
- Revisão account: 27/06
- Final: 30/06

Gera a LP seguindo o briefing e salva no Drive.
Task está na fase 'briefing' — avance para 'revisão' após entregar.
```

---

**Documentos relacionados:**
- [02-componentes/04-ekyte-mcp.md](../02-componentes/04-ekyte-mcp.md) — Tools do Ekyte
- [02-componentes/03-google-drive-mcp.md](../02-componentes/03-google-drive-mcp.md) — Drive como KB
- [01-fundacional/01-ekyte-coracao.md](../01-fundacional/01-ekyte-coracao.md) — Ekyte como centro
