# Roteiro de domínio: Atividade 1, Fundamentos de IA Generativa aplicados a RAG

## 1. Por que chunk 512 com overlap 64 e não um chunk maior?
Resposta: chunk grande traz ruído e chunk pequeno perde contexto, o ADR-041 escolheu 512 com 64 como ponto de coesão com custo aceitável de tokens.

## 2. Por que top-k 20 com rerank para top-5 em vez de similaridade pura?
Resposta: similaridade pura devolve os 20 mais próximos com ruído, o rerank filtra para os 5 mais relevantes antes de montar o prompt.

## 3. O que significa faithfulness maior ou igual a 0.8 em 10 perguntas?
Resposta: e o gate mínimo de fidelidade ao contexto recuperado, medido em 10 perguntas, com golden set de 50 pares para reproducibilidade no CI.

## 4. Para que servem threshold 0.82 e embedding de 1536 dim?
Resposta: normalizar o vetor de 1536 dim do text-embedding-3-small e comparar por cosseno com corte 0.82 padroniza o score entre textos de tamanhos distintos.

## 5. O que acontece se o guardrail falhar?
Resposta: fail-closed, a resposta e substituída por mensagem segura padrão, com 100 por cento de bloqueio antes da produção para PII, tóxico e fora de domínio.
