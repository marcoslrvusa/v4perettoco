# Deck PDI — Orquestracao Multi-agente com Handoffs e Isolamento

Area: Engenharia de IA

## Slide 1: Resumo Executivo
Padrao de orquestracao multi-agente: supervisor + especialistas com handoff explicit, isolamento de contexto, timeouts e fallbacks. Entrego o padrao e um orquestrador real.
Agente unico vira 'deus' e quebra em prompt longo.
## Slide 2: Contexto de Producao
Um agente fazia tudo: triagem, consulta, proposta.
Prompt gigante -> custo alto.
Sem timeout: sub-agente travado parava o fluxo.
## Slide 3: Diagnostico
SRP ausente entre agentes.
Contexto compartilhado -> vazamento de PII.
Sem handoff formal.
## Slide 4: Decisao Arquitetural (ADR)
ADR-043 — Topologia Multi-agente
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| Supervisor + handoff | foco, testavel | mais nos | ESCOLHIDA |
| Agente unico | simples | fragil | rejeitada |
> Nota: Handoff = mensagem tipada. Cada agente tem contexto proprio e timeout.
## Slide 5: Entregas
MULTI-AGENT.md.
orchestrator.py.
handoff_schema.py.
## Slide 6: Validacao
Simular triagem->consulta->proposta.
Forcar timeout -> fallback.
Contexto nao vaza.
## Slide 7: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Timeout/agente | <= 15 s |
| Handoff com fallback | 100% |
| Vazamento | 0 |
## Slide 8: Riscos
| Risco | Mitigacao |
| --- | --- |
| Loop | max hops |
| Custo supervisor | modelo leve |
## Slide 9: Proximos Passos
Observabilidade de handoff.
Eval por agente.