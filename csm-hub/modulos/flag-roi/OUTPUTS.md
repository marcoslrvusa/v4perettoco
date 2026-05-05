# OUTPUTS — Flag ROI V1

## Output: CHAS de ROI negativo

**Input:** "ROAS do E-commerce Moda caiu de 3.8 para 1.9 em 2 semanas"

```
CHAS — ROI Negativo — E-commerce Moda — 26/04/2025

CONTEXT:
ROAS caiu de 3.8 para 1.9 (queda de 50%) nas últimas 2 semanas.
Investimento estável em R$5.000/semana. Receita atribuída caiu de
R$19.000 para R$9.500. Cliques estáveis. CPM subiu 18%.

Tipo identificado: MISTO
- Custo: CPM subiu 18% (sazonalidade de fim de mês)
- Conversão: AOV caiu de R$280 para R$190 (mix de produto)

HYPOTHESIS:
"O ROAS caiu porque o AOV caiu — campanhas estão convertendo
produtos de menor ticket. O CPM elevado agrava mas não é a causa principal."
Confiança: Medium (precisamos confirmar por campanha)

ACTION:
1. GT quebra relatório por produto/SKU — identifica quais converteram.
   Prazo: amanhã 12h.
2. Se confirmado mix: separar campanhas por faixa de preço.
   Prazo: até quinta.
3. Copy cria 2 ângulos para produtos de ticket alto.
   Prazo: até sexta.

SUCCESS:
ROAS ≥ 3.0 por 2 semanas consecutivas.
Rollback: se ação 2 não funcionar em 10 dias → revisar segmentação de público.
```
