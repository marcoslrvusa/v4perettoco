# Deck PDI: Queries Complexas e Indexacao no Supabase (PostgreSQL)

Area: Automacao & Infraestrutura | Unidade: FV Marketing / V4 Company | Autor: Marcos Luciano | Data: Agosto 2026

## Slide 1: Titulo

Queries Complexas e Indexacao no Supabase (PostgreSQL): do Seq Scan de 1,8s ao Index Scan de 4ms com metodo EXPLAIN.

## Slide 2: Resumo executivo

O Supabase da operacao SDR IA e da fila `mt_jobs` sofria com queries sem plano de execucao. Com EXPLAIN ANALYZE como metodo, corrigimos 3 gargalos reais sem trocar de banco e sem aplicar nada em producao nesta etapa.

## Slide 3: Contexto de producao

Fila `mt_jobs` com 2,4M linhas lida pelo worker a cada 15s. `sync_log` com 12M linhas. Dashboards que abriam em 8s ou mais. Timeouts de webhook cerca de 3 por dia.

## Slide 4: O problema

| Caso | Sintoma | Causa-raiz |
|---|---|---|
| Fila `mt_jobs` | pick de 1,8s com Seq Scan | filtro sem indice composto + LEFT JOIN desnecessario |
| Sync CRM | JOIN de auditoria em 4,2s | FK sem indice + filtro em coluna sem indice |
| Dashboard | agregacao em 8,4s | count(DISTINCT) + janela sem materializacao |

## Slide 5: Diagnostico com EXPLAIN

Sinais procurados no plano: Seq Scan em tabela acima de 100k linhas, Nested Loop com re-scan alto, Sort explicito sobre coluna nao indexada, Hash Join com spill em temp file, estatisticas obsoletas.

## Slide 6: Caso 1, fila mt_jobs (1,8s para 4ms)

Antes: Seq Scan com 2,38M linhas removidas por filtro + Sort em 2,1M linhas para pegar 1. Depois: indice `(queue, status, scheduled_at)` e remocao do LEFT JOIN. Plano virou Index Scan.

## Slide 7: Caso 2, sync CRM (4,2s para 180ms)

Indice em `(client_id, object, synced_at DESC)` e CTE de janela para a auditoria de 30 dias. FK de JOIN sempre indexada.

## Slide 8: Caso 3, dashboard (8,4s para 1,1s)

Agregacao com count(DISTINCT) e janela sobre 12M linhas resolvida com materializacao parcial: tabela agregada mais indice BRIN no tempo.

## Slide 9: Padrao de indices por acesso

B-tree para igualdade, range e ORDER BY. B-tree composto na ordem igualdade, range e depois ORDER BY. GIN para arrays e jsonb. BRIN para series temporais, 10x menor que o B-tree equivalente.

## Slide 10: Particionamento, vacuum e RLS

Tabelas append-only particionadas por range com job de TTL. Autovacuum calibrado com monitoramento de bloat abaixo de 20%. RLS com policies simples e indices respeitados, fora do caminho quente.

## Slide 11: Entregas

1-standards com PERFORMANCE-SUPABASE.md. 2-sql com 5 PoCs adversariais antes/depois mais 06-planos-antes-depois.md. 3-casos com 3 gargalos reais. 7-apresentacao com deck, demo e relatorio.

## Slide 12: Metricas e metas

Pick da fila abaixo de 10ms. Sync CRM abaixo de 250ms. Dashboard abaixo de 1,5s. Bloat abaixo de 20%. Zero timeout de webhook por query lenta.

## Slide 13: Decisoes e tradeoffs

EXPLAIN obrigatorio antes de producao. Indice composto que custa escrita e paga leitura. BRIN so onde a ordem fisica acompanha o tempo. Particionamento que exige job de TTL. CONCURRENTLY fora de pico, mais lento e fora de transacao.

## Slide 14: Proximos passos e status

Rodar os planos no staging com pgbench. Aplicar indices em producao fora de pico. Configurar job de particionamento e TTL. Validar RLS com teste de forca. Status: desenvolvido, em homologacao, nada aplicado em producao.
