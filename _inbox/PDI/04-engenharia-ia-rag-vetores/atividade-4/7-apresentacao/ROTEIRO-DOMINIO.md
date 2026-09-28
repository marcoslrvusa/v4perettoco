# Roteiro de domínio: Atividade 4, Engenharia de Custos de LLM

Perguntas adversariais de coordenação, com a resposta que sustenta a defesa. A regra é responder
com número, comando ou decisão, nunca com adjetivo.

## 1. Por que não usar modelo maxi para tudo?
Resposta: porque custa 10x, a regra manda trivial para modelo leve, complexo para forte e repetido para cache.
Aprofundamento: a razão não é só o preço de tabela, é o mix. **Exemplo numérico (parâmetros
declarados: 500 tokens de entrada, 200 de saída):** `maxi = 0.004500 USD` e `mini = 0.000195 USD`,
razão de 23.1x para a mesma tarefa. Se 90% do tráfego é triagem, pagar 23.1x nessa fração é
decisão de arquitetura, não descuido. O contra-argumento honesto: modelo forte para tudo é mais
simples de operar, e é exatamente por isso que a regra está escrita em padrão, com teste de
propriedade, para a simplicidade não virar pretexto.

## 2. Como o cache atinge hit maior ou igual a 30 por cento sem vazar PII?
Resposta: cache semântico para perguntas repetidas com regra dura de nunca cachear PII, medindo hit rate a cada lote.
Aprofundamento: a ordem é guardrail primeiro, escrita depois. Se o detector achar PII, a execução
não entra no armazenamento de cache, e a chave é composta por `tenant_id`, para resposta de um
cliente nunca ser servida a outro. O hit rate é auditável por SQL, agrupado por `agent`, e a meta
de 30% é janela móvel de 7 dias: um dia ruim não reprova o sistema, uma semana ruim sim, e dispara
revisão do limiar de similaridade.

## 3. O que significa custo por tarefa menor ou igual a baseline vezes 0.4?
Resposta: e a meta de pagar no máximo 40 por cento do custo original por tarefa, com ledger de tokens e reais por fluxo para auditar.
Aprofundamento: baseline é medido com tudo no modelo forte e cache desligado, na mesma carga de
teste, para a comparação ser justa. O ledger guarda `model`, `prompt_tokens`, `completion_tokens` e
`cost_usd` por execução, então a razão se calcula em uma consulta, sem planilha. Se a razão passar
de 0.4, o diagnóstico é sempre o mesmo e nessa ordem: mix de modelo, hit rate, e só então volume.

## 4. Como o budget por cliente funciona na prática?
Resposta: cada cliente tem teto com alerta em 80 por cento, cache miss mais modelo caro dispara aviso antes do estouro.
Aprofundamento: a janela é calendário, igual à fatura. A razão é calculada no banco, não em memória,
então reinício de serviço não zera o consumo. Em 80% a account recebe aviso com o consumo
decomposto por `agent`; em 100% os agentes não-críticos são pausados e os críticos seguem, segundo
lista versionada. Teto não configurado gera alerta de configuração ausente: ausência de teto nunca
significa consumo livre.

## 5. Como manter redução maior ou igual a 85 por cento com score maior ou igual a 0.90?
Resposta: combinando roteamento mais cache mais batch assíncrono dentro do SLA, com eval que barra troca que derrube qualidade.
Aprofundamento: o score é medido antes e depois no mesmo conjunto-ouro; qualquer mudança de
roteamento que derrube a barra de 0.90 é revertida no mesmo dia. O batch entra só em fluxos com
janela de tolerância declarada, porque desconto de cerca de 50% não vale nada se estourar o SLA.
A conta fecha: roteamento ataca o mix, cache ataca a repetição e batch ataca o preço unitário de
chamadas não urgentes.

