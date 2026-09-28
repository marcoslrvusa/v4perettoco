# Queries de monitoramento: Observabilidade CRM

Banco: Postgres. Tabela central: `crm_sync_logs(ts, level, trace_id, crm, integration, op, entity, record_id, status, code, duration_ms, attempt, msg)`. Todas as consultas abaixo rodam direto na view do painel e devem responder em menos de 1 s na janela padrão.

## Taxa de erro por CRM (janela 5 min)

```sql
SELECT crm, COUNT(*) FILTER (WHERE level='ERROR') * 1.0 / COUNT(*) AS error_rate
FROM crm_sync_logs
WHERE ts > now() - interval '5 minutes'
GROUP BY crm HAVING error_rate > 0.02;
```

Leitura correta: o `HAVING` filtra grupos, não linhas. Se um CRM tiver 1 evento e ele falhar, a taxa é 1,0 e o alerta dispara com uma amostra inútil. Por isso a versão de produção precisa do piso de volume:

```sql
SELECT crm,
       COUNT(*)                                          AS total,
       COUNT(*) FILTER (WHERE level='ERROR')             AS erros,
       COUNT(*) FILTER (WHERE level='ERROR') * 1.0
         / NULLIF(COUNT(*), 0)                           AS error_rate
FROM crm_sync_logs
WHERE ts > now() - interval '5 minutes'
GROUP BY crm
HAVING COUNT(*) >= 50
   AND COUNT(*) FILTER (WHERE level='ERROR') * 1.0
       / NULLIF(COUNT(*), 0) > 0.02;
```

`NULLIF(COUNT(*), 0)` evita divisão por zero em janelas vazias. O piso de 50 eventos significa: só alertamos quando temos amostra suficiente para afirmar que 2% é 2%.

## Record com 3 falhas consecutivas (sistêmico)

```sql
SELECT record_id, crm, count(*) AS fails
FROM crm_sync_logs
WHERE level='ERROR' AND ts > now() - interval '1 hour'
GROUP BY record_id, crm HAVING count(*) >= 3;
```

Essa é a assinatura do evento envenenado. Se o mesmo `record_id` falha três vezes no CRM, o problema quase nunca é o CRM: é o payload. Próximo passo automático é enviar para a DLQ em vez de tentar pela quarta vez.

Detalhamento para o runbook, com a causa mais frequente à vista:

```sql
SELECT record_id, crm, code, msg,
       array_agg(trace_id ORDER BY ts) AS traces,
       min(ts) AS primeira, max(ts) AS ultima
FROM crm_sync_logs
WHERE level='ERROR'
  AND ts > now() - interval '1 hour'
GROUP BY record_id, crm, code, msg
HAVING count(*) >= 3
ORDER BY ultima DESC;
```

## p95 de latência por entidade (SLO)

```sql
SELECT entity, percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_ms) AS p95_ms
FROM crm_sync_logs WHERE ts > now() - interval '24 hours' GROUP BY entity;
```

`percentile_cont` faz interpolação contínua, o que é o correto para latência. Comparado com `percentile_disc`, que pula para o valor observado, a versão contínua evita o efeito de degrau em amostras pequenas.

## Cobertura de trace_id (invariante 1)

```sql
SELECT count(*) FILTER (WHERE trace_id IS NULL OR trace_id = '') AS sem_trace,
       count(*) AS total,
       100.0 * count(*) FILTER (WHERE trace_id IS NULL OR trace_id = '')
         / NULLIF(count(*), 0) AS pct_cobertura
FROM crm_sync_logs
WHERE ts > now() - interval '24 hours';
```

Aceite: `sem_trace = 0`. Qualquer valor acima de zero viola o contrato e deve bloquear o rollout da onda em andamento.

## Backlog pendente (Little's Law aplicada)

```sql
SELECT crm,
       count(*) FILTER (WHERE status = 'pending')      AS pendentes,
       count(*) FILTER (WHERE status = 'poison')       AS em_dlq,
       extract(epoch FROM now() - min(ts)
               FILTER (WHERE status = 'pending'))      AS idade_oldest_s
FROM crm_sync_logs
WHERE ts > now() - interval '15 minutes'
GROUP BY crm
HAVING count(*) FILTER (WHERE status = 'pending') > 0;
```

