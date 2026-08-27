# Deck PDI — Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Area: Engenharia de Software

## Slide 1: Resumo Executivo
Entrego uma pipeline de testes em 3 camadas (unitario/integracao/E2E) com gate de cobertura minima de 80% no CI. Inclui testes reais, config de cobertura e um workflow de CI.
A entrega e defensavel: roda em qualquer maquina e bloqueia merge abaixo do teto.
## Slide 2: Contexto de Producao
Projeto de agentes com ~30 modulos Python + nos JS.
Sem suite: refactor de prompt/tool injetava regressao em producao.
CI existente so roda lint.
## Slide 3: O Problema e o Blast Radius
Sem rede de seguranca, toda mudanca em main e indiretamente em producao.
| Sintoma | Hoje | Alvo |
| --- | --- | --- |
| Cobertura | 0% | >= 80% |
| Gate de CI | ausente | bloqueia < 80% |
| Regressao em prod | frequente | rara |
## Slide 4: Diagnostico e Causa Raiz
Sem fixtures: testes dependiam de estado global/real.
Sem distincao de camada: tudo demorava horas.
Sem teto de cobertura: era possivel piorar sem perceber.
## Slide 5: Decisao Arquitetural (ADR)
ADR-022 — Estrategia de Testes
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| pytest + testcontainers + playwright | realista, 3 camadas | setup maior | ESCOLHIDA |
| so unitarios mockados | rapido | cego a integracao | rejeitada |
> Nota: Unitario mira logica pura (90%), integracao mira ports com DB efemero (80%), E2E so happy path.
## Slide 6: Entregas desta Atividade
TEST-STRATEGY.md.
test_agent_pipeline.py.
test_integration_repo.py.
pytest.ini + .github/workflows/ci.yml.
## Slide 7: Plano de Validacao e Rollout
Rodar local: pytest --cov=src --cov-fail-under=80.
Subir o job no CI como required check.
Se < 80%, adicionar testes de lacuna.
E2E em stage separado com retry (nao trava merge).
## Slide 8: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Cobertura global (gate) | >= 80% |
| Tempo unit/int | < 3 min |
| Flaky rate | < 1% |
## Slide 9: Riscos e Mitigacoes
| Risco | Mitigacao |
| --- | --- |
| Flaky | retry 1x + isolamento |
| Cobertura vazia | code review + mutation |
## Slide 10: Proximos Passos
E2E para fluxos criticos.
Mutation testing em modulos nucleo.