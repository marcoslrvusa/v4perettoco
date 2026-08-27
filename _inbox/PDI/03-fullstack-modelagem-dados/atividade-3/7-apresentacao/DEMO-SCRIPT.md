# Script de Demonstração — Computação Serverless (Cloud Function/AWS Lambda) integrada com segurança ao banco

## Setup
```bash
# Estrutura da entrega
tree 03-fullstack-modelagem-dados/atividade-3/
```

## Passo 1: Contexto
Explique o problema:
> Tarefas pontuais (export, webhook) rodavam em instâncias always-on, desperdiçando custo e sem segurança de secrets.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Cloud Function que conecta via Secret Manager
- Pooler (PgBouncer) com TLS
- IAM de minima privilégio
- Idempotência por chave de evento

## Passo 3: Entregas
Mostre os artefatos gerados:
- SERVERLESS-SECURITY.md (padrão)
- main.py (Cloud Function segura)
- Dockerfile

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Custo (jobs esporádicos) | Always-on | Por execução |
| Secrets | Env var | Secret Manager |
