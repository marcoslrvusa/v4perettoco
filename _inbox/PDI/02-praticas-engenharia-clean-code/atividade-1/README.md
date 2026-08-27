# PDI — Refatoração de Módulo Legado com SOLID e Clean Architecture

> **Área:** Engenharia de Software
> **Unidade:** V4 Company / FV Marketing
> **Autor:** Marcos Perettoco
> **Data:** 25/08/2026
> **Status:** **Entregue (desenvolvido) · NÃO publicado — aguardando homologação**

---

## Problema Resolvido

Um módulo crítico de orquestração de campanhas estava acoplado: a classe `CampaignService` misturava regra de negócio, acesso a banco, envio de e-mail e chamadas de API de CRM em um único arquivo de 600+ linhas, impossível de testar. Esta atividade refatora o módulo aplicando os 5 princípios SOLID e separando em camadas (domain / application / infrastructure), documentando antes e depois.

## Entregas desta PDI

- Documentação SOLID antes/depois
- Código legado (exemplo)
- Código refatorado em Clean Architecture

## Validação

Artefatos desenvolvidos e versionados. Publicação em produção aguarda homologação.
