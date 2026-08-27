# Deck PDI — Idempotencia e Entrega Exactly-Once (na pratica: at-least-once + dedup)

Area: Sistemas Distribuidos

## Slide 1: Resumo Executivo
Garantir idempotencia de handlers: dedup por chave de evento + upsert, tornando 'at-least-once' equivalente a 'exactly-once' para o negocio. Entrego o padrao e um decorator.
Mensageria entrega no minimo 1 vez; sem dedup, reenvio duplica lead/fatura.
## Slide 2: Contexto de Producao
Reenvio duplicava leads (CNPJ repetido).
Fatura emitida 2x em retry.
Sem chave de evento.
## Slide 3: Diagnostico
| Hoje | Alvo |
| --- | --- |
| reatenvio duplica | dedup event_id |
| sem upsert | upsert |
| sem versao | etag |
## Slide 4: Decisao Arquitetural (ADR)
ADR-052 — Idempotencia
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| dedup event_id + upsert | exactly-once p/ negocio | store | ESCOLHIDA |
> Nota: At-least-once do broker + dedup no consumidor = exactly-once observacional.
## Slide 5: Entregas
IDEMPOTENCY.md.
idempotent.py.
schema_dedup.sql.
## Slide 6: Validacao
Mesmo evento 3x -> 1 efeito.
Concorrencia: 2 consumers, 1 aplicacao.
DLQ nao cria duplicata.
## Slide 7: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Duplicatas | 0 |
| Idempotente | 100% handlers |
## Slide 8: Riscos
| Risco | Mitigacao |
| --- | --- |
| Store cheio | TTL |
| Chave errada | event_id + negocio |
## Slide 9: Proximos Passos
Aplicar em todos os consumers.
Teste de concorrencia no CI.