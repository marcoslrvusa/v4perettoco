# Retrofit SDR IA: Aplicação do Padrão de Erro

## Situação Atual

7 workflows SDR IA com erro recorrente. Correções aplicadas nos JSONs locais
em 22/06/2026 mas **nunca pushed** para o n8n.

## Prioridade

Cada workflow classificado por criticidade:

| Prioridade | Workflow | Erro | Corrigido (JSON) | Push Pendente |
|-----------|----------|------|-----------------|---------------|
| **P0** | ADPLAN | JS timeout 25min | ✅ Sim | ✅ Sim |
| **P0** | SIGNOR | Task runner disconnect | Server tuning | N/A |
| **P0** | Genics | Redis DNS externo | Server tuning | N/A |
| **P1** | SOFIA | Rate limit Chatwoot | ✅ Sim | ✅ Sim |
| **P1** | PRO ANÁLISES | toDateTime undefined | ✅ Sim | ✅ Sim |
| **P1** | Schwalm | Null constraint telefone | ✅ Sim | ✅ Sim |
| **P1** | V4 INTERNO | 404 Ekyte board ID | ✅ Sim | ✅ Sim |

P0 = Bloqueia operação do workflow
P1 = Degrada experiência mas não bloqueia completamente

## Plano de Execução

### Fase 1: Push das Correções (1 dia)

```bash
# Para cada workflow com correcao pendente:
npx n8nac push "caminho/workflow.json" --verify
```

**Workflows para push:**
1. ADPLAN - `adplan-split-batches.json`
2. SOFIA - `sofia-wait-rate-limit.json`
3. PRO ANÁLISES - `pro-analises-try-catch.json`
4. Schwalm - `schwalm-validacao-telefone.json`
5. V4 INTERNO - `v4-ekyte-fix-board.json`

### Fase 2: Configurar Error Handling (2 dias)

Para CADA workflow SDR IA:

- [ ] Vincular Error Workflow: Settings → Error Workflow → `[CC] Error Handler Central`
- [ ] Adicionar `retryOnFail` nos nos HTTP Request/Supabase/API externa
- [ ] Adicionar `onError: continueErrorOutput` + `main[1]` nos nos falíveis
- [ ] Configurar `saveDataErrorExecution: 'ALL'`
- [ ] Publicar workflow (Shift+P)

### Fase 3: Melhoria Continua (2 dias)

- [ ] Revisar Code nodes: try/catch em acesso a campos opcionais
- [ ] Safe access (`?.`) em expressões de template
- [ ] SplitInBatches em loops que processam > 100 registros
- [ ] Wait nodes entre requests para evitar rate limit

### Fase 4: Validação (1 dia)

- [ ] Rodar cada workflow com lead real
- [ ] Verificar execuções no n8n
- [ ] Confirmar DLQ populando
- [ ] Confirmar notificações Slack chegando
- [ ] Provocar falha (ex: URL inválida) e confirmar error handler dispara

## Rollback Plan

Cada correção tem plano de rollback documentado em `SDR_IA/correcoes-fluxo/`.

Procedimento geral:
1. Desativar nos novos
2. Reconectar rota original
3. Reativar workflow
4. Notificar squad
