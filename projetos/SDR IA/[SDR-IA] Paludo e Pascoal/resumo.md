# Paludo & Pascoal Advogados — SDR IA

## Status: 🔧 Setup pendente (nunca foi ao ar)

Projeto de SDR IA completo em arquitetura mas **nunca configurado** no n8n. Nenhuma credencial foi vinculada aos workflows.

## O que existe

- `prompt-sdr-mattheus.txt` — System prompt do agente Matheus (GPT-4o, temp 0.2)
- `prompt-qa-mql.txt` — System prompt do QA/MQL (GPT-4o, temp 0.1)
- `workflow-sdr-principal.n8n.json` — Workflow principal (WhatsApp → SDR → QA → Kommo)
- `workflow-followup.n8n.json` — Workflow de follow-up 4h (Schedule → busca leads → GPT-4o-mini → WhatsApp)
- `Construção do Briefing Paludo.pdf` — Briefing original do cliente
- `GUIA_PROXIMOS_PASSOS.md` — Guia completo de implementação

## Pendências para funcionar

### Credenciais nó a nó

**Workflow Principal — `[Paludo] SDR IA - Matheus`**

| Nó | Credencial |
|---|---|
| WhatsApp Trigger | `whatsAppTriggerApi` → nome `Paludo` |
| Enviar WhatsApp | `whatsAppApi` → nome `Paludo` |
| Buscar Lead no Supabase | `supabaseApi` → Peretto |
| Criar Lead no Supabase | `supabaseApi` → Peretto |
| Salvar Msg Humano | `supabaseApi` → Peretto |
| Buscar Historico | `supabaseApi` → Peretto |
| Salvar Msg IA | `supabaseApi` → Peretto |
| Atualizar Lead | `supabaseApi` → Peretto |
| GPT-4o Matheus | `openAiApi` → OpenAi Peretto |
| GPT-4o QA | `openAiApi` → OpenAi Peretto |
| Empilha Mensagem (Redis) | `redis` → definir instância |
| Obtem Buffer (Redis) | `redis` → mesma |
| Deleta Buffer (Redis) | `redis` → mesma |
| Enviar MQL para Kommo | `kommoApi` → criar (HTTP raw) |
| Enviar Nao-MQL para Kommo | `kommoApi` → mesma |

**Workflow Follow-up — `[Paludo] Gerenciador Follow-up 4h`**

| Nó | Credencial |
|---|---|
| Buscar Todos Leads | `supabaseApi` → Peretto |
| Marcar Follow-up Enviado | `supabaseApi` → Peretto |
| GPT-4o-mini Follow-up | `openAiApi` → OpenAi Peretto |
| Redis Memory Follow-up | `redis` → mesma do principal |

Obs: OpenAI e Supabase já existem no n8n (só selecionar). WhatsApp, Redis e Kommo criam-se.

### Setup infra
- [ ] Rodar SQL: `paludo_leads` + `paludo_chat_history` no Supabase
- [ ] Configurar webhook WhatsApp Cloud API apontando pro n8n
- [ ] Criar pipelines Kommo: "Vendas" (MQL) e "SDR IA" (desqualificados)
- [ ] Criar campos customizados no Kommo: `produto_interesse`, `regime_tributario`, `faturamento_estimado`

## Arquitetura
WhatsApp Cloud API → n8n (SDR GPT-4o → QA GPT-4o → Kommo) + Follow-up automático 4h (GPT-4o-mini)
