# SOLID: Antes vs Depois

Standard de adesão da trilha de Clean Code para refatoração de módulos legados.

## Escopo e não-escopo

**Escopo:** módulos de regra de negócio com mais de 200 linhas, mais de 1 dependência de I/O e cobertura inferior a 50 por cento. É o caso do CampaignService (600+ linhas, 4 dependências de I/O, 0 por cento de cobertura).

**Não-escopo:** scripts de uma página, funções puras sem dependência externa, código gerado e adaptadores já isolados. Refatorar esses casos por este standard é burocracia sem retorno.

## Termos

- **Porta (port):** contrato que o domínio declara para o que precisa do mundo exterior. Em Python, `Protocol`; em TypeScript, `interface`; em Gó, interface implícita.
- **Adaptador (adapter):** implementação concreta da porta, o único lugar que conhece biblioteca, rede ou arquivo.
- **Bootstrap:** arquivo único e alto nível que fia domínio e adaptadores. É o único que importa os dois lados.
- **Motivo de mudança:** a razão que força alguém a editar a classe. Se existem duas, a classe já viola SRP.
- **Sombra (shadow):** execução paralela do código novo em modo de leitura, gravando o que faria sem agir, para comparação com o legado.
- **Falso (fake):** implementação em memória de uma porta, rápida e determinística, que espelha o contrato e não a implementação.

## Antes

- **SRP:** run() faz regra + SQL + SMTP + CRM.
- **OCP:** incluir canal WhatsApp exige editar o método central.
- **DIP:** importa psycopg2 e smtplib direto.

```python
# ANTES (Python): quatro motivos de mudança num método só
import psycopg2, smtplib, requests, os

class CampaignService:
    def run(self, camp):
        conn = psycopg2.connect(os.getenv("DB"))
        rows = conn.cursor().execute(
            f"SELECT * FROM leads WHERE camp={camp.id}"   # 1. injection
        )
        for r in rows:
            requests.post("https://api.crm/v1", json=r)   # 2. sem status check
            smtplib.sendmail("relay", r["email"], camp.body)  # 3. sem transação
            print("enviado", r["email"])                   # 4. log acoplado
```

## Depois

| Princípio | Onde |
|-----------|------|
| SRP | CampaignService orquestra; Notifier/Repository/Logger fazem o resto |
| OCP | novo canal = nova impl de Notifier |
| LSP | qualquer Notifier substitui outro |
| ISP | interfaces enxutas |
| DIP | serviço recebe abstrações via construtor |

```python
# DEPOIS (Python): o domínio enxerga só contrato
from typing import Protocol

class LeadRepository(Protocol):
    def pending(self, camp_id: int) -> list: ...
    def mark_sent(self, lead_id: str) -> None: ...

class Notifier(Protocol):
    def notify(self, lead: dict, body: str) -> None: ...

class CampaignService:
    def __init__(self, repo: LeadRepository, notifier: Notifier) -> None:
        self._repo = repo
        self._notifier = notifier

    def run(self, camp_id: int, body: str) -> None:
        for lead in self._repo.pending(camp_id):
            self._notifier.notify(lead, body)
            self._repo.mark_sent(lead["id"])
```

## Aplicação por linguagem

**TypeScript: ISP e DIP em contrato explícito.** O erro clássico é declarar uma interface gorda que força todo implementador a fingir que faz coisas que não faz.

```ts
// ANTES: interface gorda, ISP violado
interface LeadPort {
  pending(campId: number): Promise<Lead[]>;
  markSent(id: string): Promise<void>;
  sendEmail(to: string, body: string): Promise<void>; // o repo não manda e-mail
}

// DEPOIS: uma porta por responsabilidade
interface LeadRepository {
  pending(campId: number): Promise<Lead[]>;
  markSent(id: string): Promise<void>;
}
interface Notifier {
  notify(lead: Lead, body: string): Promise<void>;
}

class CampaignService {
  constructor(
    private readonly repo: LeadRepository,
    private readonly notifier: Notifier,
  ) {}
}
```

**Java: DIP com construtor e teste sem container.** A versão legada instância a fiação dentro do construtor, o que torna a classe impossível de testar sem ambiente.

```java
// ANTES: alto nível depende de detalhe concreto
public class CampaignService {
    public void run(Campaign c) {
        Connection conn = DriverManager.getConnection(URL);   // detalhe
        smtp.send(c.getBody());                                // detalhe
    }
}

// DEPOIS: dependência chega pronta, do lado de fora
public class CampaignService {
    private final LeadRepository repo;
    private final Notifier notifier;
    public CampaignService(LeadRepository repo, Notifier notifier) {
        this.repo = repo; this.notifier = notifier;
    }
}
```

