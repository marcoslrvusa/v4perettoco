# Orquestração Multi-agente com Handoffs e Isolamento

Engenharia de IA

## Resumo Executivo

Padrão de orquestração multi-agente: supervisor + especialistas com handoff explicit, isolamento de contexto, timeouts e fallbacks. Entrego o padrão e um orquestrador real.

Agente único vira 'deus' e quebra em prompt longo.

## Contexto de Produção

- Um agente fazia tudo: triagem, consulta, proposta.

- Prompt gigante -> custo alto.

- Sem timeout: sub-agente travado parava o fluxo.

## Diagnóstico

- SRP ausente entre agentes.

- Contexto compartilhado -> vazamento de PII.

- Sem handoff formal.

## Decisão Arquitetural (ADR)

ADR-043 : Topologia Multi-agente

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Supervisor + handoff | foco, testável | mais nos | ESCOLHIDA |

| Agente único | simples | frágil | rejeitada |

> **Nota:** Handoff = mensagem tipada. Cada agente tem contexto próprio e timeout.

## Entregas

- MULTI-AGENT.md.

- orchestrator.py.

- handoff_schema.py.

## Validação

1. Simular triagem->consulta->proposta.

2. Forcar timeout -> fallback.

3. Contexto não vaza.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Timeout/agente | <= 15 s |

| Handoff com fallback | 100% |

| Vazamento | 0 |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Loop | max hops |

| Custo supervisor | modelo leve |

## Próximos Passos

- Observabilidade de handoff.

- Eval por agente.

## Decisões e tradeoffs

- Supervisor com handoff tipado em vez de agente único com prompt de 8k tokens: aceitei mais nos para ganhar foco, teste por papel e fronteira clara entre triagem, consulta e proposta.
- Contexto próprio por agente com passagem de resumo mínimo: escolhi isolamento para zerar vazamento, com meta de 0 ocorrências, mesmo com custo de serializar o handoff.
- Timeout menor ou igual a 15 s por agente com fallback em 100 por cento dos handoffs: preferi degradar com re-rota a travar o fluxo quando um worker trava.
- Max hops contra loop e supervisor com modelo leve: contive custo e recursão em vez de deixar o supervisor reiterar sem limite.
- Memória de curto e longo prazo com estado preservado: troquei reexecução do zero por retomada a partir do último handoff valido.

## Impacto no negócio

A orquestração com timeout menor ou igual a 15 s, fallback em 100 por cento e vazamento 0 eleva o sucesso de cerca de 49 por cento para cerca de 97 por cento, com meta maior ou igual a 95 por cento em tarefas de 3 etapas, o que reduz retrabalho por contaminação e da previsibilidade de custo por papel.

## Referências de estudo

- Curso: Multi-AI Agent Systems with LangGraph, plataforma DeepLearning.AI.
- Vídeo: Padrões de orquestração com supervisor e handoff, plataforma YouTube, canal LangChain.
- Doc oficial: Documentação do LangGraph para grafos de agentes, documentação oficial LangChain.
- Doc oficial: Guia de function calling e structured outputs, documentação oficial OpenAI.
