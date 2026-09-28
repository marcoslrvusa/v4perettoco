# Sistemas Distribuídos com Mensageria (fila, tópico, DLQ)

Sistemas Distribuídos

## Resumo Executivo

Fundamentos de mensageria para desacoplar serviços: fila, tópico, DLQ e ACK. Entrego o padrão e um consumidor com backpressure e DLQ.

O ecossistema de agentes já e distribuído; sem fila, falha de 1 serviço propaga.

## Contexto de Produção

- Agentes chamam uns aos outros via HTTP síncrono.

- Falha de downstream derruba a cadeia.

- Sem DLQ: mensagem ruim some.

## Diagnóstico

| Hoje | Alvo |

| --- | --- |

| HTTP síncrono | fila desacoplada |

| sem DLQ | DLQ + retry |

| sem backpressure | prefetch limitado |

## Decisão Arquitetural (ADR)

ADR-051: Transporte de Eventos

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Fila + tópico + DLQ | desacopla | ops | ESCOLHIDA |

| HTTP síncrono | simples | cascata | rejeitada |

> **Nota:** ACK explícito; prefetch limitado; DLQ após N tentativas.

## Entregas

- MESSAGING.md.

- consumer.py.

- broker.tf.

## Validação

1. Publicar 1k msg; derrubar consumer; confirmar reprocessamento.

2. Msg inválida -> DLQ (não perde).

3. Backpressure: consumer lento não estoura.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Throughput | >= 200 msg/s |

| Perdidas | 0 |

| DLQ revisitada | < 24h |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Duplicata | idempotência (05-A2) |

| DLQ esquecida | alerta |

## Próximos Passos

- Eventos de domínio do DDD (02-A3).

- Tracing por trace_id.

## Decisões e tradeoffs

- **RabbitMQ para filas de trabalho e Kafka para eventos de fluxo**: a cobrança usa fila com 1 worker por mensagem e o Marketing e a Operação assinam o mesmo tópico em pub/sub. Troca um HTTP simples por um broker que precisa de operação.
- **ACK explícito com prefetch limitado**: o consumer confirma depois de processar e recebe poucas mensagens por vez, então um consumer lento não estoura. Troca vazão por worker por estabilidade.
- **DLQ após N tentativas com runbook de reprocessamento**: mensagem inválida vai para a DLQ em vez de sumir e volta pelo `runbook-mensageria.md`. Exige rotina de revisita em menos de 24h para a DLQ não virar depósito esquecido.
- **Publicação fire-and-forget do `venda.criada`**: o Vendas publica e segue em ~2ms sem esperar os outros times. Troca resposta imediata por consistência eventual.

## Impacto no negócio

Com alvo de 200 msg/s e zero perda em pico, o teste de 1k mensagens com o consumer derrubado prova que pico de campanha vira buffer no broker em vez de timeout em cascata. O P95 de ponta a ponta abaixo de 5s mantém Vendas, Financeiro e Marketing reagindo em segundos, o que reduz lead esquecido e retrabalho de conciliação. O risco passa a ser operacional e conhecido: manter a DLQ revisitada em menos de 24h.

## Referências de estudo

- Curso: "Apache Kafka Séries: Learn Apache Kafka for Beginners" (Udemy, Stephane Maarek).
- Vídeo: "RabbitMQ in 100 Seconds" (YouTube, Fireship).
- Documento oficial: RabbitMQ Documentation (rabbitmq.com).
- Documento oficial: Apache Kafka Documentation (kafka.apache.org).
