# ROTEIRO-DOMINIO: Queries Complexas e Indexação no Supabase (PostgreSQL)

5 perguntas de coordenador + respostas curtas para defesa da atividade 1.

## 1. Por que exigir EXPLAIN antes de qualquer query em produção?

Sem plano, a query da fila `mt_jobs` varria 2,4M linhas com Seq Scan e removia 2,38M por filtro. O `EXPLAIN (ANALYZE, BUFFERS)` mostra o plano real e e a única prova aceita na revisão.

## 2. Por que o índice composto segue a ordem igualdade, range e ORDER BY?

Nessa ordem um único B-tree cobre filtro e ordenação num Index Scan sem Sort. Foi assim que o pick do worker saiu de 1,8s para 4ms com `(queue, status, scheduled_at)`.

## 3. Quando usar BRIN em vez de B-tree?

Em série temporal fisicamente ordenada por tempo (logs, sync, eventos), o BRIN fica 10x menor que o B-tree equivalente. Se a ordem física não acompanha o tempo, ele não serve e o B-tree volta a ser a escolha.

## 4. Por que particionar tabelas de eventos em vez de só indexar?

Índice não resolve tabela que cresce sem limite: o planner continua avaliando partições antigas. Com particionamento por range e TTL, o pruning ignora o passado e o dashboard com agregação materializada saiu de 8,4s para 1,1s.

## 5. Como aplicar índice em produção sem derrubar a escrita?

Sempre `CREATE INDEX CONCURRENTLY`, fora da janela de pico: não segura `AccessExclusiveLock`. A criação é mais lenta e não roda em transação, então a janela de deploy precisa prever isso. Nenhum índice desta atividade foi aplicado em produção, apenas documentado e provado.
