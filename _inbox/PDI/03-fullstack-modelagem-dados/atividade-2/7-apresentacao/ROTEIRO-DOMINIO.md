# ROTEIRO-DOMINIO: APIs Modulares de Missao Critica (FastAPI)

5 perguntas de coordenador + respostas curtas para defesa da atividade 2.

## 1. Por que cursor-based e nao offset com indice?

Offset com indice ainda varre e descarta N linhas antes de devolver a pagina; em listas de 5k a 80k o custo cresce com a profundidade. Cursor (`after` = id) posiciona direto no ponto de partida, custo estavel por pagina.

## 2. O que acontece se o Redis cair no pico?

O endpoint faz fallback para o banco e continua respondendo. A latencia degrada para o caminho sem cache ate o Redis voltar, mas nao ha indisponibilidade por causa do cache.

## 3. Como o cliente sabe quando repetir uma chamada que falhou?

Pelo envelope: 4xx significa erro do cliente e nao deve ser retentado; 5xx significa erro nosso e pede retry com backoff. O `trace_id` amarra cliente e log para depuracao.

## 4. Por que rate limit por chave e nao global?

Limite global pune todos por causa de um cliente (ou bot) agressivo. Por chave, quem estoura a quota de 100 req/min recebe 429 isolado e os demais sistemas (3 a 5 consumidores) seguem normais.

## 5. Como foi validado antes de producao?

Carga com k6 a 200 req/s por 5 min, teste de estouro de quota esperando 429 com `Retry-After`, e confirmacao de que o segundo hit da mesma lista vem do Redis. Metas: p95 abaixo de 200ms no hit e disponibilidade de 99,5%.
