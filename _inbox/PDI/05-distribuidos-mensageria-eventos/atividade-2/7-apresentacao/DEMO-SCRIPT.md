# Roteiro de Demo: Idempotência e Entrega Exactly-Once (na prática: at-least-once + dedup)

Abra o deck (index.html) e percorra os slides na ordem.

Roteiro com 18 passos, divididos em três blocos: navegação do deck (1 a 4), demonstração técnica no terminal (5 a 14) e fechamento perante a coordenação (15 a 18). Cada passo traz o comando ou clique exato, a saída esperada, o critério de falha e o que fazer se der errado.

Pré-requisitos antes de iniciar: terminal aberto na raiz da atividade, banco de dados acessível com a tabela `processed_events` criada pelos arquivos de `3-supabase/`, e Python 3 disponível no `PATH`.

**Passo 1.** Clique em "Resumo Executivo" (primeiro slide do `index.html`).
Saída esperada: título da atividade, área Sistemas Distribuídos, e a frase sobre dedup por chave de evento.
Critério de falha: slide não renderiza ou o HTML mostra erro de assets.
Se falhar: recarregue a página com `Ctrl+Shift+R` para limpar cache; se persistir, abra `pdi-distribuidos-mensageria-eventos-a2-report.html` como alternativa.

**Passo 2.** Navegue até o slide "Decisão Arquitetural (ADR)" com as setas do teclado.
Saída esperada: tabela da ADR-052 com a opção ESCOLHIDA e a nota sobre exactly-once observacional.
Critério de falha: tabela com colunas desalinhadas ou nota ausente.
Se falhar: cite a ADR-052 de memória a partir do README da atividade, que tem a mesma tabela.

**Passo 3.** Avance para o slide "Matemática da solução".
Saída esperada: a conta $120 \times 172.800 = 20.736.000$ linhas e a Lei de Little com $L = 20$.
Critério de falha: qualquer número diferente do do README.
Se falhar: abra o README na seção Matemática da solução e leia a conta a partir dali.

**Passo 4.** Pare no slide "Modos de falha" antes de ir ao terminal.
Saída esperada: tabela com quatro sintomas, causas e recuperações.
Critério de falha: faltar a coluna de recuperação.
Se falhar: retome pelo slide de arquitetura e relate os modos de falha oralmente.

**Passo 5.** No terminal, liste os arquivos da atividade:
`find _inbox/PDI/05-distribuidos-mensageria-eventos/atividade-2 -name '*.md' | sort`
Saída esperada: seis arquivos `.md`, incluindo `1-standards/IDEMPOTENCY.md`, `DECK-PDI.md`, `DEMO-SCRIPT.md` e `ROTEIRO-DOMINIO.md`.
Critério de falha: saída vazia ou caminho inexistente.
Se falhar: você está fora da raiz do repositório; volte para a raiz com `cd "$(git rev-parse --show-toplevel)"`.

**Passo 6.** Conte as palavras do material:
`find _inbox/PDI/05-distribuidos-mensageria-eventos/atividade-2 -name '*.md' -exec wc -w {} + | tail -1`
Saída esperada: total igual ou superior a 6.800 palavras.
Critério de falha: total abaixo da meta.
Se falhar: identifique o arquivo mais curto com `wc -w` individual e expanda primeiro o README e o standard.

**Passo 7.** Garanta que não existe travessão nem entity proibida:
`grep -rn $'\u2014' _inbox/PDI/05-distribuidos-mensageria-eventos/atividade-2 && echo TRAVESSAO || echo ok`
Saída esperada: `ok`.
Critério de falha: qualquer ocorrência listada.
Se falhar: substitua cada ocorrência por dois-pontos, vírgula, ponto ou barra vertical e rode o comando de novo.

**Passo 8.** Verifique a tabela de dedup no banco:
`SELECT id, ts FROM processed_events ORDER BY ts DESC LIMIT 5;`
Saída esperada: até cinco linhas com UUID e timestamp, ou resultado vazio na primeira execução.
Critério de falha: erro de relação inexistente, o que significa que o schema não foi aplicado.
Se falhar: aplique `3-supabase/schema_dedup.sql` e repita o comando.

