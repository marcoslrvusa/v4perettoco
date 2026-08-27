# Engenharia de Custos de LLM

custo_tarefa = (in*$in + out*$out) * (1 - cache_hit)
- mini: $0.15/1M in, $0.60/1M out
- maxi: $3/1M in, $15/1M out

## Regras
1. Roteamento por complexidade.
2. Cache de prompt.
3. Budget por cliente; alerta 80%.
4. NAO cachear PII.
