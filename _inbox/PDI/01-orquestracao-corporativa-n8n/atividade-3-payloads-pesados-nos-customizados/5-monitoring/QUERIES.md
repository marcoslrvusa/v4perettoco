# Monitoring: Performance de Payload e Nós Code

Queries SQL para monitorar o processamento de payloads pesados e a saúde dos
nós Code (JS/Python) após o retrofit da atividade 3.

## Premissas

- Usa as tabelas da atividade 1 (`error_*`) e da atividade 2 (`mt_*`).
- O nó `Return Metrics` dos novos workflows expõe `processedItems`, `deduped`,
  `durationMs` e `itemsPerSecond`: alimente uma tabela de métricas se quiser
  histórico (sugestão: `mt_payload_metrics`).

## 1. Pico de processamento (top runs)

```sql
SELECT
  workflow_name,
  processed_items,
  deduped,
  duration_ms,
  items_per_second,
  executed_at
FROM mt_payload_metrics
ORDER BY processed_items DESC
LIMIT 20;
```

## 2. Runs lentas (mais de 60s)

```sql
SELECT *
FROM mt_payload_metrics
WHERE duration_ms > 60000
ORDER BY duration_ms DESC;
```

## 3. Items por segundo (tendência)

```sql
SELECT
  date_trunc('hour', executed_at) AS hr,
  round(avg(items_per_second)) AS avg_ips,
  max(items_per_second) AS max_ips
FROM mt_payload_metrics
GROUP BY hr
ORDER BY hr DESC;
```

## 4. Dedupe ratio (payloads com muita duplicação)

```sql
SELECT
  workflow_name,
  round(100.0 * deduped / NULLIF(processed_items + deduped, 0), 1) AS dedupe_pct,
  count(*) AS runs
FROM mt_payload_metrics
GROUP BY workflow_name
ORDER BY dedupe_pct DESC;
```

## 5. Alertas sugeridos

| Condição | Ação |
|---|---|
| `duration_ms > 60000` | Alertar: payload ou nó regrediu |
| `items_per_second` cai > 50% vs média 24h | Investigar nó Code |
| `dedupe_pct > 50%` | Cliente envia duplicado: orientar filtro |

### 5.1 Como montar a condição de regressão

A comparação contra média móvel evita alerta falso em pico legítimo de volume.
A forma canônica, em duas partes:

```sql
-- 1) baseline: média e desvio das últimas 24h, exceto a hora corrente
WITH base AS (
  SELECT
    workflow_name,
    avg(items_per_second) AS media_24h,
    stddev(items_per_second) AS desvio_24h
  FROM mt_payload_metrics
  WHERE executed_at >= now() - interval '24 hours'
    AND executed_at < date_trunc('hour', now())
  GROUP BY workflow_name
)
-- 2) execução atual comparada à baseline
SELECT m.workflow_name, m.items_per_second, b.media_24h,
       round(100.0 * (b.media_24h - m.items_per_second) / nullif(b.media_24h, 0), 1)
         AS queda_pct
FROM mt_payload_metrics m
JOIN base b ON b.workflow_name = m.workflow_name
WHERE m.executed_at >= date_trunc('hour', now())
  AND m.items_per_second < b.media_24h * 0.5;
```

Regra prática: alertar quando a queda passa de 50% **e** o desvio das últimas 24 h
é menor que 30% da média. Se o desvio é grande, o workflow é variável por natureza
e um único valor baixo não é evidência de regressão.

### 5.2 Cardinalidade e custo da telemetria

Uma linha por execução, nunca por item. Com 20 execuções por dia de três workflows,
a tabela cresce 60 linhas/dia, ou cerca de 22 mil linhas por ano: irrelevante para
qualquer índice. Já uma métrica por item em payload de 100k geraria 100.000 linhas
por execução, destruindo o próprio painel que deveria observar o sistema.

Índice mínimo, criado junto com a tabela:

```sql
CREATE INDEX IF NOT EXISTS mt_payload_metrics_executed_at_idx
  ON mt_payload_metrics (executed_at DESC);
```

Sem esse índice, a consulta de tendência por hora faz varredura completa da tabela
em cada refresh do painel. Com ele, a janela recente é lida direto do fim do índice.

### 5.3 Interpretação das três métricas juntas

Nenhuma métrica isolada conta a história completa. A leitura combinada:

| `duration_ms` | `items_per_second` | `dedupe_pct` | Interpretação |
|---|---|---|---|
| Alto | Baixo | Normal | Regressão de complexidade ou conteúdo mais pesado por item |
| Alto | Normal | Muito alto | Payload muito maior que o normal, processamento correto |
| Normal | Baixo | Normal | Carga de CPU do host ou execuções concorrentes disputando worker |
| Baixo | Alto | Muito alto | volume duplicado pelo produtor: performance boa, dado ruim |
| Normal | Normal | Normal | Pipeline saudável |

O caso mais sutil é o segundo: `duration_ms` alto com `items_per_second` normal
significa que a máquina está trabalhando certo e o volume é que cresceu. Não é
regressão de código, é sinal de que o produtor precisa partir o payload. Alertar
nessa condição como se fosse bug levaria o time a otimizar o que não está quebrado.

## 6. Schema sugerido (mt_payload_metrics)


```sql
CREATE TABLE IF NOT EXISTS mt_payload_metrics (
  id bigint generated always as identity primary key,
  workflow_name text not null,
  processed_items int,
  deduped int,
  duration_ms int,
  items_per_second numeric,
  executed_at timestamptz not null default now()
);
```

> Tabela de métricas é opcional e **aditiva**: não altera nenhuma tabela existente
> das atividades 1 e 2. Criar somente após homologação.