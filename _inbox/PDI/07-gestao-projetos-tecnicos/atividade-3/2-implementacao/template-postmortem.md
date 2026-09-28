# Template de Postmortem (com exemplo real preenchido)

Preencha em até 5 dias úteis. Tom blameless: sistemas e condições, nunca pessoas.

## TEMPLATE

Título: [POSTMORTEM S_/data/resumo] | Severidade: [S1-S4] | Data do incidente: [ ] | Autor: [ ]

1. Resumo (3 linhas): [o que quebrou, impacto, como voltou]
2. Impacto: [leads/campanhas/horas afetadas, com número]
3. Timeline (hora + fato):
4. Causa raiz (5 porquês):
5. O que funcionou:
6. O que não funcionou:
7. Ações (dono + prazo + cartão):

## EXEMPLO REAL: webhook de leads Meta Ads fora do ar

Título: POSTMORTEM S1 18/08/2026: webhook Meta Ads fora do ar | Severidade: S1 | Autor: Marcos Luciano

1. Resumo: o endpoint de webhook passou a responder 500 após deploy de validação de campo. Leads do formulário Meta ficaram 3h sem entrar no CRM. Mitigado com rollback do deploy; resolvido com correção da validação + teste.
2. Impacto: cerca de 40 leads represados por 3h (estimativa pelo volume médio do horário), nenhuma campanha pausada, follow-up atrasado em 1 turno.
3. Timeline:
   - 14:05 deploy da versão com validação nova
   - 14:40 alerta manual da operação (lead teste não chegou)
   - 14:50 S1 declarado, canal dedicado, comandante assumiu
   - 15:10 rollback executado, leads voltaram a fluir
   - 17:10 fila represada processada e validada com a operação
   - 19/08 correção definitiva + teste deployado
4. Causa raiz (5 porquês): leads não entraram porque o endpoint deu 500; porque a validação nova rejeitava payload sem campo opcional; porque não havia teste com payload real da Meta; porque deploy era manual sem suíte de smoke; porque não existia checklist de deploy.
5. O que funcionou: rollback rápido (código anterior versionado), canal dedicado, comunicação a cada 30 min acalmou a operação.
6. O que não funcionou: detecção manual (40 min no escuro), sem alerta de erro 500, sem teste com payload real.
7. Ações:
   - A1: alerta de erro 500 no webhook (dono: Marcos, prazo 7 dias)
   - A2: teste com 3 payloads reais da Meta no pipeline (dono: Marcos, prazo 14 dias)
   - A3: checklist de deploy de automações (dono: Marcos, prazo 7 dias)
