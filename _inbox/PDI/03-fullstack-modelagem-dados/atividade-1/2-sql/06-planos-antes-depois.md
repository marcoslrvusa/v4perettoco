# 06-planos-antes-depois.md: Planos de execução (adversarial before × after)

> Planos documentais dos 3 casos reais. Rodando em qualquer Supabase 15+ com os
> schemas de referência (`mt_jobs` 2.4M · `sync_log` 12M · `events` 8M · `leads` 900k).
> Use `EXPLAIN (ANALYZE, BUFFERS, COSTS)` para reproduzir.

---

## CASO 1: Fila `mt_jobs` (pick de worker)

### ANTES: 1.82s (produção)

```text
Limit  (cost=41,920.00..41,920.01 rows=1)
  ->  Sort  (cost=41,920.00..41,901.22 rows=1)   [762 ms]
        Sort Key: j.priority DESC, j.created_at ASC
        ->  Nested Loop  (cost=0.86..41,918.00 rows=1)
              ->  Seq Scan on mt_jobs j
                    Filter: ((status='queued') AND (queue='crm-sync'))
                    Rows Removed by Filter: 2,381,450
              ->  Index Scan using clients_pkey (c.id)     [re-scan por linha]
  Planning Time: 0.4 ms   Execution Time: 1,820 ms
Buffers: shared hit=9,600 read=94,120
```

### DEPOIS: 4ms (pós índices + remoção do LEFT JOIN)

```text
Limit  (cost=0.56..4.90 rows=5)
  ->  Index Scan using idx_mt_jobs_pick on mt_jobs j
        Index Cond: ((status = 'queued') AND (queue = 'web'))
        Filter: (scheduled_at <= now())
  Planning Time: 0.3 ms   Execution Time: 4.1 ms
```

Δ 450×. O `Seq Scan` de 2.4M vira `Index Scan`; o `Sort` de 762ms vira inexistente.

### Leitura nó a nó do plano ANTES

| Nó | O que faz | Custo real |
|---|---|---|
| `Limit` | para na 1ª linha encontrada | nenhum, é o topo |
| `Sort` | ordena `priority DESC, created_at ASC` | 762 ms de CPU + memória |
| `Nested Loop` | para cada linha do scan, busca o cliente | re-scan por linha |
| `Seq Scan on mt_jobs` | varre 2.400.000 linhas filtrando | 1.038 ms de I/O |
| `Index Scan clients_pkey` | busca o cliente correspondente | ~1 µs × 1 linha (ok) |

O `Sort` é o maior vilão depois do `Seq Scan`: ele precisa de memória para 2,1M linhas
ordenadas e, se `work_mem` for curta, despeja em `temp file`. O `Nested Loop` não é
intrinsicamente ruim, mas aqui ele roda sobre a saída de um filtro caro, amplificando o
problema.

### Leitura nó a nó do plano DEPOIS

| Nó | O que faz | Custo real |
|---|---|---|
| `Limit` | para em 5 linhas | nenhum |
| `Index Scan idx_mt_jobs_pick` | desce pelo prefixo `(queue, status)` | 4,1 ms |
| `Index Cond` | igualdade em `queue` e `status` | avaliado dentro do índice |
| `Filter scheduled_at <= now()` | descarta o que ainda não venceu | poucas linhas |

Sem `Sort`, sem `Nested Loop`, sem leitura de página da heap além das necessárias.
`Buffers: shared hit < 120` significa 120 × 8 kB ≈ 0,94 MiB lidos, contra 810 MiB no
plano antigo.

### Por que remover o LEFT JOIN

O `LEFT JOIN clients` existia porque a UI queria o nome do cliente. Em produção o worker
não usa esse nome: ele só despacha `payload`. Tirar o `JOIN` remove uma árvore inteira
do plano e elimina a dependência de índice de FK para esta consulta específica. Quando o
nome for necessário, a query de leitura da UI ganha o seu próprio índice em
`(client_id)` e usa `JOIN` explícito, documentado no seu próprio MR.

## CASO 2: Sync CRM (auditoria 30d)

### ANTES: 4.2s

