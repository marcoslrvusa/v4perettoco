# Idempotência e Entrega Exactly-Once (na prática: at-least-once + dedup)

Sistemas Distribuídos

<h2><span class="num">1.</span> Contexto</h2>

<p>Quando você <strong>desacopla</strong> com mensageria, o mesmo evento pode chegar <strong>duas vezes</strong>. Rede caiu no <code>ack</code>? O broker reentrega. Consumer reiniciou? Ele reprocessa o último lote. Se cada entrega cobrar o cliente de novo, vira prejuízo e reclamação. O desafio é garantir que <strong>processar 1x ou 5x dê o mesmo resultado</strong>: é a <strong>idempotência</strong>.</p>

<div class="didactic"><div class="didactic-title">Analogia da conta de luz</div>Você recebe a conta e paga. O banco envia o comprovante 3 vezes por engano. Se cada comprovante disparasse um <em>novo</em> débito, você pagaria 3x. A conta tem um <strong>código de autenticação</strong>: o banco vê 'já paguei esse código' e ignora as cópias. A <strong>chave de idempotência</strong> é esse código: ela diz 'esse evento já foi processado, não faça de novo'.</div>

<h2><span class="num">2.</span> Diagnóstico</h2>

<p>Sem dedupe, reentregas do broker geram <strong>cobranças duplicadas</strong>, estoque negativo e e-mails repetidos. Times gastam horas apagando incêndio manualmente. O problema é estrutural: em sistema distribuído, <em>exactly-once</em> de ponta-a-ponta é impossível: só existe <em>at-least-once</em> + idempotência, ou <em>effectively-once</em>.</p>

<div class="charts"><div class="chart-card"><div class="chart-title">Cobranças duplicadas (n/mês)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cobranças duplicadas (n/mês)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,138 68,126 94,132 121,114 147,104 173,94 199,82 225,74 251,62 278,50 304,42 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,138 68,156 94,163 121,167 147,168 173,169 199,169 225,170 251,170 278,170 304,170 330,170" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="170" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div><div class="chart-card"><div class="chart-title">Horas de correção manual (h/mês)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Horas de correção manual (h/mês)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,129 68,121 94,125 121,108 147,98 173,88 199,79 225,67 251,57 278,47 304,42 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,129 68,154 94,162 121,166 147,168 173,168 199,169 225,170 251,170 278,170 304,170 330,170" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="170" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div></div>

<div class="callout"><strong>Raiz do problema:</strong> o consumer não distingue 'evento novo' de 'evento reentregue'. Falta uma <strong>chave de idempotência</strong> persistida e uma tabela de <em>já-processados</em> consultada antes de agir.</div>

<h2><span class="num">3.</span> Solução</h2>

<p>Dois pilares: (1) <strong>idempotência no consumer</strong>: toda ação só executa se a <code>idempotency_key</code> não existir numa tabela; (2) <strong>Outbox Pattern</strong>: em vez de escrever no banco E publicar no broker na mesma transação (que pode falhar no meio), você grava o evento numa tabela <code>outbox</code> dentro da <strong>mesma transação</strong> do negócio. Um <em>relay</em> depois publica o outbox no broker. Assim o evento nunca se perde nem duplica: banco e mensagem ficam atômicos.</p>

<pre><code># Outbox + idempotência (exemplo didático, Python)
import json, uuid, psycopg2

def registrar_venda(conn, venda):
    event_id = str(uuid.uuid4())
    with conn:                          # MESMA transação: banco + evento
        cur = conn.cursor()
        cur.execute("INSERT INTO venda VALUES (%s,%s)", (venda['id'], venda['valor']))
        cur.execute(
            "INSERT INTO outbox(event_id, tipo, payload, sent) VALUES (%s,'venda.criada',%s,false)",
            (event_id, json.dumps(venda)))

