# Roteiro de Domínio: Atividade 2 (Idempotência e exactly-once)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

Complementadas por mais 6 perguntas adversariais, fechando em 11 perguntas, além da de negócio que já aparece na décima primeira. Cada resposta tem entre duas e cinco frases, prontas para ser ditas em voz alta sem ler.

## 1. Por que você não garante exactly-once no broker?
Porque em sistema distribuído só existe at-least-once; o exactly-once aparece para o negócio via dedup, o effectively-once. Garantir do outro lado exigiria commit distribuído entre broker, rede e banco, o que trava latência e não sobrevive a particionamento. A pergunta certa não é "quantas vezes a mensagem chega", e sim "quantas vezes o efeito acontece".

## 2. O que é o outbox e qual problema ele resolve?
Grava venda e evento na mesma transação; se a publicação falha, o relay republica do outbox a cada 1s em vez de perder o evento. Ele elimina a janela em que o banco commitou e a mensagem não saiu. Sem ele, o retry do consumidor não resolve nada, porque não há o que reentregar.

## 3. Onde a chave de idempotência e verificada?
No consumer, antes de cobrar, consultando a tabela de processados por `idempotency_key`. A verificação é um `INSERT ... ON CONFLICT DO NOTHING`, não um `SELECT`, porque só o banco arbitra concorrência de verdade. Se o `SELECT` retornar vazio para dois consumidores ao mesmo tempo, os dois cobram.

## 4. O que acontece se dois consumers pegarem o mesmo evento?
A verificação garante 1 aplicação; o ACK só após gravar a chave sustenta isso mesmo com 2 consumers. O banco decide quem vence pela chave primária, e o perdedor cai no ramo de descarte. A prova é a contagem de efeito por `event_id`, que tem de ficar em 1.

## 5. Como você prova que funciona?
Mesmo evento 3x gera 1 efeito, o teste injeta 5x e afirma 1 cobrança, com meta de zero duplicata e 100% dos handlers idempotentes. Fora do teste, a prova de produção é o replay: reprocessar 1 h de histórico move 1.728.000 eventos (Exemplo numérico: 12 partições a 40 msg/s por partição) e não altera um centavo de estado.

## 6. Por que não usar outbox e dedup e deixar o broker cuidar do resto?
Porque o broker só conhece a mensagem, não conhece o negócio. Duas cargas diferentes podem descrever a mesma cobrança, e nenhum broker do mundo deduplicaria isso por você. Também não resolve o caso de produtor que gera `event_id` novo a cada nova tentativa de envio.

## 7. Quanto custa manter isso rodando?
Duas contas: 1 round-trip de 2,4 ms por evento (acréscimo de 13,3% sobre handler de 18 ms, Exemplo numérico) e uma tabela de 2,2 GB com 48 h de retenção a 120 eventos/s (Exemplo numérico: 20.736.000 linhas de 104 B). Esforço de implementação: 23 h (meta). Nenhuma licença nova, nenhuma troca de broker.

## 8. Quem decide a política de retenção e quem decide o rollout?
A retenção é decisão de engenharia com validação de custo, porque sai do volume em GB; a ordem de rollout é decisão do time com o Financeiro, porque depende de qual handler move dinheiro primeiro. O que não fica em aberto é o limite técnico: `T_dedup` tem de ser maior que a janela máxima de reentrega do broker, isso não é negociável.

## 9. E se isso cair no meio da noite, o que se faz primeiro?
Pausa-se o grupo de consumidores afetado, nada se perde porque o broker mantém a posição. Depois roda-se o relatório de `event_id` com contagem acima de 1 e aciona-se o estorno pela lista. O rollback do código é seguro, porque as chaves já gravadas impedem que a versão antiga volte a duplicar.

## 10. Qual o SLO e o que acontece quando estoura?
SLI de duplicata observada com meta (meta) de 0 em janela de 30 dias, e orçamento de erro de 21,6 min por mês (0,05% de 43.200 min). Estando estourado, congela-se deploy de consumers, valida-se o TTL contra a janela de reentrega e só se libera depois de 24 h de relatório zerado.

## 11. Qual a alternativa mais barata e o que você deixaria para trás?
A mais barata já é esta: tabela de dedup, decorator e relay. A mais barata ainda seria dedup só em memória, que custa quase zero e cai no reinício do processo, que é justamente um dos gatilhos de reentrega, por isso foi rejeitada. Deixaria para trás o event sourcing e o CQRS: resolvem outro problema e exigem versionamento de schema e disciplina de compatibilidade que o time não precisa sustentar agora.

## 12. Impacto no negócio (em R$ ou horas)
Antes: cerca de 60 horas por mês de correção manual de débito duplicado, com risco financeiro de estorno por reentrega. Depois: meta (meta) de 0 duplicatas e correção próxima de 0 h por mês, com 23 h (meta) de esforço único de implementação. O ganho secundário é poder aumentar a taxa de retry sem conversa com o Financeiro a cada mudança, porque retry passa a custar I/O, não débito.
