# Deck PDI — Engenharia de Custos de LLM (custo por tarefa, cache, roteamento)

Area: Engenharia de IA

## Slide 1: Resumo Executivo
Framework de custo de LLM: custo por tarefa, cache de prompt, roteamento por complexidade e budget. Entrego o padrao e um calculador.
Sem contabilidade de tokens, nao se precifica o agente.
## Slide 2: Contexto de Producao
Modelo 'maxi' para tudo (10x custo).
Sem cache -> mesma pergunta paga 2x.
Impossivel precificar ao cliente.
## Slide 3: Diagnostico
| Hoje | Alvo |
| --- | --- |
| modelo unico | roteamento |
| sem cache | cache |
| custo invisivel | custo/tarefa |
## Slide 4: Decisao Arquitetural (ADR)
ADR-044 — Estrategia de Custo
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| Roteamento + cache + budget | previsivel | governanca | ESCOLHIDA |
> Nota: Trivial -> leve; complexo -> forte; repetido -> cache.
## Slide 5: Entregas
LLM-COST.md.
cost_calc.py.
BUDGET.md.
## Slide 6: Validacao
Medir custo/tarefa com e sem roteamento.
Habilitar cache; medir hit rate.
Budget por cliente + alerta 80%.
## Slide 7: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Custo/tarefa | <= baseline*0.4 |
| Cache hit | >= 30% |
| Budget | alerta 80% |
## Slide 8: Riscos
| Risco | Mitigacao |
| --- | --- |
| Qualidade cai | eval + roteamento |
| Cache PII | nao cachear |
## Slide 9: Proximos Passos
Precificar por tarefa.
Dashboard de custo.