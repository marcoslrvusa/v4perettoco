# Design Patterns: Notas (Python/JS)

Standard de adesão do estudo de Design Patterns para o ecossistema. Este documento é a fonte
canônica do vocabulário de revisão: se o termo não está aqui, não deve aparecer no comentário de
pull request como justificativa de design.

## Quando usar

- **Adapter**: sempre que chamar API de terceiro.
- **Strategy**: variação de algoritmo (modelo de LLM por custo).
- **Observer**: reagir a eventos sem acoplar.
- **Command**: ações de agente re-jogaveis.
- **Singleton**: NÃO. Use DI.

```python
class Cheap:  def complete(self, p): ...
class Smart:  def complete(self, p): ...
def model_for(task): return Smart() if task.get("hard") else Cheap()
```

## 1. Escopo e não-escopo

**Escopo deste standard:**

- Padrões estruturais aplicados a integração (Adapter) e a composição de serviços (Facade).
- Padrões comportamentais aplicados a seleção em runtime (Strategy), notificação de domínio
  (Observer) e empacotamento de ação reprocessável (Command).
- Regras de aceite, telemetria e checklist que o revisor usa para dizer sim ou não em PR.
- A regra de contenção: padrão só entra onde existe variação real e demonstrável.

**Não-escopo deste standard:**

- Padrões criacionais além do mínimo necessário para factory de estratégias (Abstract Factory e
  Builder ficam de fora até existir um caso de uso com mais de uma família de objetos).
- Frameworks de injeção de dependência pesados: o padrão aqui é composição simples na raiz da
  aplicação, não container com anotação e reflexão.
- Padrões de arquitetura de nível de sistema (event sourcing, CQRS), que vivem em outro standard.
- Reescrita de módulos que não têm variação: neste caso o padrão é não aplicar padrão.

## 2. Termos

| Termo | Definição operacional no ecossistema |
| --- | --- |
| Port | Contrato em formato de interface ou `Protocol` que o núcleo usa para falar com o lado de fora. Exemplos: `CrmPort`, `GatewayPagamento`, `FreteStrategy`. |
| Adapter | Implementação concreta de uma port que traduz o formato do terceiro para o formato interno, inclusive erro, moeda e idempotência. |
| Strategy | Objeto que encapsula um algoritmo variável e é trocado em tempo de execução pela factory. |
| Factory | Único módulo autorizado a conter a regra de escolha entre estratégias. |
| Observer | Reagente que assina um evento de domínio e reage sem o emissor conhecer quem assinou. |
| Bus | Mecanismo mínimo de publicação e assinatura usado pelo núcleo. No piloto é in-memory e síncrono. |
| Fake | Implementação de port que satisfaz o contrato em teste sem rede, sem segredo e sem estado externo. |
| Variação real | Ponto do código que já mudou, está mudando ou está comprometido a mudar por decisão de produto. Sem variação real, não há padrão. |
| Vazamento de abstração | Detalhe de terceiro (campo, código de erro, SDK) aparecendo em código do núcleo. |

## 3. Regra canônica

A regra que governa todo o restante do documento:

> O núcleo de negócio depende apenas de ports. Toda variação de fornecedor, de algoritmo e de
> reação a evento vive atrás de uma dessas ports, de modo que o núcleo não precise ser reescrito
> quando a implementação muda.

Formalização: sejam $M$ módulos do núcleo que conversam com o lado de fora, $F$ fornecedores e
$A$ algoritmos alternativos. Sem indireção, o número de acoplamentos vivos é
$C_{acoplado} = M \times F + M \times A$. Com ports, adapters e estratégias, o número cai para
$C_{port} = M \times 1 + F + A$: cada módulo conversa com uma única abstração, e o crescimento
passa a ser linear em $F$ e $A$, não multiplicativo.

**Exemplo numérico:** com $M = 4$ módulos, $F = 6$ fornecedores e $A = 3$ algoritmos,
$C_{acoplado} = 4 \times 6 + 4 \times 3 = 24 + 12 = 36$ acoplamentos a manter, enquanto
$C_{port} = 4 + 6 + 3 = 13$. Redução de $(36 - 13) / 36 = 63,9$ por cento de pontos de impacto
por mudança. Os números são hipóteses de exercício, rotuladas como exemplo, e serão substituídos
pela contagem real dos módulos de integração quando o piloto fechar.

Regra prática derivada: para cada novo `if` que diferencia fornecedor ou modelo, o autor do PR
precisa nomear qual port, qual adapter e qual estratégia vão absorver essa variação. Se não
conseguir nomear, o `if` não entra.

