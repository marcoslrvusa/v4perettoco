# Script de Demonstração — Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

## Setup
```bash
# Estrutura da entrega
tree 02-praticas-engenharia-clean-code/atividade-2/
```

## Passo 1: Contexto
Explique o problema:
> O projeto de agentes não tinha suíte de testes, tornando refatorações arriscadas. Mudanças em produção ocorriam sem rede de segurança.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Estratégia em 3 camadas: unitário (pytest), integração (testcontainers), E2E (playwright)
- Configuração de cobertura mínima de 80% (--cov-fail-under)
- Fixtures de banco efêmero e notifier spy para integração
- Gate de CI que bloqueia o merge abaixo de 80%

## Passo 3: Entregas
Mostre os artefatos gerados:
- TEST-STRATEGY.md (metas por camada)
- test_agent_pipeline.py (unitários)
- test_integration_repo.py (integração)
- pytest.ini (cobertura 80%)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Cobertura | 0% | >= 80% |
| Gate de CI | Não | Sim (block merge) |
| Segurança em refactor | Baixa | Alta |