**Gó: interface implícita resolve o mesmo problema.** Não existe `implements`; quem consome declara o que precisa, e o compilador confere. É a forma mais limpa de DIP do ecossistema, e o padrão é declarar a interface perto de quem consome, não perto de quem implementa.

```go
// declaração feita no pacote que consome (regra de idioma)
type Notifier interface {
    Notify(lead Lead, body string) error
}

type CampaignService struct {
    repo   LeadRepository
    notify Notifier
}
```

**SQL: a porta obriga a parametrização.** A refatoração do acesso a dados não é cosmética, é o que elimina o vetor de injeção.

```sql
-- ANTES: interpolação de valor na string (proibido)
SELECT * FROM leads WHERE camp = 17; -- id colocado à mão, escalável por f-string

-- DEPOIS: parâmetro vinculado, valor nunca vira sintaxe
SELECT id, email FROM leads WHERE camp = $1 AND sent_at IS NULL;
```

## Regra canônica

Um módulo está aderente a este standard se, e somente se, as quatro condições abaixo forem simultaneamente verdadeiras:

$$\text{aderente} = \big(\text{sem import de infra no domínio}\big) \land \big(R = 1\big) \land \big(L_{max} \lê 45\big) \land \big(c \gê 0{,}85\big)$$

com $R$ = responsabilidades por classe, $L_{max}$ = maior contagem de linhas por classe e $C$ = cobertura de linha do serviço.

## Tabela de decisão

| Se | E | Então |
| --- | --- | --- |
| classe tem mais de 1 motivo de mudança | é chamada por mais de 1 caller | extrair uma porta por motivo e mover a implementação para adaptador |
| teste exige container ou rede | cobertura abaixo de 50% | inverter dependência antes de escrever mais teste |
| novo comportamento precisa de if/else sobre tipo | a lista de tipos cresce a cada trimestre | trocar por polimorfismo com estratégia injetada (OCP) |
| interface tem mais de 4 métodos | nem todos são usados por todo implementador | quebrar por ISP em duas ou mais portas |
| subtipo levanta exceção onde o supertype retornava valor | o caller não trata | corrigir o contrato ou remover o subtipo (LSP) |
| módulo tem mais de 200 linhas | cobertura abaixo de 50% | fatiar por responsabilidade, um pull request por porta |
| divergência do sombra abaixo de 0,1% | no máximo 5 ocorrências por dia | liberar a migração de tráfego pela flag |

## Exemplo numérico

**Exemplo numérico:** módulo de 600 linhas, teto de 45 linhas por classe, 4 responsabilidades no método principal, 4 dependências de I/O, cobertura atual de 0 por cento.

1. Classes mínimas: $\lceil 600 / 45 \rceil = 14$ classes.
2. Pares de acoplamento antes: $1 \times 4 = 4$ (todo em um ponto). Depois: $14 \times 1 = 14$ (distribuídos), com impacto de mudança caindo de 4 de 4 alvos para 1 de 14 alvos, ou seja, 100 por cento para 7 por cento.
3. Instabilidade antes: $I = 4 / (4 + 1) = 0{,}8$ (domínio instável). Depois: domínio com $C_e = 0$, logo $I = 0$.
4. Linhas a cobrir: $600 \times 0{,}85 = 510$ linhas alcançadas pelo teste.
5. Suíte: $6 \times 40 = 240$ s por pull request com infra real contra $6 \times 0{,}15 = 0{,}9$ s com fakes, ganho de aproximadamente 239 s por pull request.

## Anti-padrões (o que o sênior reprovaria)

