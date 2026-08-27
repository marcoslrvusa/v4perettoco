# PDI — Apresentação: Microsserviço Consumidor Assíncrono Idempotente

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: MICROSSERVIÇO CONSUMIDOR ASSÍNCRONO IDEMPOTENTE

Marcos Perettoco — V4 Company
25/08/2026 | Sistemas Distribuídos
```

---

## Slide 2: O Problema

**Reentregas e duplicatas em filas causavam dados duplicados.**

## Diagnóstico

- Mesma mensagem processada múltiplas vezes
- Sem chave de deduplicação
- Upsert ausente no destino


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Chave event_id única no cabeçalho
- Tabela processed_events com PK (INSERT rejeita duplicata)
- Upsert (ON CONFLICT DO NOTHING) no dado de negócio
- Descarte silencioso de evento já processado


---

## Slide 4: Entregas

## Artefatos

- IDEMPOTENCY.md (padrão)
- consumer.py (consumidor idempotente)
- processed_events.sql (schema)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Duplicidade de dados | Sim | Eliminada |
| Deduplicação | Não | Sim |
---

## Slide 6: Próximos Passos

- Conectar o consumidor a um tópico real
- Testar reentrega em massa
