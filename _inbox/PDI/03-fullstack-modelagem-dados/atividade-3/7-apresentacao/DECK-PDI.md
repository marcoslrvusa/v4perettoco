# PDI — Apresentação: Computação Serverless (Cloud Function/AWS Lambda) integrada com segurança ao banco

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: COMPUTAÇÃO SERVERLESS (CLOUD FUNCTION/AWS LAMBDA) INTEGRADA COM SEGURANÇA AO BANCO

Marcos Perettoco — V4 Company
25/08/2026 | Arquitetura Full Stack
```

---

## Slide 2: O Problema

**Tarefas pontuais (export, webhook) rodavam em instâncias always-on, desperdiçando custo e sem segurança de secrets.**

## Diagnóstico

- Custo fixo de servidores para jobs esporádicos
- Secrets em env var (risco)
- Conexões de banco sem pooler/TLS


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Cloud Function que conecta via Secret Manager
- Pooler (PgBouncer) com TLS
- IAM de minima privilégio
- Idempotência por chave de evento


---

## Slide 4: Entregas

## Artefatos

- SERVERLESS-SECURITY.md (padrão)
- main.py (Cloud Function segura)
- Dockerfile


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Custo (jobs esporádicos) | Always-on | Por execução |
| Secrets | Env var | Secret Manager |
---

## Slide 6: Próximos Passos

- Deploy em staging (GCP)
- Validar IAM e rotação de secrets
