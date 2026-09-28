# APIs Modulares de Missão Crítica (FastAPI) com Paginação, Cache e Rate Limiting

Arquitetura Full Stack

<h2><span class="num">1.</span> Contexto</h2>

<p>A API de pedidos da FV cresceu sem padrão: o endpoint /pedidos devolvia a lista inteira com LIMIT/OFFSET, o banco PostgreSQL sofria em páginas profundas e o mesmo JSON era recalculado dezenas de vezes por minuto. Quando o tráfego subiu, o endpoint virou gargalo e começou a derrubar o Postgres.</p>

<div class="didactic"><div class="didactic-title">Analogia do cardápio gigante</div>Imagine um restaurante que, para te mostrar a página 50 do cardápio, relê TODAS as 5.000 receitas desde a primeira. O garçom (banco) cansa. A paginação por cursor é pedir: 'me traga o que vem DEPOIS do prato X': o garçom vai direto lá, sem reler tudo. E se 100 clientes pedem o mesmo prato popular? O cache é a foto do prato no balcão: ninguém precisa ir à cozinha de novo.</div>

<h2><span class="num">2.</span> Diagnóstico</h2>

<p>Com OFFSET grande, o Postgres varre e descarta milhares de linhas antes de devolver 20. Sem cache, consultas idênticas martelam o banco. Sem limite de taxa, um único cliente (ou bot) derruba a operação para todos.</p>

<div class="charts"><div class="chart-card"><div class="chart-title">Latência p95 do endpoint /pedidos (ms)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Latência p95 do endpoint /pedidos (ms)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,157 68,155 94,152 121,147 147,139 173,130 199,112 225,99 251,84 278,70 304,48 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,157 68,157 94,157 121,158 147,158 173,158 199,158 225,158 251,159 278,159 304,159 330,159" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="159" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div><div class="chart-card"><div class="chart-title">Consultas PostgreSQL repetidas/min</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Consultas PostgreSQL repetidas/min"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,119 68,116 94,109 121,99 147,89 173,82 199,68 225,58 251,51 278,45 304,34 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,119 68,140 94,150 121,155 147,158 173,161 199,162 225,163 251,164 278,164 304,165 330,165" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="165" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div></div>

<div class="callout"><strong>Raiz do problema:</strong> paginação deslocada (offset) + ausência de cache de leitura + nenhum limite de taxa. O custo de CPU do banco escala com o número de páginas e com a repetição de consultas idênticas.</div>

<h2><span class="num">3.</span> Solução</h2>

<p>Reescrever o endpoint com <strong>cursor pagination</strong> (ordenado por (created_at, id)), colocar um <strong>cache Redis</strong> na resposta (TTL curto, invalidado por escrita) e proteger a rota com <strong>rate limiting</strong> por cliente via token no Redis. O Postgres só é tocado quando o cache erra.</p>

<div class="didactic"><div class="didactic-title">Por que o par (created_at, id) e não só a data</div>Se a ordenação usa apenas <code>created_at</code>, duas linhas criadas no mesmo segundo empatam. O banco pode devolver essas duas linhas em ordem diferente entre uma chamada e outra, e aí uma delas aparece duas vezes na varredura ou some do meio dela. Acrescentar o <code>id</code> como segundo campo transforma a ordenação em algo único para cada linha: nenhuma posição ambígua, nenhuma omissão silenciosa. É a diferença entre um teste de varredura que passa hoje e um consumidor que reclama de dado faltante no mês que vem.</div>

<p>O encadeamento importa tanto quanto o algoritmo. A requisição passa primeiro pela identidade do chamador, depois pelo balde de tokens no Redis, depois pela chave de cache, e só então pelo banco. Cada portão é mais barato que o seguinte, então a rejeição acontece antes de qualquer trabalho caro. Inverter a ordem (cache antes do rate limit) faria um cliente abusivo consumir CPU e rede montando chaves e lendo Redis antes de ser barrado, o que entrega exatamente a proteção contrária à pretendida.</p>

<p>O cursor devolvido é opaco: o cliente não interpreta, não calcula offset, apenas repassa o valor recebido. Isso preserva a liberdade de trocar a chave de ordenação num dia futuro sem quebrar consumidor. Como consequência, cursor manipulado é rejeitado com <code>422</code> antes de qualquer consulta, o que também bloqueia tentativa de injeção de valor arbitrário no <code>WHERE</code>.</p>

<h2><span class="num">4.</span> Como funciona (pipeline)</h2>

