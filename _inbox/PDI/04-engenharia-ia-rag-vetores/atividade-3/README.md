# Orquestracao Multi-agente com Handoffs e Isolamento

Engenharia de IA

## Resumo Executivo

Padrao de orquestracao multi-agente: supervisor + especialistas com handoff explicit, isolamento de contexto, timeouts e fallbacks. Entrego o padrao e um orquestrador real.

Agente unico vira 'deus' e quebra em prompt longo.

## Contexto de Producao

- Um agente fazia tudo: triagem, consulta, proposta.

- Prompt gigante -> custo alto.

- Sem timeout: sub-agente travado parava o fluxo.

## Diagnostico

- SRP ausente entre agentes.

- Contexto compartilhado -> vazamento de PII.

- Sem handoff formal.

## Decisao Arquitetural (ADR)

ADR-043 — Topologia Multi-agente

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Supervisor + handoff | foco, testavel | mais nos | ESCOLHIDA |

| Agente unico | simples | fragil | rejeitada |

> **Nota:** Handoff = mensagem tipada. Cada agente tem contexto proprio e timeout.

## Entregas

- MULTI-AGENT.md.

- orchestrator.py.

- handoff_schema.py.

## Validacao

1. Simular triagem->consulta->proposta.

2. Forcar timeout -> fallback.

3. Contexto nao vaza.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Timeout/agente | <= 15 s |

| Handoff com fallback | 100% |

| Vazamento | 0 |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Loop | max hops |

| Custo supervisor | modelo leve |

## Proximos Passos

- Observabilidade de handoff.

- Eval por agente.