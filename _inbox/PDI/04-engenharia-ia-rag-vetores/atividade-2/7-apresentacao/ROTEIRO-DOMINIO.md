# Roteiro de dominio: Atividade 2, RAG Hibrido e GraphRAG

## 1. Quando o vetorial falha e o BM25 resolve?
Resposta: em ID exato como CNPJ, o embedding generaliza e erra, o BM25 casa o termo exato, por isso a fusao com RRF cobre os dois mundos.

## 2. Quando entra o GraphRAG em vez do hibrido textual?
Resposta: em pergunta relacional do tipo cliente contrato fatura, que exige seguir arestas do grafo, onde vetorial e BM25 retornam trechos desconectados.

## 3. Como a avaliacao em 30 perguntas prova a escolha?
Resposta: sao 10 exatas, 10 sinonimos e 10 relacao com hit@5, com metas maior ou igual a 0.95 no exato e maior ou igual a 0.9 na relacao.

## 4. Por que overlap 128 no chunking semantico?
Resposta: preserva contexto entre sentencas para o retriever nao quebrar a evidencia no meio, mesmo indexando mais tokens.

## 5. Como manter precisao@5 maior ou igual a 95 por cento com latencia menor que 150 ms?
Resposta: com job noturno de rebuild incremental do grafo e reavaliacao do chunking quando a precisao cai, sem travar a consulta do dia.
