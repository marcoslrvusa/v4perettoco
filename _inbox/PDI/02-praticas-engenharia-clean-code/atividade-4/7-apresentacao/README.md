# Estudo de Design Patterns aplicados ao ecossistema

Engenharia de Software

<h2><span class="num">1.</span> Contexto</h2><p>A FV precisa plugar fornecedores diferentes (meios de pagamento, transportadoras, gateways de SMS) sem reescrever o core a cada contratação. O código legado tinha um <code>if fornecedor == 'X'</code> para cada integração, e o time temia qualquer onboarding de parceiro novo. A <strong>flexibilidade</strong> era paga em complexidade.</p><div class="didactic"><div class="didactic-title">Analogia dos adaptadores de tomada</div>Viajar pelo mundo é fácil porque existem <strong>adaptadores de tomada</strong>: o seu carregador (core) não muda, só o pedacinho que encaixa na pareda (fornecedor) muda. <em>Strategy</em> é escolher o melhor caminho sem mudar o destino; <em>Observer</em> é o painel que avisa todo mundo quando algo acontece. Padrões são esses 'encaixes' reutilizáveis.</div><h2><span class="num">2.</span> Diagnóstico</h2><p>Com lógica de integração espalhada em condicionais, o tempo de onboarding de fornecedor cresce e cada novo parceiro duplica pontos de falha. O core se polui com detalhes de terceiros e fica mais difícil de testar.</p><div class="charts"><div class="chart-card"><div class="chart-title">Tempo de onboarding de fornecedor (dias)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tempo de onboarding de fornecedor (dias)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,118 68,112 94,107 121,99 147,91 173,84 199,76 225,65 251,57 278,47 304,39 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,118 68,139 94,146 121,152 147,154 173,157 199,160 225,160 251,162 278,162 304,162 330,165" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="165" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div><div class="chart-card"><div class="chart-title">Pontos de falha por integração (nº)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pontos de falha por integração (nº)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,129 68,122 94,115 121,108 147,95 173,88 199,81 225,67 251,60 278,47 304,40 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><polyline points="42,129 68,143 94,149 121,149 147,156 173,156 199,156 225,163 251,163 278,163 304,163 330,163" fill="none" stroke="#52d69b" stroke-width="2.5"/><circle cx="330" cy="163" r="3.5" fill="#52d69b"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jan</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Fev</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mar</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Abr</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Mai</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jun</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Jul</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Ago</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Set</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Out</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Nov</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">Dez</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Antes</text><text x="46" y="24" fill="#52d69b" font-size="10" font-family="JetBrains Mono">Depois</text></svg></div></div><div class="callout"><strong>Raiz do problema:</strong> o core conhece os detalhes de cada fornecedor. Falta uma <em>camada de indireção</em> que isole variação atrás de uma interface estável.</div><h2><span class="num">3.</span> Solução</h2><p>Aplicar três <strong>Design Patterns</strong> na FV: <strong>Adapter</strong> (traduz a API de terceiro para a interface do core: ports/adapters), <strong>Strategy</strong> (seleciona em runtime o algoritmo/fornecedor ideal) e <strong>Observer</strong> (notifica partes interessadas quando um evento de domínio ocorre, sem acoplar).</p><p><strong>Adapter</strong>: o core fala uma língua só:</p><pre><code># port do core
class GatewayPagamento:
    def cobrar(self, valor: float) -&gt; str: ...

# adapter traduz o PayPal para o port
class PayPalAdapter(GatewayPagamento):
    def cobrar(self, valor):
        return api_paypal.charge(amount=valor)  # detalhe isolado</code></pre><p><strong>Strategy</strong>: escolhe o melhor frete em runtime:</p><pre><code>class FreteStrategy:
    def calcular(self, pedido): raise NotImplementedError
class FreteExpresso(FreteStrategy):
    def calcular(self, p): return p.peso * 2.0
class FreteEconomico(FreteStrategy):
    def calcular(self, p): return p.peso * 0.8

def selecionar(pedido) -&gt; FreteStrategy:   # Strategy factory
    return FreteExpresso() if pedido.urgente else FreteEconomico()</code></pre><p><strong>Observer</strong>: o core avisa, os interessados reagem:</p><pre><code>class Observador:  # Observer
    def ao_pedido_pago(self, ev): ...
class NotificaCliente(Observador):
    def ao_pedido_pago(self, ev): email.enviar(ev.pedido_id)
class AtualizaEstoque(Observador):
    def ao_pedido_pago(self, ev): estoque.debitar(ev.itens)

