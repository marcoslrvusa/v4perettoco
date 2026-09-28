# Roteiro de domínio: Atividade 1, Fundamentos de IA Generativa aplicados a RAG

## 1. Por que chunk 512 com overlap 64 e não um chunk maior?
Resposta: chunk grande traz ruído e chunk pequeno perde contexto, o ADR-041 escolheu 512 com 64 como ponto de coesão com custo aceitável de tokens. O passo entre chunks é 448 tokens e o overlap cobre 12,5 por cento dos tokens de cada bloco, o suficiente para a frase cortada na fronteira existir inteira em pelo menos um chunk. Exemplo numérico: 1.000.000 de tokens geram 2.232 chunks com overlap, contra 1.953 sem overlap, diferença de 14 por cento paga uma única vez na indexação.

## 2. Por que top-k 20 com rerank para top-5 em vez de similaridade pura?
Resposta: similaridade pura devolve os 20 mais próximos com ruído, o rerank filtra para os 5 mais relevantes antes de montar o prompt. A busca vetorial explora e é barata; o rerank extrai e é caro. Pagar 20 passes de rerank para descartar 15 é latência sem ganho, por isso o corte em 5. O ganho é medido pela posição média do primeiro trecho relevante nas mesmas 10 perguntas, com e sem rerank.

## 3. O que significa faithfulness maior ou igual a 0.8 em 10 perguntas?
Resposta: e o gate mínimo de fidelidade ao contexto recuperado, medido em 10 perguntas, com golden set de 50 pares para reproducibilidade no CI. Se o build cai abaixo desse número, a publicação é bloqueada: é fail-closed, não relatório. As 10 perguntas cobrem o caminho quente do dia a dia; os 50 pares rodam em lote para detectar regressão ampla.

## 4. Para que servem threshold 0.82 e embedding de 1536 dim?
Resposta: normalizar o vetor de 1536 dim do text-embedding-3-small e comparar por cosseno com corte 0.82 padroniza o score entre textos de tamanhos distintos. Sem normalização, a norma do vetor entra na fórmula e texto longo ganha vantagem arbitrária. Com normalização, o denominador vira 1 e a similaridade vira produto escalar, o que torna o corte interpretável e comparável entre consultas.

## 5. O que acontece se o guardrail falhar?
Resposta: fail-closed, a resposta e substituída por mensagem segura padrão, com 100 por cento de bloqueio antes da produção para PII, tóxico e fora de domínio. A escolha é deliberada: falso positivo seguro é preferível a resposta tóxica em produção. Se a taxa de bloqueio passar de 3 por cento (meta), a ação é revisar o limiar com amostra, não desligar o guardrail.

## 6. Por que não mandar o documento inteiro no prompt e acabar com o índice?
Resposta: porque não escala e não dá para citar o trecho. Cada consulta repagaria o documento inteiro, o corpus real estoura a janela de contexto e a resposta perderia a referência exata de onde veio a informação. O índice transforma um custo proporcional ao corpus em um custo proporcional a 5 chunks de 512 tokens.

## 7. E se o recall estiver baixo, o problema é do modelo ou do pipeline?
Resposta: recall@5 baixo é problema do pipeline: chunking, embedding ou indexação. Recall alto com faithfulness baixa é problema do gerador: prompt ou modelo. É por isso que medimos as duas coisas separadas. A ordem de investigação é sempre busca primeiro, geração depois, porque otimizar prompt com contexto errado só máscara o defeito.

## 8. Qual é o custo de trocar o modelo de embedding amanhã?
Resposta: reindexação completa do corpus, porque os vetores ficam em espaço diferente. O custo é o de embedding de todos os tokens, calculado com a tabela de preços vigente, mais a janela em que as duas versões coexistem no banco. O controle que reduz o risco é manter o índice antigo até validar recall@5 do novo, e filtrar busca por versão de modelo, nunca misturar.

## 9. E se a fila de ingestão cair no meio da noite, o que acontece com a busca?
Resposta: a consulta continua funcionando, porque ingestão e serve são caminhos separados por fila. O sintoma é documento novo não aparecer na busca, detectado pela contagem de chunks por `doc_id` que deixa de crescer. A recuperação é drenar o backlog, com idempotência por `(doc_id, hash, modelo)` garantindo que nada duplica quando a fila volta.

## 10. Quem decide mudar um parâmetro como `k` ou o threshold, e como isso é registrado?
Resposta: mudança de parâmetro entra como revisão da ADR-041, com motivo, impacto em latência e em faithfulness, e o resultado da medição antes e depois. Quem propõe é quem opera o pipeline; quem aprova é a coordenação técnica da trilha. Parâmetro mudado fora de registro vira dívida impossível de auditar.

## 11. Como você prova que isto funciona, além de dizer que funciona?
Resposta: golden set de 50 pares versionado, gate de CI com faithfulness maior ou igual a 0,8, comparação controlada com e sem rerank nas mesmas 10 perguntas, e reprodutibilidade: quem clona o repositório obtém o mesmo ranking dos mesmos chunks. Nenhum desses quatro itens depende de impressão de quem desenvolveu.

## 12. Quanto isto economiza ou gasta por mês (impacto de negócio)?
Resposta: o custo por consulta é contado antes da chamada, com quatro parâmetros declarados: tokens do corpus, preço por mil tokens de embedding, preço de entrada e saída do gerador, e consultas por dia. Exemplo numérico: com 5 chunks de 512 tokens o contexto é de 2.560 tokens por consulta; cair para 3 chunks após validar recall@5 corta 40 por cento da parcela de contexto do custo de entrada. O ganho de negócio está na homologação encurtada: a decisão sobre mudar prompt ou modelo vira comparação de número em vez de discussão de impressão.