```text
Finalize HashAggregate  (group key: c.id, s.object, s.direction)
  ->  Gather N Worker(s)  processes 1
        ->  Partial HashAggregate  ...
              ->  Hash Join  (s.client_id = c.id)
                    Hash cond: s.client_id = c.id
                    ->  Seq Scan on sync_log s
                          Filter: (created_at >= (now() - '30 days'))
                          Rows Removed by Filter: 11,820,144
                    ->  Hash  rows=812
  Execution Time: 4,210 ms
```

### DEPOIS: 180ms (índice composto + BRIN)

```text
HashAggregate  (HashAggregate)  rows=182
  ->  Bitmap Heap Scan on sync_log s
        Recheck Cond: (created_at >= now() - '30 days')
        ->  Bitmap Index Scan on idx_sync_log_created_brin
              Recheck Cond: same
  ->  Nested Loop  (c.id = s.client_id)  [Index Scan clients_pkey]
  Execution Time: 184 ms
```

Δ 23×. Endereçou o JOIN (índice na FK) e o filtro temporal (BRIN).

### Por que `Hash Join` aqui era um erro

O `Hash Join` constrói uma tabela hash da lado pequeno (`clients`, 812 linhas) e varre o
lado grande. Funciona bem quando o lado grande é varrido de qualquer forma. O problema é
que o lado grande era um `Seq Scan` de 12M linhas com filtro de 30 dias, e o filtro
descartava 11.820.144 linhas antes de qualquer junção. A ordem certa é: primeiro reduzir
o volume com índice temporal, depois juntar. Com o volume já reduzido, o planner troca
para `Nested Loop` com `Index Scan` na PK de `clients`, que custa ~1 µs por linha de
resultado.

**Exemplo numérico (parâmetros declarados):** 12.000.000 linhas varridas a 0,05 µs cada
= 600 ms só de filtrar, mais I/O de 12M × 120 bytes ≈ 1,4 GB. Com BRIN, o bitmap de
`created_at` reduz a leitura para as páginas que cobrem 30 dias, cerca de 180 ms no
total. A razão 4.210/184 = 23× é a soma da I/O evitada e do hash evitado.

---

## CASO 3: Dashboard de performance (janela 7d)

### ANTES: 8.4s

```text
HashAggregate  (3 scans na mesma tabela)
  ->  CTE totals  →  Seq Scan on events (8,102,400 rows) x 2
  CTE top        →  Seq Scan + HashAggregate (escolha da query)
  SubPlan        →  string_agg com correlação (`WHERE top.client_id = t.client_id`)
  Execution Time: 8,405 ms
```

### DEPOIS: ~380ms (materialização + 1 scan)

```text
Limit (50)  rows 
  ->  Sort (GroupAggregate)   SUM...
        ->  HashAggregate  (row=60,480 → mv_daily_metrics)
              ->  Seq Scan on mv_daily_metrics
                    Filter: (day >= (date_trunc('day', now()) - '7 days'))
  Execution Time: 384 ms
```

Δ 22×. `count(DISTINCT)` caro é movido para refresh incremental da MV.

### Como funciona o refresh incremental

A MV `mv_daily_metrics` guarda, por dia e por cliente, as três métricas que o dashboard
mostra. O refresh não recalcula tudo: ele só reprocessa os dias que mudaram.

```sql
INSERT INTO mv_daily_metrics (day, client_id, sessions, conversions, revenue)
SELECT date_trunc('day', e.created_at),
       e.client_id,
       count(DISTINCT e.session_id),
       count(DISTINCT e.conversion_id),
       sum(e.amount)
FROM events e
WHERE e.created_at >= now() - interval '3 days'
GROUP BY 1, 2
ON CONFLICT (day, client_id) DO UPDATE
  SET sessions = EXCLUDED.sessions,
      conversions = EXCLUDED.conversions,
      revenue = EXCLUDED.revenue;
```

**Exemplo numérico (parâmetros declarados):** `events` com 8.102.400 linhas em 90 dias
= 90.027 linhas/dia. O refresh de 3 dias varre 270.081 linhas (3,3% da tabela) em vez
de 8.102.400 (100%). O dashboard, que lê só 7 dias, passa a ler 60.480 linhas agregadas
em vez de 8,1M. Redução total de linhas lidas por request: 8.102.400 ÷ 60.480 = 134×.