def consumer_cobrar(conn, key, venda):
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM processados WHERE idempotency_key=%s", (key,))
        if cur.fetchone():              # reentrega -&gt; ignora
            return "ignorado (dedupe)"
        cobrar(venda)                    # efeito só acontece 1x
        cur.execute("INSERT INTO processados(idempotency_key) VALUES (%s)", (key,))
    return "cobrado 1x"
</code></pre>

<h2><span class="num">4.</span> Como funciona (pipeline)</h2>

<div class="pipeline"><div class="pipeline-head"><span class="pipeline-title">Outbox + idempotência na cobrança</span><span class="pipeline-live"><span class="dot"></span> fluxo em execução</span></div><div class="pipeline-body"><div class="pl-rail"><span class="pl-pulse p1"></span><span class="pl-pulse p2"></span><span class="pl-pulse g"></span></div><div class="pl-steps"><div class="pl-step"><div class="num">1</div><div><div class="name">Transaction <code>DB.begin()</code></div><div class="desc">Grava a venda E o evento na tabela <code>outbox</code> na mesma transação.</div><span class="pl-chip"><span class="pl-tag atômico">ok</span></span></div></div><div class="pl-step"><div class="num">2</div><div><div class="name">Commit <code>db.commit()</code></div><div class="desc">Se der erro, nada é gravado: consistência garantida.</div><span class="pl-chip"><span class="pl-tag all-or-nothing">ok</span></span></div></div><div class="pl-step"><div class="num">3</div><div><div class="name">Relay <code>outbox.publish()</code></div><div class="desc">Lê o outbox não enviado e publica no broker, marcando como enviado.</div><span class="pl-chip"><span class="pl-tag 1 vez">warn</span></span></div></div><div class="pl-step"><div class="num">4</div><div><div class="name">Consumer <code>dedupe(key)</code></div><div class="desc">Antes de cobrar, consulta <code>idempotency_key</code> na tabela de processados.</div><span class="pl-chip"><span class="pl-tag dedupe">audit</span></span></div></div><div class="pl-step"><div class="num">5</div><div><div class="name">Ack <code>consumer.ack()</code></div><div class="desc">Só faz <code>ack</code> após gravar a chave: reentrega não cobra 2x.</div><span class="pl-chip"><span class="pl-tag effectively-once">ok</span></span></div></div></div><div class="pl-footer"><span>Falha no relay → evento fica no outbox até ser publicado; falha no consumer → reentrega cai no dedupe.</span></div></div></div>

<h2><span class="num">5.</span> Antes vs Depois</h2>

<table><tr><th>Cenário</th><th>Antes (sem dedupe)</th><th>Depois (outbox + dedupe)</th></tr><tr><td>Reentrega do broker</td><td>Cobra 2x</td><td>Ignorada (chave existe)</td></tr><tr><td>Falha na publicação</td><td>Evento perdido</td><td>Reprocessado do outbox</td></tr><tr><td>Consistência</td><td>Banco≠Mensagem</td><td>Atômica</td></tr><tr><td>Correção manual</td><td>~60h/mês</td><td>~0h/mês</td></tr></table>

<h2><span class="num">6.</span> Entregas</h2>

<ul><li><strong>Migração</strong> <code>001_outbox.sql</code>: tabela <code>outbox(event_id, payload, sent)</code>.</li><li><strong>Relay</strong> <code>outbox_relay.py</code>: publica pendentes no Kafka a cada 1s.</li><li><strong>Consumer</strong> <code>cobranca_idempotente.py</code>: dedupe por <code>idempotency_key</code>.</li><li><strong>Teste</strong> <code>test_reentrega.py</code>: injeta o mesmo evento 5x e afirma 1 cobrança.</li></ul>

<h2><span class="num">7.</span> Métricas</h2>

