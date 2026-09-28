# Roteiro de Demo: RAG Híbrido (BM25 + Vetorial) e GraphRAG para Relações

Abra o deck (index.html) e percorra os slides na ordem.

1. Slide de Resumo: abra com o problema de negócio e o blast radius.
2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).
3. Slide de Validação/Rollout: mostre como provamos em produção.
4. Slide de Riscos: apresente o plano de mitigação.

A partir do passo 5, cada item tem comando ou clique exato, saída esperada,
critério de falha e o que fazer se der errado. Pré-requisito único de todos os
passos: terminal aberto na raiz da atividade e o deck já carregado no navegador.

5. Abra o README da atividade na seção Modelo mental.
   Comando: `open README.md` no explorador ou `code README.md`.
   Saída esperada: quatro estágios do funil visíveis (normalização, candidatos,
   fusão, montagem).
   Falha: se a seção não abrir, use o índice do editor e procure por "Modelo
   mental". Não apresente de memória sem o texto na tela.

6. Mostre o diagrama Mermaid da Arquitetura.
   Clique: seção `## Arquitetura` do README.
   Saída esperada: três caminhos (lexical, vetorial, grafo) convergindo em uma
   única fusão RRF.
   Falha: se o Mermaid não renderizar, abra o mesmo diagrama no standard
   `1-standards/RAG-ARCHITECTURE.md` e siga. Nunca desenhe o diagrama na lousa
   como substituto.

7. Rode a consulta híbrida ponderada como baseline.
   Comando: executar o bloco SQL `SELECT id, content, (0.7 * (1 - (embedding <=>
   :q))) + (0.3 * ts_rank(...))` contra a base de homologação.
   Saída esperada: 10 linhas com coluna `score` decrescente.
   Falha: erro de coluna `tsv` significa que a migração
   `3-supabase/001_rag_schema.sql` não rodou. Pare a demo e rode a migração.

8. Rode a fusão por rank com CTE.
   Comando: executar o CTE `lex` + `vec` com `SUM(1.0 / (60 + r))`.
   Saída esperada: 10 linhas ordenadas por `score`, com documentos presentes nas
   duas listas subindo de posição.
   Falha: se a ordem for idêntica ao passo anterior, o `k` ou o tamanho de lista
   está errado. Confira `LIMIT 50` em cada CTE.

9. Demonstre a falha do vetorial sozinho com um CNPJ.
   Comando: consultar a base com o CNPJ de um cliente cadastrado, apenas pelo
   caminho vetorial.
   Saída esperada: o documento exato não aparece nos 5 primeiros.
   Falha: se aparecer, mostre o score e explique que coincidência em base pequena
   não prova cobertura; rode com 10 CNPJs diferentes para mostrar o padrão.

10. Demonstre a resolução pelo caminho lexical.
    Comando: mesma consulta, caminho `tsv @@ websearch_to_tsquery`.
    Saída esperada: o documento exato em 1º lugar.
    Falha: se a pontuação do CNPJ some, a normalização está errada. Corrija e
    reindexe o lote antes de continuar.

11. Demonstre a falha do lexical com sinônimo.
    Comando: consultar com termo interno que não existe literalmente na base.
    Saída esperada: lista vazia ou resultados sem relação.
    Falha: se retornar tudo, o `websearch_to_tsquery` está caindo em modo
    tolerante. Reduza a consulta a um termo só.

12. Demonstre a resolução pelo caminho vetorial.
    Comando: mesma consulta do passo 11, caminho embedding.
    Saída esperada: o documento certo nos primeiros.
    Falha: se não retornar, confirme a normalização dos embeddings na escrita
    (`normalize_embeddings=True`).

13. Apresente a conta fechada do RRF no slide 14.
    Clique: slide "Matemática 2, conta fechada no RRF".
    Saída esperada: score(A) = 0,0320, score(B) = 0,0323, diferença de 0,0003.
    Falha: se alguém contestar, refaça a conta no quadro com 1/61, 1/64, 1/62 e
    1/62. Não siga sem fechar a aritmética.

