# Deck PDI: Engenharia de Custos de LLM (custo por tarefa, cache, roteamento)

Área: Engenharia de IA

## Slide 1: Resumo Executivo
Framework de custo de LLM: custo por tarefa, cache de prompt, roteamento por complexidade e budget. Entrego o padrão e um calculador.
Sem contabilidade de tokens, não se precifica o agente.
## Slide 2: Contexto de Produção
Modelo 'maxi' para tudo (10x custo).
Sem cache -> mesma pergunta paga 2x.
Impossível precificar ao cliente.
## Slide 3: Diagnóstico
| Hoje | Alvo |
| --- | --- |
| modelo único | roteamento |
| sem cache | cache |
| custo invisível | custo/tarefa |
## Slide 4: Decisão Arquitetural (ADR)
ADR-044: Estratégia de Custo
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| Roteamento + cache + budget | previsível | governança | ESCOLHIDA |
> Nota: Trivial -> leve; complexo -> forte; repetido -> cache.
## Slide 5: Entregas
LLM-COST.md.
cost_calc.py.
BUDGET.md.
## Slide 6: Validação
Medir custo/tarefa com e sem roteamento.
Habilitar cache; medir hit rate.
Budget por cliente + alerta 80%.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Custo/tarefa | <= baseline*0.4 |
| Cache hit | >= 30% |
| Budget | alerta 80% |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Qualidade cai | eval + roteamento |
| Cache PII | não cachear |
## Slide 9: Próximos Passos
Precificar por tarefa.
Dashboard de custo.