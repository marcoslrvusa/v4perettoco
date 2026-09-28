# Planilha de Estimativa (template + exemplo real)

Como usar: copie o bloco TEMPLATE para cada nova entrega. O EXEMPLO mostra a automação "Relatório semanal de campanhas FV" já preenchida.

## TEMPLATE

Entrega: [nome] | Data: [data] | Fase: [conceito | requisitos | design] | Estimador: [nome]

| # | Pacote | Pronto quando | O (h) | M (h) | P (h) | E = (O+4M+P)/6 |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

- Soma dos E: [ ]h
- Buffer (20%): [ ]h
- Compromisso: [soma + buffer]h = [ ] dias úteis (6h produtivas/dia)
- Faixa do cone (fase atual): [ ] a [ ] dias úteis
- Premissas: 1) [ ] 2) [ ] 3) [ ]
- Fora de escopo: 1) [ ] 2) [ ]

## EXEMPLO REAL: Relatório semanal de campanhas FV

Entrega: automação que consolida gasto e leads de Meta Ads e Google Ads e envia resumo no Slack toda segunda 8h | Fase: requisitos aprovados | Estimador: Marcos Luciano

| # | Pacote | Pronto quando | O (h) | M (h) | P (h) | E |
|---|---|---|---|---|---|---|
| 1 | Mapear contas e credenciais de API | lista de contas + token valido testado | 1 | 2 | 4 | 2,2 |
| 2 | Extrator Meta Ads (gasto, impressões, leads) | script roda e salva CSV com 7 dias | 2 | 4 | 8 | 4,3 |
| 3 | Extrator Google Ads (mesmos campos) | script roda e salva CSV com 7 dias | 2 | 3 | 6 | 3,3 |
| 4 | Consolidação + regras (nomes, moeda, fuso) | planilha final confere com painel em 2 contas amostra | 2 | 4 | 6 | 4,0 |
| 5 | Envio Slack + agendamento segunda 8h | mensagem de teste recebida no canal + cron ativo | 1 | 2 | 3 | 2,0 |
| 6 | Doc de operação + rollback | README com como rodar, falhar e desligar | 1 | 1 | 2 | 1,2 |

- Soma dos E: 17,0h
- Buffer (20%): 3,4h
- Compromisso: 20,4h = 3,5 dias úteis (arredonda para 4 dias)
- Faixa do cone (requisitos aprovados, 0,5x a 2x): 2 a 7 dias úteis. Comunicado: "entre 2 e 7 dias úteis, centro em 4".
- Premissas: 1) tokens de API com acesso de leitura já liberados 2) canal Slack existe e bot tem permissão de post 3) servidor com cron disponível
- Fora de escopo: 1) dashboard visual (só texto no Slack) 2) alerta em tempo real (só resumo semanal) 3) reconciliação com CRM
