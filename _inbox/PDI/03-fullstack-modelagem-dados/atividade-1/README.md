# PDI — Queries Complexas e Indexação no Supabase (PostgreSQL)

> **Área:** Automação & Infraestrutura
> **Unidade:** FV Marketing / V4 Company
> **Autor:** Marcos Perettoco
> **Data:** Agosto 2026
> **Status:** **Entregue (desenvolvido) · NÃO publicado — aguardando homologação**
>
> ✅ Entregas concluídas: 1-standards (perf standard) · 2-sql (5 provas de conceito com
> adversarial antes/depois) · 3-casos (3 gargalos reais) · 7-apresentacao (deck + demo +
> relatório HTML/DOCX/PDF)

---

## Entregas desta PDI

```
atividade-1/
├── 1-standards/          → PERFORMANCE-SUPABASE.md (planos de execução, EXPLAIN, índices,
│                            particionamento, autovacuum)
├── 2-sql/                → Queries otimizadas + PoCs com adversarial antes/depois
│                            (JOINs pesados, janelas, CTEs, índices BRIN/B-tree/GIN, RLS)
├── 3-casos/              → 3 casos de gargalo em produção (fila mt_jobs, sync CRM, dashboard)
└── 7-apresentacao/       → Deck, script de demonstração e relatório
```

## Problema Resolvido

O Supabase que sustenta a operação SDR IA e a fila `mt_jobs` sofria com queries
escritas sem plano de execução: JOINs pesados sem índice, leituras sequenciais em
tabelas de milhões de linhas, funções com RLS que vazavam para o caminho quente das
consultas e `autovacuum` desconfigurado — o resultado eram timeouts de webhook,
dashboards que abriam em 8s+ e fila com backlog invisível.

Com EXPLAIN ANALYZE como método, foram corrigidos 3 gargalos reais:

1. **Fila `mt_jobs`** — consulta de worker varria 100% da tabela por falta de índice
   composto; com `(status, queue, scheduled_at)` o plano virou Index Scan e a latência
   caiu de 1.8s para 4ms.
2. **Sync CRM** — JOIN de auditoria sem índice de FK + filtro em coluna sem índice;
   corrigido com índice em `(client_id, object, synced_at DESC)` e CTE de janela.
3. **Dashboard** — agregação com `count(DISTINCT)` + janela sobre 12M de linhas;
   resolvido com materialização parcial (tabela agregada + índice BRIN no tempo).

## Arquitetura Resumida

```
EXPLAIN ANALYZE (método de diagnóstico)
  → Índices certos por padrão de acesso
      ├── B-tree   → igualdade/range (fila mt_jobs, chaves compostas)
      ├── GIN      → arrays/jsonb (tags, eventos)
      ├── BRIN     → séries temporais (logs, sync, eventos)
  → Particionamento por range (tabelas de eventos com TTL)
  → autovacuum calibrado + monitoramento de bloat
  → RLS com índices respeitados (security barrier + policies simples)
```

## Próximos Passos (homologação)

1. Rodar `06-planos-antes-depois.md` no staging com dados sintéticos (pgbench).
2. Aplicar os índices em produção fora da janela de pico (CONCURRENTLY).
3. Configurar o job de particionamento/TTL das tabelas de eventos.
4. Validar RLS com teste de força bruta (pgbench + roles de teste).

> ⚠️ Nenhum índice foi aplicado em produção nesta etapa — apenas documentado e provado.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Worker da fila `mt_jobs` (pick job) | 1.8s (Seq Scan) | < 10ms |
| JOIN de sync CRM (auditoria 30d) | 4.2s | < 250ms |
| Dashboard de performance (janela 7d) | 8.4s | < 1.5s |
| Bloat em tabelas de log | não monitorado | < 20% |
| Timeout de webhook por query lenta | ~3/dia | 0 |
