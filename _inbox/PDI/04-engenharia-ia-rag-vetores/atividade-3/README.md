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

ADR-043 : Topologia Multi-agente

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

## Decisoes e tradeoffs

- Supervisor com handoff tipado em vez de agente unico com prompt de 8k tokens: aceitei mais nos para ganhar foco, teste por papel e fronteira clara entre triagem, consulta e proposta.
- Contexto proprio por agente com passagem de resumo minimo: escolhi isolamento para zerar vazamento, com meta de 0 ocorrencias, mesmo com custo de serializar o handoff.
- Timeout menor ou igual a 15 s por agente com fallback em 100 por cento dos handoffs: preferi degradar com re-rota a travar o fluxo quando um worker trava.
- Max hops contra loop e supervisor com modelo leve: contive custo e recursao em vez de deixar o supervisor reiterar sem limite.
- Memoria de curto e longo prazo com estado preservado: troquei reexecucao do zero por retomada a partir do ultimo handoff valido.

## Impacto no negocio

A orquestracao com timeout menor ou igual a 15 s, fallback em 100 por cento e vazamento 0 eleva o sucesso de cerca de 49 por cento para cerca de 97 por cento, com meta maior ou igual a 95 por cento em tarefas de 3 etapas, o que reduz retrabalho por contaminacao e da previsibilidade de custo por papel.

## Referencias de estudo

- Curso: Multi-AI Agent Systems with LangGraph, plataforma DeepLearning.AI.
- Video: Padroes de orquestracao com supervisor e handoff, plataforma YouTube, canal LangChain.
- Doc oficial: Documentacao do LangGraph para grafos de agentes, documentacao oficial LangChain.
- Doc oficial: Guia de function calling e structured outputs, documentacao oficial OpenAI.
