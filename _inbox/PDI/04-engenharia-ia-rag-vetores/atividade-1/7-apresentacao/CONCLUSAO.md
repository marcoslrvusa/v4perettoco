# Conclusão: NVIDIA DLI
- [x] Building RAG Agents with LLMs
- [x] RAG end-to-end em corpus próprio
- [x] Transposição: chunking 512/64 + rerank

## O que ficou pronto

- Notas do curso (`DLI-NOTES.md`) com a justificativa de cada parâmetro: normalização antes do cosseno, chunk de 512 tokens com overlap 64, busca de 20 candidatos com rerank para 5 e avaliação por faithfulness e answer relevance.
- Standard de pipeline (`DATA-PIPELINE-AI.md`) com estágios, fórmula de volume do índice, tabela de decisão, telemetria, plano de teste e checklist de adesão.
- Código de baseline (`rag_baseline.py`) com `embed`, `chunk`, `retrieve` e `answer`, executável do zero no corpus de teste.
- ADR-041 registrando a opção escolhida e as alternativas descartadas com o motivo de cada recusa.

## Critérios de aceite atendidos

1. Pipeline reproduzível: mesmo corpus gera os mesmos chunks e o mesmo ranking.
2. Vetores normalizados, com score de cosseno comparável entre textos de tamanhos distintos.
3. Citação obrigatória de `chunk_id` em toda resposta, tornando a alucinação rastreável.
4. Gate de CI com faithfulness maior ou igual a 0,8 sobre golden set de 50 pares (meta).
5. Guardrail fail-closed testado em caso tóxico, caso PII e caso fora de domínio.

## Pendência conhecida

- Homologação antes da publicação: o baseline está desenvolvido e aguarda revisão.
- Atividade 04-A2 herda golden set, runbook e parâmetros, sem retrabalho.
