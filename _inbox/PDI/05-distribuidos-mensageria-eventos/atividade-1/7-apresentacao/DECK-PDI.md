# Deck PDI: Sistemas Distribuídos com Mensageria (fila, tópico, DLQ)

Área: Sistemas Distribuídos

## Slide 1: Resumo Executivo
Fundamentos de mensageria para desacoplar serviços: fila, tópico, DLQ e ACK. Entrego o padrão e um consumidor com backpressure e DLQ.
O ecossistema de agentes já e distribuído; sem fila, falha de 1 serviço propaga.
## Slide 2: Contexto de Produção
Agentes chamam uns aos outros via HTTP síncrono.
Falha de downstream derruba a cadeia.
Sem DLQ: mensagem ruim some.
## Slide 3: Diagnóstico
| Hoje | Alvo |
| --- | --- |
| HTTP síncrono | fila desacoplada |
| sem DLQ | DLQ + retry |
| sem backpressure | prefetch limitado |
## Slide 4: Decisão Arquitetural (ADR)
ADR-051: Transporte de Eventos
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| Fila + tópico + DLQ | desacopla | ops | ESCOLHIDA |
| HTTP síncrono | simples | cascata | rejeitada |
> Nota: ACK explícito; prefetch limitado; DLQ após N tentativas.
## Slide 5: Entregas
MESSAGING.md.
consumer.py.
broker.tf.
## Slide 6: Validação
Publicar 1k msg; derrubar consumer; confirmar reprocessamento.
Msg inválida -> DLQ (não perde).
Backpressure: consumer lento não estoura.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Throughput | >= 200 msg/s |
| Perdidas | 0 |
| DLQ revisitada | < 24h |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Duplicata | idempotência (05-A2) |
| DLQ esquecida | alerta |
## Slide 9: Próximos Passos
Eventos de domínio do DDD (02-A3).
Tracing por trace_id.