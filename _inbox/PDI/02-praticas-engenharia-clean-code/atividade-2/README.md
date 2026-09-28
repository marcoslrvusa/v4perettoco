# Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Engenharia de Software

## Resumo Executivo

Entrego uma pipeline de testes em 3 camadas (unitário/integração/E2E) com gate de cobertura mínima de 80% no CI. Inclui testes reais, config de cobertura e um workflow de CI.

A entrega e defensável: roda em qualquer máquina e bloqueia merge abaixo do teto.

## Contexto de Produção

- Projeto de agentes com ~30 módulos Python + nos JS.

- Sem suíte: refactor de prompt/tool injetava regressão em produção.

- CI existente só roda lint.

## O Problema e o Blast Radius

Sem rede de segurança, toda mudança em main e indiretamente em produção.

| Sintoma | Hoje | Alvo |

| --- | --- | --- |

| Cobertura | 0% | >= 80% |

| Gate de CI | ausente | bloqueia < 80% |

| Regressão em prod | frequente | rara |

## Diagnóstico e Causa Raiz

- Sem fixtures: testes dependiam de estado global/real.

- Sem distinção de camada: tudo demorava horas.

- Sem teto de cobertura: era possível piorar sem perceber.

## Decisão Arquitetural (ADR)

ADR-022: Estratégia de Testes

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| pytest + testcontainers + playwright | realista, 3 camadas | setup maior | ESCOLHIDA |

| só unitários mockados | rápido | cego a integração | rejeitada |

> **Nota:** Unitário mira lógica pura (90%), integração mira ports com DB efêmero (80%), E2E só happy path.

## Entregas desta Atividade

- TEST-STRATEGY.md.

- test_agent_pipeline.py.

- test_integration_repo.py.

- pytest.ini + .github/workflows/ci.yml.

## Plano de Validação e Rollout

1. Rodar local: pytest --cov=src --cov-fail-under=80.

2. Subir o job no CI como required check.

3. Se < 80%, adicionar testes de lacuna.

4. E2E em stage separado com retry (não trava merge).

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Cobertura global (gate) | >= 80% |

| Tempo unit/int | < 3 min |

| Flaky rate | < 1% |

## Riscos e Mitigações

| Risco | Mitigação |

| --- | --- |

| Flaky | retry 1x + isolamento |

| Cobertura vazia | code review + mutation |

## Próximos Passos

- E2E para fluxos críticos.

- Mutation testing em módulos núcleo.
## Decisões e tradeoffs
- pytest com testcontainers e playwright escolhido sobre só unitários mockados: cobre 3 camadas com realismo e o custo maior de setup compensa, pois unitário sozinho é cego a integração.
- Unitário mira lógica pura com alvo de 90 por cento, integração mira ports com DB efêmero com alvo de 80 por cento, e E2E cobre só happy path: camadas rápidas seguram o merge e a camada lenta não trava o time.
- Gate de cobertura mínima de 80 por cento com --cov-fail-under=80 como required check no CI: impede piorar a cobertura sem perceber, saindo de 0 por cento e CI que só rodava lint.
- E2E em stage separado com retry, fora do caminho crítico do merge: evita que teste lento ou instável bloqueie o fluxo diário dos cerca de 30 módulos Python e nos JS.
- Fixtures isoladas com retry de 1 vez e isolamento contra estado global: sustenta tempo de unit e integração menor que 3 min e flaky rate menor que 1 por cento.

## Impacto no negócio

O projeto tem cerca de 30 módulos Python mais nos JS e o CI atual só roda lint, então refactor de prompt ou tool injeta regressão em produção sem rede de segurança. O gate de 80 por cento com unit e integração em menos de 3 min troca dias de validação manual por minutos no CI, reduz regressão frequente para rara com flaky abaixo de 1 por cento, e evita o custo de corrigir defeito tarde, quando ele já chegou a main e a produção.

## Referências de estudo
- Curso: Testes automatizados com pytest, na Alura.
- Vídeo: Piramide de testes na prática com Python, no YouTube.
- Doc oficial: Documentação do pytest sobre execução e cobertura, em docs.pytest.org.
- Doc oficial: Documentação do Coverage.py sobre medição com branch, em coverage.readthedocs.io.
