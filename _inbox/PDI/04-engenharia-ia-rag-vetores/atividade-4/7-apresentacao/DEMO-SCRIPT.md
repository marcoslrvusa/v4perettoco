# Script de Demonstração — Monitoramento de Custos e Consumo de Tokens de LLMs de Fronteira

## Setup
```bash
# Estrutura da entrega
tree 04-engenharia-ia-rag-vetores/atividade-4/
```

## Passo 1: Contexto
Explique o problema:
> Sem visibilidade de custo, o uso de LLMs de fronteira (OpenAI, Gemini) saía do controle em picos.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Captura de prompt/completion tokens por Run
- Tabela de preço por 1k tokens (atualização mensal)
- Alertas: 80% warn, 100% block por agente
- Otimização: cache de prompt e modelo menor para tarefas simples

## Passo 3: Entregas
Mostre os artefatos gerados:
- COST-MONITORING.md (padrão)
- usage_schema.sql (schema)
- track_cost.py (cálculo de custo)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Visibilidade de custo | 0% | Por agente/modelo/dia |
| Alerta de orçamento | Não | Sim |
