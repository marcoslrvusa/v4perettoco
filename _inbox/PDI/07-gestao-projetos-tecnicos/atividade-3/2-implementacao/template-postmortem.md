# Template de Postmortem (com exemplo real preenchido)

Preencha em ate 5 dias uteis. Tom blameless: sistemas e condicoes, nunca pessoas.

## TEMPLATE

Titulo: [POSTMORTEM S_/data/resumo] | Severidade: [S1-S4] | Data do incidente: [ ] | Autor: [ ]

1. Resumo (3 linhas): [o que quebrou, impacto, como voltou]
2. Impacto: [leads/campanhas/horas afetadas, com numero]
3. Timeline (hora + fato):
4. Causa raiz (5 porques):
5. O que funcionou:
6. O que nao funcionou:
7. Acoes (dono + prazo + cartao):

## EXEMPLO REAL: webhook de leads Meta Ads fora do ar

Titulo: POSTMORTEM S1 18/08/2026: webhook Meta Ads fora do ar | Severidade: S1 | Autor: Marcos Luciano

1. Resumo: o endpoint de webhook passou a responder 500 apos deploy de validacao de campo. Leads do formulario Meta ficaram 3h sem entrar no CRM. Mitigado com rollback do deploy; resolvido com correcao da validacao + teste.
2. Impacto: cerca de 40 leads represados por 3h (estimativa pelo volume medio do horario), nenhuma campanha pausada, follow-up atrasado em 1 turno.
3. Timeline:
   - 14:05 deploy da versao com validacao nova
   - 14:40 alerta manual da operacao (lead teste nao chegou)
   - 14:50 S1 declarado, canal dedicado, comandante assumiu
   - 15:10 rollback executado, leads voltaram a fluir
   - 17:10 fila represada processada e validada com a operacao
   - 19/08 correcao definitiva + teste deployado
4. Causa raiz (5 porques): leads nao entraram porque o endpoint deu 500; porque a validacao nova rejeitava payload sem campo opcional; porque nao havia teste com payload real da Meta; porque deploy era manual sem suite de smoke; porque nao existia checklist de deploy.
5. O que funcionou: rollback rapido (codigo anterior versionado), canal dedicado, comunicacao a cada 30 min acalmou a operacao.
6. O que nao funcionou: deteccao manual (40 min no escuro), sem alerta de erro 500, sem teste com payload real.
7. Acoes:
   - A1: alerta de erro 500 no webhook (dono: Marcos, prazo 7 dias)
   - A2: teste com 3 payloads reais da Meta no pipeline (dono: Marcos, prazo 14 dias)
   - A3: checklist de deploy de automacoes (dono: Marcos, prazo 7 dias)
