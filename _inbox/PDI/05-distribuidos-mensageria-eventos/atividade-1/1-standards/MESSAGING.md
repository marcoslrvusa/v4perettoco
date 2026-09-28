# Mensageria: Padrão

Padrão autoritativo de transporte assíncrono da Atividade 1 da trilha 05 (Sistemas Distribuídos com Mensageria).

- **Fila**: 1 consumidor (trabalho).
- **Tópico**: N consumidores (evento).
- **DLQ**: falha após N -> analise.
- **ACK**: só após processar.

## 1. Escopo e não-escopo

**Escopo deste standard**

- Escolher fila ou tópico para cada fluxo, com a regra de decisão explícita.
- Definir a semântica de entrega adotada (at-least-once) e o que a aplicação precisa fazer para sobreviver a ela.
- Fixar as regras de ACK explícito, prefetch limitado, política de DLQ e backoff com jitter.
- Especificar telemetria, plano de teste e critérios de aceite que o sênior usa para dizer "pronto".

**Não-escopo**

- Deduplicação profunda e chaves de idempotência: é o foco da Atividade 2 da mesma trilha (`05-A2`, standard `IDEMPOTENCY.md`).
- Disjuntor de circuito (`circuit breaker`) e backoff em cadeia de chamadas síncronas: Atividade 3 (`05-A3`).
- Anonimização e consentimento dentro do payload do evento: Atividade 4 (`05-A4`).
- Modelagem do schema de domínio: pertence à trilha 02, eventos de domínio do DDD (`02-A3`).

## 2. Termos canônicos

| Termo | Significado operacional | O que quebra se for ignorado |
| --- | --- | --- |
| Fila (`queue`) | Estrutura FIFÓ onde 1 mensagem é entregue a 1 consumidor | Trabalho duplicado ou disputa por mensagem |
| Tópico (`topic`) | Canal de difusão onde 1 mensagem chega a N assinantes | Consumidor que precisa do evento e não recebe |
| Exchange (RabbitMQ) | Roteador que decide para qual fila o mensagem vai | Mensagem publicada e não entregue a ninguém |
| Partição (Kafka) | Log ordenado por chave dentro de um tópico | Ordem por entidade violada |
| ACK | Confirmação explícita de que a mensagem foi tratada | Perda silenciosa ou reentrega infinita |
| `prefetch` / `basic.qos` | Limite de mensagens não confirmadas por consumidor | Consumer lento engole a fila inteira |
| Redelivery | Reentrega da mesma mensagem após falha ou timeout de ACK | Efeito aplicado duas vezes se não houver idempotência |
| Poison pill | Mensagem que o consumidor nunca consegue processar | Bloqueio da fila ou da partição para sempre |
| DLQ (`dead letter queue`) | Fila de destino para mensagens que esgotaram o retry | Mensagem que some sem rastro |
| Lag | Distância entre o offset consumido e o offset mais novo | Consumidor cada vez mais atrasado sem alerta |
| Outbox | Tabela transacional de eventos publicados via CDC | Evento publicado sem escrita de domínio (ou o contrário) |
| Backpressure | Sinal de que o consumidor não acompanha o produtor | Fila cresce sem limite e o broker engasga |

## 3. Regra canônica

**R1. Toda mensagem sai com semântica at-least-once e volta idempotente.**
O broker garante que a mensagem é entregue pelo menos uma vez; a aplicação garante que o efeito acontece uma única vez. Não se compra `exactly-once` de ponta a ponta: produtor, broker e consumidor são três processos separados e a janela entre "efeito aplicado" e "ACK enviado" sempre existe.

**R2. Só existe ACK depois do efeito durável.**
Ordem obrigatória: aplicar o efeito na base de dados (commit) -> enviar o ACK ao broker. Inverter essa ordem produz perda (crash entre ACK e commit); manter a ordem correta produz duplicata (crash entre commit e ACK), que é o erro aceitável porque é detectável e remediável.

**R3. Prefetch limita a janela de trabalho.**
O consumidor nunca deve ter mais mensagens em voo do que consegue terminar dentro do tempo de `visibility timeout`. A janela efetiva é:

```text
janela_efetiva = workers x prefetch
```

