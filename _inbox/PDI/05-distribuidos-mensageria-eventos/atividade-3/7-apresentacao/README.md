# Resiliencia com Circuit Breaker e Retry/Backoff

Sistemas Distribuidos

<h2><span class="num">1.</span> Contexto</h2>

<p>A FV faz chamadas entre microsserviços: o de <strong>Pagamento</strong> chama o de <strong>Antifraude</strong>, que chama o de <strong>Score</strong>. Se o Antifraude fica lento, o Pagamento fica <strong>centenas de requisições esperando</strong>. Cada uma segura um thread. O sistema todo entra em <em>congestão</em> mesmo com os outros serviços saudáveis. É a <strong>falha em cascata</strong>.</p>

<div class="didactic"><div class="didactic-title">Analogia do guarda de trânsito</div>Num cruzamento, se uma rua alaga, os carros ficam parados esperando a água baixar e travam todo o bairro. O <strong>circuit breaker</strong> é o guarda que, ao ver a rua alagada, <em>fecha o cruzamento</em> (abre o caminho alternativo) por alguns minutos. Depois ele testa 'a água baixou?' — se sim, reabre; se não, mantém fechado. Assim o trânsito desvia e a rua alagada se recupera sem virar um caos.</div>

<h2><span class="num">2.</span> Diagnóstico</h2>

<p>Sem proteção, uma lentidão no Score derruba o Pagamento por <strong>esgotamento de threads</strong>. O P95 dispara, o timeout estoura e o cliente vê erro. Não há <em>fallback</em>: tudo ou nada. Carece de <strong>retry com backoff</strong> — retentar na hora só piora a sobrecarga.</p>

<div class="charts"><div class="chart-card"><div class="chart-title">Latência P95 do Pagamento (ms)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Latência P95 do Pagamento (ms)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,157 68,155 94,151 121,144 147,132 173,117 199,101 225,82 251,64 278,51 304,39 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,157 68,157 94,156 121,156 147,155 173,154 199,154 225,153 251,152 278,152 304,152 330,152" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="152" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div><div class="chart-card"><div class="chart-title">Taxa de erro do Pagamento (%)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Taxa de erro do Pagamento (%)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,168 68,166 94,162 121,154 147,139 173,121 199,102 225,84 251,65 278,51 304,38 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,168 68,168 94,168 121,166 147,166 173,166 199,164 225,164 251,164 278,164 304,164 330,164" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="164" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div></div>

<div class="callout"><strong>Raiz do problema:</strong> chamadas remotas não têm <strong>timeout</strong> nem <strong>isolamento</strong>. Um serviço lento consome todos os recursos do chamador e propaga a falha — não há fronteira de resiliência.</div>

<h2><span class="num">3.</span> Solução</h2>

<p>Implementar um <strong>Circuit Breaker</strong> em 3 estados: <code>CLOSED</code> (tráfego normal, conta falhas), <code>OPEN</code> (após N falhas/timeout, bloqueia e devolve <em>fallback</em> imediato) e <code>HALF_OPEN</code> (após um tempo, libera poucos testes; se passarem, volta a CLOSED, senão segue OPEN). Combinar com <strong>retry exponencial com backoff + jitter</strong> (espera 0.1s, 0.2s, 0.4s... com ruído) para não sincronizar as retentativas.</p>

<pre><code># Circuit Breaker (exemplo didático, Python)
import time

class CircuitBreaker:
    def __init__(self, falhas=5, abre=30):
        self.estado = "CLOSED"; self.f = 0; self.t = time.time(); self.abre = abre
    def call(self, fn):
        if self.estado == "OPEN":
            if time.time() - self.t &lt; self.abre:
                return self.fallback()       # degradação graciosa
            self.estado = "HALF_OPEN"         # sonda 1 chamada
        try:
            r = fn()
            self.estado = "CLOSED"; self.f = 0
            return r
        except Exception:
            self.f += 1
            if self.f &gt;= 5:
                self.estado = "OPEN"; self.t = time.time()
            raise
    def fallback(self):
        return {"score": 0, "origem": "cache"}
