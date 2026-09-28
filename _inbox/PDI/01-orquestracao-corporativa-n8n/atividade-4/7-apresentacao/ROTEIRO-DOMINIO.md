# Roteiro de Domínio: Atividade 4, Observabilidade e Logs n8n-CRM

Perguntas que um coordenador faria no presencial, com respostas curtas para estudo.

## 1. Por que log estruturado com painel SQL em vez de APM pago?
Pela decisão ADR-011: log JSON com trace_id mais painel SQL é simples e sem custo, com consulta manual como tradeoff. Contador no n8n foi rejeitado por falta de contexto e Datadog ficou como evolução futura. Os pesos foram: primeiro sinal útil (40%), custo recorrente (25%), ausência de infra nova (20%) e profundidade de investigação (15%). A opção escolhida vence em três dos quatro critérios e perde apenas em profundidade, exatamente o que a ADR prevê recuperar depois com OTel.

## 2. O que o trace_id resolve na prática?
Liga trigger, execução e escrita no CRM com cobertura de 100%. Sem ele, cada nó loga de um jeito e é impossível correlacionar timeout, 401 ou limite ao registro afetado. Com ele, o painel correlaciona por trace_id em menos de 1 min. Exemplo prático: o lead L-9 não some mais do funil sem rastro; existe uma linha para cada tentativa, com código de erro e duração, e a mesma chave aparece no webhook, na normalização, no barramento e na resposta de cada assinante.

## 3. Como o barramento trata conflito entre 4 CRMs?
Com fan-out para 3 assinantes e last-write-wins por trace_id mais timestamp, com log auditável e rollback via trace_store. Falha em 1 CRM usa retry de 3x com backoff sem bloquear os demais, com normalização prévia e descarte quando falta e-mail. O tradeoff assumido é que o último write vence mesmo quando o dado anterior era melhor; o que compensa isso é o rastro completo, que permite identificar a perda e reescrever. Consistência eventual temporária é aceita de propósito: bloquear os quatro CRMs por causa de um seria pior.

## 4. Quando o alerta dispara e como evitar ruído e PII no log?
Quando a taxa de erro por CRM passa de 2% em 5 min, com envio ao Slack. Ruído é controlado com nível e amostragem e PII é mascarada em e-mail e CNPJ. Três proteções extras: piso de 50 eventos antes de calcular a taxa, agrupamento por `crm` e nunca por `trace_id`, e alerta de silêncio para o caso de o nó parar de emitir log. A varredura por regex de e-mail e CNPJ precisa retornar zero linhas; se retornar, é incidente de segurança e não ajuste de texto.

## 5. Qual é o plano de rollout e o ganho esperado?
Piloto em 1 integração por 1 semana medindo MTTR, depois expansão para 12 integrações via template. A meta é sair de detecção em dias para menos de 15 min, de 0% para 100% de visibilidade e de 50h para cerca de 1h por semana, mirando 99% com fonte única e zero disparo duplicado. O rollout tem quatro ondas, cada uma com critério de saída: 7 dias sem PII e cobertura em 100%, alerta no máximo 1x por semana, MTTR abaixo de 15 min, e checklist obrigatório em todo nó novo.

## 6. E se a falha acontecer às 3 da manhã, quem resolve?
O plantão de integração aciona o runbook, que tem quatro linhas de decisão: checagem em 2 min, mitigação em 10 min, comunicação em 3 min, somando menos de 15 min. O alerta já traz `crm`, taxa, total de eventos e um `trace_id` de exemplo, então não há investigação prévia necessária para começar a agir. Se for falha de schema, o time de dados entra; se for vazamento de PII, segurança entra. O que não existe hoje é silêncio: hoje não há alerta nenhum, e a descoberta vem do cliente no dia seguinte.

