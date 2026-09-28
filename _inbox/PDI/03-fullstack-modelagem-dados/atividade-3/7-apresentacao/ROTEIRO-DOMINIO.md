# ROTEIRO-DOMINIO: Arquitetura Serverless para Processamento Assíncrono

5 perguntas de coordenador + respostas curtas para defesa da atividade 3.

## 1. Por que não processar a planilha dentro do request de upload?

Planilhas de 1k a 50k linhas estouram o timeout do request. O padrão grava no store, publica `file.uploaded` e responde rápido; o processamento roda no consumer com concorrência limitada a 10.

Fecha a conta: 50k linhas a 2 ms/linha dá 100 s de CPU (**Exemplo numérico:** parâmetro declarado de parsing), contra o teto de 60 s da função. Processar dentro do request transformaria uma planilha grande em erro 504 para o cliente, que reenviaria e pioraria a fila.

## 2. Como garantem que um retry não duplica leads?

Idempotência por dedup com `hash(arquivo + tenant)`: antes de processar, o handler verifica se a chave já foi consumida. Reprocessar o mesmo evento retorna `skipped` como duplicata.

Reforço defensivo: são duas barreiras. A primeira é o store rápido (Redis/DynamoDB), que evita trabalho repetido. A segunda é `UNIQUE (tenant_id, email)` no banco, que impede a duplicata mesmo se o store reiniciar e perder o histórico. Se só existisse o `SELECT` antes do `INSERT`, dois consumidores no mesmo instante leriam a ausência e inseririam igual.

## 3. O que acontece com um arquivo corrompido no meio da fila?

Isolamento por mensagem: 1 arquivo ruim não afeta os outros. Após N tentativas a mensagem vai para a DLQ, onde aguarda replay manual em vez de travar a fila.

O caminho é literal: `maxReceiveCount = 3` no Terraform, três falhas, mensagem para a DLQ, classificação em `payload_ruim`, `transitória` ou `bug`. Replay em lote de 10 com dedup ligada. A fila principal nunca é pausada para isso.

## 4. Quando serverless e a escolha errada?

Com carga constante e alta, o worker always-on sai mais barato que pagar por invocação o tempo todo. Serverless vence aqui porque o worker ficava 90% ocioso e o pico chega a 200 uploads.

A regra prática da tabela de decisão: utilização acima de 60% do tempo em janela observada, use worker. Processamento acima de 60 s com efeito não idempotente, use fila de tarefas dedicada. Transação distribuída entre dois banços, serverless não resolve o problema, só o espalha.

## 5. Como foi validado antes de produção?

Envio de 200 planilhas medindo paralelismo e custo (meta abaixo de R$ 0,20 por mil), falha parcial forçada para confirmar retry sem duplicata, e 1 arquivo ruim para provar isolamento. Metas: p95 abaixo de 60s e zero duplicatas.

## 6. Por que o payload não carrega o arquivo inteiro?

Porque fila com 5 MB por mensagem é fila lenta, cara e insegura. Mensagem com URL tem ~300 bytes, réplica rápido, e o dado bruto nunca trafega em texto nem fica retido na fila. O preço é uma chamada a mais no store por mensagem, que é ordens de magnitude mais barata do que encher a fila de binário. Bônus: arquivo sensível fica no store com controle de acesso, não num log de mensagem.

## 7. E se cair no meio da noite, quem aciona e o que acontece?

A fila segura a demanda até de manhã: sem servidor para reiniciar, sem plantão acordado por CPU. O que dispara alerta na madrugada é só DLQ maior que zero por 15 minutos ou idade da mensagem acima de 10 minutos. O runbook tem três ações na ordem: triagem da DLQ, verificação do `EXPLAIN` das consultas principais e, se for chegada anormal, subir concorrência de 10 para 20. Rollback é troca de alias da função, cronometrado em menos de 2 minutos (meta), com a fila intacta porque o contrato da mensagem não mudou.

## 8. Qual é o SLO de verdade e o que você faz quando estoura?

Quatro SLIs: p95 de `upload` até `done` abaixo de 60 s em 7 dias rolantes; custo por mil planilhas abaixo de R$ 0,20 no mês corrente; zero duplicatas confirmadas; DLQ abaixo de 0,1% do volume. Ao estourar o p95: primeiro olhar se é chegada anormal (campanha) ou serviço lento (banco sem índice), porque subir concorrência sem olhar esconde a causa. Ao estourar duplicata: pausar consumer, corrigir chave, replay. Orçamento de erro: 1% das mensagens pode demorar até 120 s antes de virar incidente.

## 9. Como você prova que funciona, além de dizer que funciona?

Cinco provas com saída esperada escrita: (1) autoverificação do handler com casos de borda (vazio, nulo, unicode, limite) executável por comando; (2) rajada de 200 planilhas com amostragem de `pg_stat_activity` mostrando no máximo 10 conexões; (3) reenvio triplo do mesmo arquivo com contagem de `lead` estável; (4) `EXPLAIN (ANALYZE, BUFFERS)` da API de status anexado, mostrando índice e não varredura; (5) rollback cronometrado em homologação. Fora isso, teste de segurança: célula `=` saneada no export, arquivo de 200 MB recusado antes do parse, leitura cruzada de tenant retornando vazio.

## 10. O que você deixaria de fora, sabendo que sobra dívida?

Deixaria de fora o particionamento das tabelas de negócio. `ingest_event` particiona por mês porque o descarte com `DROP` é a única forma barata de expirar auditoria, mas particionar `lead` por tenant geraria milhares de partições quase vazias e ainda quebraria a chave única global da dedup. Também deixaria de fora multiregião e replicação ativa: o custo operacional não se paga com uma fila de uploads. A dívida assumida e registrada: o `set` em memória da PoC precisa virar store persistente antes de produção, e a triagem da DLQ ainda é manual.

## 11. Qual a alternativa mais barata e por que não ela?

A mais barata é continuar com o worker always-on e só aumentar a máquina no pico. Ela é mais barata em complexity: sem fila, sem dedup, sem DLQ. Ela perde em três contas: paga 730 h/mês para 10% de uso, não absorve o pico sem provisionamento manual e não tem isolamento, então um arquivo ruim derruba o lote inteiro. A segunda mais barata seria fila direta para o banco, sem função: mas aí o backpressure precisa ser implementado à mão (pool de conexões, lotes, retry), que é exatamente o código que a plataforma já entrega pronto na função.

## 12. Quanto custa isso no bolso do negócio?

**Exemplo numérico com parâmetros declarados:** 10.000 planilhas por mês, 1,5 s de execução, 0,5 GB de memória, R$ 0,0000166 por GB-s e R$ 0,000002 por invocação: 7.500 GB-s dá R$ 0,1245, mais R$ 0,02 de invocação, total de R$ 0,145 por mil (meta), contra meta de R$ 0,20. No cenário de custo, o ganho real não é o centavo por planilha: é a eliminação do segundo worker (meta: 80% de redução do custo ocioso) e o fim das madrugadas de incidente em pico, que custam horas de plantão. Impacto de negócio: campanha de importação em rajada vira operação prevista, não apagamento de fogo.