<div class="pipeline"><div class="pipeline-head"><span class="pipeline-title">Fluxo de leitura paginada com cache e rate limit</span><span class="pipeline-live"><span class="dot"></span> fluxo em execução</span></div><div class="pipeline-body"><div class="pl-rail"><span class="pl-pulse p1"></span><span class="pl-pulse p2"></span><span class="pl-pulse g"></span></div><div class="pl-steps"><div class="pl-step"><div class="num">1</div><div><div class="name">Validação de token + rate limit</div><div class="desc">Middleware checa o bucket do cliente no Redis; se estourou o limite, responde 429.</div><span class="pl-chip"><span class="pl-tag rate limit ativo">ok</span></span></div></div><div class="pl-step"><div class="num">2</div><div><div class="name">Cálculo da chave de cache</div><div class="desc">Monta a chave pedidos:{cliente}:{cursor}:{size} a partir dos parâmetros.</div><span class="pl-chip"><span class="pl-tag cursor vazio = pag 1">warn</span></span></div></div><div class="pl-step"><div class="num">3</div><div><div class="name">Leitura do Redis</div><div class="desc">Se a chave existe (hit), devolve o JSON em ~1ms sem tocar o banco.</div><span class="pl-chip"><span class="pl-tag cache hit">ok</span></span></div></div><div class="pl-step"><div class="num">4</div><div><div class="name">Query cursor no Postgres</div><div class="desc">No miss, executa WHERE (created_at,id) > (?,?) ORDER BY created_at,id LIMIT ?.</div><span class="pl-chip"><span class="pl-tag índice composto">audit</span></span></div></div><div class="pl-step"><div class="num">5</div><div><div class="name">Grava cache + responde</div><div class="desc">Salva a resposta no Redis com EX 30 e devolve com o próximo cursor.</div><span class="pl-chip"><span class="pl-tag TTL 30s">ok</span></span></div></div></div><div class="pl-footer"><span>Escrita em /pedidos faz DEL pedidos:{cliente}:* para invalidar o cache daquele cliente (evita resposta stale).</span></div></div></div>

<h2><span class="num">5.</span> Antes vs Depois</h2>

<table><tr><th>Cenário</th><th>Antes (offset)</th><th>Depois (cursor+cache)</th></tr><tr><td>Página 1000</td><td>Varre 20k linhas</td><td>Seek direto no índice</td></tr><tr><td>Leitura repetida</td><td>Bate no banco sempre</td><td>Hit em Redis (~1ms)</td></tr><tr><td>Abuso de API</td><td>Sem proteção</td><td>429 após limite</td></tr><tr><td>Carga no Postgres</td><td>Alta e desnecessária</td><td>Só em cache miss</td></tr></table>

<h2><span class="num">6.</span> Entregas</h2>

<ul><li><strong>Endpoint</strong> GET /pedidos com cursor pagination e schema Pydantic de resposta.</li><li><strong>Middleware</strong> rate_limit.py: token bucket no Redis por cliente.</li><li><strong>Cache layer</strong> cache.py: get/set com invalidação por escrita.</li><li><strong>Migration</strong> 002_cursor_idx.sql: índice composto (created_at, id).</li><li><strong>Testes</strong> test_pagination.py: cobre primeira/última página e cache hit/miss.</li></ul>

<p>Além dos cinco artefatos, o padrão fica registrado no <strong>API-STANDARD.md</strong>, que é o documento que o próximo time usa ao criar uma listagem nova. Sem ele, a implementação vira conhecimento de uma pessoa; com ele, vira regra de revisão. O critério de aceite de cada entrega está no plano de teste: varredura completa contando itens, página profunda com <code>EXPLAIN (ANALYZE, BUFFERS)</code>, par de chamadas mostrando <code>MISS</code> e depois <code>HIT</code>, 101 requisições produzindo exatamente um <code>429</code>, e a lista respondendo <code>200</code> com o Redis desligado.</p>

<h2><span class="num">7.</span> Métricas</h2>

<div class="charts"><div class="chart-card"><div class="chart-title">Cache hit rate (%)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cache hit rate (%)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,170 68,142 94,120 121,100 147,80 173,66 199,57 225,48 251,40 278,34 304,29 330,26" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S1</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S2</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S3</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S4</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S5</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S6</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S7</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S8</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S9</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S10</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S11</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">S12</text><text x="46" y="12" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Mês 1</text></svg></div></div>

<div class="callout"><strong>Meta:</strong> p95 de /pedidos abaixo de 120ms e >90% de cache hit, com zero incidente de sobrecarga no Postgres.</div>

<h2><span class="num">8.</span> Matemática e capacidade</h2>

<p>Três contas sustentam a decisão. A primeira é o custo da página profunda: <code>linhas_offset = N × L + L</code> contra <code>linhas_cursor = L + 1</code>. <strong>Exemplo numérico:</strong> página de índice 1.000 com <code>L = 50</code> e linhas de 200 bytes dão <code>1000 × 50 + 50 = 50.050</code> linhas lidas no modelo antigo (cerca de 10,0 MB) contra 51 linhas no modelo novo (cerca de 10,2 KB), um fator de <code>50.050 / 51 = 981</code> vezes menos leitura.</p>