</code></pre>

<h2><span class="num">4.</span> Como funciona (pipeline)</h2>

<div class="pipeline"><div class="pipeline-head"><span class="pipeline-title">Chamada resiliente Pagamento→Score</span><span class="pipeline-live"><span class="dot"></span> fluxo em execução</span></div><div class="pipeline-body"><div class="pl-rail"><span class="pl-pulse p1"></span><span class="pl-pulse p2"></span><span class="pl-pulse g"></span></div><div class="pl-steps"><div class="pl-step"><div class="num">1</div><div><div class="name">Timeout <code>client.timeout(800)</code></div><div class="desc">Se o Score não responde em 800ms, conta como falha.</div><span class="pl-chip"><span class="pl-tag limite">warn</span></span></div></div><div class="pl-step"><div class="num">2</div><div><div class="name">Breaker <code>breaker.call()</code></div><div class="desc">Se falhas > 5 em 10s → estado <code>OPEN</code>.</div><span class="pl-chip"><span class="pl-tag abre">warn</span></span></div></div><div class="pl-step"><div class="num">3</div><div><div class="name">Fallback <code>score_cache()</code></div><div class="desc">No <code>OPEN</code>, devolve score em cache / default.</div><span class="pl-chip"><span class="pl-tag fallback">ok</span></span></div></div><div class="pl-step"><div class="num">4</div><div><div class="name">Half-open <code>breaker.test()</code></div><div class="desc">Após 30s, libera 1 chamada de teste.</div><span class="pl-chip"><span class="pl-tag sonda">audit</span></span></div></div><div class="pl-step"><div class="num">5</div><div><div class="name">Retry <code>backoff(jitter)</code></div><div class="desc">No <code>CLOSED</code>, retenta com 0.1→0.4s + ruído.</div><span class="pl-chip"><span class="pl-tag backoff">ok</span></span></div></div></div><div class="pl-footer"><span>Serviço cai → fallback em ms; sobe → half-open valida e reabre o fluxo sem cascata.</span></div></div></div>

<h2><span class="num">5.</span> Antes vs Depois</h2>

<table><tr><th>Cenário</th><th>Antes (sem breaker)</th><th>Depois (circuit breaker)</th></tr><tr><td>Score lento</td><td>Pagamento trava</td><td>Fallback em <1s</td></tr><tr><td>Falha em cascata</td><td>Toda a cadeia</td><td>Isolada no Score</td></tr><tr><td>Retry</td><td>Imediato (piora)</td><td>Backoff + jitter</td></tr><tr><td>Recuperação</td><td>Manual</td><td>Half-open automático</td></tr></table>

<h2><span class="num">6.</span> Entregas</h2>

<ul><li><strong>Classe</strong> <code>circuit_breaker.py</code>: estados CLOSED/OPEN/HALF_OPEN.</li><li><strong>Decorator</strong> <code>@resilient</code>: aplica timeout + retry + breaker.</li><li><strong>Fallback</strong> <code>score_fallback.py</code>: resposta de degradação graciosa.</li><li><strong>Teste</strong> <code>test_breaker.py</code>: simula queda e afirma abertura/fechamento.</li></ul>

<h2><span class="num">7.</span> Métricas</h2>

<div class="charts"><div class="chart-card"><div class="chart-title">Disponibilidade do Pagamento (%)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Disponibilidade do Pagamento (%)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,27 68,29 94,32 121,36 147,43 173,52 199,62 225,72 251,84 278,91 304,98 330,105" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="105" r="3.5" fill="#e6a800"/><polyline points="42,27 68,27 94,27 121,27 147,26 173,26 199,26 225,26 251,26 278,26 304,26 330,26" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div></div>

<div class="callout"><strong>Meta:</strong> 99,9% de disponibilidade do Pagamento mesmo quando o Score fica fora do ar por minutos, via fallback gracioso.</div>

<h2><span class="num">8.</span> Status final</h2>

<p><span class="status st-warn">NÃO publicado</span> — Desenvolvido e em homologação. Aguarda revisão antes de produção.</p>