- **Interface de vitrine:** criar `Protocol` com todos os métodos da classe antiga só para o diff parecer arquitetural. O contrato tem que nascer do que o domínio usa, não do que a classe antiga fazia.
- **Mock de comportamento:** mock que devolve o que o teste espera em vez do que o contrato permite. Substitua por falso em memória com validação de pré-condição.
- **God repository:** um único `LeadRepository` com 30 métodos, que é a classe antiga rebatizada. Se o port cresce, ele é o novo monólito.
- **Teste de implementação:** asserção sobre ordem interna de chamadas privadas. Quebra em toda refatoração e não valida comportamento.
- **Adaptador com regra de negócio:** o adaptador deve traduzir, não decidir. Se existe `if` de negócio dentro dele, a regra está na camada errada.
- **Transação no domínio:** o domínio não pode saber que existe transação; quem decide a ordem das operações é o caso de uso, e a transação fica no adaptador de persistência.
- **Sombra sem hipótese:** rodar em paralelo sem definir qual divergência é aceitável. Sem critério, o sombra nunca termina.
- **Cobertura inflada:** cobertura de 85 por cento atingida com teste de getter. Conte mutação sobrevivente, não linha tocada.
- **Remover o legado no mesmo pull request da migração:** mata o rollback.

## Telemetria

| Métrica | Cardinalidade | O que monitora | Alerta |
| --- | --- | --- | --- |
| divergências da reconciliação | 1 por dia | fidelidade do módulo novo | acima de 5 por dia (meta) |
| erro por adaptador | adaptador × causa | falha de infra isolada | acima de 1% em 15 min (meta) |
| leads na fila de reprocesso | 1 global | perda silenciosa de dado | acima de 50 itens (meta) |
| cobertura do serviço | 1 por pull request | gate de qualidade | abaixo de 85% bloqueia merge |
| mutação sobrevivente | 1 por pull request | qualidade real do teste | acima de 15% (meta) |
| latência p95 do adaptador de leitura | 1 por adaptador | paginação e índice | acima de 300 ms (meta) |

Regra de cardinalidade: nenhuma métrica pode carregar identificador de lead, e-mail ou ID de campanha. Identificador alto em rótulo de métrica é custo de memória e vazamento de dado; use o ID de campanha apenas no log estruturado, com ID de correlação.

## Plano de teste

| Caso | Pré-condição | Ação | Critério de aceite |
| --- | --- | --- | --- |
| caminho feliz | falso com 3 leads | `run(1, "oi")` | notificador chamado 3 vezes e 3 marcações de envio |
| lista vazia | falso com 0 leads | `run(1, "oi")` | nenhuma chamada, nenhuma exceção |
| falha no meio | notificador levanta no 2º lead | `run(1, "oi")` | erro propagado, 1 marcação, item 2 rastreável para reprocesso |
| nome hostil | lead com apóstrofo e unicode | `run(1, "oi")` | consulta parametrizada, sem exceção de sintaxe |
| contrato do port | todo adaptador | suíte de contrato | mesmo conjunto de asserções passa para real e falso |
| determinismo | 10 execuções | mesma entrada | saída idêntica, 0 dependência de relógio |
| adesão arquitetural | domínio | varredura de import | zero import de psycopg2, smtplib, requests em `domain/` |

Critério de aceite global: cobertura do serviço maior ou igual a 85 por cento, zero sobreviventes em mutação para asserções de regra, suíte abaixo de 1 segundo e o teste de adesão arquitetural vermelho quando um import proibido é introduzido propositalmente.

## Checklist de adesão

1. Escopo e não-escopo declarados antes de começar a refatorar.
2. Cada classe com um único motivo de mudança identificado por escrito.
3. Toda dependência de I/O atrás de porta tipada.
4. Bootstrap é o único arquivo que importa implementação concreta.
5. Nenhum valor interpolado em SQL.
6. Escrita de estado transacional ou com compensação explícita.
7. Teste do serviço roda sem rede, sem container, abaixo de 1 segundo.
8. Falso em memória usado no lugar de mock de comportamento para estado.
9. Suíte de contrato aplicada a todos os adaptadores de uma porta.
10. Cobertura maior ou igual a 85 por cento como gate no CI.
11. Teste de adesão arquitetural rodando no CI.
12. Métricas com cardinalidade sem identificador de dado sensível.
13. Sombra com hipótese escrita: percentual e teto absoluto de divergência.
14. Rollback por flag testado antes da migração de tráfego.
15. ADR com alternativas descartadas e consequências.

## Por que importa
SQL concatenado quebrava envio em nomes com apóstrofo. Após a refatoração, o acesso
a dados está atrás de uma porta com consulta parametrizada (injection eliminado).

## Referências de estudo
- Curso: Clean Architecture e SOLID com Python, na Alura.
- Vídeo: SOLID em código Python na prática, no YouTube.
- Doc oficial: Documentação do Python sobre Protocol e tipagem estrutural, em docs.python.org.
- Doc oficial: Documentação do pytest sobre fixtures e mocks, em docs.pytest.org.
