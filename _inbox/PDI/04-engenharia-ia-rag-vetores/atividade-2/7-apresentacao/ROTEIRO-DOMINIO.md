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

## 6. Por que não ficar só no vetorial e treinar o embedding no domínio?
Resposta: treinar embedding melhora sinônimo e paráfrase, mas não resolve igualdade de cadeia. Um CNPJ é uma cadeia de dígitos em que cada posição importa; embedding de texto não preserva isso, e a distância entre dois CNPJs vizinhos pode ser menor que a distância entre um CNPJ e um documento que nem o cita. A resposta técnica é: treinamento de embedding ataca geometria, e o problema do identificador é de igualdade literal. Só o caminho lexical cobre, e ele custa um índice GIN, não um ciclo de treino. Ressalva honesta: se o vocabulário de sinônimos crescer, um embedding ajustado ao domínio entra na lista de evolução, mas continua não substituindo o lexical.

## 7. Quanto custa manter isso rodando?
Resposta: o custo tem duas partes, horas de operação e execução. Horas: a estimativa da atividade é 48 h (meta) de construção, das quais 10 h (meta) são de grafo e extração, a parte mais frágil. Execução: Exemplo numérico com parâmetros declarados, 10.000 consultas por dia a 0,002 R$ por consulta fecham 20 R$ por dia e 600 R$ por mês. O job noturno é o item de maior variabilidade, porque roda extração por LLM sobre o delta do dia: se o volume de documentos novos dobrar, esse custo dobra junto, enquanto o custo de busca praticamente não muda. O que derruba o orçamento não é média, é pico de reindexação.

## 8. Quem decide quando trocar chunking, constante do RRF ou modelo de embedding?
Resposta: quem decide é o responsável pela trilha de IA/RAG, mas a decisão só é válida depois que o conjunto-ouro de 30 perguntas roda antes e depois. A regra é binária: trocou algo que afeta recuperação, reavalia e publica o relatório por categoria na mesma mudança. O que ninguém pode fazer sozinho é mudar dois parâmetros em janelas próximas, porque aí a regressão fica sem causa atribuível. Mudança de prompt de geração é decisão separada, com aprovação de quem responde pela resposta entregue ao usuário.

## 9. E se cair no meio da noite, qual é o SLO e o que se faz?
Resposta: o SLI de latência tem meta de p95 abaixo de 150 ms medido em janela rolante de 24 horas, e a disponibilidade do endpoint é 99,5 por cento (meta), o que dá 3,6 horas de orçamento de erro por mês de 30 dias. O procedimento da madrugada é curto e não envolve reindexar: latência alta, desligar o reranking por feature flag; grafo parado, reexecutar o job idempotente do dia; qualidade caindo, voltar ao snapshot anterior do índice; resposta sem fonte, desligar geração sem citação obrigatória. Rollback é trocar duas referências e invalidar o cache, com meta de 10 minutos (meta). Depois nasce o postmortem, com data marcada e sem busca por culpado.

## 10. Como você prova que funciona para quem não é técnico?
Resposta: com três evidências que não dependem de jargão. Primeiro, a matriz antes e depois: precisão@5 sai de cerca de 42 por cento para cerca de 98 por cento. Segundo, a mesma pergunta em três modos, mostrando a falha real do vetorial com CNPJ e a falha real do textual com sinônimo, para que a pessoa veja o problema acontecendo e não só a solução. Terceiro, a contagem de trechos relevantes nos cinco primeiros, que é contagem, não opinião. O que não serve como prova: demonstração com uma única pergunta escolhida na hora, porque amostra escolhida não é evidência.

## 11. O que você deixaria para trás e qual a alternativa mais barata?
Resposta: deixaria para trás o reranking cross-encoder, que custa cerca de 50 ms e é o primeiro item a sair quando a folga de latência some; o resumo pré-computado por comunidade do grafo, que exige job caro e difícil de auditar; e a reindexação completa a cada alteração, substituída por chave de hash por trecho. A alternativa mais barata que ainda resolve parte do problema é lexical mais vetorial sem grafo: cobre exato e sinônimo com dois índices e nenhum job noturno. O que se perde é exatamente a classe de pergunta relacional, que é a que motivou a atividade. Exemplo numérico do tradeoff: sem grafo, some o job noturno e a extração por LLM, a operação fica com dois caminhos de escrita em vez de três, e o hit@5 de relação volta a ficar abaixo de 0,9.

## 12. Qual é o impacto em R$ ou horas para o negócio?
Resposta: o ganho é tempo de conferência e a possibilidade de vender busca relacional. Antes, com precisão@5 em cerca de 42 por cento, dois dos cinco trechos por consulta eram ruído e o atendimento completava a resposta à mão. Exemplo numérico com parâmetros declarados: 200 consultas por dia, 1 minuto de conferência extra por consulta em cerca de 42 por cento delas, 84 minutos por dia, cerca de 2.520 minutos ou 42 horas por mês de 30 dias
(Exemplo numérico: 84 x 30 = 2.520 minutos, dividido por 60 = 42 horas). Some-se a isso a receita destravada por não precisar de indexação manual das relações cliente, contrato e fatura. Contra isso ficam 48 h (meta) de construção e 600 R$ por mês de execução (Exemplo numérico, parâmetros declarados na pergunta 7). A conta fecha no primeiro mês de operação plena, e o ponto que precisa de cuidado é a premissa de volume de consultas, que precisa ser confirmada com dados reais antes de virar compromisso.
