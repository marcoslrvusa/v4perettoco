# PDI — Apresentação: Refatoração de Módulo Legado com SOLID e Clean Architecture

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: REFATORAÇÃO DE MÓDULO LEGADO COM SOLID E CLEAN ARCHITECTURE

Marcos Perettoco — V4 Company
25/08/2026 | Engenharia de Software
```

---

## Slide 2: O Problema

**Um módulo crítico de orquestração de campanhas estava acoplado: a classe CampaignService misturava regra de negócio, acesso a banco, envio de e-mail e chamadas de API de CRM em um único arquivo de 600+ linhas, impossível de testar.**

## Diagnóstico

- SRP violado: uma classe cuidava de regra, DB, e-mail e CRM
- OCP violado: mudar canal exigia editar o método central
- DIP violado: camada de aplicação dependia de psycopg2 diretamente


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Aplicação dos 5 princípios SOLID documentados antes/depois
- Separação em camadas: domain / application / infrastructure
- Ports (LeadRepository, Notifier) e adapters desacoplados
- Injeção de dependência no CampaignService


---

## Slide 4: Entregas

## Artefatos

- SOLID-BEFORE-AFTER.md (mapeamento antes/depois)
- before_campaign_service.py (código legado)
- after_campaign_service.py (Clean Architecture)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Acoplamento (responsabilidades) | 4 em 1 classe | 1 por classe |
| Testabilidade | Nula | Alta (ports) |
| Linhas por classe | 600+ | < 40 |
---

## Slide 6: Próximos Passos

- Aplicar o mesmo padrão aos demais módulos legados
- Adicionar suíte de testes sobre os ports
