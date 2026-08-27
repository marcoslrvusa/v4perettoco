# PDI — Apresentação: Mapeamento de Domínios com Domain-Driven Design (DDD)

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: MAPEAMENTO DE DOMÍNIOS COM DOMAIN-DRIVEN DESIGN (DDD)

Marcos Perettoco — V4 Company
25/08/2026 | Engenharia de Software
```

---

## Slide 2: O Problema

**Antes de codificar, os domínios de dados da empresa não estavam mapeados, gerando modelos duplicados e linguagem inconsistente entre times.**

## Diagnóstico

- Modelos de dados duplicados entre squads
- Linguagem ubíqua ausente
- Agregados e bounded contexts não definidos


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Mapeamento de 4 bounded contexts (CRM, Campaign, Agent, Billing)
- Definição de agregados com raiz e filhos
- Glossário de linguagem ubíqua
- Diagrama Mermaid de relacionamento dos domínios


---

## Slide 4: Entregas

## Artefatos

- DOMAIN-MAP.md (mapa + diagrama)
- domain_models.py (modelos de domínio)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Domínios mapeados | 0 | 4 |
| Consistência de linguagem | Baixa | Alta |
---

## Slide 6: Próximos Passos

- Validar o mapa com Product e Data
- Gerar schemas a partir dos agregados