## 6. E se o roteador errar a classificação?
Resposta: o erro é sempre na direção cara, nunca na direção errada: intenção desconhecida cai no modelo forte.
Aprofundamento: degradação cara é ruído financeiro, degradação barata é ruído de qualidade, e este
segundo custa mais caro em reputação. O erro é detectável: o mix de chamadas por modelo no ledger
mostra desvio em minutos, e o rollback é trocar `route_model` pela versão anterior, sem migração.
O teste de propriedade cobre toda intenção trivial apontando para o modelo leve, então a regressão
falha em CI, não em produção.

## 7. Quanto custa manter esse sistema de medição rodando?
Resposta: menos de 5 por cento do custo que ele controla, senão a medição virou problema (meta).
Aprofundamento: **Exemplo numérico (parâmetros declarados: 100.000 execuções/mês, 1 linha de
ledger por execução):** 100.000 INSERTs e a agregação diária por `(agent, created_at)`. Se esse
volume pesar, o caminho é agregação em memória com flush periódico, nunca abandonar a medição.
Embedding para cache só acontece no caminho de miss, e avaliação roda em lote fora do pico.

## 8. Quem decide quem é agente crítico e quem é não-crítico?
Resposta: a account decide com a engenharia, a lista fica versionada no repositório e tem dono nomeado.
Aprofundamento: a postura padrão é listar poucos como críticos, porque agente crítico é o que não
pode parar sem quebrar compromisso contratual. Se tudo é crítico, o bloqueio em 100% não bloqueia
nada e o teto vira sugestão. Mudança na lista passa por revisão de código como qualquer outra
configuração de produção.

## 9. E se cair no meio da noite, qual é o runbook?
Resposta: seis passos: consumo diário, hit rate, mix de modelo, alerta de teto, suspeita de PII e escala.
Aprofundamento: rollback padrão é desligar as flags de cache e de roteamento, nessa ordem, sem
migração de dado. Engenharia de IA aciona os passos técnicos, a account aciona o passo de teto, a
coordenação aciona a revisão mensal de teto. O critério de "voltou" é: ledger consistente
(execuções menos linhas igual a zero) e mix de modelo de volta ao esperado.

## 10. Como você prova que funciona, e não que só parece funcionar?
Resposta: reconciliação diária entre execuções e linhas do ledger, hit rate por SQL, mix por SQL e alerta testado com consumo simulado.
Aprofundamento: prova é consulta reproduzível, não gráfico. A reconciliação roda todo dia e
compara contagem de execuções com contagem de linhas; divergência diferente de zero é incidente.
O alerta de 80% é testado entre 79% e 81% de razão em ambiente de teste. E os números do relatório
vêm do ledger, nunca de planilha paralela: se o relatório e o banco divergirem, o relatório está
errado por definição.

## 11. Qual a alternativa mais barata que deixaria de fora?
Resposta: só a tabela de preço versionada e o ledger, sem cache, sem roteamento e sem batch.
Aprofundamento: essa alternativa dá visibilidade, não dá redução, e é um caminho legítimo de
primeiro passo se o prazo apertar. O que se deixa para trás: o mix 23.1x, a repetição paga em dobro
e o desconto de lote. A recomendação é implementar primeiro o ledger (é barato e é pré-requisito
de tudo), depois o roteamento (maior alavanca), depois o cache (exige cuidado com PII) e por último
o batch (depende de SLA definido).

## 12. Qual o impacto disso no negócio, em R$ ou horas?
Resposta: transforma consumo de inferência de custo opaco em preço por tarefa, destravando margem e removendo subsídio invisível.
Aprofundamento: **Exemplo numérico (parâmetros declarados: 100.000 execuções no mês, baseline de
0.004500 USD por execução):** `450.00 USD` sem otimização contra `43.79 USD` com roteamento e cache
(meta de redução de 90.3%, acima da meta geral de 85%). Em horas: a account deixa de gastar
reunião para justificar fatura e passa a precificar por entrega. O ganho real, porém, não é o dólar
econômizado: é poder responder "quanto custa rodar isso" antes de aceitar a demanda.
