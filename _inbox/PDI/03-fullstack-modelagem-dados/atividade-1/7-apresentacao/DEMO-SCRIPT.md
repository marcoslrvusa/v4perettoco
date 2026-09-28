# Roteiro de Demo: Queries Complexas e Indexação no Supabase (PostgreSQL)

Abra o deck e percorra os slides na ordem. Tempo sugerido: 10 min.

## Parte A: narrativa nos slides

1. Slides 2 a 4 (3 min): abra com o problema de negócio. Fila `mt_jobs` com 2,4M linhas, dashboards de 8s e 3 timeouts de webhook por dia. Mostre a tabela dos 3 casos.
2. Slides 5 a 8 (4 min): rode ao vivo `EXPLAIN (ANALYZE, BUFFERS)` do pick da fila antes e depois. Aponte o Seq Scan com 2,38M linhas removidas, depois o Index Scan de 4ms. Repita o raciocínio para sync CRM e dashboard.
3. Slides 9 e 10 (2 min): defenda o padrão de índices por acesso e o particionamento com TTL. Reforce CONCURRENTLY fora de pico.
4. Slides 12 a 14 (1 min): feche com metas (pick abaixo de 10ms, sync abaixo de 250ms, dashboard abaixo de 1,5s) e o aviso de que nada foi aplicado em produção.

## Parte B: demonstração técnica ao vivo

Pré-requisitos: acesso de leitura ao banco de staging, papel `authenticated` criado,
volumetria de referência já populada (2,4M linhas em `mt_jobs`), e o arquivo
`2-sql/06-planos-antes-depois.md` aberto para comparação.

5. **Conferir a volumetria (30 s).** Comando:
   `SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE relname IN ('mt_jobs','sync_log','events');`
   Saída esperada: `mt_jobs` próximo de 2.400.000, `sync_log` próximo de 12.000.000.
   Critério de falha: qualquer tabela com menos de 10% da volumetria esperada.
   Se falhar: parar e rodar o seed do `2-sql/README.md`; não continuar com banco vazio,
   porque o plano antigo pode até aparecer correto em tabela pequena.

6. **Rodar o plano adversarial (1 min).** Comando:
   `EXPLAIN (ANALYZE, BUFFERS) SELECT j.id, j.client_id, j.payload FROM mt_jobs j LEFT JOIN clients c ON c.id = j.client_id WHERE j.status = 'queued' AND j.queue = 'crm-sync' ORDER BY j.priority DESC, j.created_at ASC LIMIT 1;`
   Saída esperada: `Seq Scan on mt_jobs`, `Rows Removed by Filter` acima de 2.000.000 e
   `Execution Time` acima de 1.000 ms.
   Critério de falha: aparecer `Index Scan` (o índice já existe no staging) ou
   `Execution Time` abaixo de 100 ms.
   Se falhar: rodar `DROP INDEX CONCURRENTLY idx_mt_jobs_pick;` no staging e repetir.

7. **Apontar os três nós do plano (1 min).** Comando: nenhum, é leitura. Mostrar na tela
   `Seq Scan`, `Nested Loop` e `Sort`. Dizer em voz alta: "o nó de baixo custa 2,4M
   linhas, e todo o resto herda esse custo". Critério de falha: se o público não
   acompanhar, repetir com o desenho do Slide 15.

8. **Criar o índice no staging (1 min).** Comando:
   `CREATE INDEX CONCURRENTLY idx_mt_jobs_pick ON mt_jobs (queue, status, scheduled_at);`
   Saída esperada: `CREATE INDEX` (pode levar dezenas de segundos em 2,4M linhas).
   Critério de falha: erro de lock ou de transação (`CREATE INDEX CONCURRENTLY` não roda
   dentro de `BEGIN`). Se falhar: sair da transação e repetir.

9. **Rodar o plano corrigido (1 min).** Comando: mesma query do passo 6, agora sem o
   `LEFT JOIN clients`. Saída esperada: `Index Scan using idx_mt_jobs_pick`,
   `Execution Time` abaixo de 10 ms e `Buffers: shared hit` abaixo de 200.
   Critério de falha: `Execution Time` acima de 50 ms.
   Se falhar: `ANALYZE mt_jobs;` e repetir; se persistir, conferir ordem de colunas.

