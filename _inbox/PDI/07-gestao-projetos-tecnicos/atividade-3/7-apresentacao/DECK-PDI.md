# Deck PDI: Gestao de Incidentes e Postmortems sem Culpa

## Slide 1: Capa
Gestao de Incidentes e Postmortems sem Culpa: responder rapido, aprender sempre. Marcos Luciano, FV Marketing / V4 Company, Automacao & Infraestrutura, Setembro 2026.

## Slide 2: O problema
Automacao quebra e a resposta e improviso no Slack: sem lider, sem registro do que foi tentado, operacao no escuro. Depois, nenhum postmortem: o mesmo incidente volta meses depois.

## Slide 3: Caso real
18/08/2026: webhook Meta Ads com 500 apos deploy, 40 leads represados por 3h. Deteccao manual levou 40 min. Rollback salvou, mas nada registrava a licao.

## Slide 4: Severidades S1-S4
S1 campanha ou captacao parada, todos largam tudo. S2 degradacao com workaround, atualizacao horaria. S3 falha isolada, resolve no dia. S4 dor menor, resolve na semana.

## Slide 5: Papeis
Comandante coordena e comunica, sem teclado. Executor investiga e aplica. Comunicador atualiza a operacao a cada 30-60 min. Em S2, comandante acumula comunicacao.

## Slide 6: Ordem da resposta
Classificar, mitigar, comunicar, resolver, registrar. Mitigar (rollback, manual) vem antes de entender tudo. Parar o sangramento primeiro.

## Slide 7: Comunicacao pronta
3 frases modelo: abertura com impacto + workaround + proxima atualizacao; andamento com feito/falta/previsao; encerramento com causa e data do postmortem.

## Slide 8: Postmortem sem culpa
Proibido "erro humano" como causa. Estrutura: resumo, impacto com numero, timeline, 5 porques, funcionou/nao funcionou, acoes com dono e prazo.

## Slide 9: 5 porques do caso real
500 porque validacao rejeitou payload; porque sem teste com payload real; porque deploy manual sem smoke; porque sem checklist de deploy. 3 acoes nasceram dai.

## Slide 10: Acoes que andam
Toda acao vira cartao no kanban (S1/S2 como urgente), cobrada na review semanal ate Pronto. Postmortem lido em 15 min na review seguinte.

## Slide 11: Metricas
Mitigacao S1/S2: de 4h+ estimadas para 1h (meta). Postmortem em 5 dias: de 0% para 100% (meta). Acoes concluidas: 80% em 30 dias (meta).

## Slide 12: Proximos passos
Usar o checklist no proximo incidente real. Escrever o primeiro postmortem com o template. Colar severidades e contatos no canal do time.

## Slide 13: Fechamento
Incidente bem gerido custa horas; incidente repetido custa confianca. Sem culpa para aprender, com rigor para nao repetir.