**Passo 9.** Insira o mesmo evento três vezes para provar a unicidade:
`INSERT INTO processed_events(id) VALUES ('demo-evt-001');`
repita a mesma instrução duas vezes.
Saída esperada: `INSERT 0 1` na primeira vez e erro de violação de chave primária nas duas seguintes.
Critério de falha: três `INSERT 0 1`, o que significa que a unicidade não está valendo.
Se falhar: confirme se a `PRIMARY KEY` existe com `\d processed_events` e recrie a tabela.

**Passo 10.** Rode o consumer de referência sobre o evento repetido:
`python3 2-code/consumer.py`
Saída esperada: primeira execução grava o lead; as seguintes retornam sem aplicar efeito.
Critério de falha: dois ou mais leads criados com o mesmo identificador.
Se falhar: abra `2-code/consumer.py` e confirme que a captura de `IntegrityError` vem antes do `INSERT` de domínio.

**Passo 11.** Demonstre o decorator em memória:
`python3 -c "from importlib import import_module; m=import_module('2-code.idempotent'); print('decorator carregado')"`
Saída esperada: `decorator carregado`.
Critério de falha: erro de sintaxe ou de import.
Se falhar: mostre o código no editor e explique que a versão em memória é só didática, a garantia real é a do banco.

**Passo 12.** Execute o upsert por chave de negócio:
`INSERT INTO leads(id,email) VALUES ('demo-001','a@b.c') ON CONFLICT (id) DO NOTHING;`
repita uma vez alterando apenas o e-mail.
Saída esperada: duas instruções sem erro e uma única linha final para o id `demo-001`.
Critério de falha: erro de violação, ou duas linhas para o mesmo id.
Se falhar: confirme se existe `UNIQUE` ou `PRIMARY KEY` na coluna `id` de `leads`.

**Passo 13.** Simule a reentrega usando a mesma chave nos três eventos:
`SELECT count(*) FROM processed_events WHERE id LIKE 'demo-evt-%';`
Saída esperada: contagem 1, mesmo tendo havido três tentativas de inserção.
Critério de falha: contagem maior que 1.
Se falhar: pare a apresentação e trate como incidente, porque exatamente esse cenário é o que a atividade promete eliminar.

**Passo 14.** Confira a ausência de placeholder no material:
`grep -rnE '\{\{' _inbox/PDI/05-distribuidos-mensageria-eventos/atividade-2 && echo PLACEHOLDER || echo ok`
Saída esperada: `ok`.
Critério de falha: qualquer ocorrência de marca de placeholder (chaves dobradas).
Se falhar: localize a linha, escreva o conteúdo real e rode a verificação de novo.

**Passo 15.** Volte ao deck e abra o slide "Queda no meio do caminho (recuperação)".
Saída esperada: exemplo numérico com queda aos 6 ms, reentrega após 10 s e zero efeitos adicionais.
Critério de falha: não conseguir explicar por que não há cobrança dupla.
Se falhar: retome pelo diagrama de sequência do slide 11, mostrando a chave entrando antes do efeito.

**Passo 16.** Apresente a matriz de tradeoff é peça uma objeção à coordenação.
Saída esperada: cinco linhas, cada uma com ganho, pagamento e quem sente.
Critério de falha: não saber o custo de infraestrutura da linha de retenção longa.
Se falhar: cite o Exemplo numérico de 2,2 GB com 48 h de retenção.

**Passo 17.** Feche com os critérios de aceite CA-1 a CA-6.
Saída esperada: seis frases curtas, todas verificáveis no CI.
Critério de falha: algum CÁ sem critério objetivo de verificação.
Se falhar: reescreva o CÁ com número e ação, por exemplo "injetar 5x e contar 1 efeito".

**Passo 18.** Encerre com métricas e próximos passos.
Saída esperada: duplicatas 0, handlers idempotentes 100%, orçamento de erro de 21,6 min/mês (meta), e três próximos passos.
Critério de falha: terminar sem ação seguinte com dono e prazo.
Se falhar: registre a ação "aplicar em todos os consumers" com responsável nomeado antes de encerrar.

Rollback geral da demo: nenhuma etapa acima altera dado de produção. Para limpar o ambiente de demonstração, execute `DELETE FROM processed_events WHERE id LIKE 'demo-%';` e `DELETE FROM leads WHERE id LIKE 'demo-%';`.

Material de apoio: pdi-distribuidos-mensageria-eventos-a2-report.pdf (dossiê completo).
