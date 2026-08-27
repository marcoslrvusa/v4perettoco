# Script de Demonstração — Arquitetura de Barramento de Mensageria (Pub/Sub, RabbitMQ ou Kafka)

## Setup
```bash
# Estrutura da entrega
tree 05-distribuidos-mensageria-eventos/atividade-1/
```

## Passo 1: Contexto
Explique o problema:
> Sistemas internos se integravam por chamadas síncronas frágeis, sem desacoplamento.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Kafka como barramento (event log distribuído)
- Produtores publicam em tópicos por domínio
- Consumidores assinam tópicos de interesse
- Particionamento por entity_id (ordem por chave)

## Passo 3: Entregas
Mostre os artefatos gerados:
- MESH-ARCHITECTURE.md (arquitetura + diagrama)
- topic_contracts.json (contratos)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Acoplamento | Síncrono | Event-driven |
| Resiliência | Baixa | Alta |