10. **Mostrar a conta dos buffers (1 min).** Comando: `EXPLAIN (ANALYZE, BUFFERS)` e ler
    os campos `shared hit` e `shared read`. Fazer a conta ao vivo: 103.720 páginas ×
    8 kB = 810 MiB contra 120 × 8 kB = 0,94 MiB. Critério de falha: os números não
    baterem em ordem de grandeza com o `06-planos-antes-depois.md`. Se falhar: registrar
    a diferença e não comparar tempos absolutos.

11. **Demostrar o `SKIP LOCKED` (2 min).** Abrir duas abas de SQL. Na aba 1, rodar:
    `BEGIN; SELECT id FROM mt_jobs WHERE status='queued' AND queue='crm-sync' ORDER BY priority DESC LIMIT 1 FOR UPDATE;` (sem commit).
    Na aba 2, rodar a mesma query. Saída esperada: a aba 2 não bloqueia e devolve outra
    linha (ou conjunto vazio se só houver uma). Critério de falha: a aba 2 ficar
    `idle in transaction` aguardando lock. Se falhar: `ROLLBACK;` na aba 1 e repetir.

12. **Mostrar RLS com e sem claims (1,5 min).** Comando:
    `EXPLAIN (ANALYZE, BUFFERS) SELECT id FROM mt_jobs WHERE status='queued' LIMIT 5;`
    depois `SET request.jwt.claims = '{"client_id":42}'; SET role authenticated;` e
    repetir. Saída esperada: plano idêntico nas duas rodadas, com filtro de `client_id`.
    Critério de falha: plano muito pior com claims (volta a `Seq Scan`). Se falhar:
    conferir se existe índice em `(client_id)` e se a política é de uma linha.

13. **Mostrar o refresh incremental da MV (1 min).** Comando:
    `EXPLAIN (ANALYZE, BUFFERS) SELECT count(*) FROM mv_daily_metrics WHERE day >= now() - interval '7 days';`
    Saída esperada: `Seq Scan on mv_daily_metrics` com poucas dezenas de milhares de
    linhas e `Execution Time` abaixo de 500 ms. Critério de falha: plano lendo `events`
    bruto. Se falhar: a MV não existe no staging; pular para o passo seguinte.

14. **Fechar com métricas e status (1 min).** Voltar ao Slide 20, ler a tabela antes e
    depois, e explicitar: "nada disso foi aplicado em produção nesta etapa". Critério de
    falha: alguém perguntar "e já está rodando?" e a resposta não ser "não, está em
    homologação".

## Parte C: encerramento

15. **Deixar o staging limpo (1 min).** Comando:
    `DROP INDEX CONCURRENTLY IF EXISTS idx_mt_jobs_pick;` (somente se o índice foi criado
    só para a demo). Saída esperada: `DROP INDEX`. Critério de falha: esquecer o índice e
    deixar a escrita do staging 15% mais lenta. Se falhar: rodar o `DROP` antes de sair.

16. **Material de apoio:** pdi-fullstack-modelagem-dados-a1.pdf (dossiê completo) + 2-sql/06-planos-antes-depois.md (planos para reproduzir no staging).

## Checklist antes de começar a demo

- [ ] Staging com volumetria de referência populada e `ANALYZE` rodado.
- [ ] `idx_mt_jobs_pick` removido no início (para mostrar o "antes" de verdade).
- [ ] Aba de SQL separada para o teste de `SKIP LOCKED`.
- [ ] `statement_timeout` de 30 s na sessão de demonstração.
- [ ] `06-planos-antes-depois.md` aberto para comparação lado a lado.
- [ ] Rollback do índice decorado (`DROP INDEX CONCURRENTLY`).
- [ ] Deck na tela, Slide 15 aberto para a conta de buffers.
- [ ] Relatório PDF disponível para quem quiser o dossiê completo.

## Se a internet ou o banco cair no meio

Não improvisar: voltar ao Slide 15 (a conta de buffers está no deck) e usar o
`06-planos-antes-depois.md` como prova documental. A demonstração perde o impacto ao
vivo, mas a evidência permanece, porque os planos foram capturados com
`EXPLAIN (ANALYZE, BUFFERS)` em condições declaradas.