## 4. Tabela de decisão

| Se | E | Então | Com exceção de |
| --- | --- | --- | --- |
| a assinatura do terceiro difere da nossa | a chamada é feita pelo núcleo | crie adapter atrás da port existente | o formato já é idêntico e estável há anos |
| o algoritmo muda por contexto | a escolha é decidida em runtime | crie strategy + factory | a escolha é fixa em compilação, use constante |
| uma ação precisa rodar de novo sem efeito colateral | há reprocessamento manual | crie command com idempotência | a ação é irreversível e auditada, exige fluxo humano |
| vários módulos reagem ao mesmo fato | nenhum reagente decide regra | crie observer assinando o bus | a reação precisa de ordem garantida, use fila com chave |
| é preciso uma instância única de configuração | o estado é imutável | passe por injeção de dependência na raiz | estado global mutável, proibido (não use singleton) |
| o teste precisa do terceiro | existe fake do contrato | use o fake em PR | o teste é de contrato, aí sim roda em janela com o terceiro |
| a cadeia de decisão tem mais de 3 ramos | os ramos diferem por regra de produto | mova tudo para a factory | ramo é acidente de implementação, elimine antes de modelar |
| o observador pode falhar sozinho | o emissor não pode ser afetado | isole o erro dentro do observador | o observador é crítico para o invariante, então vira fila durável |

## 5. Aplicação no código

Adapter: o núcleo fala uma língua só.

```python
from typing import Protocol

class CrmPort(Protocol):
    """Contrato que o núcleo conhece: gravar lead no CRM."""
    def upsert(self, lead: dict) -> None: ...

class HubSpotAdapter:
    """Traduz o contrato interno para a API do HubSpot."""
    def upsert(self, lead: dict) -> None:
        # aqui moram timeout, mapeamento de campo e tradução de erro
        ...
```

Strategy com factory: a escolha deixa de ser cadeia condicional espalhada.

```python
class Estrategia(Protocol):
    def estimar(self, pedido) -> float: ...

class FreteExpresso:
    def estimar(self, pedido): return pedido.peso * 2.0

class FreteEconomico:
    def estimar(self, pedido): return pedido.peso * 0.8

def selecionar(pedido) -> Estrategia:
    """Único ponto autorizado a conhecer a regra de escolha."""
    return FreteExpresso() if pedido.urgente else FreteEconomico()
```

Observer: o núcleo publica, os interessados reagem.

```python
bus.assinar("pedido.pago", NotificaCliente())
bus.assinar("pedido.pago", AtualizaEstoque())
# o núcleo só emite: bus.emitir("pedido.pago", evento)
```

Command: ação empacotada, re-jogável e auditável.

```python
class ReenviarLead:
    def __init__(self, crm: CrmPort, lead: dict):
        self.crm, self.lead = crm, lead
        self.chave = f"reenviar:{lead['id']}"

    def executar(self):
        if ja_processado(self.chave):   # idempotência
            return
        self.crm.upsert(self.lead)
        registrar(self.chave)
```

## 6. Exemplo numérico de esforço e retorno

**Exemplo numérico:** o piloto de Adapter consome 12 horas de desenvolvimento, o mesmo item do
plano de esforço do README da atividade. O retorno esperado é de 10 dias-dev economizados por
fornecedor (de 12 para 2 dias) em até 4 fornecedores por ano. Com valor hora de R$ 60 (parâmetro
declarado apenas para ensinar a conta), o custo do piloto é $12 \times 60 = \text{R\$ } 720$ e o retorno anual é $4 \times 10 \times 8 \times 60 = \text{R\$ } 19.200$, considerando 8 horas por dia-dev.
Payback no primeiro fornecedor do ano. Todos os números são hipótese de exercício; a medição real
começa no primeiro onboarding pós-piloto.

## 7. Anti-padrões

O que o revisor reprovaria imediatamente:

- **Adapter que é um alias do SDK**: método único que só repassa a chamada sem traduzir erro,
  formato ou idempotência. Isso não é adapter, é alias, e mantém o vazamento de abstração.
- **Strategy com um único implementador vivo**: criada "para o futuro" sem segundo algoritmo
  real. Complexidade antecipada sem retorno.
- **Factory que também executa negócio**: a factory escolhe; ela não calcula, não valida e não
  persiste.
- **Observer que decide**: observador alterando saldo, cobrando cartão ou alterando regra de
  preço. Reação sim, decisão não.
