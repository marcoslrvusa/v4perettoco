---
name: geral-agente-autonomo
description: >
  Sistema autônomo de fila de demandas para a Agent Orchestra V4 com learning
  loop. Gerencia o ciclo completo: flags (detector_flags.py) ou comando manual
  → fila Supabase → classificação c/ memórias similares → delegação →
  aprendizado registrado. Opera em 3 modos (manual/semi/autonomo). n8n é
  opcional — funciona com cron do sistema.
area: geral
author: Marcos Luciano Rodrigues Vieira
version: 1.1.0
aliases:
  - agente-autonomo
  - fila-demandas
  - queue-system
  - orquestrador-autonomo
tags:
  - orchestra
  - agent-queue
  - automation
  - supabase
  - learning-loop
  - autonomous
---

# Sistema Autônomo de Agentes (geral-agente-autonomo)

## O que é

Um sistema de fila de demandas que torna a Agent Orchestra V4 autônoma. Em vez
de você precisar chamar `@growth-team` manualmente, o sistema:

1. Recebe demandas de flags (`detector_flags.py`), cron ou comando manual
2. Enfileira no Supabase (`agent_queue`) com prioridade e função
3. **Busca memórias similares** no pgvector antes de classificar (learning loop)
4. Classifica qual orquestrador e especialistas acionar
5. Escreve brief enriquecido com memórias anteriores
6. **Registra aprendizado** no pgvector após cada execução
7. Alimenta dashboard de performance

## Arquitetura

```
detector_flags.py ──┐
cron (15min) ───────┼──→ Supabase agent_queue ──→ agent-orchestrator.py
comando manual ─────┘         │                       │
n8n (opcional) ───────────────┘                       │
                          ┌───────────────────────────┘
                          ▼
                   search.py (pgvector)
                          │
                          ▼
                   classify_demand()
                          │
                          ▼
                   write_brief() → /workspace/input/
                          │
                          ▼
                   record.py (pgvector) ← aprendizado
                          │
                          ▼
                   update_routing_stats()
```

## Setup Inicial

### 1. Schema Supabase

Execute no SQL Editor do Supabase:

```sql
-- .agents/skills/geral-agente-autonomo/scripts/setup/supabase-schema.sql
```

Cria: `agent_queue`, `agent_queue_log`, `agent_routing_stats`, funções `dequeue_next()`, `enqueue_demand()`, `update_routing_stats()`.

### 2. Variáveis de Ambiente

```bash
export SUPABASE_URL=https://bkenzsvexfayjcrqnmpx.supabase.co
export SUPABASE_SERVICE_KEY=<service_role_key>
export OPENAI_API_KEY=<key>  # necessário para embeddings do learning loop
```

### 3. Copiar CLI

```bash
cp .agents/skills/geral-agente-autonomo/scripts/agent-orchestrator.py /workspace/
chmod +x /workspace/agent-orchestrator.py
```

### 4. Cron (substitui scheduler do n8n)

```bash
cp .agents/skills/geral-agente-autonomo/scripts/cron-wrapper.sh /usr/local/bin/agent-orchestra-cron
chmod +x /usr/local/bin/agent-orchestra-cron

cat > /etc/cron.d/agent-orchestra << 'EOF'
*/15 * * * * root /usr/local/bin/agent-orchestra-cron >> /var/log/agent-orchestra.log 2>&1
EOF
systemctl restart cron
```

### 5. Conectar flags existentes

O `detector_flags.py` em `csm-hub/automacoes/` já está modificado para chamar
`flag-hook.py` automaticamente quando detectar flags. Verificar se o caminho
está correto:

```python
# Em detector_flags.py — o hook é chamado para cada flag detectada
python3 flag-hook.py --flag roi --urgencia Critica --dado "ROAS 1.2" --cliente "Cliente X"
```

### 6. Dashboard (opcional)

Servir `dashboard/index.html` com nginx/Caddy. Substituir `{{SUPABASE_URL}}` e
`{{SUPABASE_SERVICE_KEY}}` no HTML antes de servir.

## Uso

### CLI

```bash
# Ver fila pendente
python3 agent-orchestrator.py queue

# Processar próximo (ciclo completo c/ learning loop)
python3 agent-orchestrator.py process

# Classificar demanda específica
python3 agent-orchestrator.py classify --id <uuid>

# Enfileirar nova demanda
python3 agent-orchestrator.py enqueue \
  --function copy --urgency alta --priority 80 \
  --briefing '{"task":"Landing page novo produto","copy_type":"copy_landing"}'

# Saúde do sistema
python3 agent-orchestrator.py status

# Relatório de performance
python3 agent-orchestrator.py report
```

### n8n (opcional)

Workflows JSON exportados em `workflows/agent-orchestrator-*.json`.
Importar manualmente pelo UI do n8n.

## Learning Loop

O ciclo completo do `process`:

```
1. dequeue_next()         → pega próximo item da fila
2. search.py              → busca memórias similares no pgvector
3. classify_demand()      → orquestrador + especialistas + modo
4. write_brief()          → brief enriquecido com memórias
5. [execução do agente]   → OpenCode processa
6. record.py              → registra aprendizado no pgvector
7. update_routing_stats() → performance metrics
8. update_queue_item()    → marca como completed
```

## Arquivos do Sistema

| Arquivo | Função |
|---------|--------|
| `scripts/setup/supabase-schema.sql` | Schema + funções da fila |
| `scripts/agent-orchestrator.py` | CLI de orquestração c/ learning loop |
| `scripts/flag-hook.py` | Conecta flags detector → agent_queue |
| `scripts/cron-wrapper.sh` | Cron替代 do scheduler (lock p/ evitar concorrência) |
| `workflows/agent-orchestrator-scheduler.json` | n8n scheduler (opcional) |
| `workflows/agent-orchestrator-webhook.json` | n8n webhook (opcional) |
| `workflows/agent-orchestrator-processor.json` | n8n processor (opcional) |
| `dashboard/index.html` | Dashboard de performance |
| `PLAN.md` | Plano de deploy completo |