bus.assinar(PedidoPago, NotificaCliente())
bus.assinar(PedidoPago, AtualizaEstoque())</code></pre><h2><span class="num">4.</span> Como funciona (pipeline)</h2><div class="pipeline"><div class="pipeline-head"><span class="pipeline-title">Padrões na integração FV</span><span class="pipeline-live"><span class="dot"></span> fluxo em execução</span></div><div class="pipeline-body"><div class="pl-rail"><span class="pl-pulse p1"></span><span class="pl-pulse p2"></span><span class="pl-pulse g"></span></div><div class="pl-steps"><div class="pl-step"><div class="num">1</div><div><div class="name">Definir <code>ports</code> do core</div><div class="desc">Interfaces estáveis: GatewayPagamento, FreteStrategy, Observador.</div><span class="pl-chip"><span class="pl-tag 1">audit</span></span></div></div><div class="pl-step"><div class="num">2</div><div><div class="name">Adapter por fornecedor <code>PayPalAdapter</code></div><div class="desc">Cada terceiro vira um adapter que implementa o port.</div><span class="pl-chip"><span class="pl-tag isolado">ok</span></span></div></div><div class="pl-step"><div class="num">3</div><div><div class="name">Strategy factory <code>selecionar()</code></div><div class="desc">Em runtime escolhe a estratégia conforme o contexto do pedido.</div><span class="pl-chip"><span class="pl-tag troca veloz">ok</span></span></div></div><div class="pl-step"><div class="num">4</div><div><div class="name">Observer <code>bus.assinar()</code></div><div class="desc">Reações (e-mail, estoque) assinam eventos sem acoplar ao core.</div><span class="pl-chip"><span class="pl-tag ordem nao garantida">warn</span></span></div></div><div class="pl-step"><div class="num">5</div><div><div class="name">Testes com fakes</div><div class="desc">Port fake valida o core sem chamar fornecedor de verdade.</div><span class="pl-chip"><span class="pl-tag deterministico">ok</span></span></div></div></div><div class="pl-footer"><span>Novo fornecedor = novo adapter; o core sequer recompila.</span></div></div></div><h2><span class="num">5.</span> Antes vs Depois</h2><table><tr><th>Cenário</th><th>Antes (if/else)</th><th>Depois (padrões)</th></tr><tr><td>Novo fornecedor</td><td>Mexe no core todo</td><td>Só adapter novo</td></tr><tr><td>Trocar frete</td><td>Reescreve fluxo</td><td>Strategy em runtime</td></tr><tr><td>Avisar parceiro</td><td>Acopla no meio</td><td>Observer assina</td></tr><tr><td>Testar core</td><td>Precisa terceiro</td><td>Fake do port</td></tr></table><h2><span class="num">6.</span> Entregas</h2><ul><li><strong>Pacote</strong> <code>adapters/</code>: PayPalAdapter, StripeAdapter, CorreiosAdapter.</li><li><strong>Pacote</strong> <code>strategies/</code>: FreteExpresso, FreteEconomico + factory.</li><li><strong>Pacote</strong> <code>observers/</code>: NotificaCliente, AtualizaEstoque, EmiteNota.</li><li><strong>Exemplo</strong> <code>onboarding_fornecedor.md</code>: como plugar um novo adapter.</li></ul><h2><span class="num">7.</span> Métricas</h2><div class="charts"><div class="chart-card"><div class="chart-title">Velocidade de plugar fornecedor (fornecedores/mês)</div><svg viewBox="0 0 360 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Velocidade de plugar fornecedor (fornecedores/mês)"><line x1="42" y1="170" x2="330" y2="170" stroke="#c8d0d8"/><line x1="42" y1="170" x2="42" y2="26" stroke="#c8d0d8"/><polyline points="42,170 68,157 94,144 121,131 147,118 173,105 199,91 225,78 251,65 278,52 304,39 330,26" fill="none" stroke="#e6a800" stroke-width="2.5"/><circle cx="330" cy="26" r="3.5" fill="#e6a800"/><text x="42" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T1</text><text x="68" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T2</text><text x="94" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T3</text><text x="121" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T4</text><text x="147" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T5</text><text x="173" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T6</text><text x="199" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T7</text><text x="225" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T8</text><text x="251" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T9</text><text x="278" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T10</text><text x="304" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T11</text><text x="330" y="184" fill="#8896a8" font-size="9" text-anchor="middle">T12</text><text x="46" y="12" fill="#e6a800" font-size="10" font-family="JetBrains Mono">Trimestre 1</text></svg></div></div><div class="callout"><strong>Meta:</strong> onboarding de novo fornecedor em <em>≤ 2 dias</em>, atrás de adapter testado, sem tocar no core.</div><h2><span class="num">8.</span> Status final</h2><p><span class="status st-warn">NÃO publicado</span>: Desenvolvido e em homologação. Aguarda revisão antes de produção.</p>