<div class="charts"><div class="chart-card"><div class="chart-title">Eventos idempotentes corretos (%)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Eventos idempotentes corretos (%)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,170 68,127 94,91 121,66 147,49 173,39 199,33 225,30 251,27 278,27 304,26 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S1</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S2</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S3</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S4</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S5</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S6</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S7</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S8</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S9</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S10</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S11</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S12</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Semana 1</text></svg></div></div>

<div class="callout"><strong>Meta:</strong> 100% de <em>effectively-once</em> nas cobranças, com zero débito duplicado mesmo sob reentrega contínua.</div>

<h2><span class="num">8.</span> Decisões e tradeoffs</h2><ul><li><strong>At-least-once do broker mais dedup no consumidor:</strong> entrega exactly-once observacional para o negócio, porque exactly-once de ponta a ponta não existe em sistema distribuído.</li><li><strong>Outbox transacional:</strong> venda e evento gravados na mesma transação na tabela <code>outbox(event_id, payload, sent)</code>, então falha na publicação vira reprocessamento do outbox em vez de evento perdido. Custo: relay varrendo pendentes a cada 1s.</li><li><strong>Dedupe por <code>idempotency_key</code> antes de agir:</strong> o consumer consulta a tabela de processados antes de cobrar. Custo: store com TTL para não encher.</li><li><strong>ACK só após gravar a chave:</strong> a reentrega cai no dedupe, então o mesmo evento 5x gera 1 cobrança. A chave combina event_id com identificador do negócio para não colidir.</li></ul><div class="callout"><strong>Fio condutor:</strong> a ordem importa (gravar chave, depois ACK), e cada escolha troca um risco financeiro (débito duplo) por um custo operacional conhecido (store com TTL, relay a cada 1s).</div><h2><span class="num">9.</span> Impacto no negócio</h2><p>Sem dedupe, reentregas geravam cobranças duplicadas e cerca de 60h por mês de correção manual. Com dedup a meta é zero duplicata e 100% dos handlers idempotentes, com correção próxima de 0h por mês. O teste que injeta o mesmo evento 5x e afirma 1 cobrança dá ao Financeiro previsibilidade: retry deixa de ser risco de débito duplo.</p><h2><span class="num">10.</span> Referências de estudo</h2><ul><li><strong>Curso:</strong> "Event-Driven Architecture: From Theory to Practice" (Udemy).</li><li><strong>Vídeo:</strong> "What is Idempotency?" (YouTube, Hussein Nasser).</li><li><strong>Doc oficial:</strong> Apache Kafka Documentation, Exactly-once Semantics (kafka.apache.org).</li><li><strong>Doc oficial:</strong> PostgreSQL Documentation, INSERT ON CONFLICT (postgresql.org).</li></ul><h2><span class="num">11.</span> Status final</h2>

<p><span class="status st-warn">NÃO publicado</span>: Desenvolvido e em homologação. Aguarda revisão antes de produção.</p>

<h2><span class="num">12.</span> Matemática e capacidade</h2>

<p>Quatro contas fechadas sustentam a decisão. Nenhuma delas é medição de produção, todas têm parâmetros declarados.</p>

<table><tr><th>Conta</th><th>Fórmula</th><th>Exemplo numérico</th><th>Decisão que sai da conta</th></tr><tr><td>Capacidade do store de dedup</td><td><code>linhas = λ × T</code></td><td>120 eventos/s × 172.800 s (48 h) = 20.736.000 linhas × 104 B ≈ 2,2 GB</td><td>retenção de 48 h e particionamento por <code>ts</code></td></tr><tr><td>Concorrência de consumers</td><td><code>L = λ W</code></td><td>500 msg/s × 0,040 s = 20 execuções simultâneas</td><td>se só há 8 workers, o consumo real cai para 200 msg/s e nasce backpressure</td></tr><tr><td>Custo da checagem</td><td><code>base + RTT_store</code></td><td>18 ms + 2,4 ms = 20,4 ms, acréscimo de 13,3%</td><td>dedup e domínio precisam ficar na mesma região</td></tr><tr><td>Orçamento de erro</td><td><code>(1 − SLO) × janela</code></td><td>0,05% × 43.200 min = 21,6 min por mês</td><td>estourou, congela deploy de consumers</td></tr></table>

