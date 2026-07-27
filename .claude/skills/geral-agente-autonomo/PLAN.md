# Plano de Deploy — Sistema Autônomo de Agentes v1.1

## Inventário Completo

```
.agents/skills/geral-agente-autonomo/
├── SKILL.md                                    → Documentação
├── PLAN.md                                     → Este documento
├── scripts/
│   ├── setup/supabase-schema.sql               → Schema + RPCs da fila
│   ├── agent-orchestrator.py                   → CLI c/ learning loop
│   ├── flag-hook.py                            → Ponte flags → fila
│   └── cron-wrapper.sh                         → Cron lock p/ 15min
├── workflows/
│   ├── agent-orchestrator-scheduler.json       → n8n scheduler (opcional)
│   ├── agent-orchestrator-webhook.json         → n8n webhook (opcional)
│   └── agent-orchestrator-processor.json       → n8n processor (opcional)
└── dashboard/
    └── index.html                              → Painel de performance
```

## Pré-requisitos

| Recurso | Status | Como verificar |
|---------|--------|----------------|
| Supabase `agent_queue` | ✅ Feito | `curl -s "$SUPABASE_URL/rest/v1/agent_queue?limit=1" -H "apikey: $KEY" -H "Authorization: Bearer $KEY"` → `[]` |
| Python 3 | ✅ | `python3 --version` |
| OPENAI_API_KEY | ⚠️ Pendente | Necessário para embeddings do learning loop |
| SUPABASE_URL/KEY | ⚠️ Pendente | Configurar no servidor |
| git push | ⚠️ Pendente | Commit + push para origin |

## Passo a Passo

### Fase 1 — Variáveis de Ambiente

Adicionar no `/etc/environment` (servidor) e nos containers Dokploy:

```bash
SUPABASE_URL=https://bkenzsvexfayjcrqnmpx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
OPENAI_API_KEY=<sk-...>
```

### Fase 2 — Copiar CLI

```bash
mkdir -p /workspace/input /workspace/output
cp .agents/skills/geral-agente-autonomo/scripts/agent-orchestrator.py /workspace/
chmod +x /workspace/agent-orchestrator.py
```

### Fase 3 — Cron

```bash
cp .agents/skills/geral-agente-autonomo/scripts/cron-wrapper.sh /usr/local/bin/agent-orchestra-cron
chmod +x /usr/local/bin/agent-orchestra-cron

cat > /etc/cron.d/agent-orchestra << 'EOF'
*/15 * * * * root /usr/local/bin/agent-orchestra-cron >> /var/log/agent-orchestra.log 2>&1
EOF
systemctl restart cron
```

### Fase 4 — Verificar flag hook

O `detector_flags.py` em `csm-hub/automacoes/` já chama `flag-hook.py`
automaticamente quando executa. Confirmar que o caminho relativo está correto:

```python
# Linha adicionada: após detectar cada flag, chama:
python3 flag-hook.py --flag tipo --urgencia X --dado Y --cliente Z
```

### Fase 5 — Dashboard (opcional)

Substituir `{{SUPABASE_URL}}` e `{{SUPABASE_SERVICE_KEY}}` no HTML e servir
com nginx.

### Fase 6 — n8n (opcional)

Importar os JSONs no n8n UI (Settings → Import).

### Fase 7 — Teste de Fumaça

```bash
# 1. Enfileirar demanda de teste
python3 /workspace/agent-orchestrator.py enqueue \
  --function copy --urgency normal --priority 30 \
  --briefing '{"task":"Teste do sistema","copy_type":"copy_geral"}'

# 2. Verificar fila
python3 /workspace/agent-orchestrator.py queue

# 3. Processar (ciclo completo c/ learning loop)
python3 /workspace/agent-orchestrator.py process

# 4. Verificar saúde
python3 /workspace/agent-orchestrator.py status
```

## Diagrama do Ciclo Completo

```
detector_flags.py ──→ flag-hook.py ──→ INSERT agent_queue (pending)

cron (15min) ───────→ cron-wrapper.sh ──→ agent-orchestrator.py process

process:
  1. dequeue_next()         → SELECT ... FOR UPDATE SKIP LOCKED
  2. search.py              → busca memórias similares (pgvector)
  3. classify_demand()      → orquestrador + especialistas + modo
  4. write_brief()          → /workspace/input/{timestamp}_{id}.json
  5. record.py              → registra aprendizado (pgvector)
  6. update_routing_stats() → INSERT ... ON CONFLICT DO UPDATE
  7. update_queue_item()    → SET status = completed
```

## Rollback

| Componente | Reverter |
|------------|----------|
| Schema Supabase | `DROP TABLE agent_queue CASCADE; DROP TABLE agent_queue_log; DROP TABLE agent_routing_stats;` |
| CLI | `rm /workspace/agent-orchestrator.py` |
| Cron | `rm /etc/cron.d/agent-orchestra && systemctl restart cron` |
| flag-hook | Remover as 4 linhas adicionadas em `detector_flags.py` |
| n8n | Desativar workflows importados |

## Checklist de Deploy

- [ ] Variáveis de ambiente configuradas (SUPABASE_URL, SERVICE_KEY, OPENAI_API_KEY)
- [ ] `agent-orchestrator.py` copiado para `/workspace/`
- [ ] Cron instalado e rodando
- [ ] `detector_flags.py` com hook ativo
- [ ] Teste de fumaça: enqueue → queue → process → status
- [ ] Dashboard servido (se aplicável)
- [ ] Git commit + push
