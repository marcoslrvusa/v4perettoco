# STANDARD: Gestão de Incidentes e Postmortems sem Culpa

Área: Automação & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Severidades

| Sev | Definição | Exemplo na FV | Resposta |
|---|---|---|---|
| S1 | Campanha ou captação parada | leads não entram no CRM há 1h+ | todos largam tudo, comandante + canal dedicado |
| S2 | Degradação forte com workaround | relatório semanal não enviado, dado manual disponível | comandante + 1 executor, atualização a cada 1h |
| S3 | Falha isolada sem impacto em campanha | 1 conta com erro no extrator | cartão urgente no kanban, resolve no dia |
| S4 | Dor menor, sem impacto operacional | log com ruído, alerta falso | cartão padrão, resolve na semana |

Na dúvida entre duas, use a maior e rebaixe depois com registro.

## 2. Papéis (S1/S2)

- **Comandante**: coordena, decide e comunica. Não mexe no teclado (evita túnel técnico).
- **Executor**: investiga e aplica a mitigacao/correcao.
- **Comunicador** (S1): atualiza a operação no canal a cada 30-60 min. Pode acumular com comandante em S2.

## 3. Resposta em ordem

1. **Detectar e classificar**: sintoma, desde quando, impacto, severidade.
2. **Mitigar**: parar o sangramento (rollback, desligar automação, trocar para manual). Mitigação não é correção.
3. **Comunicar**: operação avisada com impacto + workaround + próxima atualização.
4. **Resolver**: corrigir a causa e validar com o usuário afetado.
5. **Registrar**: timeline mínima (hora dos 4 passos) no dia, postmortem completo em até 5 dias úteis.

## 4. Postmortem sem culpa: regras

1. Proibido "erro humano" ou nome de culpado como causa. Pergunte que condição permitiu o erro (falta de teste, deploy manual, alerta inexistente).
2. Estrutura obrigatória: resumo, impacto (leads, campanhas, horas), timeline, causa raiz (5 porquês), o que funcionou, o que não funcionou, ações.
3. Toda ação tem dono único e prazo. Ação sem dono vira cartão sem dono: não anda.
4. Ações entram no kanban (S1/S2 como urgente) e são cobradas na review semanal até Pronto.
5. Postmortem e lido pelo time em 15 min na review seguinte. Aprendizado não compartilhado não existe.

## 5. Anti-padroes proibidos

1. Debugar 2h sem avisar a operação.
2. Mitigação sem registro de hora (timeline furada).
3. Postmortem com causa "falha humana" e ação "ter mais atenção".
4. Ação de postmortem sem prazo nem dono.
5. Mesmo incidente repetindo sem que o postmortem anterior seja reaberto.
