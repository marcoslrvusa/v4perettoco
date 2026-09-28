# 2-sql: Queries otimizadas e provas de conceito

> Cada arquivo traz uma **query adversarial** (como estava em produção) e a **versão
> otimizada** (como ficou), com plano `EXPLAIN` antes × depois. Os planos são
> representativos para volumetria de referência V4:
> `mt_jobs` 2.4M linhas · `sync_log` 12M · `events` 8M (particionado) ·
> `leads` 900k · `dashboard_daily` (agregado) 60k linhas/mês.
>
> Simulável em qualquer Supabase com o schema `schema-demo.sql` equivalente (ou
> gerar com pgbench). Rodar com:
>
> ```sql
> EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
> ```

## Como reproduzir a volumetria

Os números dos planos só fazem sentido se o banco tiver a mesma escala. Script de
geração sintética (parâmetros declarados):

```sql
-- 2,4M de jobs distribuídos em 60 queues, 4 estados
INSERT INTO mt_jobs (client_id, queue, status, priority, scheduled_at, payload)
SELECT (random() * 812)::bigint,
       ('q' || (random() * 59)::int),
       (ARRAY['queued','running','done','failed'])[(random()*3)::int + 1],
       (random() * 10)::int,
       now() - (random() * interval '90 days'),
       jsonb_build_object('n', g)
FROM generate_series(1, 2400000) g;

ANALYZE mt_jobs;
```

**Exemplo numérico (parâmetros declarados):** com 2,4M linhas e 60 queues, cada queue
tem em média 40.000 linhas; com 4 estados, cada combinação `(queue, status)` tem 10.000
linhas. É essa faixa de 10.000 linhas que o `Index Scan` precisa varrer, contra as
2.400.000 do `Seq Scan`. A razão de 240× em linhas avaliadas vira os 450× medidos em
tempo, porque o `Seq Scan` ainda paga o `Sort` de 2,1M linhas.

Antes de rodar qualquer `EXPLAIN ANALYZE` em banco compartilhado, checar se há lock e
se a tabela está quente:

```sql
SELECT pid, state, wait_event_type, wait_event, left(query, 80)
FROM pg_stat_activity
WHERE datname = current_database() AND state <> 'idle'
ORDER BY query_start;
```

## Arquivos

| Arquivo | Conteúdo | Antes → Depois |
|---|---|---|
| `01-caso-fila-mt_jobs.sql` | JOIN pesado + pick de worker da fila | 1.8s → 4ms |
| `02-dashboard-janelas.sql` | Window functions top-N por cliente | 8.4s → 1.1s |
| `03-sync-crm-cte.sql` | CTEs de auditoria de sync + drift | 4.2s → 180ms |
| `04-indices-brin-btree-gin.sql` | PoC dos 3 tipos de índice | BRIN/B-tree/GIN |
| `05-rls-performance.sql` | RLS na fila com plano real | Seq Scan → Index Scan |
| `06-planos-antes-depois.md` | Planos de execução completos | documental |

## Matriz de leitura: qual PoC abre para cada problema

| Se o problema é... | Abra | O que olhar no plano |
|---|---|---|
| Fila lenta, worker com timeout | `01` + `06` Caso 1 | `Rows Removed by Filter` e presença de `Sort` |
| Dashboard com agregação lenta | `02` + `06` Caso 3 | número de scans na mesma tabela |
| Auditoria ou relatório de período | `03` + `06` Caso 2 | `Hash Join` com `temp file` |
| Dúvida sobre qual índice escolher | `04` | tamanho do índice e `Execution Time` por tipo |
| Lentidão só com usuário autenticado | `05` | diferença de plano com e sem `request.jwt.claims` |

## Critérios de aceite dos PoCs

1. **Antes reproduzível:** a versão adversarial precisa falhar de forma observável
   (`Execution Time` acima do SLO ou `Seq Scan` em tabela grande) em staging.
2. **Depois verificável:** a versão otimizada precisa mostrar o caminho esperado
   (`Index Scan`, `Bitmap Index Scan` ou `Seq Scan` em MV pequena) e bater com a meta.
3. **Sem regressão de escrita:** se o PoC criar índice, medir o custo de `INSERT` antes
   e depois com `pg_stat_statements`.
4. **Plano salvo:** saída do `EXPLAIN (ANALYZE, BUFFERS)` anexada ao
   `06-planos-antes-depois.md`.
5. **Rollback:** script de `DROP INDEX CONCURRENTLY` ou de desfazimento da MV incluso.

## Anti-padrões que estes PoCs denunciam

- Query que filtra por coluna sem índice e depois ordena por outra: paga `Seq Scan` mais
  `Sort`.
- `LEFT JOIN` em colunas que a query nem seleciona: custo de join sem benefício.
- Agregação recalculada a cada request sobre 8M linhas em vez de refresh incremental.
- Política RLS com subquery que força `Seq Scan` mesmo com índice perfeito.
- `count(DISTINCT)` no mesmo select de listagem, dobrando o trabalho por request.

## Como validar sem afetar ninguém

```sql
BEGIN;
SET LOCAL statement_timeout = '30s';
SET LOCAL work_mem = '64MB';
EXPLAIN (ANALYZE, BUFFERS) ...;
ROLLBACK;
```

`EXPLAIN ANALYZE` executa a query de verdade, então o `ROLLBACK` desfaz escritas, mas a
I/O continua acontecendo. Por isso o `statement_timeout` é obrigatório: numa janela de
pico, uma query de 8 s pode disputar I/O com o worker da fila.