<p>A segunda é a carga residual no banco: <code>λ_banco = λ × (1 - H)</code>, em que <code>λ</code> é a taxa de requisições e <code>H</code> a taxa de acerto do cache. <strong>Exemplo numérico:</strong> com <code>λ = 200 req/s</code> e <code>H = 0,92</code> (meta), <code>200 × 0,08 = 16 req/s</code> chegam ao Postgres. Mesmo que o Redis caia e <code>H</code> vá a zero, o teto continua em 200 req/s, que é exatamente o patamar para o qual pool e rate limit foram dimensionados.</p>

<p>A terceira é o tempo de recarga do balde: <code>tokens = min(B, tokens + ⌊Δs × r / 60⌋)</code>. <strong>Exemplo numérico:</strong> com <code>B = 100</code> e <code>r = 100/min</code>, um cliente que gasta tudo em 12 segundos e espera 60 segundos recebe <code>⌊48 × 100 / 60⌋ = 80</code> tokens de volta. O <code>Retry-After</code> devolvido é o tempo real de recarga de um token, e não um número fixo, então o retry do consumidor volta no instante em que já existe orçamento.</p>

<p>Capacidade de conexão sai da mesma conta: <code>conexões = λ_banco × t_consulta</code>. <strong>Exemplo numérico:</strong> <code>16 req/s × 0,025 s = 0,4</code> conexão em uso médio, ou 2 conexões com fator de pico de 5×. O pool é fixado em 10, sobrando folga para manter <code>max_connections</code> do Postgres confortável mesmo com outras aplicações conectadas.</p>

<h2><span class="num">9.</span> Modos de falha e runbook</h2>

<table><tr><th>Sintoma</th><th>Causa raiz</th><th>Detecção</th><th>Mitigação</th><th>Recuperação</th></tr>
<tr><td>500 em massa nas listas</td><td>pool de conexões esgotado</td><td>gauge do pool no teto, log de conexão recusada</td><td>reduzir pool, cortar varredura, rate limit</td><td>minutos</td></tr>
<tr><td>p95 dispara sem troca de tráfego</td><td>índice perdido em migração</td><td><code>EXPLAIN</code> com seq scan</td><td><code>CREATE INDEX CONCURRENTLY</code> + <code>ANALYZE</code></td><td>5 a 15 min</td></tr>
<tr><td>429 em massa</td><td>quota mal calibrada ou cliente sem backoff</td><td>proporção de 429 acima de 2%</td><td>auditar o consumidor antes de subir quota</td><td>imediato / horas</td></tr>
<tr><td>Redis fora</td><td>rede, memória ou failover</td><td>health check e <code>redis_up = 0</code></td><td>fallback banco + flag do balde local</td><td>até o Redis voltar</td></tr>
<tr><td>Dado antigo em tela</td><td>invalidação não disparou no caminho de escrita</td><td>teste de integração gravar e reler</td><td><code>DEL</code> do prefixo e correção do caminho</td><td>segundos</td></tr>
<tr><td>Item pulado ou repetido</td><td>ordenação sem desempate</td><td>varredura completa contando <code>id</code></td><td>ordenar por <code>(created_at, id)</code></td><td>minutos</td></tr></table>

<div class="callout"><strong>Regra de plantão:</strong> às três da manhã não se sobe quota às cegas. Isso transfere o problema do 429 para o banco, que é o único recurso da lista que não se recupera sozinho. Primeiro identifica qual dos quatro sintomas está ativo no painel, depois aplica a mitigação correspondente.</div>

<h2><span class="num">10.</span> Decisões e alternativas descartadas</h2>

<table><tr><th>Alternativa</th><th>Por que ficou de fora</th></tr>
<tr><td>OFFSET com índice parcial</td><td>o índice corta o custo de ordenar, não o custo de ler e descartar as linhas anteriores à página</td></tr>
<tr><td>Cache em memória local por processo</td><td>em várias réplicas cada uma teria seu próprio cache, com invalidação que não se propaga, e resposta diferente conforme a instância atingida</td></tr>
<tr><td>Só <code>Cache-Control</code> no proxy</td><td>protege quem obedece ao header, não elimina o cálculo no servidor nem centraliza a invalidação por escrita</td></tr>
<tr><td>Rate limit por IP</td><td>atrás de NAT e proxy todos os clientes internos parecem a mesma origem e um puniria os outros</td></tr>
<tr><td>Paginação por número de página</td><td>por baixo continua sendo offset, é instável sob inserção e obriga a refazer a ordenação a cada chamada</td></tr>
<tr><td>Particionamento por tempo</td><td>resolve varredura por janela, mas introduz retenção e manutenção de partição num volume de 80k linhas, pequeno demais para justificar</td></tr>
<tr><td>Invalidação global por recurso</td><td>derruba o cache de todos os clientes a cada escrita e zera a taxa de acerto no pico de gravação</td></tr></table>

