# PDI — Apresentação: Observabilidade e Logs de Sincronização n8n-CRM

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: OBSERVABILIDADE E LOGS DE SINCRONIZAÇÃO N8N-CRM

Marcos Perettoco — V4 Company
25/08/2026 | Automação & Infraestrutura
```

---

## Slide 2: O Problema

**Falhas de sincronização com CRMs terceiros (Salesforce, HubSpot, RD Station) só eram percebidas quando o cliente reclamava — não havia rastro estruturado de qual registro falhou, em qual etapa e por quê.**

## Diagnóstico

- Sem trace correlacionando a execução inteira do workflow
- Logs não estruturados impossibilitando alertas por taxa de erro
- Falta de SLO de latência e de detecção proativa de falhas


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Padrão de log estruturado (JSON) com trace_id, entity, crm, action, record_id
- Workflow de observabilidade que propaga trace e emite log centralizado
- Painel SQL com taxa de erro por CRM, falhas consecutivas e p95 de latência
- Alerta proativo em #ops-crm antes do impacto ao cliente


---

## Slide 4: Entregas

## Artefatos

- STANDARD-OBSERVABILITY-LOGS.md (padrão + SLO)
- Workflow n8n de log + alerta proativo
- Queries de dashboard (erro, falhas consecutivas, p95)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Detecção de falha de sync | Dias | < 1 min |
| Visibilidade por CRM | 0% | 100% |
| Alerta proativo | Não | Sim (SLO) |
---

## Slide 6: Próximos Passos

- Homologar o workflow de observabilidade em produção
- Integrar o painel ao dashboard do Command Center
