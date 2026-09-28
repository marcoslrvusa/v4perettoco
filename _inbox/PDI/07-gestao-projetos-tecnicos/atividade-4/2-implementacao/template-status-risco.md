# Template de Status + Risco (com exemplo preenchido)

## TEMPLATE

Semana: [ ] | Responsavel: [ ] | Link do kanban: [ ]

Feito: [ ]
Proximo: [ ]
Riscos:
- [semaforo] [risco] | plano: [ ] | dono: [ ]
Pedidos:
- [nome] ate [dia]: [pedido]

## EXEMPLO REAL: semana 01/09/2026

Semana: 01/09 a 05/09/2026 | Responsavel: Marcos Luciano

Feito:
- Relatorio semanal de campanhas passou a chegar sozinho no Slack toda segunda 8h (valores conferem com os paineis em 2 contas amostra).
- Webhook Meta Ads estabilizado apos correcao: leads fluindo sem represamento ha 10 dias.

Proximo:
- Integracao CRM fase 1 ate sexta (faixa 4 a 6 dias uteis, centro sexta).
- Alerta de erro 500 no webhook ate quarta (acao A1 do postmortem).

Riscos:
- Amarelo: token da API do CRM expira 25/09 | plano: renovacao agendada com o responsavel, fallback manual mapeado | dono: Marcos.
- Verde: limite da API Meta em 40% do uso, monitorando.

Pedidos:
- Lider de operacao ate quarta: validar os 3 campos novos do relatorio (lista no doc) para eu fechar a fase 1.
- Gestor ate quarta: acesso de leitura a conta nova do Google Ads (convite pendente no e-mail).