<div class="callout"><strong>Lei de Little aplicada:</strong> se o handler sobe de 40 ms para 200 ms, a capacidade por worker cai de 25 msg/s para 5 msg/s. Com 500 msg/s de entrada, o lag da partição sobe 20 msg/s por segundo de atraso. Dedup não é causa do problema, mas amplifica o sintoma se o store estiver lento.</div>

<pre><code># Consulta de capacidade do store de dedup (parâmetros declarados)
-- lambda = 120 eventos/s, T = 48 h
-- linhas = 120 * 172800 = 20736000
SELECT count(*)                          AS linhas,
       pg_size_pretty(pg_total_relation_size('processed_events')) AS tamanho,
       min(ts)                           AS idade_minima
FROM processed_events;

-- Critério: idade_minima deve ficar proxima de 48 h.
-- Se ficar menor, o expurgo esta agressivo demais (violacao da invariante 7).
</code></pre>

<h2><span class="num">13.</span> Invariantes e modos de falha</h2>

<table><tr><th>#</th><th>Invariante</th><th>Violação</th><th>Mitigação</th></tr><tr><td>1</td><td>O efeito de um <code>event_id</code> é aplicado no máximo 1 vez</td><td>débito duplo, fatura 2x</td><td>chave gravada antes do efeito</td></tr><tr><td>2</td><td>Chave gravada antes do <code>ack</code></td><td>queda no meio deixa efeito sem registro</td><td>teste que mata o processo nessa janela</td></tr><tr><td>3</td><td>Chave combina <code>event_id</code> com chave de negócio</td><td>colisão entre eventos legítimos</td><td>composição obrigatória da chave</td></tr><tr><td>4</td><td>Chave de partição é o identificador de negócio</td><td>reordenação sobrescreve estado novo</td><td>partição por CNPJ</td></tr><tr><td>5</td><td>Retenção do dedup maior que a janela de reentrega</td><td>duplicata tardia semanas depois</td><td><code>T_dedup &gt; T_reentrega_max</code></td></tr><tr><td>6</td><td>Nenhuma mensagem entra em retry infinito</td><td>head of line blocking na partição</td><td>DLQ após limite de tentativas</td></tr></table>

<table><tr><th>Sintome</th><th>Causa raiz</th><th>Detecção</th><th>Recuperação</th></tr><tr><td>Cobrança duplicada em lote</td><td>chave depois do efeito</td><td>contagem por <code>event_id</code> &gt; 1</td><td>inverter ordem e estornar pela lista</td></tr><tr><td>Lag subindo com consumo zerado</td><td>poison pill sem DLQ</td><td>lag estável com throughput 0</td><td>encaminhar para DLQ e corrigir payload</td></tr><tr><td>Duplicata reaparece após semanas</td><td>TTL menor que a reentrega</td><td>duplicatas correlacionadas a <code>ts</code> antigo</td><td>ampliar retenção e repovoar a janela</td></tr><tr><td>Dois consumers na mesma linha</td><td>falta de <code>ON CONFLICT</code></td><td>linhas com versão regredida</td><td>upsert condicionado por versão</td></tr></table>

<div class="callout"><strong>Regra de detecção:</strong> log não detecta, contagem detecta. O único sinal confiável é quantas vezes o efeito foi aplicado por <code>event_id</code>. Qualquer valor acima de 1 é perda financeira direta e entra em severidade alta.</div>

<h2><span class="num">14.</span> Ordenação, particionamento e replay</h2>

