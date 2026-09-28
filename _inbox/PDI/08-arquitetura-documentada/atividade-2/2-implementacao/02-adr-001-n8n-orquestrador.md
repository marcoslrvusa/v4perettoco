# ADR-001: n8n Self-Hosted como Orquestrador

- **Status:** Implementada
- **Data:** 2026-03-14
- **Autor:** Marcos Luciano
- **Decisores:** Marcos Luciano, lideranca FV Marketing

## Contexto

Em marco de 2026 a operacao rodava automacoes em scripts soltos e planilhas, sem retry, sem log central e sem visibilidade de falha. Uma coleta quebrada de Meta Ads so aparecia quando o relatorio de verba saia furado. O time tinha 1 pessoa tecnica e previsao de 3 contas novas por mes.

## Decisao

Adotar n8n self-hosted na VPS como orquestrador, com workers Python para coleta pesada via webhook.

## Alternativas consideradas

- Fila propria em Python com Celery: potente e sem licenca, mas exigia 3 semanas de obra sem UI de operacao.
- Planilha com Apps Script: custo zero e imediato, mas sem log, sem retry e com edicao manual concorrente.

## Consequencias

- Ganhamos: UI de operacao, retry nativo, credenciais em cofre e historico de execucao.
- Perdemos: mais um container para operar e versionar fluxos fora do git por padrao.
- Vamos monitorar: taxa de falha de coleta por conta em 24h, alerta acima de 5 por cento.
