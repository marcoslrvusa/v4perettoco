# Engenharia de Custos de LLM (custo por tarefa, cache, roteamento)

Engenharia de IA

## Resumo Executivo

Framework de custo de LLM: custo por tarefa, cache de prompt, roteamento por complexidade e budget. Entrego o padrao e um calculador.

Sem contabilidade de tokens, nao se precifica o agente.

## Contexto de Producao

- Modelo 'maxi' para tudo (10x custo).

- Sem cache -> mesma pergunta paga 2x.

- Impossivel precificar ao cliente.

## Diagnostico

| Hoje | Alvo |

| --- | --- |

| modelo unico | roteamento |

| sem cache | cache |

| custo invisivel | custo/tarefa |

## Decisao Arquitetural (ADR)

ADR-044 : Estrategia de Custo

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Roteamento + cache + budget | previsivel | governanca | ESCOLHIDA |

> **Nota:** Trivial -> leve; complexo -> forte; repetido -> cache.

## Entregas

- LLM-COST.md.

- cost_calc.py.

- BUDGET.md.

## Validacao

1. Medir custo/tarefa com e sem roteamento.

2. Habilitar cache; medir hit rate.

3. Budget por cliente + alerta 80%.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Custo/tarefa | <= baseline*0.4 |

| Cache hit | >= 30% |

| Budget | alerta 80% |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Qualidade cai | eval + roteamento |

| Cache PII | nao cachear |

## Proximos Passos

- Precificar por tarefa.

- Dashboard de custo.

## Decisoes e tradeoffs

- Roteamento por complexidade em vez de modelo maxi para tudo: troquei simplicidade por governanca, porque o maxi custa 10x e a regra trivial vai para leve e complexo vai para forte.
- Cache semantico com meta de hit maior ou igual a 30 por cento e regra de nunca cachear PII: aceitei gestao de invalidacao para nao pagar 2x a mesma pergunta, sem expor dado sensivel.
- Custo por tarefa com meta menor ou igual a baseline vezes 0.4 e ledger por fluxo: escolhi contabilidade visivel para permitir precificar ao cliente.
- Budget por cliente com alerta em 80 por cento: preferi travar crescimento de gasto cedo a descobrir estouro na fatura.
- Batch assincrono respeitando SLA: empacotei chamadas para buscar desconto preservando score maior ou igual a 0.90 e reducao maior ou igual a 85 por cento.

## Impacto no negocio

O framework com custo por tarefa menor ou igual a baseline vezes 0.4, hit de cache maior ou igual a 30 por cento e alerta em 80 por cento do budget torna o agente precificavel e reduz o custo mensal em meta maior ou igual a 85 por cento, o que destrava margem e evita subsidio invisivel de inferencia.

## Referencias de estudo

- Curso: FinOps for AI and LLM Cost Optimization, plataforma Udemy.
- Video: Reducao de custo de LLM com cache e roteamento, plataforma YouTube, canal Y Combinator.
- Doc oficial: Guia de precos e tokens da API, documentacao oficial OpenAI.
- Doc oficial: Guia de prompt caching, documentacao oficial Anthropic.
