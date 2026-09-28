# Estratégia de Testes: cobertura mínima 80%

| Camada | Ferramenta | Foco | Alvo |
|--------|-----------|------|------|
| Unitário | pytest | funções puras, ports | 90% |
| Integração | pytest + testcontainers | repos, migrações | 80% |
| E2E | playwright | happy path do agente | 1 cenário |

## Princípios
1. Testar comportamento, não implementação.
2. Fixtures efêmeras (nunca banco compartilhado).
3. Gate: `pytest --cov=src --cov-fail-under=80`.
4. E2E isolado e com retry.

## Escopo e não-escopo

**Escopo deste standard:**

- Definir o que pertence a cada uma das três camadas e o que fica de fora delas.
- Fixar o teto de cobertura e a forma de medição (`branch = true`) para o repositório inteiro.
- Escrever as regras de fixture, isolamento e reexecução que sustentam o SLO de menos de 3 min e flaky abaixo de 1%.
- Estabelecer o plano de teste do próprio gate: como provar que o gate bloqueia quando precisa bloquear.
- Listar os anti-padrões que o revisor reprovou na revisão de código.

**Não-escopo deste standard:**

- Teste de carga, teste de segurança e teste de acessibilidade: trilhas separadas, com ferramentas e critérios próprios.
- Teste de contrato entre serviços externos: quem expõe a API documenta o contrato, quem consome testa contra o contrato versionado.
- Refatoração de código legado: entra no plano de evolução, não no gate inicial.
- Qualidade de prompt e avaliação de resposta de modelo: métrica de eval, não de cobertura de código.

## Termos

- **Cobertura**: fração de código executável exercitada durante a execução da suíte, medida em linhas e ramos.
- **Branch coverage**: medição por par condicional tomado. `branch = true` no `coverage.py` ativa esse modo.
- **Camada unitária**: teste que exercita uma unidade isolada, sem I/O externo, em milissegundos.
- **Camada de integração**: teste que exercita a unidade contra a dependência real em contêiner efêmero.
- **Camada E2E**: teste que exercita a aplicação inteira pelo mesmo caminho que o cliente usa.
- **Fixture efêmera**: recurso criado na execução e derrubado no final, sem estado herdado entre execuções.
- **Teste instável (flaky)**: teste que falha e passa na reexecução sem mudança de código.
- **Gate**: verificação automática cujo resultado negativo impede o merge.
- **Mutation testing**: técnica que altera o código em pequenos passos para medir se os testes realmente falhariam.

## Regra canônica

Um teste só entra na suíte se satisfaz as três condições ao mesmo tempo: exercita
comportamento observável, tem resultado determinístico e falha por asserção própria.
Se qualquer condição falhar, o teste é corrigido ou removido, nunca contado a favor
do gate.

A métrica canônica do gate é a cobertura de ramo sobre o código de `src`:

$$C_b = \frac{R_t}{R_x} \times 100 \quad \text{com} \quad C_b \geq 80\%$$

em que $R_t$ é a quantidade de ramos condicionais tomados pela suíte e $R_x$ a quantidade de ramos existentes no código medido. O comando que materializa a regra:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Código de saída diferente de zero significa duas coisas obrigatoriamente ao mesmo tempo: algum teste falhou, ou a cobertura ficou abaixo do teto. O CI não precisa de lógica adicional para decidir: ele trata o código de saída e ponto.

## Tabela de decisão

| Se | E | Então | Camada |
| --- | --- | --- | --- |
| A lógica é pura | não depende de rede, disco ou banco | teste unitário com asserção direta | Unitário |
| A lógica depende de port | o port tem implementação real em contêiner | teste de integração com fixture de sessão | Integração |
| A lógica é pura | tem ramo `if/else` não coberto | usar `pytest.mark.parametrize` para cobrir todos os ramos | Unitário |
| O comportamento atravessa API inteira | é fluxo de dinheiro ou de dado crítico | um único E2E de happy path | E2E |
| O teste falha por ordem | depende de rodar depois de outro teste | isolar estado e eliminar a dependência | Unitário |
| O teste precisa de tempo | usa `sleep` para sincronizar | trocar por espera determinística na condição | Unitário |
| A cobertura cai abaixo de 80% | há código novo | adicionar teste antes de merge | Gate |
| A cobertura cai | é código legado removido, não novo | aceitar com registro no commit, sem mudar teto | Gate |
| O teste demora acima de 1 s | não faz I/O | reclamar da fixture compartilhada, não paralelizar às cegas | Integração |
| O teste falha uma vez e passa na reexecução | não houve mudança de código | tratar como defeito de teste, abrir item de correção | Qualidade |