## Apêndice técnico do relatório

O corpo do relatório acima é o que vai ao público da apresentação. Este apêndice é o material de
sustentação para a defesa: modelo mental, matemática fechada, invariantes, modos de falha com
runbook, decisões descartadas e checklist de domínio. Nada aqui é novo em relação ao relatório;
é o mesmo raciocínio em formato auditável.

### A. Modelo mental

O sistema se comporta como uma estação de tradução. O núcleo fala um único idioma, definido pelas
ports `GatewayPagamento`, `CrmPort`, `FreteStrategy` e `Observador`. Todo fornecedor externo chega
por um adapter que implementa a port e absorve a forma estranha do terceiro: nome de campo, moeda,
formato de erro, semântica de idempotência. O núcleo nunca enxerga o formato externo e por isso
nunca precisa ser reescrito quando o terceiro muda.

A variação de algoritmo sai da cadeia condicional e vira objeto escolhido em tempo de execução por
uma factory. A factory é o único lugar que conhece a regra de escolha; as estratégias conhecem
apenas o próprio cálculo. A reação a um fato de domínio é publicada em um bus simples: os
interessados assinam e reagem sem o núcleo saber quem está ouvindo. O preço dessa liberdade é
declarado de forma explícita: ordem entre observadores não é garantida, e falha em um observador
não pode derrubar o emissor.

A disciplina que impede a degeneração do desenho é uma frase só: sem variação real, não há padrão
a aplicar. Padrão aplicado onde nada varia é complexidade antecipada, paga em leitura e em
manutenção, sem retorno.

### B. Matemática da solução

Sejam $F$ fornecedores, $C$ módulos do núcleo que ramificam por fornecedor e $A$ algoritmos
alternativos. A abordagem por condicional exige $F \times C$ ramificações vivas; a abordagem por
ports e adapters exige $F + C$ pontos de toque.

**Exemplo numérico:** $F = 6$, $C = 4$ e $A = 3$. Condicionais: $6 \times 4 = 24$ ramificações.
Ports e adapters: $6 + 4 = 10$ pontos de toque. Redução de $(24 - 10) / 24 = 58,3$ por cento. No
eixo dos algoritmos, a contagem vai de $M \times A = 4 \times 3 = 12$ acoplamentos para 3
estratégias mais 1 factory, ou seja, 4 pontos. O crescimento passa de multiplicativo para linear.

Probabilidade de erro por mudança: com chance $p$ de erro independente por ponto tocado,
$P = 1 - (1 - p)^{k}$. **Exemplo numérico:** com $p = 0,15$ e $k = 6$, $P = 1 - 0,85^{6} = 1 -
0,377 = 0,623$, ou 62,3 por cento; com $k = 1$, $P = 0,15$. A razão $0,623 / 0,15 = 4,2$ vezes
mostra quanto o desenho reduz a exposição a erro no mesmo trabalho de onboarding.

Custo de oportunidade: $CustoAnual = N \times \Delta d \times C_{dia}$. **Exemplo numérico:** com
$N = 4$ fornecedores por ano, $\Delta d = 10$ dias por fornecedor e $C_{dia} = \text{R\$ } 350$
por dia-dev, o total é $4 \times 10 \times 350 = \text{R\$ } 14.000$ por ano (meta de ganho,
com parâmetros de exercício, não medição). Contra um piloto de 30 horas, o payback se dá no
primeiro fornecedor do ano.

### C. Invariantes

| Invariante | Se violar, acontece |
| --- | --- |
| O núcleo nunca importa SDK de terceiro | qualquer mudança externa força deploy do núcleo |
| Toda variação de fornecedor vive atrás de port nomeada | cadeia condicional nova escapa da revisão |
| A factory é o único ponto com regra de escolha | seleção duplicada e divergência silenciosa |
| Observador falho não propaga erro ao emissor | falha de e-mail cancela confirmação de pedido |
| Ordem entre observadores nunca é pressuposto | estado divergente entre estoque e notificação |
| Adapter traduz erro de terceiro para erro de domínio | mensagem e código externos vazam para o log interno |
| Sem singleton de cliente, tudo por injeção | estado global e teste dependente de ordem |
| Todo port tem fake em teste | suíte depende de credencial e não roda em pull request |

### D. Modos de falha e runbook

