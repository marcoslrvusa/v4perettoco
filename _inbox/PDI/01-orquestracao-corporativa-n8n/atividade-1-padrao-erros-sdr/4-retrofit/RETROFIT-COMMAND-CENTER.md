# Retrofit Command Center: Workflows de Infraestrutura

## Situação Atual

3 workflows do Command Center operam SEM tratamento de erro algum.

| Workflow | Trigger | Função | Risco |
|----------|---------|--------|-------|
| `[CC] Collector` | Schedule 2min | Sincroniza workflows com Supabase | Falha silencia → dashboard desatualizado |
| `[CC] Heartbeat` | Schedule 5min | Saúde da instância n8n | Falha silencia → falso positivo de saúde |
| `[CC] Metrics` | Schedule 1h | Snapshot de métricas | Falha silencia → lacuna histórica |

## O que Implementar

### Em cada workflow

- [ ] `retryOnFail: true, maxTries: 3, waitBetweenTries: 5000` no HTTP Request
- [ ] `onError: "continueErrorOutput"` + `main[1]` conectado
- [ ] Error Workflow vinculado → `[CC] Error Handler Central`

### No Collector (crítico)

O Collector faz GET `/api/v1/workflows` e UPSERT no Supabase. Se falha,
o dashboard fica desatualizado por até 2 minutos (próximo ciclo).

Adicional:
- [ ] Log de última sync bem-sucedida no `error_dlq` (status = sucesso)
- [ ] Alerta se 3 ciclos consecutivos falharem (circuit breaker)

### No Heartbeat

Se o Heartbeat falha, podemos achar que a instância caiu quando foi
só o workflow que quebrou.

Adicional:
- [ ] Diferenciar: falha do workflow vs falha da instância
- [ ] Se workflow falha 3x seguidas: alertar squad

## Prioridade

| Workflow | Prioridade | Esforço | Impacto |
|----------|-----------|---------|---------|
| Collector | P1 | 30min | Médio (dashboard desatualizado) |
| Heartbeat | P2 | 20min | Baixo (falso positivo) |
| Metrics | P2 | 20min | Baixo (lacuna histórica) |
