# PDI — Apresentação: Arquitetura de Barramento de Mensageria (Pub/Sub, RabbitMQ ou Kafka)

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: ARQUITETURA DE BARRAMENTO DE MENSAGERIA (PUB/SUB, RABBITMQ OU KAFKA)

Marcos Perettoco — V4 Company
25/08/2026 | Sistemas Distribuídos
```

---

## Slide 2: O Problema

**Sistemas internos se integravam por chamadas síncronas frágeis, sem desacoplamento.**

## Diagnóstico

- Acoplamento síncrono ponto a ponto
- Sem contrato de evento versionado
- Cascata de falhas em chamadas diretas


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Kafka como barramento (event log distribuído)
- Produtores publicam em tópicos por domínio
- Consumidores assinam tópicos de interesse
- Particionamento por entity_id (ordem por chave)


---

## Slide 4: Entregas

## Artefatos

- MESH-ARCHITECTURE.md (arquitetura + diagrama)
- topic_contracts.json (contratos)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Acoplamento | Síncrono | Event-driven |
| Resiliência | Baixa | Alta |
---

## Slide 6: Próximos Passos

- Prototipar tópico crm.lead.created em staging
- Adicionar Schema Registry
