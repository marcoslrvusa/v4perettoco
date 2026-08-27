# Script de Demonstração — Observabilidade e Logs de Sincronização n8n-CRM

## Setup
```bash
# Estrutura da entrega
tree 01-orquestracao-corporativa-n8n/atividade-4/
```

## Passo 1: Contexto
Explique o problema:
> Falhas de sincronização com CRMs terceiros (Salesforce, HubSpot, RD Station) só eram percebidas quando o cliente reclamava — não havia rastro estruturado de qual registro falhou, em qual etapa e por quê.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Padrão de log estruturado (JSON) com trace_id, entity, crm, action, record_id
- Workflow de observabilidade que propaga trace e emite log centralizado
- Painel SQL com taxa de erro por CRM, falhas consecutivas e p95 de latência
- Alerta proativo em #ops-crm antes do impacto ao cliente

## Passo 3: Entregas
Mostre os artefatos gerados:
- STANDARD-OBSERVABILITY-LOGS.md (padrão + SLO)
- Workflow n8n de log + alerta proativo
- Queries de dashboard (erro, falhas consecutivas, p95)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Detecção de falha de sync | Dias | < 1 min |
| Visibilidade por CRM | 0% | 100% |
| Alerta proativo | Não | Sim (SLO) |
