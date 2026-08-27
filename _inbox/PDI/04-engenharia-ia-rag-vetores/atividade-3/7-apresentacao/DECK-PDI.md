# PDI — Apresentação: Sistema Multi-Agente Assíncrono (autoaperfeiçoamento contínuo)

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: SISTEMA MULTI-AGENTE ASSÍNCRONO (AUTOAPERFEIÇOAMENTO CONTÍNUO)

Marcos Perettoco — V4 Company
25/08/2026 | Engenharia de IA
```

---

## Slide 2: O Problema

**Agentes atuais eram síncronos e de passo único, sem memória nem melhoria contínua.**

## Diagnóstico

- Sem memória entre execuções
- Sem comunicação entre agentes
- Sem loop de autoavaliação


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Bus de mensagens assíncrono (asyncio/Redis Streams)
- MemoryStore por agente (curto + longo prazo)
- CriticAgent que avalia e escreve lições (lessons.md)
- Orchestrator roteando tarefas por capacidade


---

## Slide 4: Entregas

## Artefatos

- MULTIAGENT-PROTOCOL.md (protocolo)
- multiagent.py (protótipo assíncrono)
- lessons.md (memória de melhoria)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Memória entre runs | Não | Sim |
| Autoaperfeiçoamento | Não | Sim (loop) |
---

## Slide 6: Próximos Passos

- Rodar em ambiente controlado com tarefas reais
- Persistir MemoryStore em banco
