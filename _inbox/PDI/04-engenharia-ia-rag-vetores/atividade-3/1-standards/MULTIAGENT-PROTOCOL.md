# Protocolo Multi-Agente Assíncrono

- **Comunicação:** fila de mensagens (asyncio.Queue / Redis Streams).
- **Memória:** cada agente tem `MemoryStore` (curto + longo prazo).
- **Autoaperfeiçoamento:** loop de reflexão — após cada Run, um `CriticAgent`
  avalia a saída e escreve melhoria em `lessons.md`.
- **Supervisão:** `Orchestrator` roteia tarefas por capacidade.
