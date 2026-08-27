# Mensageria — Padrao

- **Fila**: 1 consumidor (trabalho).
- **Topico**: N consumidores (evento).
- **DLQ**: falha apos N -> analise.
- **ACK**: so apos processar.

## Regras
1. ACK explicito apos sucesso.
2. Prefetch limitado (backpressure).
3. DLQ com maxReceiveCount.
4. Idempotencia no consumer.
