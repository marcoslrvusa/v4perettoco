# Roteiro de Domínio: Atividade 2, Resiliência MarTech

Perguntas que um coordenador faria no presencial, com respostas curtas para estudo.

## 1. Por que responder ACK 202 em menos de 2s em vez de processar no webhook?
Porque pico de campanha e importação trava a instância se processar de forma síncrona. O Gateway só enfileira em mt_jobs e responde queued. O status final é consultado na fila, não na resposta imediata.

## 2. Como a concorrência fica sob controle?
Com worker em polling a cada 15s e semáforo em mt_concurrency por fila. Isso troca uma latência mínima de ciclo por garantia de nunca estourar o limite, saindo de concorrência ilimitada para limite por slot.

## 3. O que acontece se um job pesado falhar no meio?
Ele retoma do checkpoint em mt_job_progress com backoff de 30s, 1m e 2m e máximo de 3 tentativas. Falha no chunk 4 de 10 retoma do chunk 4, sem recomeçar do zero e sem perder o que já processou.

## 4. Como uma divergência com o CRM aparece antes do cliente reclamar?
Todo sync envia envelope expected x confirmed e o cálculo de drift abre mt_sync_delta acima de 5%. No exemplo, 1000 esperados e 860 confirmados geram 14% e disparam alerta para detecção em menos de 15 min com dashboard em tempo real.

## 5. Por que o schema v3.0 não quebra a atividade 1?
Porque é aditivo, com 6 tabelas e 5 views convivendo com as tabelas error do schema v2.1. São 4 workflows novos validados com n8nac e nenhum workflow foi publicado no n8n antes da homologação.

## 6. Por que fila no Postgres e não em Redis, que é feito para isso?
Porque o Supabase já é operado pelo time, com credencial, backup e consulta já prontos, e o volume atual cabe em uma tabela com índice. Redis ganharia em throughput acima de 50x o volume, mas introduziria um sistema novo para monitorar hoje. A troca futura muda só o conector do Worker, porque o contrato do job (chave, status, tentativa, backoff) continua o mesmo.

## 7. Quanto custa manter isso rodando?
O custo adicional operacional é de uma tabela em banco que já existe, mais o tempo de execução dos 4 workflows. Com 1.800 jobs por hora e 10 s de processamento médio, a carga é de 5 slots simultâneos (meta), sem servidor novo e sem licença extra. O custo que evitamos é o de retrabalho: um job de 10 mil itens que refaz tudo após timeout.

## 8. E se cair no meio da noite, quem resolve?
O alarme que importa é o de job parado: vw_mt_queue_backlog com stale_queued maior que zero por 10 minutos. Quem está de plantão (analista de automação) confere se o Worker está ativo e se a credencial Supabase não expirou, os dois casos que explicam quase toda parada. Restauração de instância e credencial escala para Infraestrutura. Nenhum caso exige acesso ao banco para desbloquear.

## 9. Qual o SLO do sistema?
Quatro medidos: ACK do Gateway com p95 abaixo de 2 s, conclusão na primeira tentativa acima de 95%, detecção de drift em menos de 15 minutos e zero jobs em queued sem Worker por 10 minutos. Janela de 30 dias para o ACK, 7 dias para a primeira tentativa e contínua para os dois últimos. Estourou: primeiro a causa raiz, nunca aumentar max_attempts para maquiar o número.

## 10. Como você prova que funciona?
Com oito casos de teste: ACK em rajada de 200 posts, idempotência com o mesmo job_key três vezes, limite de 5 slots sob 50 jobs, morte do Worker com retomada pelo Reaper, backoff de 30s, 1m e 2m, exaustão indo para DLQ, drift de 14% abrindo delta e retomada no chunk 4 de 10. Tudo com a saída das queries de 5-monitoring na tela, não com afirmação de tela de slides.

## 11. O que você deixaria de fora, se precisasse encurtar?
Deixaria de fora a camada de enriquecimento em Python no Heavy Payload Processor, que é opcional e pode ser feita depois, e a view de resumo de 24 horas, que é conforto de dashboard e não bloqueia detecção de problema. Não deixaria de fora o checkpoint nem o envelope de drift, porque são exatamente o que impede retrabalho e reclamação de cliente.

## 12. Qual a alternativa mais barata do que isso?
Manter o workflow síncrono e só aumentar o timeout. Custa zero em implementação e resolve o caso raro, mas mantém o risco de travar a instância inteira em pico e não gera nenhuma trilha. Depois disso, a opção intermediária é o Retrofit somente do gateway, sem observabilidade: mais barato que o pacote completo, porém sem detecção antes do cliente.

## 13. Qual o impacto no negócio, em horas ou reais?
O número principal é o tempo de detecção: antes, a falha de sync só aparecia na reclamação; depois disso, a meta é menos de 15 minutos (meta). Cada hora entre a falha e a descoberta vira hora de retrabalho do time de atendimento e risco de perda de registro em CRM do cliente. Somando o job de 10 mil itens que deixava de ser refeito do zero e a eliminação do travamento em pico, a economia projetada fica em horas de operação por mês (meta), a ser medida nos primeiros 30 dias após o retrofit do primeiro cliente real.