**R4. Retry usa backoff exponencial com jitter, com teto.**
A espera da tentativa `n` (n iniciando em 0) é:

```text
espera(n) = min(base_ms * 2^n, teto_ms) + jitter(0 .. jitter_ms)
```

Sem jitter, todas as réplicas re-tentam no mesmo instante e criam um `thundering herd` contra o mesmo recurso já degradado. Com teto fixo, uma falha duradoura não vira espera de horas dentro do `visibility timeout`.

**R5. DLQ depois de N tentativas, sempre com o motivo anexado.**
A mensagem que esgota o `maxReceiveCount` vai para a DLQ com o cabeçalho de histórico de morte preservado, para que a análise diga qual etapa a matou, e não apenas que ela morreu.

**R6. Ordem só é prometida dentro de uma partição (ou de uma fila única).**
Ordem global entre duas filas ou dois tópicos não existe em sistema distribuído. Se a regra de negócio exige ordem, a chave de partição tem de ser a mesma entidade afetada.

## 4. Tabela de decisão

| Se | E | Então | Por quê |
| --- | --- | --- | --- |
| A mensagem é trabalho exclusivo | 1 worker por mensagem | Fila clássica/quorum | Competição é desejada: ninguém faz a mesma cobrança duas vezes |
| A mesma mensagem interessa a times diferentes | Cada time reage ao seu modo | Tópico pub/sub com assinante por time | Evita que o produtor conheça os consumidores |
| O consumidor pode falhar por bug de parse | Payload vem de fonte externa | Rota direta para DLQ no primeiro `Nack` | Não adianta re-tentar 5x o mesmo parse inválido |
| O consumidor falha por indisponibilidade transitória | Dependência externa fora do ar | Backoff exponencial e depois DLQ | O problema some sozinho; re-tentar cedo só piora |
| Duas mensagens podem chegar duplicadas | Efeito é aditivo (log, contador) | Idempotência por chave e janela de retenção | Duplicata inócua se a deduplicação cobre a janela |
| A ordem entre eventos da mesma entidade importa | Ex.: `pedido.aberto` antes de `pedido.fechado` | Partição por `entity_id` / fila única | Ordem é propriedade de partição, não do tópico |
| O payload tem mais de 256 KB | Broker com limite de mensagem | Payload fora da fila, só o ponteiro dentro | Estoura limite e trava a rota inteira |
| O produtor precisa de confirmação de persistência | Perda não é aceitável | Publisher confirm / `acks=all` + `min.insync.replicas=2` | `fire-and-forget` silencia falha de disco e de réplica |

## 5. Exemplo numérico: capacidade da janela de consumo

**Exemplo numérico:** cenário de pico de campanha com `$\lambda$ = 200 msg/s` (alvo de SLO já usado na atividade), tempo médio de serviço por mensagem `$W = 250 ms` e 5 workers do Financeiro.

1. Little's Law, `$L = \lambda \cdot W$`: `$L = 200 \cdot 0{,}250 = 50$` mensagens em processamento simultâneo, em média.
2. Com `workers = 5`, a janela mínima por worker é `$50 / 5 = 10$` mensagens. Configurar `prefetch = 10` cobre a média exata.
3. Margem de pico de 3x por 2 s: `$\lambda_{pico} = 600 msg/s$` exige `$L = 600 \cdot 0{,}250 = 150$` mensagens em voo. Com `prefetch = 10` e `workers = 5` só há 50 slots, então 100 mensagens ficam represadas no broker: exatamente o comportamento desejado de backpressure (fila cresce, memória do consumer fica estável).
4. Conclusão: `prefetch = 10` não é chute, é `$\lambda W / workers$` arredondado para cima com margem controlada pela fila.

Contra-exemplo do mesmo cenário com `prefetch = 1000`: `$5 \cdot 1000 = 5000$` mensagens na memória do processo. Exemplo numérico: cada mensagem de 20 KB ocupa cerca de 20 KB de buffer mais objeto Python em memória, ou seja, ordem de 100 MB retidos só em deserialização, fora o custo de re-entrega se o processo morrer com tudo em voo.

## 6. Garantias de entrega: o que cada camada realmente promete