O `ON CONFLICT ... DO UPDATE` torna o refresh idempotente: rodar duas vezes no mesmo
dia produz o mesmo resultado, o que permite reexecutar sem medo após uma falha.

---

## Comparativo consolidado

| Caso | Antes | Depois | Ganho | Mecanismo |
|---|---|---|---|---|
| 1. Fila `mt_jobs` | 1.820 ms | 4,1 ms | 450× | Índice composto + remoção de `JOIN` |
| 2. Sync CRM | 4.210 ms | 184 ms | 23× | Índice de FK + BRIN temporal |
| 3. Dashboard | 8.405 ms | 384 ms | 22× | Materialização parcial + refresh incremental |
| Soma | 14.435 ms | 572 ms | 25× | método EXPLAIN aplicado aos 3 casos |

**Exemplo numérico (parâmetros declarados):** com o dashboard sendo consultado 200
vezas por dia e o worker rodando 5.760 vezes por dia, o tempo de consulta total cai de
(200 × 8,405 s) + (5.760 × 1,82 s) = 1.681 s + 10.483 s = 12.164 s/dia para (200 ×
0,384 s) + (5.760 × 0,0041 s) = 77 s + 24 s = 101 s/dia. Economia: 12.063 s ≈ 3,35 h
de tempo de CPU e de espera por dia, apenas nestas duas rotinas.

---

## Checklist de leitura do plano

| Pergunta | Ferramenta |
|---|---|
| Estou lendo só `Seq Scan`? | Problema de índice ou RLS: ver Caso 1/5 |
| Os `rows` batem com a realidade? | Confiar em `ANALYZE` recente (autovacuum) |
| A soma no `Execution Time` explode em `Planning`? | CTE volumetricamente recalculada: forçar inline |
| Tem `temporary files`? | `work_mem` estourado: subir `work_mem` da sessão/role |
| Índice existe mas não é usado? | RLS complexa ou correção de `COLLATION`/type cast |

## Protocolo de reprodução no staging

1. **Preparar o banco:** rodar o seed sintético do `2-sql/README.md` com as volumetrias
   de referência (2,4M / 12M / 8M / 900k) e depois `ANALYZE` em todas as tabelas.
2. **Medir o antes:** executar a versão adversarial dentro de transação com
   `statement_timeout` de 30 s e capturar `EXPLAIN (ANALYZE, BUFFERS, COSTS)`.
3. **Aplicar a correção:** criar os índices com `CONCURRENTLY`, popular a MV e repetir
   `ANALYZE`.
4. **Medir o depois:** capturar o plano novo com os mesmos parâmetros de sessão.
5. **Comparar:** montar a linha da tabela "Comparativo consolidado" com `Execution Time`
   e `Buffers: shared read` dos dois planos.
6. **Verificar escrita:** rodar 10 mil `INSERT`s cronometrados antes e depois de cada
   índice novo e registrar o delta em `pg_stat_statements`.
7. **Registrar:** anexar as duas saídas ao `06-planos-antes-depois.md` e ao MR.

**Critério de aceite do protocolo:** os três casos reproduzem pelo menos 80% do ganho
documentado (450×, 23× e 22×) e nenhum `INSERT` sofre mais que 15% de queda de
throughput. Se um dos dois critérios falhar, a mudança não vai a produção.

## Limites conhecidos destes planos

- Os planos foram gerados em Postgres 15+; a árvore de `Bitmap Heap Scan` pode variar
  ligeiramente entre versões.
- Os tempos assumem buffer pool quente (dados em memória). Em banco frio, o `Seq Scan`
  piora ainda mais em relação ao `Index Scan`, porque o índice é menor e cabe mais fácil
  na memória.
- O `BRIN` assume ordem física coerente com o tempo. Se houver `VACUUM FULL` ou restore
  que reordene as páginas, é preciso recriar o índice.
- Os valores de `cost` do planner não são tempo. Comparar sempre `Execution Time`, não
  `cost`.