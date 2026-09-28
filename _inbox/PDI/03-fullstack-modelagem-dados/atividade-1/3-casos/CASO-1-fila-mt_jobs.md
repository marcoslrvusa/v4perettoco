# CASO 1: Gargalo: fila `mt_jobs` no pick do worker

## Sinais

- Worker SDR IA rodando polling a cada 15s começou a estourar o timeout do comando.
- `mt_jobs` quebrou 2.4M linhas; pódio do Grafana mostrava `Seq Scan on mt_jobs`.
- O pick de job, que rodava em ~50ms, degradou para **1.82s** quando a fila encheu
  numa campanha de pico (black friday) e o webhook de enfileiramento começou a 504.

## Diagnóstico

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT j.id, j.client_id, j.payload
FROM mt_jobs j
LEFT JOIN clients c ON c.id = j.client_id
WHERE j.status = 'queued' AND j.queue = 'crm-sync'
ORDER BY j.priority DESC, j.created_at ASC
LIMIT 1;
```

O plano mostrava:

- `Seq Scan on mt_jobs` com `Rows Removed by Filter: 2,381,450`: status/queue sem índice.
- `Nested Loop` no JOIN (FK `client_id` desindexada): re-scan por linha.
- `Sort` em 2,1M linhas para pegar 1: pobríssimo.

Duas causas-raiz: filtro da fila sem índice composto (**igualdade→range→ORDER BY**) e LEFT JOIN
que o pick nunca precisava (payload já trazia o que o worker usa).

## Correção

```sql
-- rascunho reprovado na revisão: ordem invertida (range antes da igualdade) e
-- expressão inválida no índice. Ficou registrado para mostrar o que não fazer:
CREATE INDEX CONCURRENTLY idx_mt_jobs_pick
  ON mt_jobs (status, queue, scheduled_at->fim DESC? não);
-- versão final:
CREATE INDEX CONCURRENTLY idx_mt_jobs_pick
  ON mt_jobs (queue, status, scheduled_at);
CREATE INDEX CONCURRENTLY idx_mt_jobs_client ON mt_jobs (client_id);
```

A ordem `(queue, status, scheduled_at)` foi escolhida assim: `queue` é igualdade, logo
primeiro; `status` também é igualdade e vem depois para reduzir ainda mais a faixa;
`scheduled_at` entra por último porque é a coluna de range e de ordenação. Na ordem
`(status, queue, ...)` o plano também funciona para este `WHERE`, mas o índice passa a
ser comum a todas as queues e cresce mais devagar para cada faixa específica. A
diferença foi medida no staging e ficou abaixo da margem de ruído, então a decisão
documentada é: **igualdade mais seletiva primeiro, depois igualdade, depois range.**

Índice auxiliar de `client_id` é separado porque não pode entrar no índice composto: se
entrasse como primeira coluna, o pick (que não filtra por cliente) não conseguiria usá-lo
como prefixo.

Uso id segura: `FOR UPDATE SKIP LOCKED` no pick para 5 workers consumindo a mesma URL.

```sql
WITH picked AS (
  SELECT id
  FROM mt_jobs
  WHERE status = 'queued'
    AND queue = 'crm-sync'
    AND scheduled_at <= now()
  ORDER BY priority DESC, scheduled_at ASC
  LIMIT 5
  FOR UPDATE SKIP LOCKED
)
UPDATE mt_jobs j
SET status = 'running', started_at = now()
FROM picked p
WHERE j.id = p.id
RETURNING j.id, j.client_id, j.payload;
```

Por que `SKIP LOCKED`: sem ele, dois workers que leem ao mesmo tempo prendem a mesma
linha com `FOR UPDATE` e o segundo espera o primeiro terminar. Com `SKIP LOCKED`, o
segundo simplesmente pula a linha já tomada e pega a seguinte. O `LIMIT 5` é obrigatório
porque uma leitura sem limite em fila de 2,4M linhas devolveria tudo o que está `queued`
num pico.

Por que `ORDER BY priority DESC, scheduled_at ASC` e não só `created_at`: prioridade
alta precisa furar a fila mesmo que tenha chegado depois, e o desempate por
`scheduled_at` mantém a ordem de chegada dentro de cada prioridade. O índice
`(queue, status, scheduled_at)` cobre o filtro; a ordenação por `priority` ainda gera um
`Sort` pequeno, agora sobre 10.000 linhas em vez de 2,1M, o que cabe em `work_mem` sem
spill.

### Resultado

| Métrica | Antes | Depois |
|---|---|---|
| Execution Time | 1.82s | **4.1ms** |
| Estratégia | Seq Scan + Sort | Index Scan |
| Enqueue sob pico | 504 / fila cresce | processo continua |
| Read (buffers) | 94,400 | < 120 |

## Aplicação do padrão

- Toda classe de query de worker deve ter `EXPLAIN` no MR.
- Pick de fila sempre `FOR UPDATE SKIP LOCKED` + limite explícito (`LIMIT 5`).
- `update_status` em batch (CTE): nunca editor linha a linha no loop.

## Monitoramento e rollback

**Sinais que o problema voltou:** p95 do pick acima de 10 ms por 5 minutos, contagem de
`queued` subindo sem novo pico de enfileiramento, ou `seq_scan` de `mt_jobs` crescendo
mais rápido que `idx_scan`.

```sql
SELECT seq_scan, idx_scan, n_live_tup, n_dead_tup
FROM pg_stat_user_tables WHERE relname = 'mt_jobs';

SELECT schemaname, relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE relname = 'mt_jobs' ORDER BY idx_scan ASC;
```

Um índice com `idx_scan = 0` depois de uma semana de produção significa que o planner
não está escolhendo ele: revisar ordem de colunas, `COLLATION` e se alguma função
envolvendo a coluna apareceu no `WHERE`.

**Rollback:** se o índice novo piorar a escrita em mais de 15% de throughput, remover em
janela de manutenção:

```sql
DROP INDEX CONCURRENTLY idx_mt_jobs_pick;
```

`CONCURRENTLY` também na remoção, porque um `DROP` simples segura
`AccessExclusiveLock` e pararia o enfileiramento durante a operação.

**Custo de manter o índice (Exemplo numérico: parâmetros declarados):** fila com 500
escritas/s e índice de 3 colunas de ~60 bytes. Overhead de `WAL` ≈ 500 × 60 × 2,5 =
75.000 bytes/s ≈ 75 kB/s. Em 24 h: 75 kB/s × 86.400 s = 6,48 GB de `WAL` extra por dia.
Aceito porque o `WAL` é sequencial e o ganho de 1,8 s por leitura (5.760 leituras/dia)
devolve mais de 2,8 h de espera por dia.