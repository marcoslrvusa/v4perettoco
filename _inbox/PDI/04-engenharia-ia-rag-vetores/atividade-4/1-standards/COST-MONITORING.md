# STANDARD — Monitoramento de Custo LLM

- **Capture:** log de `prompt_tokens`, `completion_tokens`, `model`, `agent` por Run.
- **Custo:** tabela de preço por 1k tokens (atualizar mensal).
- **Alerta:** orçamento diário por agente; 80% → warn, 100% → bloqueio.
- **Otimização:** cache de prompt, modelo menor para tarefas simples.