<p>Idempotência sem ordem é metade da garantia. Se a chave de partição for o <code>event_id</code>, dois eventos do mesmo cliente caem em partições diferentes, são consumidos em ordem trocada e o mais antigo sobrescreve o mais novo. A regra é <strong>chave de partição = identificador de negócio</strong>, de modo que tudo que pertence à mesma entidade vive na mesma partição e o broker preserva a ordem relativa.</p>

<p><strong>Exemplo numérico:</strong> 12 partições com 480 msg/s no total dão 40 msg/s por partição. Um lote de 1.000 mensagens drena em 1.000 / 40 = 25 s. Se o <code>max.poll.interval.ms</code> estiver em 300.000 ms, a margem é 12x. Se o handler subir para 200 ms por mensagem, o tempo de lote sobe para 200 s e a margem cai para 1,5x: é o ponto em que a reposição de sessão vira risco.</p>

<p><strong>Replay como prova:</strong> reprocessar 1 h com 12 partições a 40 msg/s por partição move 12 × 3.600 × 40 = 1.728.000 eventos. Sem dedup seriam 1.728.000 efeitos repetidos. Com dedup, todas as chaves já existem, nada muda de estado e o replay custa só I/O. É o teste de aceite mais barato que existe, e está registrado como CA-5.</p>

<pre><code># Replay seguro: primeiro auditar, depois reprocessar
-- 1) Estado de partida: quantos eventos ja foram aplicados
SELECT count(*) FROM processed_events WHERE ts &lt;= now() - interval '1 hour';

-- 2) Reexecutar o consumer a partir do offset antigo (exemplo didático)
-- consumer --topic cobranca --from-offset &lt;offset-1h-atras&gt;

-- 3) Prova: contagem de efeito por event_id continua 1
-- Se subir para 2, o dedup esta cobrindo a janela errada.
</code></pre>

<div class="callout"><strong>Event sourcing e CQRS:</strong> resolvem outro problema. Dão replay e auditoria de brinde, mas exigem versionamento de schema de evento, migração de projeção e disciplina de compatibilidade por anos. Custo maior do que o risco financeiro que esta atividade cobre, por isso ficaram registradas como alternativas descartadas na ADR-052.</div>

<h2><span class="num">15.</span> Critérios de aceite e checklist de domínio</h2>

<ol><li><strong>CA-1:</strong> mesmo <code>event_id</code> inserido 3 vezes resulta em 1 efeito e 2 descartes.</li><li><strong>CA-2:</strong> dois processos consumidores em paralelo aplicam 1 vez por <code>event_id</code>.</li><li><strong>CA-3:</strong> processo morto entre efeito e <code>ack</code> gera 0 efeitos adicionais na reentrega.</li><li><strong>CA-4:</strong> payload inválido vai para DLQ e não reduz o throughput das partições saudáveis.</li><li><strong>CA-5:</strong> replay de 1 h sobre histórico processado não altera estado de negócio.</li><li><strong>CA-6:</strong> consulta de cobertura reporta 100% dos handlers antes do merge.</li></ol>

<p>Checklist que o sênior roda antes de dizer pronto: chave combinando <code>event_id</code> com chave de negócio em todo handler financeiro; unicidade imposta por <code>PRIMARY KEY</code> e não por <code>SELECT</code>; <code>ON CONFLICT</code> no upsert; chave gravada antes do <code>ack</code>; partição por identificador de negócio; retenção maior que a janela de reentrega; DLQ e limite de tentativas; contagem de efeito por <code>event_id</code> no dashboard com alerta; seis critérios de aceite no CI bloqueando merge; runbook com dono e rollback; replay já executado uma vez; alternativas descartadas registradas na ADR; política de expurgo documentada com o volume em GB; rota de estorno acertada com o Financeiro.</p>

<div class="callout"><strong>Fecho técnico:</strong> at-least-once no transporte, idempotência no efeito, ordem garantida por partição e replay como prova. Quatro mecanismos, nenhum deles exige transação distribuída, e todos verificáveis por contagem.</div>