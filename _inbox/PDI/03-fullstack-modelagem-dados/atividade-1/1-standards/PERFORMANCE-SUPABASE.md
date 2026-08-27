# PERFORMANCE-SUPABASE.md — Standard de Performance em PostgreSQL (Supabase)

> Padrão da V4 para escrever, revisar e rodar queries de Supabase (PostgreSQL) em
> produção. Aplica a fila `mt_jobs`, sync de CRM, dashboards e qualquer view com dado vivo.

## 1. Regra de ouro: nenhuma query sem plano de execução

Toda query que entra em ciclo de produção (webhook, worker, dashboard, view) deve
passar por `EXPLAIN (ANALYZE, BUFFERS)`. O plano de execução é a fonte da verdade.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id FROM mt_jobs
WHERE status = 'queued' AND queue = 'crm-sync'
ORDER BY scheduled_at ASC
LIMIT 5;
```

Ao revisar um plano, procurar por estes sinais de gargalo:

| Sinal no plano | Consequência |
|---|---|
| `Seq Scan` em tabela > 100k linhas | leitura linear — trava em carga real |
| `Nested Loop` com re-scan alto | índice de FK ou de JOIN ausente |
| rows estimadas ≪ rows reais | estatísticas obsoletas (`ANALYZE` atrasado) |
| `Sort` explícito sobre coluna não indexada | ordem do índice não cobre o `ORDER BY` |
| `Bitmap Heap Scan` em série temporal | BRIN não foi considerado |
| `Hash Join` com `temp file` (spill) | trabalho excede `work_mem` |

## 2. Índices por padrão de acesso

| Tipo | Quando usar | Exemplo |
|---|---|---|
| **B-tree** (default) | igualdade, range, `ORDER BY`, unicidade | `(queue, status, scheduled_at)` |
| **B-tree composto** | igualdade → range → ordenação | `(client_id, object, synced_at DESC)` |
| **GIN** | arrays, jsonb, busca full-text | `ON events USING gin(tags)` |
| **BRIN** | séries temporais fisicamente ordenadas por tempo | `ON sync_log USING brin(created_at)` |

Composição de índice B-tree:
1. Colunas de **igualdade primeiro**, depois **range**, depois **ORDER BY**.
2. Padrão `WHERE queue='x' AND status='y' ORDER BY created_at` → índice `(queue, status, created_at)` cobre Index Scan sem Sort.
3. PK já é índice (unique) — não recriar.
4. **FK sempre indexada quando participa de JOIN.**

Em produção, usar sempre `CREATE INDEX ... CONCURRENTLY` (não segura `AccessExclusiveLock`, não derruba escrita durante criação).

## 3. Particionamento por range (séries temporais)

Tabelas append-only (logs, eventos, sync) devem ser particionadas por range. O planner
aplica *partition pruning* e ignora partições antigas.

```sql
CREATE TABLE sync_log (
  id        bigint generated always as identity primary key,
  client_id bigint not null,
  object    text not null,
  synced_at timestamptz not null default now()
) PARTITION BY RANGE (synced_at);

CREATE TABLE sync_log_p2026_08 PARTITION OF sync_log
  FOR VALUES FROM ('2026-08-01') TO ('2026-08-08');
```

Para dado append-only ordenado por tempo, **BRIN** no índice de tempo é bem mais barato
que B-tree e resolve 90% dos casos de série temporal.

## 4. autovacuum calibrado

O default não acompanha tabela com updates/deletes frequentes (`mt_jobs`, filas).

```sql
ALTER TABLE mt_jobs SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_analyze_scale_factor = 0.01,
  autovacuum_vacuum_threshold = 1000,
  autovacuum_vacuum_cost_delay = 5
);
```

Monitorar bloat/dead tuples:

```sql
SELECT relname,
       n_dead_tup,
       n_live_tup,
       round(n_dead_tup * 100.0 / nullif(n_live_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY dead_pct DESC;
```

Meta: `dead_pct` < 10%. Deleção em massa → `VACUUM FULL` em janela de manutenção ou
drop de partição, nunca no horário de pico.

## 5. RLS sem destruir performance

RLS é aplicado **por linha** durante o scan — política complexa (subquery, JOIN em
função) força o planner para `Seq Scan`. Padrão V4:

1. Coluna de tenant `client_id` na própria linha + índice.
2. Política simples com `SECURITY DEFINER` (evita JOIN na política).
3. Verificar com `EXPLAIN` usando um usuário real com RLS ativo.

```sql
CREATE FUNCTION public.current_client_id() RETURNS bigint
  LANGUAGE sql STABLE SECURITY DEFINER AS
$$ SELECT NULLIF(current_setting('request.jwt.claims', true)::json->>'client_id', '')::bigint $$;

CREATE POLICY mt_jobs_rls ON mt_jobs
  FOR SELECT USING (client_id = public.current_client_id());
```

:warning: rodar `EXPLAIN` SEMSETTING o header de autenticação mostra um plano limpo mas
falso. O plano real precisa do `request.jwt.claims` setado.

## 6. Padrões de query que a V4 adota

- **Paginação por cursor** em vez de `LIMIT/OFFSET` (OFFSET cresce O(n)).
- **Janelas (window functions)** para top-N por grupo no mesmo scan.
- **CTEs** para pipelines legíveis — inlined pelo planner sempre que possivel.
- **`count(DISTINCT)`** em dados grandes: materializar agregado em tabela de resumo.
- Sem `SELECT *` — planejador e tamanho de linha importam em wide tables.
- **UPDATE/DELETE em batch** via CTE para evitar lock storm.

## 7. Checklist de revisão de query

- [ ] `EXPLAIN ANALYZE BUFFERS` no MR
- [ ] Sem `Seq Scan` em tabela > 100k linhas
- [ ] Índice composto com igualdade → range → ORDER BY
- [ ] FKs indexadas nos JOINs
- [ ] Séries temporais particionadas + BRIN
- [ ] `count(DISTINCT)` em grandes volumes materializado em tabela de resumo
- [ ] RLS validado com plano real (header de autenticação setado)
- [ ] Paginação por cursor
- [ ] `autovacuum` calibrado para tabelas quentes
- [ ] `CONCURRENTLY` em todo CREATE INDEX de produção