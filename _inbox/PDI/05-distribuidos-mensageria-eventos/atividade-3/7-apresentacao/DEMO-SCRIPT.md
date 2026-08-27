# Script de Demonstração — Contingência Automatizada (Circuit Breaker) para APIs Externas

## Setup
```bash
# Estrutura da entrega
tree 05-distribuidos-mensageria-eventos/atividade-3/
```

## Passo 1: Contexto
Explique o problema:
> Quedas de CRMs/ERPs externos derrubavam workflows inteiros.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Circuit Breaker com estados closed/open/half-open
- Threshold de falhas + cooldown + recovery
- Fallback automático quando aberto
- Recuperação automática testando 1 requisição

## Passo 3: Entregas
Mostre os artefatos gerados:
- CIRCUIT-BREAKER.md (padrão)
- circuit_breaker.py (implementação)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Cascata de falhas | Sim | Mitigada |
| Fallback | Não | Sim |
