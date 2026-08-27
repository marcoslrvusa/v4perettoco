# PDI — Apresentação: Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: PIPELINE DE TESTES AUTOMATIZADOS (UNIT/INTEGRATION/E2E) COM 80% DE COBERTURA

Marcos Perettoco — V4 Company
25/08/2026 | Engenharia de Software
```

---

## Slide 2: O Problema

**O projeto de agentes não tinha suíte de testes, tornando refatorações arriscadas. Mudanças em produção ocorriam sem rede de segurança.**

## Diagnóstico

- Zero cobertura de testes automatizados
- Refatorações feitas em produção sem validação
- Sem gate de CI para bloquear queda de qualidade


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Estratégia em 3 camadas: unitário (pytest), integração (testcontainers), E2E (playwright)
- Configuração de cobertura mínima de 80% (--cov-fail-under)
- Fixtures de banco efêmero e notifier spy para integração
- Gate de CI que bloqueia o merge abaixo de 80%


---

## Slide 4: Entregas

## Artefatos

- TEST-STRATEGY.md (metas por camada)
- test_agent_pipeline.py (unitários)
- test_integration_repo.py (integração)
- pytest.ini (cobertura 80%)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Cobertura | 0% | >= 80% |
| Gate de CI | Não | Sim (block merge) |
| Segurança em refactor | Baixa | Alta |
---

## Slide 6: Próximos Passos

- Subir o pipeline no CI do repositório
- Ampliar E2E para os fluxos críticos de agentes
