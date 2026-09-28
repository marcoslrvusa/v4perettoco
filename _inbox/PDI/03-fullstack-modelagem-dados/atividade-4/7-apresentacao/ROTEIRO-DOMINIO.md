# ROTEIRO-DOMINIO: Otimização de Core Web Vitals (LCP/INP/CLS)

11 perguntas de coordenador + respostas curtas para defesa da atividade 4.

## 1. Por que otimizar LCP primeiro e deixar CLS por último?

ADR-034, ordem por ROI: LCP de 4,1s afasta mais usuário e pesa mais no ranqueamento que o deslocamento de layout. CLS continua um ciclo, mas o ganho de LCP compensa primeiro.

Aprofundamento se insistirem: são três frentes em janela de 28 dias. Se as três mudarem no mesmo ciclo, o campo não consegue separar efeito de causa. Uma frente por release preserva a capacidade de atribuição.

## 2. Por que medir no CrUX e não só no Lighthouse?

Lighthouse e laboratório: ambiente controlado que não captura gargalo real de dispositivo e rede. O CrUX traz campo (p75, janela de 28 dias); o script `field_cwv.py` coleta o baseline e o laboratório guia o dia a dia.

Aprofundamento: laboratório responde "o que este commit quebrou", campo responde "o que o usuário sentiu". O pipeline usa as duas coisas com papéis diferentes: gate em CI para regressão, campo para veredito.

## 3. Qual foi a causa do LCP em 4,1s e a correção?

Hero sem `fetchpriority` nem preconnect, imagem pesada sem formato moderno. Correção: `next/image` com `priority` só no hero, preconnect nas origens e AVIF.

Aprofundamento: a decomposição é $LCP = TTFB + t_{fetch} + t_{decode/render}$. A correção ataca os dois últimos termos; se o TTFB estiver acima de 800 ms, o próximo ciclo é de servidor (cache e render), e isso fica registrado como pendência.

## 4. Qual foi a causa do INP em 410ms e a correção?

Handler síncrono bloqueando a thread no clique. Correção: dynamic import com code splitting por rota para tirar chat e mapa do caminho crítico, mais debounce nas ações.

Aprofundamento: acima de 50 ms a task já é `long task` e bloqueia entradas seguintes. O trabalho é fatiado em blocos de 8 ms com `yield` entre eles, e o orçamento de 200 ms é repartido em atraso de entrada, processamento e apresentação.

## 5. Como evitam regressão depois de atingir as metas?

Budget no CI barra regressão a cada merge, RUM próprio cobre rotas com pouco volume no CrUX, e a re-medição de campo confirma LCP até 2,5s, INP até 200ms e CLS até 0,1 em 75% das sessões.

Aprofundamento: o orçamento é asserção de pipeline, não relatório. Se a asserção não falhar com uma regressão plantada, ela não vale como proteção, e por isso o teste do gate com commit proposital ruim entra no checklist.

## 6. E se isso cair no meio da noite, o que acontece?

O detecta é o alerta de p75 cruzando o limite e o gate do pipeline. A ação é mitigar primeiro: rollback do deploy ou desligamento da feature responsável, em minutos, sem discussão de causa nesse momento. Diagnóstico (diff de HTML, perfil de `long task`, sessão de CLS) vem só depois, com o ambiente estável.

A ordem não é negociável: mitigar, diagnosticar, publicar com gate verde e confirmar em campo. Quem decide o rollback é quem responde pela experiência naquele plantão, não quem escreveu o commit.

## 7. Qual é o SLO e o que acontece quando ele estoura?

SLO: p75 de LCP até 2,5 s, INP até 200 ms e CLS até 0,1, medido em campo na janela rolante de 28 dias, com meta de 75% das sessões nas três métricas ao mesmo tempo.

Ao estourar: abrir ocorrência, identificar a rota e o último deploy que tocou nela, mitigar e só então diagnosticar. Orçamento de erro (meta): no máximo 1 rota em regressão por release e nenhuma persistindo por mais de 2 releases sem plano.

## 8. Como você prova que funciona, além de dizer que melhorou?

Três evidências obrigatórias e independentes: gate verde no CI, leitura de laboratório com elemento LCP e `long task` dentro do alvo, e comparação de campo contra a linha de base congelada, com a janela de 28 dias declarada.

Toda métrica publicada indica fonte (campo ou laboratório), formato de aparelho e janela. Sem os três, o número não entra no relatório.

## 9. Qual é a alternativa mais barata que você descartou e por quê?

Mais barata em esforço: só acelerar com cache agressivo no CDN, sem mexer em prioridade e sem orçamento. Descartada porque reduz o termo $t_{fetch}$ apenas para quem já tinha conexão quente, não resolve o primeiro acesso nem o TTFB, e não impede regressão porque não há gate.

Outra descartada: medir só com Lighthouse e considerar resolvido. Barata, rápida e errada, porque laboratório não representa rede, aparelho nem cache reais.

## 10. Quanto custa e quem paga essa conta?

Exemplo numérico (meta, parâmetros declarados): 12 h de diagnóstico e baseline, 16 h de correções de LCP, 20 h de INP, 8 h de CLS, 16 h de orçamento em CI e RUM, total de 72 h de engenharia. Sem infraestrutura nova: a coleta usa a API já existente e o banco já provisionado.

Custo recorrente: execução agendada do script de coleta e retenção de 13 meses de amostra (meta). Quem decide a retenção maior é negócio, porque passa a ser decisão de armazenamento, não de desempenho.

## 11. O que você deixaria para trás e qual o próximo gargalo depois disso?

Deixo para trás, por decisão consciente: a otimização de terceiros do tag manager (risco aceito com detecção), a revisão de performance das rotas fora do conjunto crítico e o refino de acessibilidade que tem standard próprio.

Próximo gargalo (meta): TTFB em servidor, se a decomposição do LCP apontar acima de 800 ms depois das correções de borda, e o INP de rotas com volume insuficiente no CrUX, resolvido pelo RUM por rota já previsto nos próximos passos.

## 12. Impacto de negócio: o que isso vale em horas ou em R$?

O impacto é de retenção e de sinal de ranqueamento: sessões lentas aumentam abandono e a degradação das métricas de experiência acompanha a perda de tráfego orgânico. Em termos operacionais, cada rota crítica fora do limite gera investigação manual depois do deploy; o gate no CI troca essa hora recorrente por uma asserção que roda a cada merge.

Exemplo numérico (meta, parâmetros declarados): com 4 rotas críticas e 2 investigações manuais por semana a 1,5 h cada, o custo operacional evitado é de 3 h por semana, 12 h por mês (meta). A defesa da atividade usa esse número como piso de retorno, não como promessa de receita.
