# STANDARD: Comunicacao com Stakeholders nao Tecnicos

Area: Automacao & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Principio

Stakeholder nao precisa entender como foi feito, precisa decidir o que fazer. Todo status responde 4 perguntas: o que foi entregue de valor, o que vem a seguir, o que pode dar errado (com plano) e do que preciso deles (com prazo).

## 2. Matriz de stakeholders (preencher com nomes reais)

| Stakeholder | Papel | Quer saber | Canal | Frequencia |
|---|---|---|---|---|
| [gestor direto] | prioriza e remove impedimento | risco, prazo, pedido | reuniao seg 9h + doc | semanal |
| [lider de operacao] | usa as entregas no dia a dia | data, workaround, mudanca de rotina | Slack + validacao | por entrega |
| [diretoria] | decide verba e prazo | impacto, risco vermelho, decisao | resumo mensal | mensal |
| [time de midia] | depende de dados e integracoes | disponibilidade dos dados | Slack | por entrega |
| [financeiro] | aprova custo de ferramenta | custo, alternativa | e-mail/doc | sob demanda |

## 3. Ritual semanal (segunda 9h, 30 min, pauta fixa)

1. **Feito** (5 min): valor entregue na semana passada, em linguagem de negocio. Proibido jargao.
2. **Proximo** (5 min): compromisso desta semana (do kanban, topo da fila).
3. **Riscos** (10 min): cada risco com semaforo, plano e dono (ver secao 4).
4. **Pedidos** (10 min): decisao ou ajuda necessaria, com prazo de resposta. Sem dono e sem prazo nao entra.

Doc do status enviado antes da reuniao. Reuniao decide, nao informa.

## 4. Semaforo de risco

- **Verde**: sob controle, monitorando. Ex.: API com limite confortavel.
- **Amarelo**: atencao, plano pronto. Ex.: token expira em 20 dias, renovacao agendada, dono nomeado.
- **Vermelho**: acao agora, decisao na mesa. Ex.: integracao pode parar sexta sem token novo, preciso de acesso ate quarta.

Regras: todo amarelo e vermelho tem plano + dono. Vermelho sem plano nao existe: se nao ha plano, o pedido da reuniao e ajuda para montar o plano. Risco novo entra no doc na hora.

## 5. Traducao tecnica para negocio (exemplos)

| Nao diga | Diga |
|---|---|
| Refatorei o extrator e subi o cron | Relatorio semanal passa a chegar sozinho toda segunda 8h |
| Webhook com 500, fiz rollback | Leads voltaram a entrar no CRM as 15:10; causa corrigida amanha |
| WIP estourado em Revisao | 3 entregas aguardando validacao da operacao; preciso de resposta ate quarta |
| Spike de 4h na API | Ate quinta digo se a integracao sai nesta ou na proxima semana |

## 6. Anti-padroes proibidos

1. Status so verbal, sem doc.
2. Jargao sem traducao ("deploy", "cron", "payload" sem explicar o efeito).
3. Risco citado sem plano nem dono.
4. Atraso avisado no dia (minimo 48h de antecedencia).
5. Pedido sem prazo de resposta ("quando puderem olhar").