## Exemplo numérico de aplicação

**Exemplo numérico:** módulo `src/agente/parser.py` com $R_x = 40$ ramos condicionais. Após escrever 12 testes unitários, $R_t = 31$, logo $C_b = 77{,}5\%$. O gate reprova. Ao adicionar os testes dos três ramos remanescentes do caminho de erro, $R_t = 34$ e $C_b = 85\%$. O gate aprova e a mudança sobe com a rede de segurança instalada.

Contagem do tempo da suíte no mesmo módulo: $T_{unit} = 40$ ms por teste, 45 testes, total $45 \times 0{,}04 = 1{,}8$ s. Somado aos outros módulos, a camada unitária inteira roda em dezenas de segundos, muito abaixo do orçamento de 180 s do gate, o que deixa folga para a camada de integração, naturalmente mais cara.

## Anti-padrões

O que o sênior reprovaria na revisão:

1. **Teste de implementação**: asserção sobre chamada interna exata (`mock.assert_called_once_with` como única verificação). O teste quebra em toda refatoração legítima e não protege comportamento.
2. **Teto alterado para fazer o PR passar**: subir `--cov-fail-under` para baixo em branch de feature. Teto só muda por decisão registrada.
3. **Banco compartilhado entre testes**: deixa estado para o próximo teste e transforma ordem de execução em variável oculta.
4. **Retry usado como política**: reexecutar até passar. Isola sintoma, esconde defeito e corrompe a taxa de flaky.
5. **Time fixo grande**: `sleep(5)` antes da asserção. Aumenta a suíte inteira e continua falhando em máquina lenta.
6. **Teste duplicado com outro nome**: mesma asserção em dois arquivos infla cobertura de aparência sem acrescentar rede de segurança.
7. **Mock do próprio código sob teste**: mockar a função interna que o teste deveria exercitar anula o teste.
8. **Asserção vazia**: teste que executa sem `assert`. Passa sempre e conta a favor da cobertura sem verificar nada.
9. **Acoplamento ao arquivo de configuração**: teste que depende de variável de ambiente do desenvolvedor. Reproduzibilidade morre.
10. **Cobertura coletada só no CI**: quem não consegue medir localmente também não consegue corrigir antes do push.

## Telemetria

| Métrica | Fonte | Cardinalidade | Alerta |
| --- | --- | --- | --- |
| Cobertura global | `pytest-cov` no CI | 1 por execução | Abaixo de 80%, bloqueia merge |
| Cobertura por camada | relatório separado por diretório | 3 por execução | Unitário abaixo de 90% (meta) |
| Duração do gate | tempo do job no CI | 1 por execução | Acima de 180 s na mediana semanal |
| Duração por teste | `pytest --durations=20` | top 20 por execução | Teste unitário acima de 1 s |
| Taxa de flaky | falha seguida de sucesso sem diff | 1 por teste por semana | Acima de 1% no agregado |
| Testes vermelhos no main | status do job na branch principal | contínuo | Qualquer ocorrência |

Regra de cardinalidade: nenhuma métrica por pull request deve gerar série por arquivo
ou por autor, senão o custo de armazenamento cresce sem que a decisão mude. A decisão
é sempre por execução e por semana.

## Plano de teste do gate

O próprio gate precisa ser testado. Casos e critério de aceite:

| Caso | Execução | Critério de aceite |
| --- | --- | --- |
| Suíte completa com teto atingido | `pytest --cov=src --cov-fail-under=80` local | Código de saída 0 |
| Lacuna proposital em um arquivo | Remover temporariamente um teste | Código de saída diferente de 0 e lista `Missing` apontando o trecho |
| Teste em falha | Injetar `assert False` temporário | Falha reportada como `AssertionError`, código de saída diferente de 0 |
| Duas execuções seguidas | Rodar o comando duas vezes | Resultados idênticos, sem efeito de ordem |
| Suíte em máquina limpa | Novo ambiente com só as dependências | Verde sem passo manual de preparação |
| Rollback do gate | Reverter a configuração de teto | Pipeline volta ao comportamento anterior em um commit |

Critério de aceite geral: todos os seis casos verdes, e o sétimo, de reversão, documentado, para que ninguém precise descobrir como desligar o gate em uma madrugada.

## Padrões de projeto e o que cada um exige de teste

| Padrão | O que isolar | Como se testa | Anti-padrão típico |
| --- | --- | --- | --- |
| Ports e adapters | a porta (interface) do adapter | Unitário com falso na porta, integração com adaptador real | Testar o adaptador junto com a regra |
| Injeção de dependência | a dependência chegando pelo construtor | Unitário passando um falso no construtor | `monkeypatch` de módulo global |
| Factory | o objeto criado, não a fábrica | Unitário sobre o objeto devolvido | Assegurar chamada da fábrica |
| Strategy | a escolha do algoritmo | `parametrize` cobrindo toda estratégia disponível | Só testar a estratégia padrão |
| Repository | a persistência | Integração com contêiner efêmero | Mock do próprio repositório no teste de integração |
| Singleton / estado global | o estado compartilhado | Proibido na camada unitária | Ordem de teste virando variável |
| Circuit breaker / retry | o tempo e a contagem de tentativas | Unitário com relógio injetado e falso falho | `sleep` real dentro do teste |

Regra que decorre da tabela: o padrão decide a camada. Quando a decisão não é óbvia,
o teste ainda não está escrito, porque falta desenho. Teste confuso é sintoma de
acoplamento, não de falta de disciplina.

## Fixtures de referência

A fixture efêmera é o coração da camada de integração. Ela cria, entrega pronta e
derruba, garantindo que nenhuma execução herde estado da anterior:

```python
# tests/integration/conftest.py
import pytest

@pytest.fixture(scope="session")
def banco():
    """Sobe um contêiner de Postgres, aplica migrações e derruba ao final."""
    cont = PostgresContainer("postgres:16").start()
    aplicar_migracoes(cont.url)
    yield cont
    cont.stop()          # derrubada garantida mesmo se o teste falhar

@pytest.fixture
def sessao(banco):
    """Sessão de persistência nova por teste, sem estado herdado."""
    with banco.nova_sessao() as s:
        yield s
        s.rollback()
        s.close()

@pytest.fixture
def notificador_falso():
    """Escreve em lista em memória, sem rede."""
    return SpyNotifier()
```

Pontos que o revisor confere nesse bloco: `yield` em vez de `return` para que a
derrubada rode mesmo em falha; escopo de sessão para o contêiner caro e de função
para o estado barato; nenhuma asserção dentro da fixture, porque fixture prepara,
não verifica.

## Refatoração incremental em sombra

Refatorar sob rede de segurança tem sequência fixa. Cada passo termina com a suíte
verde, e nenhum passo mistura mudança de estrutura com mudança de comportamento:

1. Escrever o teste que descreve o comportamento atual, mesmo que feio. Ele é a
   especificação em forma de código.
2. Rodar a suíte e confirmar verde. Sem isso, não há linha de base.
3. Mudar uma única coisa: extrair função, renomear, mover de módulo.
4. Rodar a suíte de novo. Vermelho significa que o passo 3 alterou comportamento,
   então se desfaz o passo 3 e não se mexe no teste.
5. Repetir 3 e 4 até a estrutura desejada, um recorte por rodada.
6. Reconciliar: comparar a cobertura antes e depois e remover o teste temporário
   que só existia para descrever o comportamento antigo, se ele virou duplicata.

