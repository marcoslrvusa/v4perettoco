# Fluxo Coordenação — Comitê com Ekyte no Centro

**Propósito:** Mostrar como o Comitê de P&EG usa o Ekyte como fonte única de dados para o briefing semanal.

---

## 1. Macro Fluxo

```
DOMINGO 20H (n8n)         SEGUNDA 9H              DURANTE A SEMANA
     │                        │                        │
     ▼                        ▼                        ▼
n8n dispara:             Coordenador abre       Coordenação
→ Puxa tasks do Ekyte   OpenCode e roda:       acompanha tasks
  por squad              @executor-comite       no Ekyte
→ Puxa OKRs do Drive      "Gera briefing"
→ Salva consolidação     ──────────────────►   Ekyte = fonte única
  no Drive               Agente lê dados         de verdade
                          do Drive, chama        ─────────────
TOOLs EKYTE USADAS:       @analista-dados        list_tasks
  list_tasks              para cliente,          list_tickets
  list_tickets            @revisor valida,       get_detailed_task
  list_time_trackings     consolida em           list_project_tasks
  list_projects           markdown + HTML
                          Salva no Drive
                          Envia por email
```

## 2. Briefing do Comitê com Ekyte

```
Workflow n8n (cron: domingo 20h):

1. Para cada squad ativo:
   a. Ekyte → list_tasks(
        workspaceId: squad.X,
        status: ["em_andamento", "atrasada"],
        limit: 200
      )
   b. Ekyte → list_tickets(
        workspaceId: squad.X,
        status: ["aberto", "em_atendimento"],
        limit: 200
      )
   c. Ekyte → list_time_trackings(
        period: "last_30_days",
        squadId: squad.X
      )
   d. Ekyte → list_projects(
        squadId: squad.X,
        status: "ativo"
      )

2. Consolida em JSON e salva no Drive

3. Coordenador roda:
   @executor-comite "Gera briefing do comitê com dados do Drive"

4. Agente:
   → Lê dados consolidados do Drive
   → Para cada cliente:
       → Convoca @analista-dados
       → Analisa performance, tasks atrasadas, tickets abertos
       → Gera recomendação
   → @revisor valida cada análise
   → Consolida em briefing markdown + HTML
   → Salva no Drive
   → Envia por email (via n8n)
```

## 3. Indicadores no Ekyte para o Comitê

| Indicador | Onde no Ekyte | Tool |
|---|---|---|
| Tasks criadas na semana | Tarefas por período | `list_tasks` com filtro de data |
| Tasks atrasadas | Tarefas com dueDate vencido | `list_tasks` com filtro overdue |
| Taxa de conclusão | Tasks fechadas / total | `list_tasks` + cálculo |
| Tickets abertos | Tickets não resolvidos | `list_tickets` com filtro |
| Horas apontadas | Time tracking por squad | `list_time_trackings` |
| Projetos em andamento | Projetos ativos | `list_projects` |
| Tasks por fase | Distribuição no workflow | `list_tasks` + `list_task_flow_phases` |

## 4. Exemplo de Prompt para o Comitê

```
"Gera o briefing do comitê desta semana.

Dados consolidados estão em:
  /drive/comite/2026-06-22-dados-consolidados.json

Estrutura:
1. Overview geral (tasks criadas, concluídas, atrasadas)
2. Por squad (Account, GT, Copy, Design, CSM)
   - Tasks atrasadas com responsável
   - Tickets abertos há mais de 7 dias
   - Projetos em risco
3. Destaques positivos da semana
4. Alertas e recomendações
5. Anexar HTML formatado para apresentação
```

---

**Documentos relacionados:**
- [02-componentes/04-ekyte-mcp.md](../02-componentes/04-ekyte-mcp.md)
- [02-componentes/05-n8n.md](../02-componentes/05-n8n.md)
