# Roteiro de Demo: Otimização de Core Web Vitals (LCP/INP/CLS) com Diagnóstico Real

Abra o deck (index.html) e percorra os slides na ordem.

## Pré-requisitos

- Acesso ao repositório da atividade e ao navegador com DevTools liberado.
- Chave da API de CrUX disponível para o script de coleta (variável de ambiente já configurada).
- Ambiente de laboratório capaz de simular dispositivo móvel e conexão lenta.
- Acesso ao banco provisionado para conferir a série histórica (somente leitura na demo).

## Seed e linha de base

1. **Rodar a coleta de linha de base.** Comando: `python 3-supabase/field_cwv.py`. Saída esperada: um objeto com `largest_contentful_paint`, `interaction_to_next_paint` e `cumulative_layout_shift` em p75. Critério de falha: exceção de autenticação ou resposta sem o objeto `record`. Se falhar: conferir a chave da API e repetir; sem linha de base, não iniciar a demo.

2. **Registrar a linha de base na tabela de histórico.** Comando: executar o `insert ... on conflict` do standard com os p75 coletados. Saída esperada: `INSERT 0 1` na primeira vez e `UPDATE 1` no reenvio. Critério de falha: duas linhas para a mesma (url, dia, formato, fonte). Se falhar: a chave única não existe; criar o índice e limpar a duplicata.

3. **Abrir a rota crítica no laboratório.** Comando: executar a auditoria de performance com dispositivo móvel. Saída esperada: pontuação baixa e elemento LCP nomeado na lista de oportunidades. Critério de falha: auditoria sem elemento LCP identificado. Se falhar: conferir se o elemento está no primeiro viewport.

## Demo dos slides

4. **Slide de Resumo:** abra com o problema de negócio e o blast radius. Fale os três números de campo (4,1 s, 410 ms, 0,22) antes de qualquer jargão. Critério de falha: público sem entender o tamanho do buraco. Se acontecer: volte ao slide do problema e repita a tabela sem os nomes das métricas.

5. **Slide do ADR:** defenda a opção escolhida vs as rejeitadas (trade-offs). Cite o ADR-034 e a alternativa descartada de corrigir as três métricas no mesmo ciclo. Critério de falha: pergunta "por que essa ordem?" sem resposta numérica. Se acontecer: cite a distância até o alvo: 1,6 s no LCP, 210 ms no INP, 0,12 no CLS.

6. **Slide de Matemática:** feche a conta de transferência. Comando: escrever no quadro `420 * 8 / 1600 = 2,1 s`. Saída esperada: conta fechada em segundos e ligação com o orçamento de bundle. Critério de falha: plateia sem conseguir ligar a conta com a técnica de code splitting. Se acontecer: refaça a conta citando o componente de chat que sai do bundle.

7. **Slide de Tradeoffs:** percorra a matriz linha a linha e diga explicitamente o que se aceitou perder em cada troca. Critério de falha: alguém apontar ganho sem custo. Se acontecer: reforce a linha da reserva de espaço: a área vazia breve é o preço do CLS baixo.

8. **Slide de Validação/Rollout:** mostre como provamos em produção. Apresente as três evidências obrigatórias: gate verde no CI, leitura de laboratório e confirmação em campo. Critério de falha: plateia achando que laboratório fecha a entrega. Se acontecer: volte ao slide que separa campo de laboratório.

9. **Slide de Riscos:** apresente o plano de mitigação. Fale dos dois riscos endêmicos: regressão silenciosa e origem sem amostra no CrUX. Critério de falha: risco sem detecção associada. Se acontecer: associe cada risco à linha da tabela de modos de falha.

10. **Slide de Modos de falha:** percorra o diagrama de recuperação e enfatize a ordem: mitigar, diagnosticar, publicar, confirmar. Critério de falha: plateia entendendo que o diagnóstico vem antes da mitigação. Se acontecer: repita a regra com um cenário de madrugada.

11. **Slide de Modelo de dados:** explique a chave única da ingestão e o motivo do índice BRIN. Saída esperada: público entendendo que a leitura do dashboard é sempre intervalo de tempo. Critério de falha: pergunta "por que não um índice B-tree no tempo?" sem resposta. Se acontecer: cite custo de escrita e ordenação física da tabela.

12. **Slide de Métricas e SLO:** feche com o SLI, a meta de 75% das sessões e a janela de 28 dias. Critério de falha: plateia sem saber qual número é medido em qual janela. Se acontecer: repita: p75 rolante, 28 dias, por formato de aparelho.

13. **Slide de Entregas:** abra `cwv_fixes.html` e mostre as quatro linhas que resolvem os três sintomas: `preconnect`, `fetchpriority` no herói, `aspect-ratio` no card e o clique com fatiamento de trabalho. Saída esperada: HTML de 7 linhas legível na tela. Critério de falha: público sem conseguir mapear linha para métrica. Se acontecer: leia cada linha apontando a métrica que ela resolve.

14. **Slide de Próximos Passos:** feche com Lighthouse CI no pipeline e RUM de INP por rota, mais o checklist de domínio. Critério de falha: saída sem dono e sem prazo. Se acontecer: assigne o gate de CI e o RUM por rota a responsáveis nomeados.

## Verificação ao vivo (opcional, se houver ambiente)

15. **Demonstrar o gate falhando.** Comando: remover `priority` da imagem herói, submeter a mudança e rodar o pipeline. Saída esperada: asserção de orçamento em vermelho. Critério de falha: pipeline verde com a regressão plantada. Se falhar: a asserção não está ativa; corrigir o CI antes de qualquer outra demonstração.

16. **Demonstrar a leitura de histórico.** Comando: consultar a tendência de 28 dias com a consulta do standard. Saída esperada: uma linha por dia com status `bom` ou `fora do limite`. Critério de falha: datas repetidas ou dias ausentes não sinalizados. Se falhar: conferir a chave única e o job de coleta.

17. **Demonstrar a paginação por cursor.** Comando: pedir a primeira página de 50 eventos e depois a seguinte usando o último identificador retornado. Saída esperada: nenhuma repetição entre páginas. Critério de falha: item repetido ou sumiço. Se falhar: o endpoint está usando `offset`; trocar por chave composta.

18. **Demonstrar o idempotência da ingestão.** Comando: enviar o mesmo lote duas vezes. Saída esperada: segunda chamada não altera a contagem de eventos. Critério de falha: contagem dobrada. Se falhar: falta a chave única de conflito na tabela.

19. **Demonstrar rollback.** Comando: aplicar a regressão plantada e reverter o deploy. Saída esperada: rota volta ao orçamento em uma execução. Critério de falha: recuperação exigindo mais de um ciclo. Se falhar: documentar o procedimento real de rollback e refazer a demo só depois.

20. **Fechar com a confirmação de campo.** Comando: rodar novamente `python 3-supabase/field_cwv.py` e comparar com a linha de base congelada. Saída esperada: comparação explícita antes e depois, com a janela declarada. Critério de falha: comparação sem janela de 28 dias declarada. Se falhar: não declare vitória; a entrega continua aberta.

## Rollback da demo

- Qualquer demonstração plantada é revertida no mesmo dia, antes de encerrar a sessão.
- A linha de base original nunca é sobrescrita: a comparação usa a linha congelada no passo 1.
- Se a reversão falhar, o estado passa a ser incidente e segue o runbook do README (mitigar primeiro, diagnosticar depois).

Material de apoio: pdi-fullstack-modelagem-dados-a4-report.pdf (dossiê completo).
