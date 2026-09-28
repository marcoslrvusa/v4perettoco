# PERFORMANCE-SUPABASE.md: Standard de Performance em PostgreSQL (Supabase)

> Padrão da V4 para escrever, revisar e rodar queries de Supabase (PostgreSQL) em
> produção. Aplica a fila `mt_jobs`, sync de CRM, dashboards e qualquer view com dado vivo.

## 0. Escopo, não-escopo e termos

**Escopo:** toda query que roda em ciclo de produção (webhook, worker, view, dashboard,
função RPC) no Postgres gerenciado pelo Supabase. Inclui índices, particionamento,
`autovacuum`, RLS, paginação, janelas, CTEs e revisão de plano.

**Não-escopo:** modelagem de domínio (documentada no módulo de modelagem), tuning do
motor (parâmetros globais do Postgres, `shared_buffers`, `effective_cache_size` são
escopo de infraestrutura), e replicação/HA (escopo do provedor). Também ficam fora
queries de migração pontual que rodam uma única vez em janela de manutenção.

**Termos usados neste standard:**

| Termo | Significado operacional |
|---|---|
| Plano de execução | Árvore de nós que o planner escolheu: cada nó é um acesso, um join ou uma agregação |
| Custo estimado | Número sem unidade que o planner usa para comparar caminhos; não é tempo |
| `ANALYZE` | Comando que atualiza as estatísticas de coluna usadas pelo planner |
| `autovacuum` | Processo que limpa linhas mortas e atualiza estatísticas automaticamente |
| Bloat | Espaço ocupado por linhas mortas ou páginas não compactadas |
| Seletividade | Fração de linhas que um predicado deixa passar (0 a 1) |
| Cardinalidade | Número de valores distintos de uma coluna, usado para estimar `GROUP BY` |
| `work_mem` | Memória por operação antes de despejar em arquivo temporário |
| Spill | Saída de uma etapa para `temp file` quando `work_mem` estoura |
| `security barrier` | Cláusula que impede o planner de "puxar" a subquery da política para antes do filtro |

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

### 1.1 Regra canônica

> **Regra:** aceite a query somente se, para o mesmo `WHERE`, o plano escolher o caminho
> que lê o menor número de buffers e não apresenta `Sort` de materialização nem `temp
> file`.

Custo de uma consulta, em ordem de grandeza:

$$T \approx \frac{\text{buffers lidos} \times 8\,\text{kB}}{\text{vazão (MB/s)}} + \text{linhas avaliadas} \times c_f + \text{linhas retornadas} \times c_r$$

com $c_f$ ≈ 0,05 µs por linha filtrada, $c_r$ ≈ 1 µs por linha retornada e transferida
ao cliente.

**Exemplo numérico (parâmetros declarados):** plano A lê 94.120 buffers (735 MiB) e
retorna 5 linhas; plano B lê 90 buffers (0,7 MiB) e retorna 5 linhas. Com SSD a 500 MB/s:
$T_A$ = 735/500 + 2.400.000 × 0,05 µs = 1,47 s + 0,12 s = 1,59 s. $T_B$ = 0,0014 s +
0,00005 s ≈ 1,5 ms. Razão ≈ 1.000×. Mesmo com $c_f$ 10× pior, o plano B continua
ganhando por duas ordens de grandeza de I/O.

### 1.2 Sinais de gargalo ao ler o plano

Ao revisar um plano, procurar por estes sinais de gargalo:

| Sinal no plano | Consequência |
|---|---|
| `Seq Scan` em tabela > 100k linhas | leitura linear: trava em carga real |
| `Nested Loop` com re-scan alto | índice de FK ou de JOIN ausente |
| rows estimadas ≪ rows reais | estatísticas obsoletas (`ANALYZE` atrasado) |
| `Sort` explícito sobre coluna não indexada | ordem do índice não cobre o `ORDER BY` |
| `Bitmap Heap Scan` em série temporal | BRIN não foi considerado |
| `Hash Join` com `temp file` (spill) | trabalho excede `work_mem` |
| `Rows Removed by Filter` acima de 10× as linhas retornadas | seletividade do índice não aproveitada |
| `Planning Time` > `Execution Time` em query repetida | CTE não inlined ou `PREPARE` ausente |
| `Buffers: shared read` alto com `hit` baixo | buffer pool frio: índice grande demais para a memória |
| `SubPlan` com correlação executada N vezes | `count(DISTINCT)` ou função escalar no SELECT |

