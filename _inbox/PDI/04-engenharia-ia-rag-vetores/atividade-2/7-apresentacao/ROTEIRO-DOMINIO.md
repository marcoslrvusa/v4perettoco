# Roteiro de domínio: Atividade 2, RAG Híbrido e GraphRAG

## 1. Quando o vetorial falha e o BM25 resolve?
Resposta: em ID exato como CNPJ, o embedding generaliza e erra, o BM25 casa o termo exato, por isso a fusão com RRF cobre os dois mundos.

## 2. Quando entra o GraphRAG em vez do híbrido textual?
Resposta: em pergunta relacional do tipo cliente contrato fatura, que exige seguir arestas do grafo, onde vetorial e BM25 retornam trechos desconectados.

## 3. Como a avaliação em 30 perguntas prova a escolha?
Resposta: são 10 exatas, 10 sinônimos e 10 relação com hit@5, com metas maior ou igual a 0.95 no exato e maior ou igual a 0.9 na relação.

## 4. Por que overlap 128 no chunking semântico?
Resposta: preserva contexto entre sentenças para o retriever não quebrar a evidência no meio, mesmo indexando mais tokens.

## 5. Como manter precisão@5 maior ou igual a 95 por cento com latência menor que 150 ms?
Resposta: com job noturno de rebuild incremental do grafo e reavaliação do chunking quando a precisão cai, sem travar a consulta do dia.
