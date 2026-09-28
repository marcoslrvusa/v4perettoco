# ROTEIRO-DOMINIO: APIs Modulares de Missão Crítica (FastAPI)

5 perguntas de coordenador + respostas curtas para defesa da atividade 2.

As respostas são curtas de propósito: em defesa oral, quem domina o assunto responde em uma frase e só detalha se perguntarem. As cinco primeiras são as perguntas clássicas; as sete seguintes são as adversariais que costumam aparecer quando a banca quer testar se a decisão foi pensada ou copiada.

## 1. Por que cursor-based e não offset com índice?

Offset com índice ainda varre e descarta N linhas antes de devolver a página; em listas de 5k a 80k o custo cresce com a profundidade. Cursor (`after` = id) posiciona direto no ponto de partida, custo estável por página.

A prova numérica é simples: a página 1.000 com `limit = 50` precisa de `1000 × 50 + 50 = 50.050` linhas lidas no modelo de offset, contra `51` linhas no modelo de cursor, um fator de 981 vezes (Exemplo numérico). O índice elimina o custo de ordenar em memória, não elimina a leitura das linhas que serão descartadas.

## 2. O que acontece se o Redis cair no pico?

O endpoint faz fallback para o banco e continua respondendo. A latência degrada para o caminho sem cache até o Redis voltar, mas não há indisponibilidade por causa do cache.

O ponto que fecha a resposta: a taxa de acerto cai para zero, então toda a carga de listagem volta ao Postgres. É exatamente por isso que o rate limit por chave e o pool dimensionado existem: eles são a rede de segurança do cenário sem cache. Disponibilidade vale mais que p95 nesse caso, e essa troca está registrada como decisão, não como acidente.

## 3. Como o cliente sabe quando repetir uma chamada que falhou?

Pelo envelope: 4xx significa erro do cliente e não deve ser retentado; 5xx significa erro nosso e pede retry com backoff. O `trace_id` amarra cliente e log para depuração.

Exceção que convém citar se perguntarem: o `429` é um 4xx que retenta, e a regra de quanto esperar está no próprio cabeçalho `Retry-After`. O consumidor não precisa adivinhar, ele obedece ao tempo de recarga do balde.

## 4. Por que rate limit por chave e não global?

Limite global pune todos por causa de um cliente (ou bot) agressivo. Por chave, quem estoura a quota de 100 req/min recebe 429 isolado e os demais sistemas (3 a 5 consumidores) seguem normais.

Complemento útil: por IP também foi descartado, porque atrás de NAT e proxy todos os clientes internos compartilham origem e um puniria os outros. A identidade estável é a credencial, não o endereço de rede.

## 5. Como foi validado antes de produção?

Carga com k6 a 200 req/s por 5 min, teste de estouro de quota esperando 429 com `Retry-After`, e confirmação de que o segundo hit da mesma lista vem do Redis. Metas: p95 abaixo de 200ms no hit e disponibilidade de 99,5%.

O teste que costuma faltar em revisão e que foi incluído: a varredura completa, que paginar do início ao fim contando itens para provar zero duplicidade e zero omissão. Sem ele, uma ordenação sem desempatador passaria despercebida até o consumidor reclamar de item pulado.

## 6. Por que não simplesmente aumentar o hardware do banco?

Porque o problema é de forma, não de tamanho. O OFFSET de uma página profunda continua lendo e descartando linhas em qualquer hardware; dobrar CPU adia o sintoma e aumenta a conta. Com cursor e cache, a carga residual cai para `λ × (1 - H)`: com 200 req/s e 92% de acerto (meta), sobram 16 req/s no banco. Esse ganho não se compra com instância maior.

Há ainda um limite prático: rate limit ausente deixa qualquer cliente novo derrubar o banco de novo, independentemente do tamanho contratado.

## 7. Quem decide se o TTL pode subir de 30 para 300 segundos?