### 1.3 Tabela de decisão

| Se | E | Então |
|---|---|---|
| `Seq Scan` em tabela > 100k | filtro tem 1-3 predicados de igualdade | índice B-tree composto na ordem igualdade → range → `ORDER BY` |
| `Seq Scan` em série temporal | coluna monotônica com a física da tabela | índice BRIN + conferir ordenação física |
| Filtro em `jsonb` ou array | sem função sobre a coluna no `WHERE` | índice GIN |
| `Sort` de milhões de linhas | `ORDER BY` já no índice | acrescentar a coluna do `ORDER BY` ao índice composto |
| `temp file` no plano | agregação ou hash grande | subir `work_mem` da sessão/role ou pré-agregar |
| `count(DISTINCT)` > 1M de linhas | resultado cacheável por período | materializar em tabela de resumo com refresh incremental |
| `OFFSET` crescente | listagem passa da página 100 | trocar para paginação por cursor composto |
| Plano muda após release | estatísticas ou `search_path` mudou | `ANALYZE` + revisar `pg_stat_user_tables` |
| `EXPLAIN` limpo em dev | RLS ativo em produção | repetir o plano com `request.jwt.claims` setado |

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
3. PK já é índice (unique): não recriar.
4. **FK sempre indexada quando participa de JOIN.**

Em produção, usar sempre `CREATE INDEX ... CONCURRENTLY` (não segura `AccessExclusiveLock`, não derruba escrita durante criação).

### 2.1 Custo de escrita: quanto cada índice cobra

Cada índice é um formato de armazenamento a mais que `INSERT`, `UPDATE` e `DELETE`
precisam manter, além do `WAL` correspondente.

**Exemplo numérico (parâmetros declarados):** tabela com 100 escritas/s, largura média
de linha 300 bytes, três índices de 2 colunas (≈ 80 bytes de entrada cada). Escrita
líquida de índices: 100 × 3 × 80 × 2,5 = 60.000 bytes/s ≈ 60 kB/s de `WAL` extra. Para
uma tabela de 5.000 escritas/s no mesmo formato: 5.000 × 3 × 80 × 2,5 = 3.000.000
bytes/s ≈ 3 MB/s, o que passa a importar e justifica repensar quais índices existem.

**Regra prática:** antes de criar o quarto índice de uma tabela quente, medir
`pg_stat_user_indexes.idx_scan` por 7 dias. Índice com menos de 100 scans na janela é
candidato a remoção.

### 2.2 Índice parcial e índice de expressão

Índice parcial cobre só as linhas que interessam e reduz tamanho e custo de escrita:

```sql
CREATE INDEX CONCURRENTLY idx_mt_jobs_queued
  ON mt_jobs (queue, scheduled_at)
  WHERE status = 'queued';
```

Cuidado: o `WHERE` da query precisa ser **compatível** com o do índice (o planner só
usa o índice se conseguir provar que o predicado da query implica o do índice). Índice
de expressão resolve filtro sobre função, desde que a função seja `IMMUTABLE`:

```sql
CREATE INDEX CONCURRENTLY idx_leads_email_lower ON leads (lower(email));
-- a query precisa usar exatamente lower(email), não email
```

### 2.3 Por que o índice não é usado (checklist do planner)

1. Cast implícito entre `text` e `varchar`/`citext` quebra a comparação binária.
2. Função sobre a coluna no `WHERE` (`date(created_at) = ...`) esconde a coluna.
3. `COLLATION` diferente da usada na criação do índice.
4. Predicado com `OR` de colunas diferentes sem índice `Bitmap OR` viável.
5. Estatísticas antigas fazendo o planner achar o índice seletivo demais.
6. RLS complexa introduzindo `JOIN` antes do acesso.
7. Tabela pequena: varrer 500 linhas é mais barato que descer a árvore.

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

### 3.1 Retenção e TTL

Partição velha não deve viver para sempre. O job de retenção precisa de três passos:
criar a partição futura com folga, desanexar a partição expirada, dropar.

```sql
-- 1. criação adiantada (executar semanalmente)
CREATE TABLE IF NOT EXISTS sync_log_p2026_09 PARTITION OF sync_log
  FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');

-- 2 e 3. retenção de 180 dias
DETACH PARTITION sync_log_p2026_02 FROM sync_log CONCURRENTLY;
DROP TABLE sync_log_p2026_02;
```

