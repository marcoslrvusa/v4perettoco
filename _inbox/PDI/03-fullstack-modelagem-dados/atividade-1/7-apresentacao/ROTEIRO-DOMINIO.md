# ROTEIRO-DOMINIO: Queries Complexas e Indexacao no Supabase (PostgreSQL)

5 perguntas de coordenador + respostas curtas para defesa da atividade 1.

## 1. Por que exigir EXPLAIN antes de qualquer query em producao?

Sem plano, a query da fila `mt_jobs` varria 2,4M linhas com Seq Scan e removia 2,38M por filtro. O `EXPLAIN (ANALYZE, BUFFERS)` mostra o plano real e e a unica prova aceita na revisao.

## 2. Por que o indice composto segue a ordem igualdade, range e ORDER BY?

Nessa ordem um unico B-tree cobre filtro e ordenacao num Index Scan sem Sort. Foi assim que o pick do worker saiu de 1,8s para 4ms com `(queue, status, scheduled_at)`.

## 3. Quando usar BRIN em vez de B-tree?

Em serie temporal fisicamente ordenada por tempo (logs, sync, eventos), o BRIN fica 10x menor que o B-tree equivalente. Se a ordem fisica nao acompanha o tempo, ele nao serve e o B-tree volta a ser a escolha.

## 4. Por que particionar tabelas de eventos em vez de so indexar?

Indice nao resolve tabela que cresce sem limite: o planner continua avaliando particoes antigas. Com particionamento por range e TTL, o pruning ignora o passado e o dashboard com agregacao materializada saiu de 8,4s para 1,1s.

## 5. Como aplicar indice em producao sem derrubar a escrita?

Sempre `CREATE INDEX CONCURRENTLY`, fora da janela de pico: nao segura `AccessExclusiveLock`. A criacao e mais lenta e nao roda em transacao, entao a janela de deploy precisa prever isso. Nenhum indice desta atividade foi aplicado em producao, apenas documentado e provado.
