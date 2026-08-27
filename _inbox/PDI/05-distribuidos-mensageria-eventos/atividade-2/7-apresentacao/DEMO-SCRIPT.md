# Script de Demonstração — Microsserviço Consumidor Assíncrono Idempotente

## Setup
```bash
# Estrutura da entrega
tree 05-distribuidos-mensageria-eventos/atividade-2/
```

## Passo 1: Contexto
Explique o problema:
> Reentregas e duplicatas em filas causavam dados duplicados.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Chave event_id única no cabeçalho
- Tabela processed_events com PK (INSERT rejeita duplicata)
- Upsert (ON CONFLICT DO NOTHING) no dado de negócio
- Descarte silencioso de evento já processado

## Passo 3: Entregas
Mostre os artefatos gerados:
- IDEMPOTENCY.md (padrão)
- consumer.py (consumidor idempotente)
- processed_events.sql (schema)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Duplicidade de dados | Sim | Eliminada |
| Deduplicação | Não | Sim |