- **Bus síncrono usado como garantia de ordem**: escrever código que depende da ordem de
  assinatura no bus in-memory é guardar bug para o dia em que a ordem mudar.
- **Singleton de cliente**: estado global compartilhado, teste dependente de ordem e vazamento
  de credencial entre módulos. A alternativa é injeção de dependência na raiz.
- **Padrão no comentário, if no código**: citar Adapter no PR sem existir a port correspondente.
- **Herança para variar**: sobrescrever método de classe base para trocar comportamento. Troca em
  runtime não nasce de hierarquia, nasce de composição.
- **Teste que exige credencial**: qualquer teste de núcleo que precise de rede falha em PR e
  paralisa o gate de cobertura.
- **Tratamento de erro engolido**: `except Exception: pass` dentro de adapter ou observador.
  Toda exceção vira log com contexto e decisão explícita de retry, fallback ou descarte.

## 8. Telemetria

| Métrica | Cardinalidade | O que indica | Ação ao estourar |
| --- | --- | --- | --- |
| `integracao.chamadas_total{adapter}` | 1 por adapter (baixa) | volume por fornecedor | investigar pico e possível retry em loop |
| `integracao.erros_total{adapter,classe}` | adapter x classe de erro (controlada) | contrato quebrado ou fornecedor degradado | circuit breaker e chamado com o parceiro |
| `integracao.latencia_p95_ms{adapter}` | 1 por adapter | timeout mal dimensionado | revisar timeout e chamada síncrona no caminho crítico |
| `estrategia.escolhas_total{estrategia}` | 1 por estratégia | se a factory está equilibrada e se há estratégia morta | aposentar estratégia sem uso |
| `evento.emitido_total{tipo}` | 1 por tipo de evento | saúde do bus | verificar consumidor parado |
| `evento.processado_total{tipo,outro}` | tipo x origem (limitar a poucas origens) | observador falho | reprocessar e corrigir o consumidor |
| `evento.duplicado_total{tipo}` | 1 por tipo | semântica at-least-once se tornando problema | reforçar idempotência por chave |
| `adaptador.cobertura_ports` | 1 por port | rede de segurança do núcleo | bloquear merge no gate |

Regra de cardinalidade: nenhum rótulo aceita identificador de usuário, identificador de pedido ou
texto livre. Cardinalidade sem controle é a forma mais comum de transformar um painel útil em
custo de armazenamento. O conjunto de rótulos é fixo e revisado junto com o ADR.

Alertas sugeridos:

- Erro 5xx do núcleo causado por terceiro acima de 1 por cento em 15 minutos (meta).
- p95 de um adapter acima de 800 ms por 10 minutos (meta).
- Contador `evento.processado_total` parado por 15 minutos enquanto `evento.emitido_total` sobe.
- Estratégia sem seleção por 30 dias, sinal de código morto a aposentar.

## 9. Plano de teste

| Caso | Dado | Quando | Esperado | Critério de aceite |
| --- | --- | --- | --- | --- |
| Contrato do adapter | payload válido de terceiro | unitário, sem rede | retorno convertido para formato interno | 100 por cento dos campos mapeados assertados |
| Erro do terceiro | exceção de timeout simulada | unitário | erro de domínio tipado, sem mensagem do SDK | nenhuma classe de SDK aparece no log do núcleo |
| Tabela da factory | cada entrada documentada | unitário | estratégia exata selecionada | cobertura total de ramo da tabela |
| Observador falho | um assinante lança exceção | unitário | demais assinantes executam, emissor não falha | teste verde com um observador sabotado |
| Idempotência do command | mesmo comando executado 2 vezes | unitário | efeito aplicado 1 vez | contador de efeito igual a 1 |
| Fallback | fornecedor degradado por feature flag | integração | caminho de fallback registrado no log | flag desliga sem deploy |
| Import proibido | núcleo com import de SDK | teste de arquitetura | falha explícita | quebra o build ao violar a regra |
| Suíte sem credencial | todas as suítes de núcleo | CI | passa sem variável de ambiente | tempo de execução abaixo de 60 s (meta) |

Critério de aceite global do standard: a suíte roda em pull request, sem rede e sem segredo, e o
teste de arquitetura impede novo import de SDK no núcleo.

## 10. Checklist de adesão