| Camada | Promete | Não promete |
| --- | --- | --- |
| Produtor -> broker (sem confirm) | Entrega "provável" | Persistência antes do ACK do socket |
| Produtor -> broker (confirm / `acks=all`) | Persistência em N réplicas antes do retorno | Que o consumidor vai conseguir processar |
| Broker -> consumidor | Pelo menos uma entrega enquanto não houver ACK | Ausência de duplicata |
| Efeito no banco + ACK | Efeito durável; duplicata possível | Efeito único sem chave de idempotência |
| Ponta a ponta | At-least-once com efeito único via dedup | Exactly-once matematicamente puro |

A impossibilidade vem da janela entre commit e ACK. Duas falhas provam:

- **Crash depois do ACK e antes do commit**: mensagem confirmada, efeito perdido. Só se evita com ACK após o commit (regra R2).
- **Crash depois do commit e antes do ACK**: efeito aplicado, broker reentrega. Perda zero, duplicata certa. É por isso que a Atividade 2 existe.

Corolário operacional: deduplicação tem de cobrir um horizonte de tempo maior que o pior caso de reentrega. Exemplo numérico: `visibility_timeout = 60 s` e reentrega manual no máximo 5 vezes em 1 hora, logo a janela de dedup precisa ser de, no mínimo, 1 hora + margem, não de 60 s.

## 7. Idempotência e deduplicação (ponte com 05-A2)

Chave de idempotência canônica do evento:

```text
idempotency_key = sha256(type + ":" + version + ":" + entity_id + ":" + entity_version)
```

`entity_version` é um contador monotônico por entidade (versão otimista do registro), não o timestamp: dois eventos no mesmo segundo têm timestamp igual e se anulariam na dedup.

Estrutura mínima do consumidor:

```python
def handle(msg):
    chave = chave_idempotente(msg)
    if ja_processado(chave):          # SELECT na tabela de dedup
        ack(msg)                      # deduplicado, não é erro
        return
    with transacao():                 # efeito + registro da chave no MESMO commit
        aplicar_efeito(msg)
        registrar_deducao(chave)
    ack(msg)
```

O detalhe que separa sênior de pleno: o registro da chave entra na **mesma transação** do efeito. Se forem duas transações, o crash entre elas reabre a janela de duplicata.

## 8. Backpressure e prefetch na prática

Sinais de que falta backpressure:

1. `memory RSS` do consumidor subindo de forma monotônica com o tamanho da fila.
2. `unacked` perto do `prefetch` o tempo todo, com `ack` cada vez mais lento.
3. Número de conexões/treads do consumidor crescendo sem limite (autoscaling corrigindo lentidão de código).

Configuração de referência (RabbitMQ):

```python
channel.basic_qos(prefetch_count=10)          # janela por canal
channel.basic_consume(queue="cobranca.v1", on_message_callback=cb, auto_ack=False)
# auto_ack=False é obrigatório: auto_ack confirma ANTES do processamento
```

Se o processamento for lento, a resposta certa é reduzir `prefetch` ou adicionar workers, nunca aumentar `prefetch` para "deixar a fila correr". Aumentar `prefetch` apenas transfere a pressão da fila para a memória do processo, que é um lugar pior para perder dados.

## 9. Ordenação, poison pill e head of line blocking

- **Fila única**: ordenação FIFÓ relativa ao consumo, mas um `Nack` com requeue devolve a mensagem para a frente da fila e pode reiniciar o ciclo infinito. Use `Nack(requeue=False)` + contagem própria para fugir desse laço.
- **Partições**: ordem garantida só dentro da partição. Se `entity_id = 42` cai sempre na partição 7, os eventos de 42 saem em ordem; os de 43 podem chegar antes, e isso está correto.
- **Poison pill em partição**: como o consumidor processa a partição sequencialmente, uma mensagem que nunca passa bloqueia todo o fluxo daquela partição (head of line blocking). Mitigação em duas camadas: tentativas limitadas por mensagem, e salto para a DLQ por offset com log do offset problemático.
- **Consumer group**: membros dividem partições. Adicionar um consumidor rebalanceia a partição; durante o rebalanceio a entrega congela. Estratégias usuais: `max.poll.interval` maior que o pior lote, e processamento que tolera pausa de segundos.

