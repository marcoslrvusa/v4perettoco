# Roteiro de Demo: Engenharia de Custos de LLM (custo por tarefa, cache, roteamento)

Abra o deck (index.html) e percorra os slides na ordem.

Pré-requisitos: navegador com acesso ao `index.html` da pasta `7-apresentacao/`, terminal na raiz
da atividade e acesso de leitura ao banco onde está a tabela `llm_usage`. Se qualquer pré-requisito
faltar, faça a parte conceitual e deixe a parte de dado para depois, sem inventar número.

Seed de demonstração (parâmetros declarados, sem tocar em produção): 12 execuções de exemplo com
500 tokens de entrada e 200 de saída, intenções mistas `triagem` e `proposta`. Rollback: apagar
as linhas de teste criadas com a marcação `agent = 'demo_a4'`.

1. Slide de Resumo: abra com o problema de negócio e o blast radius. Saída esperada: a frase
   "sem contabilidade de tokens, não se precifica o agente" na tela. Critério de falha: se a
   pergunta do público não for respondida em 30 segundos, volte ao Slide 2 e refaça o diagnóstico
   antes de seguir.
2. Slide do Contexto: mostre os três sintomas (modelo único, sem cache, custo invisível). Saída
   esperada: o público identifica qual dos três mais dói no dia a dia dele.
3. Slide do Diagnóstico: tabela Hoje x Alvo. Saída esperada: três linhas lidas em voz alta,
   cada uma com um custo associado.
4. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs). Saída esperada: o
   público entende por que "só cache" e "só roteamento" foram descartadas.
5. Slide do Modelo mental: explique a ordem roteamento, cache, chamada, contabilidade. Critério
   de falha: se alguém perguntar "por que não cache primeiro?", responda com o custo da
   classificação paga no caminho caro.
6. Slide da Arquitetura: percorra o `flowchart` etapa por etapa. Saída esperada: o público
   consegue apontar onde o PII é barrado.
7. Execução ao vivo do calculador no terminal: `python3 2-code/cost_calc.py`. Saída esperada:
   dois valores impressos, um diferente de zero (miss) e outro igual a zero (hit). Critério de
   falha: se os dois forem iguais, o `cache_hit` não está sendo aplicado; confira a assinatura
   de `cost(task, cache_hit=True)`.
8. Rodada do track de custo: rode o cálculo de `track_cost.py` para um modelo conhecido e para
   um modelo fora da tabela. Saída esperada: o modelo conhecido com preço e o desconhecido caindo
   no fallback. Critério de falha: se o desconhecido retornar zero, o fallback está errado e o
   alerta de preço ausente não dispararia.
9. Slide de Matemática: mostre as duas contas (mini e maxi) e a razão de 23.1x. Saída esperada:
   o público acompanha a conta no quadro, com os parâmetros declarados.
10. Consulta do mix por modelo: rode a consulta de `agent`, `model`, contagem e soma de `cost_usd`
    do standard de monitoramento. Saída esperada: linhas agrupadas, ordenadas por custo. Critério
    de falha: se a consulta falhar por coluna inexistente, o esquema não foi aplicado; aplique
    `3-supabase/usage_schema.sql` em ambiente de teste antes de continuar.
11. Consulta de hit rate por fluxo: rode a agregação de `from_cache` por `agent`. Saída esperada:
    uma razão entre 0 e 1 por fluxo. Critério de falha: se a coluna não existir, acrescente
    `from_cache boolean not null default false` e regenere o seed.
12. Slide do Pipeline: percorra as cinco etapas com o custo de cada uma. Saída esperada: o
    público vê que a etapa 5 (contabilidade) é a única que sempre roda.
13. Slide do Antes vs Depois: tabela de quatro linhas. Saída esperada: comparação lida por
    coluna, sem ler a tabela inteira.
14. Simulação de budget: rode a consulta de razão de consumo por cliente com teto de teste.
    Saída esperada: razão calculada. Critério de falha: se retornar nulo, o teto não está
    configurado; não siga para o alerta sem configurar, porque teto ausente não é consumo livre.
15. Simulação de alerta em 80%: suba o consumo de teste até `razao >= 0.80` e confirme o aviso.
    Saída esperada: exatamente um alerta entregue. Critério de falha: se chegar mais de um
    aviso, a idempotência do alerta está quebrada.
16. Simulação de bloqueio em 100%: leve ao teto e confirme a pausa de agentes não-críticos.
    Saída esperada: agentes críticos ativos e não-críticos pausados. Critério de falha: se o
    agente crítico parar, revise a lista versionada de agentes não-críticos.
17. Slide dos Riscos: apresente o plano de mitigação. Saída esperada: duas linhas de risco com
    detecção e mitigation nomeadas.
18. Slide dos Modos de falha: mostre a tabela de sintoma, detecção, mitigação e recuperação.
    Saída esperada: o público escolhe uma falha e você descreve o rollback na hora.
19. Rollback ao vivo (ambiente de teste): desligue as flags de cache e de roteamento, nessa
    ordem. Saída esperada: o sistema volta a comportar como modelo único, sem erro. Critério de
    falha: se houver migração pendente, pare; rollback desse padrão não envolve migração de dado.
20. Slide de Validação: liste os critérios de aceite por item. Saída esperada: cada critério com
    a forma de prova correspondente.
21. Slide de Métricas e SLO: leia os três SLI com janela e ação. Saída esperada: meta, janela e
    o que fazer quando estoura, nessa ordem.
22. Slide de Esforço: apresente as horas com a marcação de projeção. Critério de falha: se
    algum número for apresentado como medição, corrija na hora; são projeções de esforço.
23. Slide de Impacto no negócio: feche com preço por tarefa, margem auditável e preço conhecido
    antes de decisão de arquitetura.
24. Limpeza do seed: apague as linhas com `agent = 'demo_a4'` e desligue as flags de teste.
    Saída esperada: ledger de produção sem resíduo de demonstração.
25. Encerramento: abra para perguntas usando o ROTEIRO-DOMINIO.md como lista de defesa.

Material de apoio: pdi-engenharia-ia-rag-vetores-a4-report.pdf (dossiê completo).
