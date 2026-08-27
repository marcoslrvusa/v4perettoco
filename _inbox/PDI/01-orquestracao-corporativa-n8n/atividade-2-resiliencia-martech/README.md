# PDI — Resiliência MarTech n8n Enterprise

> **Área:** Automação & Infraestrutura
> **Unidade:** FV Marketing / V4 Company
> **Autor:** Marcos Perettoco
> **Data:** Agosto 2026
> **Status:** **Entregue (desenvolvido) · NÃO publicado — aguardando homologação**
>
> ✅ Entregas concluídas: 1-standards (3 docs) · 2-workflows (4 workflows validados
> com n8nac) · 3-supabase (schema v3.0 + migração) · 4-retrofit · 5-monitoring ·
> 6-automation · 7-apresentacao (deck HTML + relatório HTML/DOCX/PDF)

---

## Entregas desta PDI

```
PDI-MARTECH/
├── 1-standards/          → Padrões de filas, payload pesado e observabilidade
├── 2-workflows/          → Workflows n8n prontos para deploy (.workflow.ts)
├── 3-supabase/           → Schema + migração do banco de dados
├── 4-retrofit/           → Plano de retrofit para workflows MarTech existentes
├── 5-monitoring/         → Dashboards, queries e regras de alerta
├── 6-automation/         → Scripts de deploy e automação
└── 7-apresentacao/       → Deck e script de demonstração
```

## Problema Resolvido

A operação MarTech (integrações com CRMs terceiros, sincronizações em lote e
campanhas de pico) roda workflows síncronos em linha reta no n8n. Quando o volume
sobe — black friday, lançamento de campanha, importação em massa — os workflows
travam em payloads pesados, estouram a concorrência do n8n, e falhas de
sincronização com CRMs terceiros só aparecem depois de impactar o cliente.

Três frentes de trabalho:

1. **Filas e concorrência** — sub-workflows assíncronos com gestão de fila de
   mensagens para absorver picos de requisições MarTech sem travar a instância.
2. **Payload pesado** — nós Code otimizados (JS/Python) para processar payloads
   grandes de forma incremental, sem estourar memória ou event loop.
3. **Observabilidade CRM** — trilha de auditoria de sincronização com CRMs
   terceiros, com detecção precoce de divergência antes de afetar o cliente.

## Arquitetura Resumida

```
Gateways HTTP (pico MarTech)
  → Fila assíncrona (Supabase, status: queued → running → done/failed)
    → Workers com concorrência limitada (semáforo por slot)
      → Sub-workflow assíncrono por job
        → Payload Heavy Processor (chunking + streaming + memo)
          → CRM Sync Log (auditoria completa)
            → Detector de divergência (antes de afetar o cliente)
```

## Próximos Passos (homologação)

1. Revisar `1-standards/` (3 padrões) — já escritos
2. Aplicar schema v3.0 no Supabase (`bash 6-automation/run-migration.sh`)
3. Publicar workflows (`bash 6-automation/deploy-martech.sh`) e ajustar o ID do
   sub-workflow `[CC] MT - Heavy Payload Processor` no Worker
4. Executar retrofit nos workflows MarTech (`4-retrofit/`)
5. Configurar alertas (`5-monitoring/`) e validar com pico simulado

> ⚠️ NENHUM workflow foi enviado ao n8n nesta etapa — publicação apenas após homologação.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Pico absorvido sem travar instância | Nao suportado | 5x volume nominal |
| Concorrencia maxima no n8n | Ilimitada (travamento) | Limitada por slot |
| Payloads pesados processados | Travam / OOM | > 90% dos casos |
| Falha de sync CRM detectada | Apos cliente reclamar | < 5 min |
| Rastreabilidade de sync | Nenhuma | 100% dos jobs logados |