Código do caminho de falha com contagem explícita:

```python
def callback(ch, method, properties, body):
    tentativas = (properties.headers or {}).get("x-retry", 0)
    try:
        processar(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except ErroDeParse:
        # mensagem nunca vai passar: não adianta requeue
        publicar_na_dlq(body, motivo="parse")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception:
        if tentativas + 1 >= MAX_TENTATIVAS:
            publicar_na_dlq(body, motivo=f"esgotou {tentativas + 1} tentativas")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            reagendar_com_backoff(method.delivery_tag, tentativas + 1)
```

## 10. Atomicidade produtor: transactional outbox

Problema: gravar no banco e publicar no broker são duas operações. O meio-termo frágil (commit e depois `publish`) perde eventos se o processo cair entre as duas; o inverso (publicar e depois commit) cria evento de venda que não existe.

Padrão do `outbox`:

```text
BEGIN;
  INSERT INTO vendas (...) VALUES (...);
  INSERT INTO outbox (id, tipo, payload, criado_em) VALUES (..., 'venda.criada', ...);
COMMIT;
-- um leitor CDC (ou job de varredura) publica o registro e marca publicado=true
```

Critério de aceite do outbox: nenhuma venda commitada fica com `outbox.publicado = false` por mais de `(meta) 5 s` em condições normais, e o atraso máximo observado é medido, não assumido.

Alternativa mais simples, aceita quando a perda é tolerada: `publish` dentro da transação com transação XA. Na prática é mais frágil e menos portável, por isso o outbox é o padrão escolhido.

## 11. Anti-padrões (o que o sênior reprovaria)

1. `auto_ack=True` "para simplificar": confirma antes do trabalho; qualquer crash no meio é perda pura.
2. `prefetch` ilimitado: transforma backpressure em estouro de memória.
3. Retry infinito com espera fixa de 1 s: martela a dependência quebrada e mantém a fila presa por horas.
4. DLQ sem alerta nem dono: vira depósito de mensagens que ninguém abre, que é perda disfarçada de suporte.
5. Payload gigante dentro da mensagem: acopla o broker ao tamanho do documento e pode travar a rota inteira.
6. Ordem buscada com `sleep` no consumidor: tempo não é ordem.
7. `Nack(requeue=True)` em erro de parse: ciclo infinito de reentrega da mesma mensagem.
8. Publicar evento fora de qualquer transação e chamar de "consistência eventual": na verdade é inconsistência não observada.
9. Contar mensagens publicadas como métrica de sucesso: o que importa é `processadas / publicadas` na mesma janela.
10. Esconder duplicata "porque nunca aconteceu": em at-least-once, duplicata é questão de estatística, não de sorte.
11. Assinar o tópico inteiro com um consumidor que só precisa de um tipo de evento: tráfego inútil e acoplamento por nome.
12. Fila compartilhada entre domínios diferentes: um domínio em pico suga a capacidade do outro.

## 12. Telemetria

| Métrica | Tipo | Cardinalidade aceitável | Alerta |
| --- | --- | --- | --- |
| `queue.depth` | gauge | 1 por fila (fase: `cobranca`, `marking`) | > `$\lambda \cdot 300 ms$` sustentado por 5 min (meta) |
| `consumer.unacked` | gauge | 1 por fila + consumidor | igual ao `prefetch` por > 2 min (meta) |
| `consumer.lag` (offset) | gauge | 1 por partição | crescendo por > 10 min (meta) |
| `redelivery.rate` | counter | 1 por fila | > 1% das entregas (meta) |
| `dlq.depth` | gauge | 1 por DLQ | > 0 por 1 h (meta); alerta crítico em > 24 h |
| `publish.latency.p95` | histograma | buckets fixos em ms | p95 > 100 ms (meta) |
| `e2e.latency.p95` | histograma | por tipo de evento | p95 > 5 s (meta, já usado no SLO) |
| `ack.failures` | counter | 1 por consumidor | qualquer crescimento sustentado |

Regra de cardinalidade: nunca usar `entity_id`, `order_id` ou `trace_id` como rótulo de métrica. Esses valores vão para log estruturado e tracing; em métrica eles detonam a memória do coletor.

