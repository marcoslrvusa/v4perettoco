# Análise: n8n vigiando Supabase para "demandas novas"

## Contexto da task proposta

> "N8n vigiando o Supabase no ciclo definido (10–30min) e pegando as demandas novas desde a última passada."

## Não faz sentido — 3 razões estruturais

### 1. Hub de agentes é chat-driven, não queue-driven

Os agentes do hub vivem dentro do OpenCode/Claude Code (`.opencode/agents/`, `.agents/skills/`). São invocados por menção explícita:

```
@cmoorch
@account-orchestrator
@content-studio
@launch-pad
```

- **Não existe** API ou hook para o n8n disparar um agente OpenCode
- O AI Maestro Messaging existente é intra-runtime (agente ↔ agente), não para trigger externo
- Um `SELECT * FROM demandas WHERE processada = false` não tem consumidor do lado dos agentes

### 2. Polling circular quando produtor e consumidor são o mesmo sistema

A proposta cria um ciclo: n8n escreve "demanda" no Supabase → n8n lê "demanda" do Supabase. Se o n8n é quem produz e quem consome, a demanda deveria ser processada inline — não tem ganho em serializar via banco e religar com polling.

| Cenário | Solução correta |
|---|---|
| Produtor = Consumidor (n8n → Supabase → n8n) | Processamento direto, sem banco intermediário |
| Produtor ≠ Consumidor (ex: webhook serverless → Supabase → n8n) | Supabase Realtime + Webhook node (evento, não polling) |

Em ambos os casos, polling de 10-30min adiciona latência e complexidade sem benefício. Se for o mesmo sistema, é desvio desnecessário. Se forem sistemas diferentes, webhook ou trigger de banco entrega em segundos sem custo de query cíclica.

### 3. O padrão existente é n8n → Supabase (escrita), não n8n ← Supabase (leitura cíclica)

Os [CC] workflows escrevem **do** n8n **para** o Supabase (workflow state, heartbeat, métricas). O Supabase serve como **storage de observabilidade**, não como **fila de demandas**.

As fontes reais de "demanda" (leads no Kommo, tasks no Ekyte, mensagens no Chatwoot) o n8n já acessa **diretamente** — sem precisar de uma tabela intermediária.

## O que faria sentido em vez disso

| Se a necessidade real é... | O caminho certo |
|---|---|
| n8n processar leads/mensagens que estão no Supabase | **Supabase Realtime + Webhook node** (pubsub, não polling — entrega em segundos) |
| Processar dados de fontes que n8n já acessa (Kommo, Ekyte, Chatwoot) | **Polling direto na fonte** ou webhook da fonte. Supabase como intermediário não agrega |
| Acionar programaticamente um agente OpenCode via n8n | **Script bridge CLI** (`executeCommand` node → `opencode "prompt"`). Frágil (sessão headless, sem garantia de conclusão) — mas é o único caminho hoje. Recomendado apenas para provas de conceito |

## Conclusão

**Recusar a task como está.** O problema que ela tenta resolver não existe na arquitetura atual — ou já é resolvido por triggers diretos. Redirecionar para uma conversa de discovery do que realmente está sem solução no fluxo atual.