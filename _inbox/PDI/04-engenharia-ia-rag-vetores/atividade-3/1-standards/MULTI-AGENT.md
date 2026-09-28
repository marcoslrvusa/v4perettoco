# Multi-Agente: Padrão

```
Supervisor (roteia)
  |-> Triagem
  |-> Consulta (RAG)
  |-> Proposta
```
1. Handoff explícito: {from, to, intent, payload, trace_id}.
2. Contexto isolado: cada agente só recebe o payload.
3. Timeout por agente (15s) -> volta ao supervisor.
4. Max hops: impede loop.
5. Supervisor leve (modelo barato).
