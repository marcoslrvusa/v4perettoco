# Template de Status + Risco (com exemplo preenchido)

## TEMPLATE

Semana: [ ] | Responsável: [ ] | Link do kanban: [ ]

Feito: [ ]
Próximo: [ ]
Riscos:
- [semáforo] [risco] | plano: [ ] | dono: [ ]
Pedidos:
- [nome] até [dia]: [pedido]

## EXEMPLO REAL: semana 01/09/2026

Semana: 01/09 a 05/09/2026 | Responsável: Marcos Luciano

Feito:
- Relatório semanal de campanhas passou a chegar sozinho no Slack toda segunda 8h (valores conferem com os painéis em 2 contas amostra).
- Webhook Meta Ads estabilizado após correção: leads fluindo sem represamento há 10 dias.

Próximo:
- Integração CRM fase 1 até sexta (faixa 4 a 6 dias úteis, centro sexta).
- Alerta de erro 500 no webhook até quarta (ação A1 do postmortem).

Riscos:
- Amarelo: token da API do CRM expira 25/09 | plano: renovação agendada com o responsável, fallback manual mapeado | dono: Marcos.
- Verde: limite da API Meta em 40% do uso, monitorando.

Pedidos:
- Líder de operação até quarta: validar os 3 campos novos do relatório (lista no doc) para eu fechar a fase 1.
- Gestor até quarta: acesso de leitura a conta nova do Google Ads (convite pendente no e-mail).
