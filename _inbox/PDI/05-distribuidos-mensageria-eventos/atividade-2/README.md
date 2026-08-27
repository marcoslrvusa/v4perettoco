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

ADR-052 — Idempotencia

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