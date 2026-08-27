# Sistemas Distribuidos com Mensageria (fila, topico, DLQ)

Sistemas Distribuidos

## Resumo Executivo

Fundamentos de mensageria para desacoplar servicos: fila, topico, DLQ e ACK. Entrego o padrao e um consumidor com backpressure e DLQ.

O ecossistema de agentes ja e distribuido; sem fila, falha de 1 servico propaga.

## Contexto de Producao

- Agentes chamam uns aos outros via HTTP sincrono.

- Falha de downstream derruba a cadeia.

- Sem DLQ: mensagem ruim some.

## Diagnostico

| Hoje | Alvo |

| --- | --- |

| HTTP sincrono | fila desacoplada |

| sem DLQ | DLQ + retry |

| sem backpressure | prefetch limitado |

## Decisao Arquitetural (ADR)

ADR-051 — Transporte de Eventos

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Fila + topico + DLQ | desacopla | ops | ESCOLHIDA |

| HTTP sincrono | simples | cascata | rejeitada |

> **Nota:** ACK explicito; prefetch limitado; DLQ apos N tentativas.

## Entregas

- MESSAGING.md.

- consumer.py.

- broker.tf.

## Validacao

1. Publicar 1k msg; derrubar consumer; confirmar reprocessamento.

2. Msg invalida -> DLQ (nao perde).

3. Backpressure: consumer lento nao estoura.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Throughput | >= 200 msg/s |

| Perdidas | 0 |

| DLQ revisitada | < 24h |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Duplicata | idempotencia (05-A2) |

| DLQ esquecida | alerta |

## Proximos Passos

- Eventos de dominio do DDD (02-A3).

- Tracing por trace_id.