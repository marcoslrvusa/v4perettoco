# PDI — Apresentação: Contingência Automatizada (Circuit Breaker) para APIs Externas

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: CONTINGÊNCIA AUTOMATIZADA (CIRCUIT BREAKER) PARA APIS EXTERNAS

Marcos Perettoco — V4 Company
25/08/2026 | Sistemas Distribuídos
```

---

## Slide 2: O Problema

**Quedas de CRMs/ERPs externos derrubavam workflows inteiros.**

## Diagnóstico

- Sem proteção contra instabilidade de terceiros
- Chamadas repetidas agravando a falha
- Sem fallback


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Circuit Breaker com estados closed/open/half-open
- Threshold de falhas + cooldown + recovery
- Fallback automático quando aberto
- Recuperação automática testando 1 requisição


---

## Slide 4: Entregas

## Artefatos

- CIRCUIT-BREAKER.md (padrão)
- circuit_breaker.py (implementação)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Cascata de falhas | Sim | Mitigada |
| Fallback | Não | Sim |
---

## Slide 6: Próximos Passos

- Aplicar aos nós de CRM/ERP nos workflows
- Expor métricas de estado do breaker
