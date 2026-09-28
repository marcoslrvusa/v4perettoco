# STANDARD: Gestao de Incidentes e Postmortems sem Culpa

Area: Automacao & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Severidades

| Sev | Definicao | Exemplo na FV | Resposta |
|---|---|---|---|
| S1 | Campanha ou captacao parada | leads nao entram no CRM ha 1h+ | todos largam tudo, comandante + canal dedicado |
| S2 | Degradacao forte com workaround | relatorio semanal nao enviado, dado manual disponivel | comandante + 1 executor, atualizacao a cada 1h |
| S3 | Falha isolada sem impacto em campanha | 1 conta com erro no extrator | cartao urgente no kanban, resolve no dia |
| S4 | Dor menor, sem impacto operacional | log com ruido, alerta falso | cartao padrao, resolve na semana |

Na duvida entre duas, use a maior e rebaixe depois com registro.

## 2. Papeis (S1/S2)

- **Comandante**: coordena, decide e comunica. Nao mexe no teclado (evita tunel tecnico).
- **Executor**: investiga e aplica a mitigacao/correcao.
- **Comunicador** (S1): atualiza a operacao no canal a cada 30-60 min. Pode acumular com comandante em S2.

## 3. Resposta em ordem

1. **Detectar e classificar**: sintoma, desde quando, impacto, severidade.
2. **Mitigar**: parar o sangramento (rollback, desligar automacao, trocar para manual). Mitigacao nao e correcao.
3. **Comunicar**: operacao avisada com impacto + workaround + proxima atualizacao.
4. **Resolver**: corrigir a causa e validar com o usuario afetado.
5. **Registrar**: timeline minima (hora dos 4 passos) no dia, postmortem completo em ate 5 dias uteis.

## 4. Postmortem sem culpa: regras

1. Proibido "erro humano" ou nome de culpado como causa. Pergunte que condicao permitiu o erro (falta de teste, deploy manual, alerta inexistente).
2. Estrutura obrigatoria: resumo, impacto (leads, campanhas, horas), timeline, causa raiz (5 porques), o que funcionou, o que nao funcionou, acoes.
3. Toda acao tem dono unico e prazo. Acao sem dono vira cartao sem dono: nao anda.
4. Acoes entram no kanban (S1/S2 como urgente) e sao cobradas na review semanal ate Pronto.
5. Postmortem e lido pelo time em 15 min na review seguinte. Aprendizado nao compartilhado nao existe.

## 5. Anti-padroes proibidos

1. Debugar 2h sem avisar a operacao.
2. Mitigacao sem registro de hora (timeline furada).
3. Postmortem com causa "falha humana" e acao "ter mais atencao".
4. Acao de postmortem sem prazo nem dono.
5. Mesmo incidente repetindo sem que o postmortem anterior seja reaberto.
