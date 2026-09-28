# STANDARD: Comunicação com Stakeholders não Técnicos

Área: Automação & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Princípio

Stakeholder não precisa entender como foi feito, precisa decidir o que fazer. Todo status responde 4 perguntas: o que foi entregue de valor, o que vem a seguir, o que pode dar errado (com plano) e do que preciso deles (com prazo).

## 2. Matriz de stakeholders (preencher com nomes reais)

| Stakeholder | Papel | Quer saber | Canal | Frequência |
|---|---|---|---|---|
| [gestor direto] | prioriza e remove impedimento | risco, prazo, pedido | reunião seg 9h + doc | semanal |
| [líder de operação] | usa as entregas no dia a dia | data, workaround, mudança de rotina | Slack + validação | por entrega |
| [diretoria] | decide verba e prazo | impacto, risco vermelho, decisão | resumo mensal | mensal |
| [time de mídia] | depende de dados e integrações | disponibilidade dos dados | Slack | por entrega |
| [financeiro] | aprova custo de ferramenta | custo, alternativa | e-mail/doc | sob demanda |

## 3. Ritual semanal (segunda 9h, 30 min, pauta fixa)

1. **Feito** (5 min): valor entregue na semana passada, em linguagem de negócio. Proibido jargão.
2. **Próximo** (5 min): compromisso desta semana (do kanban, topo da fila).
3. **Riscos** (10 min): cada risco com semáforo, plano e dono (ver seção 4).
4. **Pedidos** (10 min): decisão ou ajuda necessária, com prazo de resposta. Sem dono e sem prazo não entra.

Doc do status enviado antes da reunião. Reunião decide, não informa.

## 4. Semáforo de risco

- **Verde**: sob controle, monitorando. Ex.: API com limite confortável.
- **Amarelo**: atenção, plano pronto. Ex.: token expira em 20 dias, renovação agendada, dono nomeado.
- **Vermelho**: ação agora, decisão na mesa. Ex.: integração pode parar sexta sem token novo, preciso de acesso até quarta.

Regras: todo amarelo e vermelho tem plano + dono. Vermelho sem plano não existe: se não há plano, o pedido da reunião e ajuda para montar o plano. Risco novo entra no doc na hora.

## 5. Tradução técnica para negócio (exemplos)

| Não diga | Diga |
|---|---|
| Refatorei o extrator e subi o cron | Relatório semanal passa a chegar sozinho toda segunda 8h |
| Webhook com 500, fiz rollback | Leads voltaram a entrar no CRM as 15:10; causa corrigida amanhã |
| WIP estourado em Revisão | 3 entregas aguardando validação da operação; preciso de resposta até quarta |
| Spike de 4h na API | Até quinta digo se a integração sai nesta ou na próxima semana |

## 6. Anti-padroes proibidos

1. Status só verbal, sem doc.
2. Jargão sem tradução ("deploy", "cron", "payload" sem explicar o efeito).
3. Risco citado sem plano nem dono.
4. Atraso avisado no dia (mínimo 48h de antecedência).
5. Pedido sem prazo de resposta ("quando puderem olhar").
