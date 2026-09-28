# PDI: Padrao Universal de Tratamento de Erros n8n Enterprise

> **Area:** Automacao & Infraestrutura
> **Unidade:** FV Marketing / V4 Company
> **Autor:** Marcos Perettoco
> **Data:** Julho 2026
> **Status:** Homologado

---

## Entregas desta PDI

```
PDI/
├── 1-standards/          → Documentacao do padrao (+ taxonomia, retry matrix)
├── 2-workflows/          → Workflows n8n prontos para deploy (.workflow.ts)
├── 3-supabase/           → Schema + migracao do banco de dados
├── 4-retrofit/           → Plano de retrofit para workflows existentes
├── 5-monitoring/         → Dashboards, queries e regras de alerta
├── 6-automation/         → Scripts de deploy e automacao
└── 7-apresentacao/       → Deck e script de demonstracao
```

## Problema Resolvido

7 workflows SDR IA com erro recorrente, sem padrao de tratamento, sem notificacao,
sem dead letter queue, sem circuit breaker. Falhas silenciosas que passavam dias
sem deteccao.

## Arquitetura Resumida
    
```
Node-Level (retryOnFail + onError)
  → Error Handler Central (classifica + notifica + persiste)
    → Circuit Breaker (abre apos 5 falhas)
      → Dead Letter Queue (payload completo para replay)
```

## Proximos Passos

1. Revisar `1-standards/STANDARD-ERROR-HANDLING.md`
2. Subir schema v2.1 no Supabase (`3-supabase/`)
3. Fazer push dos workflows de orquestracao (`2-workflows/`)
4. Executar retrofit nos SDR IA (`4-retrofit/`)
5. Validar com falha provocada (`5-monitoring/`)

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Falhas silenciosas | 7 workflows sem notificacao | Zero |
| Tempo medio de deteccao | Dias | < 1 minuto |
| Taxa de auto-cura (retry) | 0% | > 70% |
| Circuitos abertos sem alerta | 100% | 0% |

## Decisoes e tradeoffs

1. Handler central unico em vez de um handler por workflow: reduz a manutencao a um unico ponto com 10 nos validados com n8nac. O tradeoff e concentrar o risco: se o handler cair, perde-se notificacao, mas nao se perde dado porque a DLQ vive no Supabase com SLA proprio e o Circuit Breaker Monitor roda a cada 5 min de forma independente.
2. Tres camadas obrigatorias em vez de uma: a Camada 1 com retryOnFail captura cerca de 73% das falhas transientes no proprio no sem overhead de workflow externo, a Camada 2 classifica o que escapa e a Camada 3 protege contra cascata. O custo e mais configuracao por no, compensado pela taxa de auto-cura acima de 70%.
3. Code node nunca retenta: erro de logica (como toDateTime undefined ou null constraint em telefone) nao se resolve com nova tentativa. O tradeoff e exigir validacao previa com IF e try/catch, em troca de nao queimar creditos de API com retry inutil.
4. Circuit breaker isolado por workflow com limiar de 5 falhas consecutivas e cooldown de 5 min com recovery automatico: impede que uma API fragilizada receba chamadas em sequencia. O tradeoff e pausar temporariamente um fluxo que poderia ter uma tentativa isolada com sucesso, em troca de estabilidade sistemica.
5. DLQ permanente no Supabase (schema v2.1 com 4 tabelas e 4 views) em vez de confiar no log interno do n8n: o prune do n8n apaga execucoes antigas, enquanto a DLQ preserva payload completo com correlationId estavel para replay e auditoria. O custo e manter migracao e views como vw_error_health_score e vw_circuits_open_now.

## Impacto no negocio

Com 7 workflows SDR IA sem notificacao e deteccao levando dias, cada falha silenciosa derrubava o SLA de atendimento a leads sem ninguem saber. O padrao reduz a deteccao para menos de 1 min via Slack, eleva a auto-cura para mais de 70% com retry no no e zera circuitos abertos sem alerta (de 100% para 0%). O retrofit completo cabe em 4 dias, com cerca de 1h para as 5 correcoes pontuais ja mapeadas (20 min no ADPLAN e 10 min em cada um dos outros 4), o que corta risco operacional e retrabalho de investigacao manual.

## Referencias de estudo

- Curso: Automacao e Orquestracao n8n do Basico ao Avancado, na Udemy.
- Video: Error Trigger in n8n, tratamento centralizado de erros, no YouTube, canal oficial n8n.
- Doc: n8n Docs, Error handling with Error Trigger workflows, na plataforma n8n Docs.
- Doc: Supabase Docs, Database tables, views and indexes, na plataforma Supabase Docs.