O dono do dado de negócio, com a operação junto. A conta é direta: o pior caso de defasagem é `TTL + stale-while-revalidate`, ou seja, `30 + 60 = 90` segundos com a configuração atual. Triplicar o TTL levaria esse teto a 360 segundos e só faz sentido se a área aceitar listagem com até seis minutos de atraso.

A regra de governança adotada: mudança de TTL é decisão de produto registrada em ADR, não ajuste de performance feito por engenharia sozinha.

## 8. E se o consumidor fizer retry agressivo e virar tempestade?

Primeiro, o balde de tokens limita o volume por chave, então a tempestade não chega ao banco. Segundo, o `429` carrega `Retry-After` real, o que alinha o retry do consumidor ao momento em que já existe orçamento.

O que não resolve sozinho: retry simultâneo de mil clientes no mesmo segundo (efeito de alinhamento). Por isso o contrato de integração exige backoff exponencial com jitter. Quem não joga com jitter repete o problema em outra camada, e isso é item de revisão de integração.

## 9. E se cair no meio da noite, o que o plantão faz primeiro?

O runbook tem quatro sintomas com detecção automática: pool esgotado, índice perdido, Redis fora e 429 em massa. A ordem de ação é checar o painel, identificar qual dos quatro está ativo e aplicar a mitigação correspondente: reduzir pool e cortar varredura, recriar índice com `CREATE INDEX CONCURRENTLY`, confirmar o fallback do Redis ou auditar o consumidor que estoura a quota.

O que nunca se faz às três da manhã: subir quota às cegas. Isso transfere o problema do 429 para o banco, que é justamente o recurso que não se recupera sozinho.

## 10. Qual o SLO e o que acontece quando estoura?

Disponibilidade de 99,5% em 30 dias móveis, p95 da lista abaixo de 200 ms no cache hit, hit rate de cache acima de 90%, todos com janela de medição declarada (meta).

O orçamento de erro decorre da conta: `0,005 × 30 × 24 × 60 = 216` minutos por mês. Ao consumir 50% desse orçamento na metade do mês, suspende-se toda mudança não corretiva na API até o mês fechar. Isso impede a morte por mil cortes de 90 segundos.

## 11. Como você prova que funciona, além de dizer que funciona?

Com evidência reproduzível: `EXPLAIN (ANALYZE, BUFFERS)` da página 1.000 mostrando linhas lidas próximas de `limit + 1`; par de chamadas idênticas mostrando `X-Cache: MISS` e depois `HIT`; 101 requisições no minuto produzindo exatamente um `429` com `Retry-After`; e a mesma lista devolvendo `200` com o Redis desligado.

Nenhuma dessas evidências é opinião. São saídas de comando que qualquer revisor roda de novo em homologação.

## 12. Qual a alternativa mais barata que você deixaria de fora?

A mais barata é manter offset com limite de página e só impor rate limit global. Custa quase nada de implementação, mas não resolve a página profunda nem isola clientes: o OFFSET continua caro e um cliente novo derruba os outros.

Existe um meio-termo defensável: offset até a página 100 (5.000 linhas com `limit = 50`) combinado com cursor além disso. Foi considerado e descartado porque cria dois caminhos de paginação para testar e documentar, e o ganho se perde na complexidade de manter as duas regras.

## 13. Pergunta de negócio: qual o impacto em horas e em R$?

Em horas: uma varredura completa de 80k em páginas de 50 são 1.600 chamadas; com páginas profundas lentas e travamentos, cada ciclo de incidente consome tempo de suporte, de reprocessamento nos consumidores e de reanálise de dados. Com custo estável por página, a duração da varredura vira previsível e o sincronismo noturno deixa de brigar com o horário comercial.

Em R$ o ganho é de uso, não de capacidade: nenhuma instância adicional de banco (meta: redução de 92% do tráfego de listagem com 90% de acerto de cache). O custo de infraestrutura nova é apenas o Redis, cujo uso efetivo fica em torno de 20 MB (Exemplo numérico) numa instância de 256 MB. Não há número medido de economia monetária no material; a afirmação segura é que a solução não exige escala de compute.
