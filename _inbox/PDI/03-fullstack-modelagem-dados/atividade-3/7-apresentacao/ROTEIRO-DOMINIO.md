# ROTEIRO-DOMINIO: Arquitetura Serverless para Processamento Assincrono

5 perguntas de coordenador + respostas curtas para defesa da atividade 3.

## 1. Por que nao processar a planilha dentro do request de upload?

Planilhas de 1k a 50k linhas estouram o timeout do request. O padrao grava no store, publica `file.uploaded` e responde rapido; o processamento roda no consumer com concorrencia limitada a 10.

## 2. Como garantem que um retry nao duplica leads?

Idempotencia por dedup com `hash(arquivo + tenant)`: antes de processar, o handler verifica se a chave ja foi consumida. Reprocessar o mesmo evento retorna `skipped` como duplicata.

## 3. O que acontece com um arquivo corrompido no meio da fila?

Isolamento por mensagem: 1 arquivo ruim nao afeta os outros. Apos N tentativas a mensagem vai para a DLQ, onde aguarda replay manual em vez de travar a fila.

## 4. Quando serverless e a escolha errada?

Com carga constante e alta, o worker always-on sai mais barato que pagar por invocacao o tempo todo. Serverless vence aqui porque o worker ficava 90% ocioso e o pico chega a 200 uploads.

## 5. Como foi validado antes de producao?

Envio de 200 planilhas medindo paralelismo e custo (meta abaixo de R$ 0,20 por mil), falha parcial forcada para confirmar retry sem duplicata, e 1 arquivo ruim para provar isolamento. Metas: p95 abaixo de 60s e zero duplicatas.
