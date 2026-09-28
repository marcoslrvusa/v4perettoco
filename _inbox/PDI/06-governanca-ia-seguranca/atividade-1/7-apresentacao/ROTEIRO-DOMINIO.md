# Roteiro de Domínio | A1 Guardrails e anti-prompt-injection

Respostas prontas para as perguntas adversariais de um coordenador. Cada bloco termina com a evidência que se aponta na hora (arquivo, seção ou número).

## P1: Qual a diferença entre injeção direta e indireta?
Direta vem do usuário no prompt; indireta vem de fonte que o modelo consome (documento, página, e-mail) com instrução embutida. A indireta é mais perigosa porque dispensa o atacante de falar com o bot. Defesa igual para as duas: delimitar dado, detectar padrão e validar saída. O que muda é a telemetria: na indireta o bloqueio precisa registrar a origem da fonte (URL, e-mail, arquivo), senão não se localiza o documento envenenado. Evidência: seção 2.2 do `STANDARD-GUARDRAILS-LLM.md`.

## P2: Por que não confiar só em prompt bem escrito?
Porque o modelo não separa com segurança instrução de dado: texto dentro da janela vira candidato a comando. Barreira estrutural (delimitador, detector, contrato de saída, HITL) funciona mesmo quando o prompt falha. O argumento de fundo é técnico: não existe bit de proveniência no tensor de entrada, então a marcação de confiança precisa ser anotada fora do modelo. O prompt de política ajuda na qualidade e na aderência à tarefa, mas segurança não pode depender da redação de quem mantém o fluxo.

## P3: O que o proxy faz e o que ele não faz?
Faz sanitização, detecção por regras e validação de contrato sem dependência externa. Não substitui Moderation API nos casos duvidosos nem dispensa HITL em ação irreversível; ele é a primeira muralha, não o castelo. Também não faz: anonimização de PII (isso acontece antes, no worker), rotação de segredos, nem decisão de negócio. Se ele falhar em silêncio, o modo de falha seguro é bloquear e reprocessar, nunca seguir sem checagem.

## P4: Como medir se funciona?
Bateria de 60 casos (20 diretas, 20 indiretas, 10 extrações, 10 fora de contrato) com placar e piso de 95% para sair de staging, mais latência p95 e cobertura de HITL no alto risco. Três detalhes de quem já mediu isso: cada caso vale 1,67 ponto percentual, então 57 de 60 é o piso e 56 reprova; os blocos de extração de política e de saída fora do contrato são de tolerância zero; e o placar precisa de data, versão da bateria e versão do modelo, senão não há como comparar duas séries.

## P5: Qual o custo de operar?
Regras custam milissegundos; o custo real é mapear o contrato de saída por automação e operar o HITL. Em troca, cada novo fluxo com LLM nasce com teto de dano conhecido. **Exemplo numérico (parâmetros declarados):** 10.000 chamadas/dia com 1% de falso positivo e 40 s de revisão dão 66,7 min/dia de humano; a 6% de encaminhamento à Moderation API sobre 10.000 chamadas/mês a R$ 0,002 cada, o custo de API é R$ 1,20/mês. A API é ruído; o contrato e o HITL são a despesa.

## P6: E se cair no meio da noite, quem resolve?
O guardrail não é serviço novo com ponto único: roda dentro do worker, então a queda dele é a queda do fluxo, já coberta pelo runbook do fluxo. O modo de falha seguro é bloquear e reprocessar, porque liberar sem checagem expõe LLM02. Se a `feature-flag` do detector estiver causando falso positivo em massa, o rollback é desligar a regra pontual, sem deploy. Quem aciona: responsável pelo fluxo para desempenho, responsável pelo guardrail para padrão novo, coordenação da trilha para estouro de SLO, encarregado se houver dado de titular. Evidência: seção "Operação" do `README.md`.

## P7: Qual o SLO?
p95 do proxy abaixo de 150 ms (meta, janela de 7 dias), bloqueio na bateria de ao menos 95% (meta, execução mensal), HITL em 100% das automações de alto risco (meta), disponibilidade da camada de guardrail em 99,9% (meta) e cobertura de log em 100% das decisões (meta). Regra de parada: acima de 5 escapes confirmados por 10.000 chamadas em 30 dias (meta), nenhuma automação nova entra em produção até o placar voltar ao piso.

## P8: Como você prova que funciona?
Publicando o placar datado da bateria, com o caso a caso arquivado junto: entrada, decisão, motivo e tempo de resposta. Complementa a prova a contagem diária de decisões registradas versus decisões tomadas, que detecta perda de auditoria, e a leitura humana de 20 bloqueios por semana para confirmar que o motivo faz sentido. Placar sem data, sem versão de bateria e sem versão de modelo não vale como prova.

## P9: O que você deixaria para trás nesta fase?
Coisa que eu mesmo deixaria: modelo juiz em todos os casos (só entra no duvidoso), proxy como serviço separado com fila própria (só quando a política precisar mudar sem deploy, lá na casa de dezenas de automações), e painel dedicado de guardrails (hoje a telemetria vive junto das métricas do fluxo). Também deixaria para trás a tentação de salvar prompt completo para debug: não se debuga LGPD com log de dado pessoal.

## P10: Qual a alternativa mais barata?
Só prompt bem escrito e filtro de palavras. Custo zero, latência zero, cobertura parcial e não estrutural. Ela falha exatamente nos dois vetores que motivam a atividade: não marca proveniência e não valida saída. O degrau barato que já funciona é a base que adotamos: regex compiladas, teto de 4.000 caracteres e contrato JSON, sem custo de plataforma. **Exemplo numérico (parâmetros declarados):** 5,1 ms de latência adicionada contra um orçamento de 150 ms (meta), ou 3,4% do orçamento.

## P11: Quem decide o que vai para HITL e quem muda a regra?
A linha de irreversibilidade é decidida pela coordenação da trilha junto do dono do fluxo, e fica documentada por automação: escrita em CRM, alteração de verba, mensagem ao cliente e apagação de dado são sensíveis por padrão. A lista de padrões do detector e a `feature-flag` por regra mudam por pull request com revisão de quem não escreveu o fluxo. Ninguém muda regra de segurança sozinho no caminho de produção; toda mudança tem dono, data e reversão.

## P12: Quanto custa por ano e vale a pena?
Exemplo numérico (parâmetros declarados): 12 automações, cada uma com 6 h de integração (meta) = 72 h iniciais, mais 4 h/mês de bateria (meta) = 48 h/ano, mais 66,7 min/dia de revisão de falso positivo = cerca de 40 h/ano. Total aproximado de 160 h/ano (meta). Contra a conta de escape: 500 eventos/mês sem barreira a 15 min de investigação cada seriam 125 h/mês de retrabalho e risco. Vale a pena assim que a barreira evitar uma fração disso.

## P13 (de negócio): Qual o impacto em horas e em R$?
Horas: redução de 75 h/mês de investigação na conta de 300 eventos evitados por mês a 15 min cada (parâmetros declarados) e queda de 5 dias úteis para 1 dia (meta) no tempo de ativação de fluxo novo, porque o checklist fecha a discussão arquitetural. R$: o custo direto de segurança é R$ 1,20/mês de API mais o tempo de humano já contado acima; do lado do risco, a perda que não se contabiliza é vazamento de dado de titular e ação indevida em CRM ou verba, que é justamente o que a diretoria quer ver coberto por evidência auditável alinhada ao OWASP.
