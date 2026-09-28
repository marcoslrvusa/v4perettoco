# Idempotência e Entrega Exactly-Once (na prática: at-least-once + dedup)

Sistemas Distribuídos

## Resumo Executivo

Garantir idempotência de handlers: dedup por chave de evento + upsert, tornando 'at-least-once' equivalente a 'exactly-once' para o negócio. Entrego o padrão e um decorator.

Mensageria entrega no mínimo 1 vez; sem dedup, reenvio duplica lead/fatura.

## Contexto de Produção

- Reenvio duplicava leads (CNPJ repetido).

- Fatura emitida 2x em retry.

- Sem chave de evento.

## Diagnóstico

| Hoje | Alvo |

| --- | --- |

| reatenvio duplica | dedup event_id |

| sem upsert | upsert |

| sem versão | etag |

## Decisão Arquitetural (ADR)

ADR-052: Idempotência

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| dedup event_id + upsert | exactly-once p/ negócio | store | ESCOLHIDA |

> **Nota:** At-least-once do broker + dedup no consumidor = exactly-once observacional.

## Entregas

- IDEMPOTENCY.md.

- idempotent.py.

- schema_dedup.sql.

## Validação

1. Mesmo evento 3x -> 1 efeito.

2. Concorrência: 2 consumers, 1 aplicação.

3. DLQ não cria duplicata.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Duplicatas | 0 |

| Idempotente | 100% handlers |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Store cheio | TTL |

| Chave errada | event_id + negócio |

## Próximos Passos

- Aplicar em todos os consumers.

- Teste de concorrência no CI.

## Decisões e tradeoffs

- **At-least-once do broker mais dedup no consumidor**: entrega exactly-once observacional para o negócio, porque exactly-once de ponta a ponta não existe em sistema distribuído.
- **Outbox transacional**: venda e evento gravados na mesma transação na tabela `outbox(event_id, payload, sent)`, então falha na publicação vira reprocessamento do outbox em vez de evento perdido. Custo: relay varrendo pendentes a cada 1s.
- **Dedupe por `idempotency_key` antes de agir**: o consumer consulta a tabela de processados antes de cobrar. Custo: store com TTL para não encher.
- **ACK só após gravar a chave**: a reentrega cai no dedupe, então o mesmo evento 5x gera 1 cobrança. A chave combina event_id com identificador do negócio para não colidir.

## Impacto no negócio

Sem dedupe, reentregas geravam cobranças duplicadas e cerca de 60h por mês de correção manual. Com dedup a meta e zero duplicata e 100% dos handlers idempotentes, com correção próxima de 0h por mês. O teste que injeta o mesmo evento 5x e afirma 1 cobrança da ao Financeiro previsibilidade: retry deixa de ser risco de débito duplo.

## Referências de estudo

- Curso: "Event-Driven Architecture: From Theory to Practice" (Udemy).
- Vídeo: "What is Idempotency?" (YouTube, Hussein Nasser).
- Documento oficial: Apache Kafka Documentation, Exactly-once Semantics (kafka.apache.org).
- Documento oficial: PostgreSQL Documentation, INSERT ON CONFLICT (postgresql.org).
