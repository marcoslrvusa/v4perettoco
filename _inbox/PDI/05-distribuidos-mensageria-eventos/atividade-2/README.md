# Idempotencia e Entrega Exactly-Once (na pratica: at-least-once + dedup)

Sistemas Distribuidos

## Resumo Executivo

Garantir idempotencia de handlers: dedup por chave de evento + upsert, tornando 'at-least-once' equivalente a 'exactly-once' para o negocio. Entrego o padrao e um decorator.

Mensageria entrega no minimo 1 vez; sem dedup, reenvio duplica lead/fatura.

## Contexto de Producao

- Reenvio duplicava leads (CNPJ repetido).

- Fatura emitida 2x em retry.

- Sem chave de evento.

## Diagnostico

| Hoje | Alvo |

| --- | --- |

| reatenvio duplica | dedup event_id |

| sem upsert | upsert |

| sem versao | etag |

## Decisao Arquitetural (ADR)

ADR-052: Idempotencia

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| dedup event_id + upsert | exactly-once p/ negocio | store | ESCOLHIDA |

> **Nota:** At-least-once do broker + dedup no consumidor = exactly-once observacional.

## Entregas

- IDEMPOTENCY.md.

- idempotent.py.

- schema_dedup.sql.

## Validacao

1. Mesmo evento 3x -> 1 efeito.

2. Concorrencia: 2 consumers, 1 aplicacao.

3. DLQ nao cria duplicata.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Duplicatas | 0 |

| Idempotente | 100% handlers |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Store cheio | TTL |

| Chave errada | event_id + negocio |

## Proximos Passos

- Aplicar em todos os consumers.

- Teste de concorrencia no CI.

## Decisoes e tradeoffs

- **At-least-once do broker mais dedup no consumidor**: entrega exactly-once observacional para o negocio, porque exactly-once de ponta a ponta nao existe em sistema distribuido.
- **Outbox transacional**: venda e evento gravados na mesma transacao na tabela `outbox(event_id, payload, sent)`, entao falha na publicacao vira reprocessamento do outbox em vez de evento perdido. Custo: relay varrendo pendentes a cada 1s.
- **Dedupe por `idempotency_key` antes de agir**: o consumer consulta a tabela de processados antes de cobrar. Custo: store com TTL para nao encher.
- **ACK so apos gravar a chave**: a reentrega cai no dedupe, entao o mesmo evento 5x gera 1 cobranca. A chave combina event_id com identificador do negocio para nao colidir.

## Impacto no negocio

Sem dedupe, reentregas geravam cobrancas duplicadas e cerca de 60h por mes de correcao manual. Com dedup a meta e zero duplicata e 100% dos handlers idempotentes, com correcao proxima de 0h por mes. O teste que injeta o mesmo evento 5x e afirma 1 cobranca da ao Financeiro previsibilidade: retry deixa de ser risco de debito duplo.

## Referencias de estudo

- Curso: "Event-Driven Architecture: From Theory to Practice" (Udemy).
- Video: "What is Idempotency?" (YouTube, Hussein Nasser).
- Documento oficial: Apache Kafka Documentation, Exactly-once Semantics (kafka.apache.org).
- Documento oficial: PostgreSQL Documentation, INSERT ON CONFLICT (postgresql.org).