- [ ] A variação foi identificada como real (já mudou ou está comprometida a mudar).
- [ ] Existe port nomeada e documentada para cada fronteira com o lado de fora.
- [ ] O adapter traduz formato, erro e idempotência, não apenas repassa a chamada.
- [ ] Toda cadeia condicional de escolha foi movida para a factory.
- [ ] A factory tem teste de tabela cobrindo cada entrada.
- [ ] Todo observador isola seu próprio erro e não propaga ao emissor.
- [ ] Nenhum código depende da ordem de assinatura do bus.
- [ ] Todo command tem chave de idempotência e registro de execução.
- [ ] Não foi introduzido singleton de cliente ou estado global mutável.
- [ ] O núcleo não importa SDK de terceiro (verificado por teste de arquitetura).
- [ ] Existe fake de port para cada port nova.
- [ ] A suíte de núcleo roda em PR sem credencial.
- [ ] A métrica de telemetria correspondente foi criada junto com o padrão.
- [ ] O runbook cita o dono e a ação de mitigação para o novo ponto de falha.
- [ ] O comentário do PR nomeia o padrão aplicado e a variação que ele absorve.
- [ ] Nada foi modelado como padrão onde não havia variação.

## 11. Padrões na orquestração de agentes

Os agentes são o caso de uso mais propenso a over-engineering desta trilha, porque a variação é
tríplice: qual modelo, qual ferramenta e qual política de custo. O padrão que isola as três é a
combinação de Strategy para seleção, Command para ação e Observer para telemetria do ciclo.

```python
class Completar:
    """Command: ação de agente empacotada, re-jogável e auditável."""
    def __init__(self, prompt: str, chave: str):
        self.prompt, self.chave = prompt, chave

    def executar(self, modelo: Estrategia) -> str:
        if ja_executado(self.chave):
            return ultimo_resultado(self.chave)
        saida = modelo.completar(self.prompt)
        registrar(self.chave, saida)
        bus.emitir("agente.concluido", {"chave": self.chave})
        return saida
```

Regras específicas para agentes:

- A seleção de modelo é Strategy, nunca cadeia condicional no orquestrador. O custo, a latência
  e a política de ferramenta são entradas da factory, e não condicionais espalhados.

- A execução de ferramenta é Command: cada chamada carrega chave de idempotência, porque agente
  reexecutado não pode cobrar duas vezes nem enviar duas mensagens.

- O ciclo do agente publica eventos de domínio (`agente.iniciado`, `agente.concluido`,
  `agente.falhou`) no bus, e a observabilidade assina esses eventos em vez de instrumentar o
  orquestrador com chamadas diretas de log.

- O adapter de provedor de LLM traduz formato, erro e limite de taxa. Erro de rate limit do
  provedor vira erro de domínio tipado, para que a factory possa rebaixar de estratégia cara para
  barata sem vazar detalhe do fornecedor.

- Estratégia morta é código morto: se uma opção de modelo não for selecionada por 30 dias, ela é
  aposentada, e não mantida "por garantia".

## 12. Perguntas frequentes em revisão

**Se o adapter tem um único método, ele ainda é adapter?**
Sim, desde que haja tradução. O critério não é o número de métodos, é se o formato externo mora
dentro dele. Repassar a chamada sem traduzir é alias, e alias está no rol de anti-padrões.

**Posso criar a Strategy antes de existir o segundo algoritmo?**
Não. A regra é variação real. Quando o segundo algoritmo chegar, a extração é barata porque o
primeiro já está isolado atrás da mesma interface.

**Por que não usar um `dict` de configuração para escolher o adapter?**
Porque o `dict` não tem contrato: erro aparece só em runtime, não dá para tipar, testar ramo a
ramo nem receber ajuda do interpretador. A factory com retorno de port dá as três coisas.

**O bus in-memory não é acoplamento de processo?**
É, e isso está declarado como consequência negativa do ADR. Ele é aceito porque o piloto precisa
provar desacoplamento de código. Durabilidade e ordenação exigem fila, e fila exige outro ADR.

**Quem decide que um padrão entrou?**
O autor nomeia o padrão e a variação no pull request; o revisor confere contra a tabela de
decisão; se a variante não estiver na tabela, o ADR é reaberto antes do merge.

**Como sei que o padrão não virou burocracia?**
Contando o tempo entre a abertura do PR e o primeiro comentário útil, e comparando com a média
anterior (meta). Padrão que não reduz tempo de revisão não está pagando seu custo de leitura.

## 13. Referências

- Curso: Design Patterns com Python, na Alura.
- Vídeo: Strategy na prática para trocar if else, no YouTube.
- Doc oficial: Catálogo de padrões com exemplos em Python, em refactoring.guru.
- Doc oficial: Documentação do Python sobre abc e protocolos para ports e adapters, em docs.python.org.
