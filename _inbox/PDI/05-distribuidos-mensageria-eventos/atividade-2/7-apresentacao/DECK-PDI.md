# Deck PDI: Idempotência e Entrega Exactly-Once (na prática: at-least-once + dedup)

Área: Sistemas Distribuídos

## Slide 1: Resumo Executivo
Garantir idempotência de handlers: dedup por chave de evento + upsert, tornando 'at-least-once' equivalente a 'exactly-once' para o negócio. Entrego o padrão e um decorator.
Mensageria entrega no mínimo 1 vez; sem dedup, reenvio duplica lead/fatura.
## Slide 2: Contexto de Produção
Reenvio duplicava leads (CNPJ repetido).
Fatura emitida 2x em retry.
Sem chave de evento.
## Slide 3: Diagnóstico
| Hoje | Alvo |
| --- | --- |
| reatenvio duplica | dedup event_id |
| sem upsert | upsert |
| sem versão | etag |
## Slide 4: Decisão Arquitetural (ADR)
ADR-052: Idempotência
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| dedup event_id + upsert | exactly-once p/ negócio | store | ESCOLHIDA |
> Nota: At-least-once do broker + dedup no consumidor = exactly-once observacional.
## Slide 5: Entregas
IDEMPOTENCY.md.
idempotent.py.
schema_dedup.sql.
## Slide 6: Validação
Mesmo evento 3x -> 1 efeito.
Concorrência: 2 consumers, 1 aplicação.
DLQ não cria duplicata.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Duplicatas | 0 |
| Idempotente | 100% handlers |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Store cheio | TTL |
| Chave errada | event_id + negócio |
## Slide 9: Próximos Passos
Aplicar em todos os consumers.
Teste de concorrência no CI.