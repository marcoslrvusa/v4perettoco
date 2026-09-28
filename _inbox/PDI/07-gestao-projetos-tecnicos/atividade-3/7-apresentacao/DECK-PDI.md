# Deck PDI: Gestão de Incidentes e Postmortems sem Culpa

## Slide 1: Capa
Gestão de Incidentes e Postmortems sem Culpa: responder rápido, aprender sempre. Marcos Luciano, FV Marketing / V4 Company, Automação & Infraestrutura, Setembro 2026.

## Slide 2: O problema
Automação quebra e a resposta e improviso no Slack: sem líder, sem registro do que foi tentado, operação no escuro. Depois, nenhum postmortem: o mesmo incidente volta meses depois.

## Slide 3: Caso real
18/08/2026: webhook Meta Ads com 500 após deploy, 40 leads represados por 3h. Detecção manual levou 40 min. Rollback salvou, mas nada registrava a lição.

## Slide 4: Severidades S1-S4
S1 campanha ou captação parada, todos largam tudo. S2 degradação com workaround, atualização horária. S3 falha isolada, resolve no dia. S4 dor menor, resolve na semana.

## Slide 5: Papéis
Comandante coordena e comunica, sem teclado. Executor investiga e aplica. Comunicador atualiza a operação a cada 30-60 min. Em S2, comandante acumula comunicação.

## Slide 6: Ordem da resposta
Classificar, mitigar, comunicar, resolver, registrar. Mitigar (rollback, manual) vem antes de entender tudo. Parar o sangramento primeiro.

## Slide 7: Comunicação pronta
3 frases modelo: abertura com impacto + workaround + próxima atualização; andamento com feito/falta/previsao; encerramento com causa e data do postmortem.

## Slide 8: Postmortem sem culpa
Proibido "erro humano" como causa. Estrutura: resumo, impacto com número, timeline, 5 porquês, funcionou/não funcionou, ações com dono e prazo.

## Slide 9: 5 porquês do caso real
500 porque validação rejeitou payload; porque sem teste com payload real; porque deploy manual sem smoke; porque sem checklist de deploy. 3 ações nasceram daí.

## Slide 10: Ações que andam
Toda ação vira cartão no kanban (S1/S2 como urgente), cobrada na review semanal até Pronto. Postmortem lido em 15 min na review seguinte.

## Slide 11: Métricas
Mitigação S1/S2: de 4h+ estimadas para 1h (meta). Postmortem em 5 dias: de 0% para 100% (meta). Ações concluídas: 80% em 30 dias (meta).

## Slide 12: Próximos passos
Usar o checklist no próximo incidente real. Escrever o primeiro postmortem com o template. Colar severidades e contatos no canal do time.

## Slide 13: Fechamento
Incidente bem gerido custa horas; incidente repetido custa confiança. Sem culpa para aprender, com rigor para não repetir.
