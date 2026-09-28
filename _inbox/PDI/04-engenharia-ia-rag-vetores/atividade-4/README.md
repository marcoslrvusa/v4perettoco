# Engenharia de Custos de LLM (custo por tarefa, cache, roteamento)

Engenharia de IA

## Resumo Executivo

Framework de custo de LLM: custo por tarefa, cache de prompt, roteamento por complexidade e budget. Entrego o padrão e um calculador.

Sem contabilidade de tokens, não se precifica o agente.

## Contexto de Produção

- Modelo 'maxi' para tudo (10x custo).

- Sem cache -> mesma pergunta paga 2x.

- Impossível precificar ao cliente.

## Diagnóstico

| Hoje | Alvo |

| --- | --- |

| modelo único | roteamento |

| sem cache | cache |

| custo invisível | custo/tarefa |

## Decisão Arquitetural (ADR)

ADR-044 : Estratégia de Custo

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Roteamento + cache + budget | previsível | governança | ESCOLHIDA |

> **Nota:** Trivial -> leve; complexo -> forte; repetido -> cache.

## Entregas

- LLM-COST.md.

- cost_calc.py.

- BUDGET.md.

## Validação

1. Medir custo/tarefa com e sem roteamento.

2. Habilitar cache; medir hit rate.

3. Budget por cliente + alerta 80%.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Custo/tarefa | <= baseline*0.4 |

| Cache hit | >= 30% |

| Budget | alerta 80% |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Qualidade cai | eval + roteamento |

| Cache PII | não cachear |

## Próximos Passos

- Precificar por tarefa.

- Dashboard de custo.

## Decisões e tradeoffs

- Roteamento por complexidade em vez de modelo maxi para tudo: troquei simplicidade por governança, porque o maxi custa 10x e a regra trivial vai para leve e complexo vai para forte.
- Cache semântico com meta de hit maior ou igual a 30 por cento e regra de nunca cachear PII: aceitei gestão de invalidação para não pagar 2x a mesma pergunta, sem expor dado sensível.
- Custo por tarefa com meta menor ou igual a baseline vezes 0.4 e ledger por fluxo: escolhi contabilidade visível para permitir precificar ao cliente.
- Budget por cliente com alerta em 80 por cento: preferi travar crescimento de gasto cedo a descobrir estouro na fatura.
- Batch assíncrono respeitando SLA: empacotei chamadas para buscar desconto preservando score maior ou igual a 0.90 e redução maior ou igual a 85 por cento.

## Impacto no negócio

O framework com custo por tarefa menor ou igual a baseline vezes 0.4, hit de cache maior ou igual a 30 por cento e alerta em 80 por cento do budget torna o agente precificável e reduz o custo mensal em meta maior ou igual a 85 por cento, o que destrava margem e evita subsídio invisível de inferência.

## Referências de estudo

- Curso: FinOps for AI and LLM Cost Optimization, plataforma Udemy.
- Vídeo: Redução de custo de LLM com cache e roteamento, plataforma YouTube, canal Y Combinator.
- Doc oficial: Guia de preços e tokens da API, documentação oficial OpenAI.
- Doc oficial: Guia de prompt caching, documentação oficial Anthropic.
