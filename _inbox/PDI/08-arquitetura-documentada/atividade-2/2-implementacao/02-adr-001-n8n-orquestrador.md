# ADR-001: n8n Self-Hosted como Orquestrador

- **Status:** Implementada
- **Data:** 2026-03-14
- **Autor:** Marcos Luciano
- **Decisores:** Marcos Luciano, liderança FV Marketing

## Contexto

Em março de 2026 a operação rodava automações em scripts soltos e planilhas, sem retry, sem log central e sem visibilidade de falha. Uma coleta quebrada de Meta Ads só aparecia quando o relatório de verba saía furado. O time tinha 1 pessoa técnica e previsão de 3 contas novas por mês.

## Decisão

Adotar n8n self-hosted na VPS como orquestrador, com workers Python para coleta pesada via webhook.

## Alternativas consideradas

- Fila própria em Python com Celery: potente e sem licença, mas exigia 3 semanas de obra sem UI de operação.
- Planilha com Apps Script: custo zero e imediato, mas sem log, sem retry e com edição manual concorrente.

## Consequências

- Ganhamos: UI de operação, retry nativo, credenciais em cofre e histórico de execução.
- Perdemos: mais um container para operar e versionar fluxos fora do git por padrão.
- Vamos monitorar: taxa de falha de coleta por conta em 24h, alerta acima de 5 por cento.
