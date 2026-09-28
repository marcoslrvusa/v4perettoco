# Deck PDI: Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Área: Engenharia de Software

## Slide 1: Resumo Executivo
Entrego uma pipeline de testes em 3 camadas (unitário/integração/E2E) com gate de cobertura mínima de 80% no CI. Inclui testes reais, config de cobertura e um workflow de CI.
A entrega e defensável: roda em qualquer máquina e bloqueia merge abaixo do teto.
## Slide 2: Contexto de Produção
Projeto de agentes com ~30 módulos Python + nos JS.
Sem suíte: refactor de prompt/tool injetava regressão em produção.
CI existente só roda lint.
## Slide 3: O Problema e o Blast Radius
Sem rede de segurança, toda mudança em main e indiretamente em produção.
| Sintoma | Hoje | Alvo |
| --- | --- | --- |
| Cobertura | 0% | >= 80% |
| Gate de CI | ausente | bloqueia < 80% |
| Regressão em prod | frequente | rara |
## Slide 4: Diagnóstico e Causa Raiz
Sem fixtures: testes dependiam de estado global/real.
Sem distinção de camada: tudo demorava horas.
Sem teto de cobertura: era possível piorar sem perceber.
## Slide 5: Decisão Arquitetural (ADR)
ADR-022: Estratégia de Testes
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| pytest + testcontainers + playwright | realista, 3 camadas | setup maior | ESCOLHIDA |
| só unitários mockados | rápido | cego a integração | rejeitada |
> Nota: Unitário mira lógica pura (90%), integração mira ports com DB efêmero (80%), E2E só happy path.
## Slide 6: Entregas desta Atividade
TEST-STRATEGY.md.
test_agent_pipeline.py.
test_integration_repo.py.
pytest.ini + .github/workflows/ci.yml.
## Slide 7: Plano de Validação e Rollout
Rodar local: pytest --cov=src --cov-fail-under=80.
Subir o job no CI como required check.
Se < 80%, adicionar testes de lacuna.
E2E em stage separado com retry (não trava merge).
## Slide 8: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Cobertura global (gate) | >= 80% |
| Tempo unit/int | < 3 min |
| Flaky rate | < 1% |
## Slide 9: Riscos e Mitigações
| Risco | Mitigação |
| --- | --- |
| Flaky | retry 1x + isolamento |
| Cobertura vazia | code review + mutation |
## Slide 10: Próximos Passos
E2E para fluxos críticos.
Mutation testing em módulos núcleo.