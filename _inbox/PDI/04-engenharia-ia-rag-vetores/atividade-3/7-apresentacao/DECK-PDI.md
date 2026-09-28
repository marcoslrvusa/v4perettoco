# Deck PDI: Orquestração Multi-agente com Handoffs e Isolamento

Área: Engenharia de IA

## Slide 1: Resumo Executivo
Padrão de orquestração multi-agente: supervisor + especialistas com handoff explicit, isolamento de contexto, timeouts e fallbacks. Entrego o padrão e um orquestrador real.
Agente único vira 'deus' e quebra em prompt longo.
## Slide 2: Contexto de Produção
Um agente fazia tudo: triagem, consulta, proposta.
Prompt gigante -> custo alto.
Sem timeout: sub-agente travado parava o fluxo.
## Slide 3: Diagnóstico
SRP ausente entre agentes.
Contexto compartilhado -> vazamento de PII.
Sem handoff formal.
## Slide 4: Decisão Arquitetural (ADR)
ADR-043: Topologia Multi-agente
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| Supervisor + handoff | foco, testável | mais nos | ESCOLHIDA |
| Agente único | simples | frágil | rejeitada |
> Nota: Handoff = mensagem tipada. Cada agente tem contexto próprio e timeout.
## Slide 5: Entregas
MULTI-AGENT.md.
orchestrator.py.
handoff_schema.py.
## Slide 6: Validação
Simular triagem->consulta->proposta.
Forcar timeout -> fallback.
Contexto não vaza.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Timeout/agente | <= 15 s |
| Handoff com fallback | 100% |
| Vazamento | 0 |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Loop | max hops |
| Custo supervisor | modelo leve |
## Slide 9: Próximos Passos
Observabilidade de handoff.
Eval por agente.