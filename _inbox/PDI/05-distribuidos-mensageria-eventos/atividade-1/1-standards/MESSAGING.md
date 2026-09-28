# Mensageria: Padrão

- **Fila**: 1 consumidor (trabalho).
- **Tópico**: N consumidores (evento).
- **DLQ**: falha após N -> analise.
- **ACK**: só após processar.

## Regras
1. ACK explícito após sucesso.
2. Prefetch limitado (backpressure).
3. DLQ com maxReceiveCount.
4. Idempotência no consumer.
