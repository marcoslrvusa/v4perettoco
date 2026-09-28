# Roteiro de Dominio: Atividade 1, Padrao Universal de Tratamento de Erros

Perguntas que um coordenador faria no presencial, com respostas curtas para estudo.

## 1. Por que um handler central unico em vez de um por workflow?
Porque reduz a manutencao a um unico ponto com 10 nos validados com n8nac. Se o handler cair, perde-se notificacao temporaria, mas nao o dado, pois a DLQ esta no Supabase e o Monitor roda a cada 5 min.

## 2. Por que 3 camadas e nao so retry no no?
Porque a Camada 1 captura cerca de 73% das falhas transientes com custo baixo, mas nao cobre erro de logica. A Camada 2 classifica e notifica em menos de 1 min e a Camada 3 impede cascata com breaker de 5 falhas e cooldown de 5 min.

## 3. Quando devo retentar e quando nunca devo retentar?
Retenta 5xx, 429, 408, 409, 425, timeout e DNS, com maxTries 3 e espera de 5000 ms no HTTP. Nunca retenta 4xx como 400, 401, 403 e 404, nem validacao de dado, runtime e OOM. Code node nunca retenta por ser erro de logica.

## 4. O que garante replay de uma falha sem perder contexto?
O envelope com correlationId estavel entre retries mais a DLQ permanente no schema v2.1 com 4 tabelas e 4 views. O prune do n8n apaga historico, a DLQ preserva payload completo com status pending ate resolved.

## 5. Quanto custa aplicar o padrao nos 10 workflows?
O retrofit completo leva 4 dias em 3 fases (push mais schema, error handling e validacao). As 5 correcoes pontuais somam cerca de 1h (20 min no ADPLAN e 10 min em cada um dos outros 4), com validacao por falha provocada e checagem em vw_error_health_score.
