# PDI — Apresentação: Monitoramento de Custos e Consumo de Tokens de LLMs de Fronteira

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: MONITORAMENTO DE CUSTOS E CONSUMO DE TOKENS DE LLMS DE FRONTEIRA

Marcos Perettoco — V4 Company
25/08/2026 | Engenharia de IA
```

---

## Slide 2: O Problema

**Sem visibilidade de custo, o uso de LLMs de fronteira (OpenAI, Gemini) saía do controle em picos.**

## Diagnóstico

- Sem log de tokens por agente/modelo
- Sem tabela de preço atualizada
- Sem alerta de orçamento


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Captura de prompt/completion tokens por Run
- Tabela de preço por 1k tokens (atualização mensal)
- Alertas: 80% warn, 100% block por agente
- Otimização: cache de prompt e modelo menor para tarefas simples


---

## Slide 4: Entregas

## Artefatos

- COST-MONITORING.md (padrão)
- usage_schema.sql (schema)
- track_cost.py (cálculo de custo)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Visibilidade de custo | 0% | Por agente/modelo/dia |
| Alerta de orçamento | Não | Sim |
---

## Slide 6: Próximos Passos

- Instrumentar os agentes em produção
- Dashboard de custo no Command Center
