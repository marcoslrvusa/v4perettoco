# PDI — Computação Serverless (Cloud Function/AWS Lambda) integrada com segurança ao banco

> **Área:** Arquitetura Full Stack
> **Unidade:** V4 Company / FV Marketing
> **Autor:** Marcos Perettoco
> **Data:** 25/08/2026
> **Status:** **Entregue (desenvolvido) · NÃO publicado — aguardando homologação**

---

## Problema Resolvido

Tarefas pontuais (export de relatório, webhook de CRM) rodavam em instâncias always-on, desperdiçando custo. Esta atividade entrega uma função serverless (GCP Cloud Function) que se conecta ao banco de forma segura (Secret Manager + pooler), processa o evento e desliga — sem servidor dedicado.

## Entregas desta PDI

- Padrão de segurança serverless
- Função Cloud Function
- Dockerfile

## Validação

Artefatos desenvolvidos e versionados. Publicação em produção aguarda homologação.