| Sintome | Causa raiz | Detecção | Mitigação | Recuperação |
| --- | --- | --- | --- | --- |
| Erro 500 no webhook | exceção bruta do SDK dentro do adapter | taxa de erro por rota e classe de exceção | mapear para erro de domínio tipado | retry com backoff na borda de entrada |
| Mensagem de e-mail duplicada | reprocessamento sem chave de idempotência | contador de duplicatas por chave | idempotência no consumidor | deduplicação em janela |
| Estoque divergente | observador parado ou fora de ordem | reconciliação diária evento contra saldo | fila durável por observador | reprocessar o evento pendente |
| Núcleo degradado | terceiro lento sem timeout no caminho crítico | p95 e timeout por adapter | timeout curto, circuit breaker e fallback | desligar fornecedor por feature flag |
| Estratégia errada | cadeia residual fora da factory | teste de tabela e log da escolha | mover regra para a factory | correção pontual, sem tocar estratégias |
| Teste que só passa com credencial | fake ausente para a port | execução da suíte em PR sem ambiente | criar fake do contrato | bloquear merge até o fake existir |

Runbook resumido: checar taxa de erro e p95 por adapter, localizar o fornecedor degradado,
aplicar circuit breaker e fallback, acionar o responsável pelo módulo de integração, escalar para
a coordenação quando a janela passar de 30 minutos (meta). Rollback é feito por feature flag, não
por deploy reverso. Depois do fato, postmortem sem culpa em até 2 dias úteis, com ação rastreável
e dono, alimentando a tabela acima.

### E. Decisões e alternativas descartadas

| Alternativa | Por que foi descartada |
| --- | --- |
| Herança de um cliente base com métodos sobrescritos | hierarquia rígida, troca exige recompilação e a árvore de tipos acopla as variantes entre si |
| Dicionário de configuração que mapeia fornecedor por string | troca o `if` por um dicionário opaco, sem contrato e com erro só em tempo de execução |
| Biblioteca de integração de terceiro pronta | mais uma dependência no caminho crítico, sem resolver o modelo interno nem o teste com fake |
| Singleton de cliente para economizar instanciação | estado global oculto, teste dependente de ordem e vazamento de segredo entre módulos |
| Broker de mensagens desde o piloto | infra nova antes de provar o desacoplamento de código; ordem e durabilidade entram com ADR próprio |
| Teste ponta a ponta como única rede de segurança | lento, frágil e exige sandbox, então não roda em pull request |

### F. Telemetria e observabilidade

Métricas por fronteira, com cardinalidade fixa e revisada junto com o ADR:
`integracao.chamadas_total{adapter}`, `integracao.erros_total{adapter,classe}`,
`integracao.latencia_p95_ms{adapter}`, `estrategia.escolhas_total{estrategia}`,
`evento.emitido_total{tipo}`, `evento.processado_total{tipo}` e `evento.duplicado_total{tipo}`.

Proibido usar identificador de pedido, de lead ou de usuário como rótulo: cardinalidade sem
controle transforma painel útil em custo de armazenamento. Alertas sugeridos: erro do núcleo
causado por terceiro acima de 1 por cento em 15 minutos (meta), p95 de adapter acima de 800 ms
por 10 minutos (meta), consumidor parado enquanto o contador de eventos emitidos sobe, e estratégia sem seleção por
30 dias, sinal de código morto.

Segurança: segredos de terceiro nunca aparecem em log nem em mensagem de erro exposta; toda
chamada de rede do núcleo tem timeout explícito; e a checagem de assinatura de webhook acontece
na borda, antes do núcleo, para que payload inválido jamais alcance a regra de negócio.

### G. Checklist de domínio

- [ ] Toda dependência de terceiro vive atrás de port, sem import de SDK no núcleo.
- [ ] Toda cadeia condicional de escolha está na factory, com teste de tabela.
- [ ] Todo observador isola erro e nenhuma regra depende da ordem de assinatura.
- [ ] Todo adapter traduz erro de terceiro para erro de domínio tipado.
- [ ] Existe timeout explícito em toda chamada de rede do núcleo.
- [ ] Os ports têm fake e a suíte roda em pull request sem credencial e sem rede.
- [ ] Nenhum singleton de cliente foi introduzido; tudo entra por injeção de dependência.
- [ ] Todo command tem chave de idempotência e registro de execução.
- [ ] A telemetria correspondente foi criada junto com o padrão, com cardinalidade fixa.
- [ ] O runbook tem dono, canal de acionamento e janela de escalonamento.
- [ ] O pull request nomeia o padrão aplicado e a variação que ele absorve.
- [ ] As consequências negativas do ADR-024 foram lidas em voz alta na revisão.
- [ ] A métrica de onboarding tem instrumento definido antes de a meta ser prometida.
- [ ] Nenhum padrão foi aplicado onde não existia variação real.