14. Apresente o orçamento de latência no slide 15.
    Clique: slide "Matemática 3, orçamento de latência".
    Saída esperada: 111 ms somando as seis etapas e 39 ms de folga.
    Falha: se a soma não fechar, use a tabela de p95 por etapa do standard. Nunca
    apresente número de latência sem a etapa associada.

15. Rode a pergunta relacional no caminho textual puro.
    Comando: consultar "quais faturas o contrato K-01 gerou" só com híbrido
    textual.
    Saída esperada: trechos sobre cliente, contrato e fatura, desconectados.
    Falha: se vier resposta coerente, o dado está em um único trecho. Escolha
    outra relação da base.

16. Rode a mesma pergunta com travessia no grafo.
    Comando: executar a CTE recursiva `WITH RECURSIVE caminho AS (...)` com
    `WHERE c.profundidade < 4`.
    Saída esperada: a cadeia cliente, contrato, fatura com profundidade 0, 1 e 2.
    Falha: caminho vazio significa aresta ausente. Mostre o fallback textual com
    aviso ao usuário, ele é parte do roteiro.

17. Mostre o esquema Cypher equivalente.
    Comando: abrir `3-supabase/graph_schema.cypher`.
    Saída esperada: `MATCH (c:Cliente {id:$x})-[:TEM]->(ct)-[:GERA]->(f) RETURN f`.
    Falha: se o arquivo não abrir, cite o trecho do standard. Não invente
    sintaxe alternativa durante a apresentação.

18. Rode o lote de ingestão duas vezes.
    Comando: executar o mesmo lote de ingestão em seguida.
    Saída esperada: contagem de linhas idêntica antes e depois.
    Falha: crescimento de linhas indica upsert sem chave. Cancele a demo, corrija
    a chave `(doc_id, hash_conteudo)` e reexecute.

19. Mostre a avaliação em três configurações.
    Comando: rodar as 30 perguntas em modo só vetorial, só lexical e híbrido.
    Saída esperada: relatório de hit@5 por categoria, com o híbrido nunca pior
    que o vetorial.
    Falha: se o relatório vier agregado, não apresente. A média esconde a classe
    quebrada, e essa é a pergunta que o coordenador faz.

20. Apresente os critérios de aceite binários.
    Clique: seção Avaliação e critérios de aceite no README.
    Saída esperada: cinco critérios com alvo e condição de bloqueio.
    Falha: se algum critério estiver sem alvo numérico, declare que é meta e
    registre a pendência antes de seguir.

21. Apresente a tabela de modos de falha.
    Clique: slide 21 e seção Modos de falha do README.
    Saída esperada: dez linhas com sintome, causa, detecção, mitigação e
    recuperação.
    Falha: se pedirem um caso fora da tabela, responda com a rotina de detecção
    correspondente, sem inventar causa nova.

22. Apresente o diagrama de falha e recuperação.
    Clique: slide 22, diagrama Mermaid do fluxo às 3 da manhã.
    Saída esperada: métrica estoura, três ramos de mitigação e postmortem com
    data.
    Falha: se o Mermaid não renderizar, use o texto da seção Operação do README.

23. Feche com métricas e próximos passos.
    Clique: slide 29 (métricas) e slide 30 (fecho).
    Saída esperada: precisão@5 de cerca de 42 por cento para cerca de 98 por
    cento, e a sequência RAGAS, cache de subgrafos, reranking.
    Falha: se o tempo acabar, pule do passo 18 direto para este. Métricas e fecho
    são o mínimo inegociável da demo.

Rollback de demonstração: se qualquer etapa ficar inconsistente, volte ao deck e
apresente o dossiê completo em PDF, sem improvisar resultado.

Material de apoio: pdi-engenharia-ia-rag-vetores-a2-report.pdf (dossiê completo).