## 13. Plano de teste

| Caso | Passo | Saída esperada | Critério de aceite |
| --- | --- | --- | --- |
| T1 Perda | Publicar 1k mensagens, derrubar o consumer no meio, subir de novo | Todas as 1k terminam processadas | Contagem final igual à publicada, sem exceção |
| T2 Duplicata | Reiniciar o consumer logo após o commit e antes do ACK | Reentrega ocorre, efeito aplicado 1x | Tabela de dedup com 1k chaves distintas |
| T3 DLQ | Enviar payload inválido no meio do lote | Inválida vai para DLQ, válidas seguem | `dlq.depth = 1`, `queue.depth = 0` |
| T4 Backpressure | Rodar consumer 10x mais lento que o produtor | Fila cresce, memória do consumer estável | RSS variação < 10% (meta) com fila em crescimento |
| T5 Backoff | Simular dependência externa fora do ar por 60 s | Esperas 1s, 2s, 4s, 8s... com jitter | Nenhum retry com espera fixa; pico de chamadas < 2x a média |
| T6 Ordem | Publicar 100 eventos da mesma `entity_id` | Consumidor vê ordem de versão crescente | Zero inversões de `entity_version` |
| T7 Ordenação cruzada | Publicar eventos de duas entidades | Ordem entre entidades livre, dentro de cada uma preservada | Nenhuma inversão dentro da mesma entidade |
| T8 Outbox | Matar o publicador entre commit e envio | Evento é publicado pelo leitor de outbox | `publicado=false` não persiste além da SLO do outbox |
| T9 Rebalance | Adicionar um terceiro consumer ao grupo | Rebalanceio congela por instantes e retoma | Nenhuma mensagem perdida, apenas atraso |
| T10 DLQ esquecida | Deixar DLQ com item por 25 h | Alerta dispara antes das 24 h | Alerta em < 24 h (meta), com dono notificado |

## 14. Critérios de aceite da atividade

1. Publicar 1k mensagens com o consumer derrubado e confirmar reprocessamento integral ao religar.
2. Mensagem inválida cai na DLQ e continua consultável, com motivo registrado.
3. Consumer lento não estoura memória: backpressure visível na fila, não no processo.
4. `>= 200 msg/s` sustentado no pico de teste, com `0` mensagens perdidas.
5. P95 de ponta a ponta `< 5 s` (meta) medido de publicação até ACK.
6. DLQ revisitada em `< 24 h`, com evidência de revisão registrada.
7. Toda fila e tópico usados em produção tem dono, alerta e runbook apontados no catálogo.

## 15. Checklist de adesão

1. Fila usada só para trabalho exclusivo; tópico usado para evento difundido.
2. `auto_ack` desligado em qualquer consumidor de produção.
3. `prefetch` derivado de `$\lambda W / workers$`, não de chute.
4. ACK sempre depois do commit do efeito.
5. Registro de dedup na mesma transação do efeito.
6. Retry com backoff exponencial + jitter + teto.
7. Erro de parse vai direto à DLQ, sem requeue.
8. `maxReceiveCount` definido e documentado por fila.
9. DLQ com alerta, dono e rotina de revisita < 24 h.
10. Payload com ponteiro, não com documento inteiro.
11. `trace_id` propagado do produtor ao consumidor via cabeçalho.
12. Sem rótulo de métrica com `entity_id` ou `order_id`.
13. Partição definida por `entity_id` quando a ordem importa.
14. Publisher confirm ou `acks=all` em fluxo que não pode perder.
15. Outbox onde domínio e publicação precisam ser atômicos.
16. Runbook de reprocessamento da DLQ testado, não só escrito.
17. Contrato de evento versionado e compatível com consumidores antigos.
18. Teste T1 (perda) executado antes de qualquer troca de versão do consumer.

## 16. Referências de estudo

- Curso: "Apache Kafka Séries: Learn Apache Kafka for Beginners" (Udemy, Stephane Maarek).
- Vídeo: "RabbitMQ in 100 Seconds" (YouTube, Fireship).
- Documento oficial: RabbitMQ Documentation (rabbitmq.com).
- Documento oficial: Apache Kafka Documentation (kafka.apache.org).
