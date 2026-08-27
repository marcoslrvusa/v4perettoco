# Script de Demonstração — Refatoração de Módulo Legado com SOLID e Clean Architecture

## Setup
```bash
# Estrutura da entrega
tree 02-praticas-engenharia-clean-code/atividade-1/
```

## Passo 1: Contexto
Explique o problema:
> Um módulo crítico de orquestração de campanhas estava acoplado: a classe CampaignService misturava regra de negócio, acesso a banco, envio de e-mail e chamadas de API de CRM em um único arquivo de 600+ linhas, impossível de testar.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Aplicação dos 5 princípios SOLID documentados antes/depois
- Separação em camadas: domain / application / infrastructure
- Ports (LeadRepository, Notifier) e adapters desacoplados
- Injeção de dependência no CampaignService

## Passo 3: Entregas
Mostre os artefatos gerados:
- SOLID-BEFORE-AFTER.md (mapeamento antes/depois)
- before_campaign_service.py (código legado)
- after_campaign_service.py (Clean Architecture)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Acoplamento (responsabilidades) | 4 em 1 classe | 1 por classe |
| Testabilidade | Nula | Alta (ports) |
| Linhas por classe | 600+ | < 40 |
