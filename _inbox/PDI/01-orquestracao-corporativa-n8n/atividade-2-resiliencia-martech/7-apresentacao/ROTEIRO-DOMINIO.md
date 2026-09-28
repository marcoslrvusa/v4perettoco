# Roteiro de Domínio: Atividade 2, Resiliência MarTech

Perguntas que um coordenador faria no presencial, com respostas curtas para estudo.

## 1. Por que responder ACK 202 em menos de 2s em vez de processar no webhook?
Porque pico de campanha e importação trava a instância se processar de forma síncrona. O Gateway só enfileira em mt_jobs e responde queued. O status final e consultado na fila, não na resposta imediata.

## 2. Como a concorrência fica sob controle?
Com worker em polling a cada 15s e semáforo em mt_concurrency por fila. Isso troca uma latência mínima de ciclo por garantia de nunca estourar o limite, saindo de concorrência ilimitada para limite por slot.

## 3. O que acontece se um job pesado falhar no meio?
Ele retoma do checkpoint em mt_job_progress com backoff de 30s, 1m e 2m e máximo de 3 tentativas. Falha no chunk 4 de 10 retoma do chunk 4, sem recomeçar do zero e sem perder o que já processou.

## 4. Como uma divergência com o CRM aparece antes do cliente reclamar?
Todo sync envia envelope expected x confirmed e o cálculo de drift abre mt_sync_delta acima de 5%. No exemplo, 1000 esperados e 860 confirmados geram 14% e disparam alerta para detecção em menos de 15 min com dashboard em tempo real.

## 5. Por que o schema v3.0 não quebra a atividade 1?
Porque e aditivo, com 6 tabelas e 5 views convivendo com as tabelas error do schema v2.1. São 4 workflows novos validados com n8nac e nenhum workflow foi publicado no n8n antes da homologação.
