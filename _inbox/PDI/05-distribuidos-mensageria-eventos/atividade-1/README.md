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

ADR-051: Transporte de Eventos

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

## Decisoes e tradeoffs

- **RabbitMQ para filas de trabalho e Kafka para eventos de fluxo**: a cobranca usa fila com 1 worker por mensagem e o Marketing e a Operacao assinam o mesmo topico em pub/sub. Troca um HTTP simples por um broker que precisa de operacao.
- **ACK explicito com prefetch limitado**: o consumer confirma depois de processar e recebe poucas mensagens por vez, entao um consumer lento nao estoura. Troca vazao por worker por estabilidade.
- **DLQ apos N tentativas com runbook de reprocessamento**: mensagem invalida vai para a DLQ em vez de sumir e volta pelo `runbook-mensageria.md`. Exige rotina de revisita em menos de 24h para a DLQ nao virar deposito esquecido.
- **Publicacao fire-and-forget do `venda.criada`**: o Vendas publica e segue em ~2ms sem esperar os outros times. Troca resposta imediata por consistencia eventual.

## Impacto no negocio

Com alvo de 200 msg/s e zero perda em pico, o teste de 1k mensagens com o consumer derrubado prova que pico de campanha vira buffer no broker em vez de timeout em cascata. O P95 de ponta a ponta abaixo de 5s mantem Vendas, Financeiro e Marketing reagindo em segundos, o que reduz lead esquecido e retrabalho de conciliacao. O risco passa a ser operacional e conhecido: manter a DLQ revisitada em menos de 24h.

## Referencias de estudo

- Curso: "Apache Kafka Series: Learn Apache Kafka for Beginners" (Udemy, Stephane Maarek).
- Video: "RabbitMQ in 100 Seconds" (YouTube, Fireship).
- Documento oficial: RabbitMQ Documentation (rabbitmq.com).
- Documento oficial: Apache Kafka Documentation (kafka.apache.org).
