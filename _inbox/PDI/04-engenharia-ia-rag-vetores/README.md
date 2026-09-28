# PDI: Engenharia de IA, RAG e Vetores

> **Área:** Automação & Infraestrutura | Engenharia de IA
> **Autor:** Marcos Perettoco
> **Perfil:** Tech Lead Sênior L2 / GPTS
> **Período:** 2026
> **Status:** Em desenvolvimento

Módulo com 4 atividades. Cada atividade na própria pasta `atividade-{N}/`.

| Atividade | Foco | Pasta |
|-----------|------|-------|
| 1 | Fundamentos de IA generativa (NVIDIA DLI) aplicados a RAG: chunking com sobreposição, embeddings de dimensão fixa, reranking e avaliação com conjunto-ouro | `atividade-1/` |
| 2 | RAG híbrido (BM25 + vetorial com fusão RRF) e GraphRAG para relações do tipo cliente, contrato e fatura | `atividade-2/` |
| 3 | Orquestração multi-agente com handoff tipado, isolamento de contexto, timeout por agente e fallback | `atividade-3/` |
| 4 | Engenharia de custos de LLM: custo por tarefa, cache de prompt, roteamento por complexidade e budget por cliente | `atividade-4/` |

## O que sustenta o módulo

As quatro atividades formam uma cadeia, não quatro projetos soltos. A atividade 1
funda o pipeline de recuperação e o hábito de medir; a atividade 2 resolve os casos
que a similaridade pura não cobre (termo exato e relação); a atividade 3 troca o agente
monolítico por papéis com fronteira clara; a atividade 4 fecha o ciclo com contabilidade
de tokens, sem a qual nenhum dos três anteriores é precificável.

| De | Para | O que passa de uma para a outra |
|----|------|--------------------------------|
| 1 para 2 | baseline medido | hit@5 e golden set viram a régua do híbrido |
| 2 para 3 | contexto recuperado | o agente de consulta recebe só o payload do handoff |
| 3 para 4 | fluxo em papéis | cada papel vira uma linha do ledger de custo |
| 4 para 1 | orçamento | o budget limita k, modelo e orçamento de tokens do baseline |

## Padrões do módulo

- Todo artefato numérico novo é rotulado como exemplo numérico, com parâmetros declarados.
- Toda projeção leva `(meta)`; número medido existente é reaproveitado sem alteração.
- Referências citadas por título e plataforma, sem link não verificado.
- Três ADRs guiam as decisões: ADR-041 (baseline RAG), ADR-042 (recuperação híbrida
  mais grafo) e ADR-043 (topologia multi-agente). A atividade 4 fecha com ADR-044
  (estratégia de custo).

## Mapa de artefatos

```
04-engenharia-ia-rag-vetores/
├── README.md                        ← este card
├── atividade-1/                     ← fundações, chunking e avaliação
│   ├── 1-standards/  DATA-PIPELINE-AI.md, DLI-NOTES.md
│   ├── 2-code/       rag_baseline.py
│   └── 7-apresentacao/  DECK-PDI.md, DEMO-SCRIPT.md, ROTEIRO-DOMINIO.md
├── atividade-2/                     ← híbrido BM25 + vetorial + GraphRAG
│   ├── 1-standards/  RAG-ARCHITECTURE.md, HYBRID-RAG.md
│   ├── 2-code/       hybrid_rag.py, rag_hybrid.py
│   ├── 3-supabase/   001_rag_schema.sql, graph_schema.cypher
│   └── 7-apresentacao/
├── atividade-3/                     ← orquestração multi-agente
│   ├── 1-standards/  MULTI-AGENT.md, MULTIAGENT-PROTOCOL.md
│   ├── 2-code/       orchestrator.py, multiagent.py, handoff_schema.py
│   └── 7-apresentacao/
└── atividade-4/                     ← custo, cache e roteamento
    ├── 1-standards/  LLM-COST.md, COST-MONITORING.md, BUDGET.md
    ├── 2-code/       cost_calc.py, track_cost.py
    ├── 3-supabase/   usage_schema.sql
    └── 7-apresentacao/
```

## Como revisar esta trilha

1. Comece pelo `README.md` de cada atividade: ele traz problema, modelo mental,
   matemática, invariantes, modos de falha, SLO e runbook.
2. Depois vá ao padrão principal em `1-standards/`, onde ficam regra canônica,
   tabela de decisão, anti-padrões, telemetria e plano de teste.
3. Feche com `7-apresentacao/`: DECK-PDI.md para defender, DEMO-SCRIPT.md para
   executar e ROTEIRO-DOMINIO.md para responder a perguntas adversariais.