`DETACH ... CONCURRENTLY` evita o lock longo; o `DROP` subsequente é instantâneo do
ponto de vista das queries. Nunca usar `DELETE FROM tabela WHERE synced_at < ...` em
tabela de 12M linhas: o `DELETE` gera dead tuples, força `VACUUM` e mantém o tamanho do
arquivo. **Exemplo numérico (parâmetros declarados):** apagar 1M linhas de 120 bytes
gera 120 MB de dead tuples que o `autovacuum` leva em torno de 2 minutos para recolher
em `cost_delay = 5`; dropar a partição correspondente devolve os 120 MB no mesmo
segundo, sem varredura.

### 3.2 Quando não particionar

- Tabela abaixo de 5M de linhas sem previsão de crescimento: o overhead das partições
  não se paga e o `pg_partman` vira mais uma coisa para manter.
- Tabela com `UNIQUE` global que envolva colunas fora da chave de partição: o Postgres
  exige que a chave de partição esteja em toda `UNIQUE`/`PK`.
- Tabela com muitos `UPDATE` aleatórios: particionamento não reduz custo de escrita.

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

### 4.1 Por que o default atrasa

O parâmetro padrão `autovacuum_vacuum_scale_factor = 0,2` faz o Postgres esperar 20% da
tabela morrer. Em tabela de 2,4M linhas, isso significa 480.000 linhas mortas antes do
primeiro `VACUUM`, e nesse meio tempo o planner vê um mapa de visibilidade sujo e pode
escolher caminhos piores. Com `scale_factor = 0,02` e `threshold = 1000`, a conta vira
`max(1000, 2% da tabela)`, ou seja 48.000 linhas: dez vezes mais frequente.

**Exemplo numérico (parâmetros declarados):** fila com 2.400.000 linhas e 500
finalizações por minuto. Padrão: `VACUUM` a cada 480.000 ÷ 500 = 960 min, quase 16 h.
Calibrado: 48.000 ÷ 500 = 96 min. O custo de CPU do `VACUUM` calibrado é ~10× maior em
frequência, mas cada execução varre menos páginas, então o total de I/O por dia fica na
mesma ordem de grandeza.

### 4.2 Registros de `autovacuum` em andamento

```sql
SELECT pid, relid::regclass, phase, round(100.0 * blobs_done / nullif(blobs_total,0),1) AS pct
FROM pg_stat_progress_vacuum;
```

Se esse `SELECT` retorna linha durante pico, o `VACUUM` está disputando I/O com a
aplicação: subir `autovacuum_vacuum_cost_limit` ou mover a calibragem para a madrugada.

## 5. RLS sem destruir performance

