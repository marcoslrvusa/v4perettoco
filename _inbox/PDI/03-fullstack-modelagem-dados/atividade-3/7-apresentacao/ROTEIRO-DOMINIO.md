# ROTEIRO-DOMINIO: Arquitetura Serverless para Processamento Assíncrono

5 perguntas de coordenador + respostas curtas para defesa da atividade 3.

## 1. Por que não processar a planilha dentro do request de upload?

Planilhas de 1k a 50k linhas estouram o timeout do request. O padrão grava no store, publica `file.uploaded` e responde rápido; o processamento roda no consumer com concorrência limitada a 10.

## 2. Como garantem que um retry não duplica leads?

Idempotência por dedup com `hash(arquivo + tenant)`: antes de processar, o handler verifica se a chave já foi consumida. Reprocessar o mesmo evento retorna `skipped` como duplicata.

## 3. O que acontece com um arquivo corrompido no meio da fila?

Isolamento por mensagem: 1 arquivo ruim não afeta os outros. Após N tentativas a mensagem vai para a DLQ, onde aguarda replay manual em vez de travar a fila.

## 4. Quando serverless e a escolha errada?

Com carga constante e alta, o worker always-on sai mais barato que pagar por invocação o tempo todo. Serverless vence aqui porque o worker ficava 90% ocioso e o pico chega a 200 uploads.

## 5. Como foi validado antes de produção?

Envio de 200 planilhas medindo paralelismo e custo (meta abaixo de R$ 0,20 por mil), falha parcial forçada para confirmar retry sem duplicata, e 1 arquivo ruim para provar isolamento. Metas: p95 abaixo de 60s e zero duplicatas.
