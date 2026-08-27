# Script de Demonstração — Mapeamento de Domínios com Domain-Driven Design (DDD)

## Setup
```bash
# Estrutura da entrega
tree 02-praticas-engenharia-clean-code/atividade-3/
```

## Passo 1: Contexto
Explique o problema:
> Antes de codificar, os domínios de dados da empresa não estavam mapeados, gerando modelos duplicados e linguagem inconsistente entre times.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Mapeamento de 4 bounded contexts (CRM, Campaign, Agent, Billing)
- Definição de agregados com raiz e filhos
- Glossário de linguagem ubíqua
- Diagrama Mermaid de relacionamento dos domínios

## Passo 3: Entregas
Mostre os artefatos gerados:
- DOMAIN-MAP.md (mapa + diagrama)
- domain_models.py (modelos de domínio)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Domínios mapeados | 0 | 4 |
| Consistência de linguagem | Baixa | Alta |