Critério de parada: a estrutura desejada foi alcançada, a cobertura não caiu, e a
duração da suíte não subiu mais de 10% (meta) em relação à linha de base. Se subiu,
o gargalo é fixture, e não paralelismo.

## Critérios de aceite por camada

| Camada | Critério de aceite | Como mede | Falha que bloqueia |
| --- | --- | --- | --- |
| Unitário | cobertura >= 90% (meta), nenhum I/O | `pytest tests/unit --cov=src` | Qualquer teste de rede ou disco |
| Integração | cobertura >= 80% (meta), fixture efêmera derrubada | `pytest tests/integration` duas vezes seguidas | Contêiner ou sessão vazando |
| E2E | um fluxo feliz completo por API | `pytest tests/e2e` com retry de 1 | Fluxo de dinheiro sem E2E |
| Gate | código de saída 0 com teto atingido | `pytest --cov-fail-under=80` | Saída diferente de 0 |
| Documentação | comando local idêntico ao do CI | Comparação literal dos comandos | Duas fontes de verdade |

## Comandos de operação

Os quatro comandos que o time usa no dia a dia, todos reproduzíveis fora do CI:

```bash
# 1. rodar tudo com o gate, como o CI roda
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# 2. só a camada rápida, no laço de desenvolvimento
pytest tests/unit -q

# 3. achar o que derruba o tempo da suíte
pytest --durations=10

# 4. descobrir o que falta cobrir em um arquivo
pytest src/agente/parser.py --cov=src/agente/parser.py --cov-report=term-missing
```

O laço de desenvolvimento usa o comando 2 a cada mudança, o comando 4 antes de abrir
o pull request e o comando 1 como confirmação final. Quem pula direto para o comando 1
descobre a lacuna com o contexto já frio, e isso custa mais tempo no agregado.

## Modos de falha da própria estratégia

| Modo | Sintoma | Causa | Correção |
| --- | --- | --- | --- |
| Teto contornável | PR passa com lacuna | Teto em variável de ambiente | Mover teto para arquivo versionado |
| Cobertura inflada | 90% sem defeito caindo | Asserção vazia ou teste de implementação | Revisão do teste e mutation testing |
| Suíte lenta | gate acima de 180 s | Fixture recriada por teste | Escopar fixture para sessão |
| Ordem importa | teste falha só em lote | Estado compartilhado | Isolar estado por teste |
| Retry mascarador | verde depois de duas tentativas | Retry configurado no gate | Remover retry do gate, isolar causa |
| Falso verde de integração | integração sem contêiner | Falso usado no lugar do adaptador real | Exigir contêiner efêmero na camada |

## Checklist de adesão

1. `pytest.ini` ou `pyproject.toml` versionado contém `--cov-fail-under=80`.
2. `branch = true` está configurado no `coverage`.
3. Diretórios `tests/unit`, `tests/integration` e `tests/e2e` existem e estão nomeados.
4. Todo teste unitário roda sem rede, sem disco e sem banco.
5. Todo teste de integração usa fixture efêmera com derrubada garantida.
6. Nenhum teste depende de execução em ordem específica.
7. Nenhum teste usa `sleep` como sincronismo.
8. Retry, quando existe, é limitado a 1 e nunca no gate de merge.
9. O comando do CI é idêntico ao comando documentado para rodar localmente.
10. O job de teste está marcado como required check no repositório.
11. O E2E roda em estágio separado e não bloqueia merge.
12. O relatório `term-missing` é anexado ao resultado do CI.
13. O tempo do gate ficou abaixo de 180 s na mediana.
14. A taxa de flaky ficou abaixo de 1% na semana.
15. Existe caminho registrado para propor aumento do teto, e ele não é um commit de feature.

## Referências de estudo
- Curso: Testes automatizados com pytest, na Alura.
- Vídeo: Piramide de testes na prática com Python, no YouTube.
- Doc oficial: Documentação do pytest sobre execução e cobertura, em docs.pytest.org.
- Doc oficial: Documentação do Coverage.py sobre medição com branch, em coverage.readthedocs.io.