## 7. Qual é o SLO exatamente e o que acontece quando ele estoura?
Três SLIs: disponibilidade (eventos que chegam a `settled` sem erro persistente, janela de 5 min por CRM), latência (p95 entre publish e resposta do último assinante, janela de 24 h) e cobertura de `trace_id` (100%, sem tolerância). A meta é 98% dos eventos concluídos em até 30 s. Com meta de 98%, o orçamento de erro mensal é de 2%, cerca de 8,6 h em 30 dias (Exemplo numérico: `30 dias × 24 h × 0,02 = 14,4 h` de folga cheia, descontados os incidentes já consumidos no mês). Ao estourar: congelamento de rollout, incidente com responsável nomeado e postmortem em até 5 dias úteis, sem culpa.

## 8. Como você prova que funciona, e não apenas que foi implementado?
Três evidências, nessa ordem. Primeiro, medição de MTTR antes e depois com os parâmetros declarados e a mesma definição de evento em ambos os lados. Segundo, o teste de falha proposital: provocar um 401, ver a linha `error`, o alerta no Slack e o rastro no painel dentro da janela de 1 min. Terceiro, a consulta de cobertura retornando zero linhas sem `trace_id` durante sete dias seguidos. Sem essas três, o que se tem é código escrito, não observabilidade entregue.

## 9. Qual a alternativa mais barata e por que ela não basta?
A mais barata é o contador no n8n, rejeitado por falta de contexto: diz quantos erros houve e nunca quais registros, nunca qual causa, nunca qual CRM. Custa zero e também vale zero em investigação. A segunda mais barata é continuar com log de texto livre e melhorar a formação do time; o custo é nulo, mas a consulta continua manual e não indexável, e o MTTR permanece em dias. A terceira, APM, custa mais e só passa a valer quando houver orquestração multi-serviço para correlacionar.

## 10. O que você deixaria para trás, sabendo do que abriu mão?
Deixaria a profundidade de investigação de um APM nativo: sem trace distribuído, não há flame de chamadas nem árvore de dependências entre serviços. Também deixaria a busca textual livre, porque consultar JSON no Postgres exige sabedoria nas funções de extração. E deixaria a ambição de SLO por cliente no primeiro ciclo, porque hoje a granularidade operacional é por CRM; SLO por cliente exige identidade de cliente confiável no evento, que ainda não existe.

## 11. Quem decide cada coisa e quanto isso custa por mês?
Decisões de contrato (schema, níveis, proibições): time de integração, sem custo adicional. Decisão de ferramenta (ADR-011): arquitetura da operação, custo zero de infraestrutura por usar banco e orquestrador existentes. Decisão de alerta e plantão: plantão de integração, custo de resposta. Esforço de construção: 60 h (meta), cerca de R$ 7.200 a R$ 120/h (Exemplo numérico). Armazenamento: cerca de 72 MB/mês (meta), irrelevante. O custo real é disciplina: alguém precisa recusar nó novo sem o template.

## 12. Por que não adiar tudo para depois, quando o sistema está funcionando?
Porque o sistema não está funcionando de forma verificável: 12 integrações com 4 CRMs só mostram falha quando o cliente reclama, e o retrabalho atual é de cerca de 50h por semana. Adiar mantém um custo operacional contínuo contra um custo único de 60 h (meta). Há ainda o argumento de reversibilidade: observabilidade é aditiva, não altera payload de negócio, logo o rollback é desligar o template. O risco de fazer agora é baixo; o risco de não fazer é lead perdido sem ninguém saber.

## 13. Pergunta de negócio: qual o impacto em R$ e em horas?
Hoje: cerca de 50h/semana de conciliação manual, lead duplicado com 3 e-mails e 2 telefones, disparo duplo de campanha e risco reputacional de spam. Depois (meta): cerca de 1h/semana, 99% dos leads com fonte única e zero disparo duplicado, com MTTR abaixo de 15 min. Exemplo numérico: 49h/semana poupadas × 4 semanas = 196 h/mês (meta); a R$ 60/h (Exemplo numérico), cerca de R$ 11.760 por mês (meta), contra um investimento único de cerca de R$ 7.200 (meta). O retorno, portanto, não depende de vender mais, depende de parar de perder tempo e lead.
