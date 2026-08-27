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

ADR-044 — Estrategia de Custo

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