RLS é aplicado **por linha** durante o scan: política complexa (subquery, JOIN em
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

### 5.1 Três formas de simular o plano com RLS ativo

```sql
-- A: setar as claims na própria sessão (mais simples)
SET request.jwt.claims = '{"sub":"...","client_id":42}';
SET role authenticated;
EXPLAIN (ANALYZE, BUFFERS) SELECT id FROM mt_jobs WHERE status = 'queued' LIMIT 5;

-- B: rodar pela API com header de autenticação e logging de plano habilitado
-- C: criar role de teste no staging com a mesma policy aplicada
```

Na prática, a opção A é a que entra no MR porque reproduz o caminho quente sem depender
do serviço HTTP.

### 5.2 `SECURITY BARRIER` e a troca de custo

Sem `SECURITY BARRIER`, o planner pode mover a subquery da política para antes do
filtro principal, avaliando-a N vezes. Com a cláusula, a política só roda nas linhas que
o filtro deixou passar. Em tabela de 2,4M linhas com política que consulta outra tabela:

**Exemplo numérico (parâmetros declarados):** sem `BARRIER`, a política roda 2,4M
vezes (1,8 s). Com `BARRIER`, roda apenas sobre as 5 linhas do `LIMIT` (0,001 ms). O
custo é que o planner perde alguma liberdade de reordenar, o que em políticas simples
não é relevante.

```sql
CREATE POLICY mt_jobs_rls ON mt_jobs
  FOR SELECT
  USING (client_id = public.current_client_id())
  WITH CHECK (client_id = public.current_client_id());
```

## 6. Padrões de query que a V4 adota

- **Paginação por cursor** em vez de `LIMIT/OFFSET` (OFFSET cresce O(n)).
- **Janelas (window functions)** para top-N por grupo no mesmo scan.
- **CTEs** para pipelines legíveis: inlined pelo planner sempre que possível.
- **`count(DISTINCT)`** em dados grandes: materializar agregado em tabela de resumo.
- Sem `SELECT *`: planejador e tamanho de linha importam em wide tables.
- **UPDATE/DELETE em batch** via CTE para evitar lock storm.

### 6.1 Paginação por cursor (padrão completo)

```sql
-- primeira página
SELECT id, created_at, payload
FROM mt_jobs
WHERE client_id = $1
ORDER BY created_at DESC, id DESC
LIMIT 50;

-- páginas seguintes: usar as chaves da última linha retornada
SELECT id, created_at, payload
FROM mt_jobs
WHERE client_id = $1
  AND (created_at, id) < ($2_cursor_created_at, $2_cursor_id)
ORDER BY created_at DESC, id DESC
LIMIT 50;
```

O índice deve ser `(client_id, created_at DESC, id DESC)` para casar exatamente com a
ordem. Com `OFFSET`, cada página recarrega e descarta; com cursor, o planner reentra
pelo índice na posição exata.

**Exemplo numérico (parâmetros declarados):** 2,4M linhas, `LIMIT 50`, página 1.000.
`OFFSET` lê 50.050 linhas; cursor lê 50. Latência relativa: 1.001× pior para o `OFFSET`,
mesmo com índice perfeito.

### 6.2 Janela para top-N por grupo (sem N+1)

```sql
SELECT *
FROM (
  SELECT client_id,
         object,
         synced_at,
         row_number() OVER (PARTITION BY client_id ORDER BY synced_at DESC) AS rn
  FROM sync_log
  WHERE synced_at >= now() - interval '30 days'
) t
WHERE rn = 1;
```

Um único scan substitui uma consulta por cliente. Se antes eram 812 clientes × 1
consulta = 812 round-trips, agora é 1.

### 6.3 CTE: quando inlined e quando materializada

Antes do PostgreSQL 12, todo `WITH` era materializado. A partir do 12 o planner
inlina CTEs não referenciadas mais de uma vez e sem `MATERIALIZED` explícito. CTE
referenciada duas vezes ou com `OFFSET`/`LIMIT` costuma ser materializada, o que pode
ser bom (evita recalcular) ou ruim (materializa 8M linhas).

**Regra:** se a CTE aparece mais de uma vez, escrever `WITH ... AS MATERIALIZED` de
forma explícita para documentar a intenção; se aparece uma vez só, deixar o planner
decidir e conferir com `EXPLAIN`.

### 6.4 Anti-padrões (o que o sênior reprovaria no MR)

| Anti-padrão | Por que reprova | Correção |
|---|---|---|
| `SELECT *` em wide table | transfere colunas que ninguém usa e quebra contrato de API | listar colunas |
| `LIMIT` sem `ORDER BY` determinístico | página pode pular ou repetir linha | ordenar por chave única |
| `OFFSET` em listagem administrativa | custo O(n) por página | cursor composto |
| `count(*)` a cada request de listagem | conta a tabela inteira toda vez | cache ou aproximação com limite |
| `UPDATE` linha a linha em loop | lock storm e N round-trips | `UPDATE ... FROM (VALUES ...)` em batch |
| `NOT IN` com subquery que pode ter `NULL` | conjunto vazio inesperado | `NOT EXISTS` |
| Função sobre coluna indexada (`date(col)`) | esconde a coluna do índice | predicado de range na coluna pura |
| `JOIN` em coluna com cast (`::text`) | impede uso do índice | alinhar tipos no schema |
| Ordem de índice por cardinalidade estimada errada | índice largo e pouco usado | medir com `pg_stats` e testar plano |
| `count(DISTINCT)` sobre 12M linhas | caro e não cacheável | tabela de resumo com refresh incremental |

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

## 8. Telemetria e alertas

| Métrica | Fonte | Cardinalidade | Alerta |
|---|---|---|---|
| Latência p95 do pick | log de duração do worker | por `queue` (baixa) | > 10 ms por 5 min |
| `buffers` lidos por query | `pg_stat_statements` | por `queryid` | crescimento > 3× sem deploy |
| Sequencial vs índice | `pg_stat_user_tables.seq_scan / idx_scan` | por tabela | `seq_scan` subindo em tabela quente |
| Dead tuples | `pg_stat_user_tables.n_dead_tup` | por tabela | `dead_pct` > 10% |
| Tamanho de partição | `pg_partition_tree` | por partição | partição ativa > 50 GB |
| Spill em disco | `pg_stat_temp_files` | por banco | > 0 em horário de pico |
| `temp file` total | `pg_stat_database.temp_bytes` | por banco | > 1 GB/dia |
| Chamadas lentas | `pg_stat_statements.mean_time` | por `queryid` | p95 > SLO |

**Regra de cardinalidade:** métrica por `queryid` é segura (centenas); métrica por
`client_id` explode (milhares) e só entra em log estruturado, nunca em etiqueta de
série temporal.

## 9. Plano de teste e critérios de aceite

**Cenários mínimos antes de dizer que a otimização funcionou:**

| Caso | Preparação | Esperado | Critério de falha |
|---|---|---|---|
| Pick da fila | 2,4M linhas sintéticas, 60 queues | `Index Scan`, `Execution Time` < 10 ms | qualquer `Seq Scan` na tabela |
| JOIN de auditoria | 12M linhas em `sync_log`, 30 dias | `Bitmap Index Scan` + `Nested Loop` por PK | `Hash Join` com `temp file` |
| Dashboard 7d | MV populada com 60k linhas/dia | `Seq Scan` na MV, < 1,5 s | scan em `events` bruto |
| RLS | claims setadas na sessão | mesmo plano da seção 1 | plano diferente com e sem claims |
| Paginação | 10 páginas seguidas | tempo constante por página | latência crescendo linearmente |
| Concorrência | 10 workers com `SKIP LOCKED` | 10 jobs distintos devolvidos | job processado duas vezes |
| Retenção | drop de partição de 180 dias | `DETACH` sem lock acima de 1 s | qualquer espera de lock visível |
| Bloat | 500 updates/s por 10 min | `dead_pct` < 10% após `VACUUM` | `dead_pct` > 20% |

**Procedimento:** rodar cada caso com `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)`, salvar
a saída em `2-sql/06-planos-antes-depois.md`, comparar `Execution Time` e `shared read`
com o plano documentado. Diferença maior que 2× exige investigação antes do merge.

## 10. Checklist de adesão ao standard

- [ ] Escopo e não-escopo lidos antes de escrever a query.
- [ ] Todo `SELECT` de produção tem `EXPLAIN (ANALYZE, BUFFERS)` anexado ao MR.
- [ ] Fórmula da seção 1 usada para justificar o plano escolhido.
- [ ] Tabela de decisão (se X e Y então Z) consultada quando há dúvida de índice.
- [ ] Ordem de colunas do índice composto justificada em comentário no MR.
- [ ] Custo de escrita estimado antes de adicionar índice em tabela quente.
- [ ] `pg_stat_user_indexes.idx_scan` verificado para índices candidatos a remoção.
- [ ] FK usada em `JOIN` indexada.
- [ ] Série temporal com BRIN só após conferir ordem física.
- [ ] Tabela append-only acima de 1M de linhas com partição e TTL.
- [ ] `DETACH CONCURRENTLY` usado na retenção, nunca `DELETE` massivo.
- [ ] `autovacuum` calibrado nas tabelas quentes e `dead_pct` < 10%.
- [ ] RLS com política de uma linha, sem `JOIN`, e plano validado com claims.
- [ ] Paginação por cursor com índice casado com a ordem.
- [ ] `count(DISTINCT)` grande materializado em resumo.
- [ ] Anti-padrões da seção 6.4 ausentes do código revisado.
- [ ] Métricas da seção 8 exportadas e alertas configurados.
- [ ] Cenários da seção 9 rodados em staging com volumetria representativa.
- [ ] Rollback documentado para toda mudança de índice ou MV.

## 11. Referências

- Curso: SQL Performance Explained, de Markus Winand (use-the-index-luke.com)
- Vídeo: Postgres Performance (Supabase, YouTube)
- Doc oficial: Using EXPLAIN (PostgreSQL), https://www.postgresql.org/docs/current/using-explain.html (verificada em 2026-09-28)
- Doc oficial: Query Optimization (Supabase), https://supabase.com/docs/guides/database/query-optimization (verificada em 2026-09-28)