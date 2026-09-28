# Estratégia de Testes: cobertura mínima 80%

| Camada | Ferramenta | Foco | Alvo |
|--------|-----------|------|------|
| Unitário | pytest | funções puras, ports | 90% |
| Integração | pytest + testcontainers | repos, migrações | 80% |
| E2E | playwright | happy path do agente | 1 cenário |

## Princípios
1. Testar comportamento, não implementação.
2. Fixtures efêmeras (nunca banco compartilhado).
3. Gate: `pytest --cov=src --cov-fail-under=80`.
4. E2E isolado e com retry.
