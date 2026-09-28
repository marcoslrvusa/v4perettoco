# Deck PDI: Queries Complexas e Indexação no Supabase (PostgreSQL)

Área: Automação & Infraestrutura | Unidade: FV Marketing / V4 Company | Autor: Marcos Luciano | Data: Agosto 2026

## Slide 1: Título

Queries Complexas e Indexação no Supabase (PostgreSQL): do Seq Scan de 1,8s ao Index Scan de 4ms com método EXPLAIN.

## Slide 2: Resumo executivo

O Supabase da operação SDR IA e da fila `mt_jobs` sofria com queries sem plano de execução. Com EXPLAIN ANALYZE como método, corrigimos 3 gargalos reais sem trocar de banco e sem aplicar nada em produção nesta etapa.

## Slide 3: Contexto de produção

Fila `mt_jobs` com 2,4M linhas lida pelo worker a cada 15s. `sync_log` com 12M linhas. Dashboards que abriam em 8s ou mais. Timeouts de webhook cerca de 3 por dia.

## Slide 4: O problema

| Caso | Sintoma | Causa-raiz |
|---|---|---|
| Fila `mt_jobs` | pick de 1,8s com Seq Scan | filtro sem índice composto + LEFT JOIN desnecessário |
| Sync CRM | JOIN de auditoria em 4,2s | FK sem índice + filtro em coluna sem índice |
| Dashboard | agregação em 8,4s | count(DISTINCT) + janela sem materialização |

## Slide 5: Diagnóstico com EXPLAIN

Sinais procurados no plano: Seq Scan em tabela acima de 100k linhas, Nested Loop com re-scan alto, Sort explícito sobre coluna não indexada, Hash Join com spill em temp file, estatísticas obsoletas.

## Slide 6: Caso 1, fila mt_jobs (1,8s para 4ms)

Antes: Seq Scan com 2,38M linhas removidas por filtro + Sort em 2,1M linhas para pegar 1. Depois: índice `(queue, status, scheduled_at)` e remoção do LEFT JOIN. Plano virou Index Scan.

## Slide 7: Caso 2, sync CRM (4,2s para 180ms)

Índice em `(client_id, object, synced_at DESC)` e CTE de janela para a auditoria de 30 dias. FK de JOIN sempre indexada.

## Slide 8: Caso 3, dashboard (8,4s para 1,1s)

Agregação com count(DISTINCT) e janela sobre 12M linhas resolvida com materialização parcial: tabela agregada mais índice BRIN no tempo.

## Slide 9: Padrão de índices por acesso

B-tree para igualdade, range e ORDER BY. B-tree composto na ordem igualdade, range e depois ORDER BY. GIN para arrays e jsonb. BRIN para séries temporais, 10x menor que o B-tree equivalente.

## Slide 10: Particionamento, vacuum e RLS

Tabelas append-only particionadas por range com job de TTL. Autovacuum calibrado com monitoramento de bloat abaixo de 20%. RLS com policies simples e índices respeitados, fora do caminho quente.

## Slide 11: Entregas

1-standards com PERFORMANCE-SUPABASE.md. 2-sql com 5 PoCs adversariais antes/depois mais 06-planos-antes-depois.md. 3-casos com 3 gargalos reais. 7-apresentacao com deck, demo e relatório.

## Slide 12: Métricas e metas

Pick da fila abaixo de 10ms. Sync CRM abaixo de 250ms. Dashboard abaixo de 1,5s. Bloat abaixo de 20%. Zero timeout de webhook por query lenta.

## Slide 13: Decisões e tradeoffs

EXPLAIN obrigatório antes de produção. Índice composto que custa escrita e paga leitura. BRIN só onde a ordem física acompanha o tempo. Particionamento que exige job de TTL. CONCURRENTLY fora de pico, mais lento e fora de transação.

## Slide 14: Próximos passos e status

Rodar os planos no staging com pgbench. Aplicar índices em produção fora de pico. Configurar job de particionamento e TTL. Validar RLS com teste de força. Status: desenvolvido, em homologação, nada aplicado em produção.
