# PDI: Padrão Universal de Tratamento de Erros n8n Enterprise

> **Área:** Automação & Infraestrutura
> **Unidade:** FV Marketing / V4 Company
> **Autor:** Marcos Perettoco
> **Data:** Julho 2026
> **Status:** Homologado

---

## Entregas desta PDI

```
PDI/
├── 1-standards/          → Documentação do padrão (+ taxonomia, retry matrix)
├── 2-workflows/          → Workflows n8n prontos para deploy (.workflow.ts)
├── 3-supabase/           → Schema + migração do banco de dados
├── 4-retrofit/           → Plano de retrofit para workflows existentes
├── 5-monitoring/         → Dashboards, queries e regras de alerta
├── 6-automation/         → Scripts de deploy e automacao
└── 7-apresentacao/       → Deck e script de demonstracao
```

## Problema Resolvido

7 workflows SDR IA com erro recorrente, sem padrão de tratamento, sem notificação,
sem dead letter queue, sem circuit breaker. Falhas silenciosas que passavam dias
sem detecção.

## Arquitetura Resumida
    
```
Node-Level (retryOnFail + onError)
  → Error Handler Central (classifica + notifica + persiste)
    → Circuit Breaker (abre após 5 falhas)
      → Dead Letter Queue (payload completo para replay)
```

## Próximos Passos

1. Revisar `1-standards/STANDARD-ERROR-HANDLING.md`
2. Subir schema v2.1 no Supabase (`3-supabase/`)
3. Fazer push dos workflows de orquestração (`2-workflows/`)
4. Executar retrofit nos SDR IA (`4-retrofit/`)
5. Validar com falha provocada (`5-monitoring/`)

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Falhas silenciosas | 7 workflows sem notificação | Zero |
| Tempo médio de detecção | Dias | < 1 minuto |
| Taxa de auto-cura (retry) | 0% | > 70% |
| Circuitos abertos sem alerta | 100% | 0% |

## Decisões e tradeoffs

1. Handler central único em vez de um handler por workflow: reduz a manutenção a um único ponto com 10 nos validados com n8nac. O tradeoff é concentrar o risco: se o handler cair, perde-se notificação, mas não se perde dado porque a DLQ vive no Supabase com SLA próprio e o Circuit Breaker Monitor roda a cada 5 min de forma independente.
2. Três camadas obrigatórias em vez de uma: a Camada 1 com retryOnFail captura cerca de 73% das falhas transientes no próprio no sem overhead de workflow externo, a Camada 2 classifica o que escapa e a Camada 3 protege contra cascata. O custo é mais configuração por nó, compensado pela taxa de auto-cura acima de 70%.
3. Code node nunca retenta: erro de lógica (como toDateTime undefined ou null constraint em telefone) não se resolve com nova tentativa. O tradeoff é exigir validação previa com IF e try/catch, em troca de não queimar créditos de API com retry inútil.
4. Circuit breaker isolado por workflow com limiar de 5 falhas consecutivas e cooldown de 5 min com recovery automático: impede que uma API fragilizada receba chamadas em sequência. O tradeoff é pausar temporariamente um fluxo que poderia ter uma tentativa isolada com sucesso, em troca de estabilidade sistêmica.
5. DLQ permanente no Supabase (schema v2.1 com 4 tabelas e 4 views) em vez de confiar no log interno do n8n: o prune do n8n apaga execuções antigas, enquanto a DLQ preserva payload completo com correlationId estável para replay e auditoria. O custo é manter migração e views como vw_error_health_score e vw_circuits_open_now.

## Impacto no negócio

Com 7 workflows SDR IA sem notificação e detecção levando dias, cada falha silenciosa derrubava o SLA de atendimento a leads sem ninguém saber. O padrão reduz a detecção para menos de 1 min via Slack, eleva a auto-cura para mais de 70% com retry no nó e zera circuitos abertos sem alerta (de 100% para 0%). O retrofit completo cabe em 4 dias, com cerca de 1h para as 5 correções pontuais já mapeadas (20 min no ADPLAN e 10 min em cada um dos outros 4), o que corta risco operacional e retrabalho de investigação manual.

## Referências de estudo

- Curso: Automação e Orquestração n8n do Básico ao Avançado, na Udemy.
- Vídeo: Error Trigger in n8n, tratamento centralizado de erros, no YouTube, canal oficial n8n.
- Doc: n8n Docs, Error handling with Error Trigger workflows, na plataforma n8n Docs.
- Doc: Supabase Docs, Database tables, views and indexes, na plataforma Supabase Docs.
