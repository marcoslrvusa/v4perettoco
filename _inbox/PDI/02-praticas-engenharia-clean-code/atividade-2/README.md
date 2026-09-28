# Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Engenharia de Software

## Resumo Executivo

Entrego uma pipeline de testes em 3 camadas (unitario/integracao/E2E) com gate de cobertura minima de 80% no CI. Inclui testes reais, config de cobertura e um workflow de CI.

A entrega e defensavel: roda em qualquer maquina e bloqueia merge abaixo do teto.

## Contexto de Producao

- Projeto de agentes com ~30 modulos Python + nos JS.

- Sem suite: refactor de prompt/tool injetava regressao em producao.

- CI existente so roda lint.

## O Problema e o Blast Radius

Sem rede de seguranca, toda mudanca em main e indiretamente em producao.

| Sintoma | Hoje | Alvo |

| --- | --- | --- |

| Cobertura | 0% | >= 80% |

| Gate de CI | ausente | bloqueia < 80% |

| Regressao em prod | frequente | rara |

## Diagnostico e Causa Raiz

- Sem fixtures: testes dependiam de estado global/real.

- Sem distincao de camada: tudo demorava horas.

- Sem teto de cobertura: era possivel piorar sem perceber.

## Decisao Arquitetural (ADR)

ADR-022: Estrategia de Testes

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| pytest + testcontainers + playwright | realista, 3 camadas | setup maior | ESCOLHIDA |

| so unitarios mockados | rapido | cego a integracao | rejeitada |

> **Nota:** Unitario mira logica pura (90%), integracao mira ports com DB efemero (80%), E2E so happy path.

## Entregas desta Atividade

- TEST-STRATEGY.md.

- test_agent_pipeline.py.

- test_integration_repo.py.

- pytest.ini + .github/workflows/ci.yml.

## Plano de Validacao e Rollout

1. Rodar local: pytest --cov=src --cov-fail-under=80.

2. Subir o job no CI como required check.

3. Se < 80%, adicionar testes de lacuna.

4. E2E em stage separado com retry (nao trava merge).

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Cobertura global (gate) | >= 80% |

| Tempo unit/int | < 3 min |

| Flaky rate | < 1% |

## Riscos e Mitigacoes

| Risco | Mitigacao |

| --- | --- |

| Flaky | retry 1x + isolamento |

| Cobertura vazia | code review + mutation |

## Proximos Passos

- E2E para fluxos criticos.

- Mutation testing em modulos nucleo.
## Decisoes e tradeoffs
- pytest com testcontainers e playwright escolhido sobre so unitarios mockados: cobre 3 camadas com realismo e o custo maior de setup compensa, pois unitario sozinho e cego a integracao.
- Unitario mira logica pura com alvo de 90 por cento, integracao mira ports com DB efemero com alvo de 80 por cento, e E2E cobre so happy path: camadas rapidas seguram o merge e a camada lenta nao trava o time.
- Gate de cobertura minima de 80 por cento com --cov-fail-under=80 como required check no CI: impede piorar a cobertura sem perceber, saindo de 0 por cento e CI que so rodava lint.
- E2E em stage separado com retry, fora do caminho critico do merge: evita que teste lento ou instavel bloqueie o fluxo diario dos cerca de 30 modulos Python e nos JS.
- Fixtures isoladas com retry de 1 vez e isolamento contra estado global: sustenta tempo de unit e integracao menor que 3 min e flaky rate menor que 1 por cento.

## Impacto no negocio

O projeto tem cerca de 30 modulos Python mais nos JS e o CI atual so roda lint, entao refactor de prompt ou tool injeta regressao em producao sem rede de seguranca. O gate de 80 por cento com unit e integracao em menos de 3 min troca dias de validacao manual por minutos no CI, reduz regressao frequente para rara com flaky abaixo de 1 por cento, e evita o custo de corrigir defeito tarde, quando ele ja chegou a main e a producao.

## Referencias de estudo
- Curso: Testes automatizados com pytest, na Alura.
- Video: Piramide de testes na pratica com Python, no YouTube.
- Doc oficial: Documentacao do pytest sobre execucao e cobertura, em docs.pytest.org.
- Doc oficial: Documentacao do Coverage.py sobre medicao com branch, em coverage.readthedocs.io.