<p>A matriz de trade-offs que acompanha a decisão: cursor ganha custo estável e perde o salto direto para a página N; TTL de 30 segundos ganha dado fresco e perde taxa de acerto frente a um TTL de 5 minutos; rate limit por chave ganha isolamento e perde conforto em pico legítimo; fallback ao banco ganha disponibilidade e perde p95 no pior caso. Cada perda foi aceita explicitamente, com o motivo registrado, o que é o que separa decisão de acidente.</p>

<h2><span class="num">11.</span> Segurança e observabilidade</h2>

<p><strong>Segurança.</strong> A chave de cache sempre carrega o prefixo do <code>api_key</code>, então dois clientes nunca dividem a mesma entrada, mesmo com a mesma listagem; filtro de permissão diferente com cache compartilhado seria vazamento de dado entre contas. O cursor é validado antes de tocar o banco, o que rejeita valor arbitrário no <code>WHERE</code>. Nenhuma resposta devolve stack trace, caminho de arquivo ou SQL: exceção vira <code>code</code> genérico no envelope e detalhe completo só no log estruturado, amarrado pelo mesmo <code>trace_id</code> que foi devolvido ao cliente. Identidade de alto volume (<code>api_key</code>, <code>cursor</code>, <code>trace_id</code>) nunca vira label de métrica, porque a cardinalidade ilimitada transformaria o coletor no novo gargalo: identidade vai para log, não para série temporal.</p>

<p><strong>Observabilidade.</strong> Seis métricas cobrem o sistema inteiro com cardinalidade baixa: duração de requisição (histograma por rota, método e cache), total de requisições por status, resultados do rate limit, resultados de cache por recurso, uso do pool e estado do Redis. Delas saem os SLIs do SLO: disponibilidade em 30 dias móveis, p95 do hit em 5 minutos rolantes, taxa de acerto em 15 minutos e proporção de 429 em 15 minutos. Alertas: p95 acima de 200 ms por 10 minutos, 5xx acima de 1% por 5 minutos, 429 acima de 5% por 15 minutos, hit rate abaixo de 70% por 15 minutos, <code>redis_up = 0</code> por 1 minuto.</p>

<div class="callout"><strong>Orçamento de erro:</strong> 99,5% em 30 dias dá <code>0,005 × 30 × 24 × 60 = 216</code> minutos de indisponibilidade. Um corte de 15 minutos consome 6,9% do mês. Se o consumo passar de 50% na metade do mês, congela-se toda mudança não corretiva na API: isso impede a morte por mil cortes de 90 segundos.</div>

<h2><span class="num">12.</span> Checklist de domínio</h2>

<ol>
<li>Nenhum <code>SELECT</code> de listagem com <code>OFFSET</code> acima de 10k aparece no código nem em migração.</li>
<li>Todo endpoint tem <code>limit</code> com teto servidor-side, menor ou igual a 200.</li>
<li>A ordenação é pelo par estável <code>(created_at, id)</code> e existe índice cobrindo essa ordem.</li>
<li><code>EXPLAIN (ANALYZE, BUFFERS)</code> da página profunda mostra busca no índice, sem seq scan.</li>
<li>Toda chave de cache começa com o prefixo do cliente; nenhum dado cru cruza contas.</li>
<li>Toda escrita no recurso invalida o prefixo depois do commit, nunca antes.</li>
<li>O rate limit está antes do cache e usa o Redis como fonte única entre instâncias.</li>
<li>O <code>429</code> existe por chave e carrega <code>Retry-After</code> real.</li>
<li>Todo erro 5xx tem <code>trace_id</code> igual ao do log estruturado.</li>
<li>O pool de conexões é único e de tamanho fixo, sem criação por requisição.</li>
<li>Desligar o Redis não derruba nenhum teste de caminho feliz da listagem.</li>
<li>Existe teste de varredura completa que conta itens e garante zero duplicidade.</li>
<li>Métricas sem <code>api_key</code>, <code>cursor</code> ou <code>trace_id</code> como label.</li>
<li>Runbook cobre pool esgotado, índice perdido, Redis fora e 429 em massa, com quem aciona.</li>
<li>As metas de SLO têm janela de medição e alarme configurado, não só texto no documento.</li>
</ol>

<h2><span class="num">13.</span> Status final</h2>

<p><span class="status st-warn">NÃO publicado</span>: Desenvolvido e em homologação. Aguarda revisão antes de produção.</p>