`idade_oldest_s > 300` significa evento parado há mais de 5 min, ou seja, fila engasgada. Pela Lei de Little, com $\lambda = 4$ eventos/s e fila de 12 eventos, o tempo médio esperado é $W = L/\lambda = 12/4 = 3$ s. Se a medição mostra 300 s, a fila está 100 vezes mais lenta que o projeto: isso é alerta, não é ruído.

## PII em claro (invariante 3)

```sql
SELECT trace_id, integration, msg
FROM crm_sync_logs
WHERE ts > now() - interval '24 hours'
  AND (msg ~* '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    OR msg ~* '\b[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}\b');
```

Deve retornar zero linhas. Se retornar, é incidente de segurança, não é ajuste de texto: revogar acesso ao log, apagar as linhas afetadas e corrigir o nó que emitiu.

## Duplicatas por idempotency key

```sql
SELECT trace_id, crm, op, count(*) AS aplicacoes
FROM crm_sync_logs
WHERE status = 'ok'
  AND ts > now() - interval '1 hour'
GROUP BY trace_id, crm, op
HAVING count(*) > 1;
```

Com idempotência funcionando, uma reinjeção do mesmo evento gera registro de "duplicata detectada", não uma segunda escrita `ok`. Se essa consulta retornar linhas, o dedupe está quebrado.

## Latência p95 e alerta composto

```sql
WITH j AS (
  SELECT crm,
         count(*) AS total,
         count(*) FILTER (WHERE level='ERROR') * 1.0
           / NULLIF(count(*),0) AS taxa,
         percentile_cont(0.95)
           WITHIN GROUP (ORDER BY duration_ms) AS p95_ms
  FROM crm_sync_logs
  WHERE ts > now() - interval '5 minutes'
  GROUP BY crm
)
SELECT * FROM j
WHERE total >= 50 AND (taxa > 0.02 OR p95_ms > 30000);
```

Um único disparo cobre os dois sinais: estabilidade (taxa) e agudeza (latência). Dois alertas separados multiplicam o ruído; um alerta composto com duas condições é mais fácil de operar.

## Índices recomendados

```sql
CREATE INDEX IF NOT EXISTS idx_sync_ts        ON crm_sync_logs (ts DESC);
CREATE INDEX IF NOT EXISTS idx_sync_trace     ON crm_sync_logs (trace_id);
CREATE INDEX IF NOT EXISTS idx_sync_crm_ts    ON crm_sync_logs (crm, ts DESC);
CREATE INDEX IF NOT EXISTS idx_sync_rec       ON crm_sync_logs (record_id, crm)
       WHERE level = 'ERROR';
CREATE INDEX IF NOT EXISTS idx_sync_partial_err ON crm_sync_logs (ts DESC)
       WHERE level = 'ERROR';
```

Custo de escrita: cinco índices em tabela de log com cerca de 72 MB/mês é irrelevante em armazenamento, mas cada índice adiciona trabalho a cada INSERT. Por isso o índice parcial `WHERE level = 'ERROR'` é o que mais importa: ele é pequeno e atende justamente as consultas de incidente.

## Custo de consulta e retenção

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT crm, count(*) FROM crm_sync_logs
WHERE ts > now() - interval '5 minutes' GROUP BY crm;
```

Critério de aceite: `actual time` abaixo de 1000 ms e nenhum `Seq Scan` sobre a tabela cheia na janela de 5 min. Se aparecer `Seq Scan`, o índice de `ts` não está sendo usado, geralmente por comparação com expressão em vez de coluna pura.

Retenção:

```sql
DELETE FROM crm_sync_logs WHERE ts < now() - interval '90 days';
```

Agendado diariamente. Manter `trace_store` por 180 dias, porque auditoria e rollback de conflito entre CRMs exigem histórico maior do que a janela de operação.

## Painel: consulta do dia a dia do plantão

```sql
SELECT crm,
       count(*) FILTER (WHERE status='settled') AS concluidos,
       count(*) FILTER (WHERE status='pending') AS pendentes,
       count(*) FILTER (WHERE status='poison')  AS dlq,
       round(100.0 * count(*) FILTER (WHERE level='ERROR')
             / NULLIF(count(*),0), 2)           AS pct_erro
FROM crm_sync_logs
WHERE ts > now() - interval '1 hour'
GROUP BY crm
ORDER BY pct_erro DESC NULLS LAST;
```

Uma tela, quatro números por CRM, nenhuma navegação. Se o plantão precisar de mais do que isso para decidir, o contrato está incompleto.
