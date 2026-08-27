# Idempotencia e Entrega Exactly-Once (na pratica: at-least-once + dedup)

Sistemas Distribuidos

<h2><span class="num">1.</span> Contexto</h2>

<p>Quando você <strong>desacopla</strong> com mensageria, o mesmo evento pode chegar <strong>duas vezes</strong>. Rede caiu no <code>ack</code>? O broker reentrega. Consumer reiniciou? Ele reprocessa o último lote. Se cada entrega cobrar o cliente de novo, vira prejuízo e reclamação. O desafio é garantir que <strong>processar 1x ou 5x dê o mesmo resultado</strong>: é a <strong>idempotência</strong>.</p>

<div class="didactic"><div class="didactic-title">Analogia da conta de luz</div>Você recebe a conta e paga. O banco envia o comprovante 3 vezes por engano. Se cada comprovante disparasse um <em>novo</em> débito, você pagaria 3x. A conta tem um <strong>código de autenticação</strong>: o banco vê 'já paguei esse código' e ignora as cópias. A <strong>chave de idempotência</strong> é esse código — ela diz 'esse evento já foi processado, não faça de novo'.</div>

<h2><span class="num">2.</span> Diagnóstico</h2>

<p>Sem dedupe, reentregas do broker geram <strong>cobranças duplicadas</strong>, estoque negativo e e-mails repetidos. Times gastam horas apagando incêndio manualmente. O problema é estrutural: em sistema distribuído, <em>exactly-once</em> de ponta-a-ponta é impossível — só existe <em>at-least-once</em> + idempotência, ou <em>effectively-once</em>.</p>

<div class="charts"><div class="chart-card"><div class="chart-title">Cobranças duplicadas (n/mês)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cobranças duplicadas (n/mês)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,138 68,126 94,132 121,114 147,104 173,94 199,82 225,74 251,62 278,50 304,42 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,138 68,156 94,163 121,167 147,168 173,169 199,169 225,170 251,170 278,170 304,170 330,170" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="170" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div><div class="chart-card"><div class="chart-title">Horas de correção manual (h/mês)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Horas de correção manual (h/mês)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,129 68,121 94,125 121,108 147,98 173,88 199,79 225,67 251,57 278,47 304,42 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,129 68,154 94,162 121,166 147,168 173,168 199,169 225,170 251,170 278,170 304,170 330,170" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="170" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div></div>

<div class="callout"><strong>Raiz do problema:</strong> o consumer não distingue 'evento novo' de 'evento reentregue'. Falta uma <strong>chave de idempotência</strong> persistida e uma tabela de <em>já-processados</em> consultada antes de agir.</div>

<h2><span class="num">3.</span> Solução</h2>

<p>Dois pilares: (1) <strong>idempotência no consumer</strong> — toda ação só executa se a <code>idempotency_key</code> não existir numa tabela; (2) <strong>Outbox Pattern</strong> — em vez de escrever no banco E publicar no broker na mesma transação (que pode falhar no meio), você grava o evento numa tabela <code>outbox</code> dentro da <strong>mesma transação</strong> do negócio. Um <em>relay</em> depois publica o outbox no broker. Assim o evento nunca se perde nem duplica: banco e mensagem ficam atômicos.</p>

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

<div class="pipeline"><div class="pipeline-head"><span class="pipeline-title">Outbox + idempotência na cobrança</span><span class="pipeline-live"><span class="dot"></span> fluxo em execução</span></div><div class="pipeline-body"><div class="pl-rail"><span class="pl-pulse p1"></span><span class="pl-pulse p2"></span><span class="pl-pulse g"></span></div><div class="pl-steps"><div class="pl-step"><div class="num">1</div><div><div class="name">Transaction <code>DB.begin()</code></div><div class="desc">Grava a venda E o evento na tabela <code>outbox</code> na mesma transação.</div><span class="pl-chip"><span class="pl-tag atômico">ok</span></span></div></div><div class="pl-step"><div class="num">2</div><div><div class="name">Commit <code>db.commit()</code></div><div class="desc">Se der erro, nada é gravado — consistência garantida.</div><span class="pl-chip"><span class="pl-tag all-or-nothing">ok</span></span></div></div><div class="pl-step"><div class="num">3</div><div><div class="name">Relay <code>outbox.publish()</code></div><div class="desc">Lê o outbox não enviado e publica no broker, marcando como enviado.</div><span class="pl-chip"><span class="pl-tag 1 vez">warn</span></span></div></div><div class="pl-step"><div class="num">4</div><div><div class="name">Consumer <code>dedupe(key)</code></div><div class="desc">Antes de cobrar, consulta <code>idempotency_key</code> na tabela de processados.</div><span class="pl-chip"><span class="pl-tag dedupe">audit</span></span></div></div><div class="pl-step"><div class="num">5</div><div><div class="name">Ack <code>consumer.ack()</code></div><div class="desc">Só faz <code>ack</code> após gravar a chave — reentrega não cobra 2x.</div><span class="pl-chip"><span class="pl-tag effectively-once">ok</span></span></div></div></div><div class="pl-footer"><span>Falha no relay → evento fica no outbox até ser publicado; falha no consumer → reentrega cai no dedupe.</span></div></div></div>

<h2><span class="num">5.</span> Antes vs Depois</h2>

<table><tr><th>Cenário</th><th>Antes (sem dedupe)</th><th>Depois (outbox + dedupe)</th></tr><tr><td>Reentrega do broker</td><td>Cobra 2x</td><td>Ignorada (chave existe)</td></tr><tr><td>Falha na publicação</td><td>Evento perdido</td><td>Reprocessado do outbox</td></tr><tr><td>Consistência</td><td>Banco≠Mensagem</td><td>Atômica</td></tr><tr><td>Correção manual</td><td>~60h/mês</td><td>~0h/mês</td></tr></table>

<h2><span class="num">6.</span> Entregas</h2>

<ul><li><strong>Migração</strong> <code>001_outbox.sql</code>: tabela <code>outbox(event_id, payload, sent)</code>.</li><li><strong>Relay</strong> <code>outbox_relay.py</code>: publica pendentes no Kafka a cada 1s.</li><li><strong>Consumer</strong> <code>cobranca_idempotente.py</code>: dedupe por <code>idempotency_key</code>.</li><li><strong>Teste</strong> <code>test_reentrega.py</code>: injeta o mesmo evento 5x e afirma 1 cobrança.</li></ul>

<h2><span class="num">7.</span> Métricas</h2>

<div class="charts"><div class="chart-card"><div class="chart-title">Eventos idempotentes corretos (%)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Eventos idempotentes corretos (%)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,170 68,127 94,91 121,66 147,49 173,39 199,33 225,30 251,27 278,27 304,26 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S1</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S2</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S3</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S4</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S5</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S6</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S7</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S8</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S9</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S10</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S11</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S12</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Semana 1</text></svg></div></div>

<div class="callout"><strong>Meta:</strong> 100% de <em>effectively-once</em> nas cobranças, com zero débito duplicado mesmo sob reentrega contínua.</div>

<h2><span class="num">8.</span> Status final</h2>

<p><span class="status st-warn">NÃO publicado</span> — Desenvolvido e em homologação. Aguarda revisão antes de produção.</p>