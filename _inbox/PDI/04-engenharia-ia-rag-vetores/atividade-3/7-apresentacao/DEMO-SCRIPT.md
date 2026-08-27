# Script de Demonstração — Sistema Multi-Agente Assíncrono (autoaperfeiçoamento contínuo)

## Setup
```bash
# Estrutura da entrega
tree 04-engenharia-ia-rag-vetores/atividade-3/
```

## Passo 1: Contexto
Explique o problema:
> Agentes atuais eram síncronos e de passo único, sem memória nem melhoria contínua.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- Bus de mensagens assíncrono (asyncio/Redis Streams)
- MemoryStore por agente (curto + longo prazo)
- CriticAgent que avalia e escreve lições (lessons.md)
- Orchestrator roteando tarefas por capacidade

## Passo 3: Entregas
Mostre os artefatos gerados:
- MULTIAGENT-PROTOCOL.md (protocolo)
- multiagent.py (protótipo assíncrono)
- lessons.md (memória de melhoria)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Memória entre runs | Não | Sim |
| Autoaperfeiçoamento | Não | Sim (loop) |
