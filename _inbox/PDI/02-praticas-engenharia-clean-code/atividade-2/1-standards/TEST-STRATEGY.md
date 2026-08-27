# Estrategia de Testes — cobertura minima 80%

| Camada | Ferramenta | Foco | Alvo |
|--------|-----------|------|------|
| Unitario | pytest | funcoes puras, ports | 90% |
| Integracao | pytest + testcontainers | repos, migracoes | 80% |
| E2E | playwright | happy path do agente | 1 cenario |

## Principios
1. Testar comportamento, nao implementacao.
2. Fixtures efemeras (nunca banco compartilhado).
3. Gate: `pytest --cov=src --cov-fail-under=80`.
4. E2E isolado e com retry.
