# Estratégia de Testes — cobertura mínima 80%

| Camada | Ferramenta | Foco | Meta |
|--------|-----------|------|------|
| Unitário | pytest | funções puras, ports | 90% |
| Integração | pytest + testcontainers | repo DB, notifier | 80% |
| E2E | playwright | fluxo do agente | happy path |

Regra de CI: `pytest --cov=src --cov-fail-under=80` bloqueia o merge.
