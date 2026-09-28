# Mapa de Domínios (DDD)

Standard da atividade 3 da trilha 02 (práticas de engenharia e clean code). Define como a empresa identifica fronteiras de modelo, nomeia agregados, publica eventos e bloqueia integração ilegítima entre contextos. Aplica-se a todo código novo que crie tabela, entidade ou evento, e a toda revisão de código que altere regra de negócio.

## Escopo e não-escopo

**Escopo:**

- Identificação e nomes de bounded contexts, com raiz de agregado declarada.
- Glossário por contexto (linguagem ubíqua) e regra de renomeação.
- Contrato mínimo dos eventos de domínio e da anti-corruption layer (ACL).
- Critérios de aceite e gate de verificação em CI que impedem leitura cruzada de dados.
- Telemetria do mapa: o que medir para provar que a fronteira está de pé.

**Fora de escopo:**

- Escolha de banco, motor de busca ou tecnologia de fila: isso é decisão de infraestrutura.
- Desenho de API pública e versionamento de URL: pertence ao padrão de contrato de serviço.
- Métricas de produto (conversão, receita): não descrevem fronteira de modelo.
- Microsserviços e estratégia de deploy: o mapa é de modelo, o deploy pode continuar monólito modular.

## Termos

| Termo | Significado nesta atividade | Não confundir com |
| --- | --- | --- |
| Bounded context | Fronteira dentro da qual um termo tem um único significado e existe um dono de dados | Módulo de código ou pacote Python |
| Agregado | Grupo de objetos alterados na mesma transação, com uma raiz | Tabela ou entidade isolada |
| Raiz de agregado | Único ponto de entrada externo; carrega a invariante | Primary key da tabela principal |
| Entidade filha | Item interno sem identidade pública fora da raiz | Registro consultável por endpoint |
| Valor primitivo | Dado sem identidade, copiado por valor (email, canal, moeda) | Entidade com id próprio |
| Evento de domínio | Fato passado, datado e imutável, publicado por um contexto | Notificação de sistema ou log de auditoria |
| Linguagem ubíqua | Vocabulário comum entre negócio, produto e código, um significado por termo | Sinônimos livres no chat |
| ACL | Tradutor na fronteira que converte modelo externo em modelo local | Proxy ou adaptador de banco |
| Event storming | Oficina que revelã fronteiras a partir de eventos laranja no quadro | Reunião de levantamento de requisitos |

## Bounded Contexts
| Contexto | Raiz de Agregado | Filhos |
|----------|-----------------|-------|
| CRM | Lead | Activities, Scores |
| Campaign | Campaign | Segments |
| Agent | Agent | Tasks -> ToolCalls |
| Billing | Invoice | Plan, Usage |

Como a fronteira foi decidida: um contexto novo só nasce quando existe regra de consistência própria, dono de dados identificável e vocabulário que diverge do vizinho. Se faltar qualquer um dos três, o conceito permanece dentro do contexto existente, porque fronteira sem regra é custo de governança sem benefício.

## Linguagem ubíqua
- **Lead**: contato capturado, ainda não qualificado.
- **Deal**: oportunidade com stage e value.
- **Run**: execução de um agente com trace_id.

Regras do glossário:

1. Um termo, um significado por contexto. Se o CRM precisa de dois sentidos, um deles ganha outro nome no próprio glossário.

2. O nome do código é o nome do negócio: `Lead`, `Deal`, `Run`, sem tradução técnica como `ProspectRow` ou `JobInstance`.

3. Glossário versionado no mesmo repositório dos schemas; mudou o nome, mudou o glossário na mesma revisão.

4. Sinônimo detectado em código (`contact`, `prospect`, `registro`) é tratado como dívida: abrir item e corrigir antes de adicionar coluna nova.

5. Termo compartilhado entre contextos exige contrato explícito: ou os dois contextos usam o mesmo significado provado por teste, ou um deles renomeia.

## Integração
Nunca via tabela compartilhada. Via evento: `LeadCreated` (CRM) -> `CampaignEligibilityCheck`.

Contrato mínimo do evento:

```python
@dataclass(frozen=True)
class DomainEvent:
    type: str          # "crm.lead.created"
    aggregate_id: str  # raiz que publicou
    event_id: str      # chave de deduplicação no consumidor
    ts: datetime       # instante da ocorrência, nunca editado depois
```

Regras de fronteira:

- O payload carrega apenas valor primitivo e identificadores da raiz, nunca objeto interno do agregado.

- Consumidor trata o payload como dado externo: valida schema, aplica ACL e só então cria objeto local.

- Evento publicado é imutável. Correção publica outro evento, por exemplo `LeadEmailCorrected`, e não edita o original.

- Compatibilidade é para trás: campo novo é opcional; campo removido exige janela de um release com os dois presentes.

## Regra canônica com fórmula

**Regra:** fronteira legítima entre contextos é evento versionado ou ACL, nunca leitura direta.

$$A = \frac{C_{tocados}}{C_{dono}} \quad \text{com meta } A = 1$$

onde $C_{tocados}$ é o número de contextos alterados por uma mudança de regra e $C_{dono}$ é o número de contextos que de fato carregam a regra.

**Exemplo numérico:** a regra "lead não qualificado não pode ser contatado" é carregada pelo CRM (1 contexto). Antes do mapa, a mesma checagem existia em CRM, Campaign, export de Billing, painel e ETL, ou seja, 5 toques: $A = 5/1 = 5$. Com o mapa, Campaign reage a `LeadCreated` e o painel lê o resultado publicado: $A = 1/1 = 1$.

Segunda métrica de sanidade, o custo transacional do agregado:

$$T_{tx} = T_{lock} + \sum_{i=1}^{n} T_{op,i}$$

**Exemplo numérico:** agregado com 3 filhos, operação de 8 ms e lock de 4 ms dá $T_{tx} = 4 + 3 \times 8 = 28$ ms; agregado com 12 filhos dá $T_{tx} = 4 + 12 \times 8 = 100$ ms. Se a invariante não justifica, o agregado está grande demais.

Terceira métrica, a carga do barramento:

$$\lambda_{eventos} = \lambda_{comandos} \times e \qquad L = \lambda W$$

**Exemplo numérico:** 40 comandos/s com $e = 1{,}5$ publicam 60 eventos/s; consumidor com $W = 25$ ms mantém $L = 60 \times 0{,}025 = 1{,}5$ eventos simultâneos por worker.

## Tabela de decisão

| Se | E | Então |
| --- | --- | --- |
| A regra precisa de transação conjunta | envolve raiz e filhos | Mesmo agregado, transação única |
| Dois conceitos têm o mesmo nome | e sentidos diferentes | Contextos diferentes ou renomear um |
| O contexto precisa ler dado vizinho | só para exibir | Espelhe por evento, não faça join |
| O contexto precisa reagir a mudança vizinha | e a regra é local | Consome evento versionado |
| O payload externo tem forma estranha ao modelo local | | Insere ACL na fronteira |
| A invariante cruza dois contextos | | Reavalie a fronteira antes de criar saga |
| Não existe regra de consistência | e não há dono | Não cria contexto novo |
| A integração é chamada de API síncrona | entre domínios internos | Prefira evento, salvo exigência de latência |
| O evento precisa de resposta obrigatória | antes de concluir | Comando síncrono no mesmo contexto, evento só notifica |

## Anti-padrões (o que o sênior reprovaria em revisão)

1. **Foreign key cruzando fronteira.** `campaign.lead_id` apontando para tabela do CRM: amarra sortimento dos dois contextos. Reprovação: mover para referência por evento, guardando apenas o id recebido.

2. **Coluna só para o vizinho.** `is_eligible_for_campaign` escrita pelo CRM para o Campaign ler. Reprovação: o Campaign calcula a elegibilidade a partir do evento que recebe.

3. **Entidade filha exposta.** Endpoint `GET /items/123` sem citar o agregado. Reprovação: expor `GET /orders/456` e, dentro, os itens.

4. **Evento editável.** Payload alterado após publicação ou registro sobrescrito no banco do produtor. Reprovação: evento congelado, correção por novo evento.

5. **Nome técnico no lugar do nome do negócio.** `ProspectRecord`, `JobRunDTO`. Reprovação: adotar o termo do glossário.

6. **Contexto sem dono.** Ninguém responde por schema, glossário e eventos. Reprovação: nomear dono antes de criar o contexto.

7. **God aggregate.** Um agregado com regras de quatro domínios. Reprovação: dividir por invariante real, validar com user story.

8. **Join em query de leitura com dados de outro contexto.** Reprovação: leitura projetada por evento, mesmo que com atraso declarado.

9. **Evento que carrega objeto inteiro.** Payload com 40 campos, quase todos internos. Reprovação: raiz + valor primitivo.

10. **Integração por log.** "Já que logamos tudo, o outro time lê o log". Reprovação: log é para diagnóstico, contrato é para integração.

## Telemetria

| Métrica | Cardinalidade | O que medir | Alerta |
| --- | --- | --- | --- |
| Contextos tocados por mudança | por PR | contagem de contextos alterados na revisão | > 1 contexto por PR de regra |
| Leitura cruzada em CI | por módulo | importações proibidas detectadas | qualquer ocorrência, bloqueia merge |
| Eventos publicados | por tipo de evento | taxa em eventos/s por contexto | 0 eventos por 24 h com sistema ativo |
| Idempotência | por consumidor | efeitos / eventos publicados | razão > 1,02 |
| Latência de processamento | por consumidor | p95 em ms | acima de 1000 ms por 15 min |
| Modelos duplicados | global | contagem de nome repetido sem ACL | > 0 |
| Contrato de schema | por evento | payload válido no consumidor | qualquer payload inválido |

Evitar cardinalidade alta: não etiquetar evento com `user_id` ou `lead_id`, que explode a série temporal. Usar `tipo_evento`, `contexto` e `status` apenas.

## Plano de teste

| Caso de teste | Dado | Quando | Critério de aceite |
| --- | --- | --- | --- |
| Invariante de contato | lead não qualificado tenta ser contatado | unidade | `DomainError` levantada, nenhum `Contact` criado |
| Transação de agregado | comando inválido em filho | unidade | nada persistido, exceção propagada |
| Imutabilidade de evento | tentativa de alterar campo publicado | unidade | `FrozenInstanceError` ou equivalente |
| Deduplicação | mesmo `event_id` entregue duas vezes | integração | efeito aplicado 1 vez |
| Compatibilidade de contrato | payload da versão anterior | integração | consumidor valida sem erro |
| ACL | payload externo com nome diferente | integração | objeto local criado com vocabulário do contexto |
| Dependência entre contextos | import proibido | CI | build falha com mensagem do violador |
| Caso de borda vazio | agregado sem filhos | unidade | regra aplicada sem `IndexError` |
| Caso de borda nulo | `aggregate_id` nulo | unidade | rejeitado na validação da raiz |
| Caso de borda unicode | email com acento e emoji | unidade | evento publicado com payload íntegro |
| Caso de limite | 1000 filhos no agregado | carga | $T_{tx}$ medido e dentro da meta ou agregado dividido |

## Checklist de adesão

1. O contexto está declarado no DOMAIN-MAP com raiz de agregado nomeada.

2. O glossário do contexto está versionado e sem sinônimos pendentes.

3. Nenhum import, query ou FK aponta de um contexto para dados de outro.

4. Toda entidade filha é alcançada somente pela raiz.

5. Toda transação altera um agregado e um só.

6. Todo evento é `frozen` ou equivalente, com `type`, `aggregate_id`, `event_id` e `ts`.

7. Todo consumidor valida schema e deduplica por `event_id`.

8. Toda fronteira com payload externo tem ACL nomeada no código.

9. Todo PR de regra de negócio cita o termo do glossário na descrição.

10. O gate de dependência entre contextos está configurado em CI e verde.

11. Os casos de borda (vazio, nulo, unicode, limite) estão cobertos por teste.

12. Existe dono nomeado para o contexto e para cada contrato de evento.

13. Existe runbook de rollback para o evento publicado.

14. A revisão de código pergunta explicitamente: "isso pertence a qual contexto?"

## Padrão de PR e revisão de código

Todo PR que toque regra de negócio segue o mesmo formato, para que a pergunta de domínio apareça antes da discussão de estilo.

**Título:** `[contexto] ação curta com o termo do glossário`

Exemplo: `[crm] impede contato de lead não qualificado`.

**Descrição obrigatória:**

```text
Contexto: CRM
Termo do glossário: Lead (contato capturado, ainda não qualificado)
Invariante afetada: INV-01 / INV-05
Contextos tocados: 1 (justificar se for mais de um)
Eventos publicados: LeadCreated (novo) ou nenhum
Testes: invariante, caso de borda, contrato
```

**Roteiro do revisor (o que olhar, nesta ordem):**

1. A mudança pertence a este contexto? Se tocar dois, exigir justificativa ou reavaliar fronteira.

2. Existe FK, import ou query apontando para dado de outro contexto? Se sim, reprovar e pedir evento ou ACL.

3. A entidade filha está sendo exposta fora da raiz? Se sim, reprovar.

4. O evento novo é datado, imutável e tem `event_id`? Se não, reprovar.

5. Os testes cobrem o caso de borda (vazio, nulo, unicode, limite) além do caminho feliz?

6. O glossário foi atualizado na mesma revisão se o nome mudou?

7. O ADR foi anexado se a fronteira mudou?

SLA de revisão: primeira resposta em até 1 dia útil (meta); PR que espera mais de 2 dias úteis (meta) sobe para a pauta do time.

**Padrão de aprovação:** ao menos 1 aprovação de quem conhece o contexto dono da regra. Se o PR tocar mais de 1 contexto, exigir 2 aprovações, uma por contexto afetado.

## Automação de qualidade

O mapa só se mantém se uma máquina o defender. Três verificações rodam em CI, na ordem:

```bash
# 1. dependencia entre contextos: falha o build se houver leitura cruzada
python tools/check_context_deps.py --fail-on-cross-read

# 2. duplicacao de modelo: nome repetido sem ACL registrada
python tools/check_duplicate_models.py --expected 0

# 3. contrato de evento: schema validado dos dois lados
python tools/check_event_contracts.py --all
```

Critérios de aceite do gate:

- Qualquer leitura cruzada entre contextos bloqueia o merge.

- Contagem de modelos duplicados acima de 0 bloqueia o merge.

- Payload de evento inválido no consumidor bloqueia o merge.

- Testes de invariantes (INV-01 a INV-08) verdes são pré-condição para aprovação.

- O relatório do gate é anexado ao PR, para auditoria posterior.

Se o gate cair por engano (falso positivo), o caminho não é desligar a checagem: registra-se a exceção com data de expiração e dono, e a exceção expira sozinha em 30 dias (meta).

## Referências de estudo
- Curso: Domain-Driven Design do zero, na Alura.
- Vídeo: Bounded contexts e linguagem ubíqua na prática, no YouTube.
- Doc oficial: Domain-Driven Design Reference, de Eric Evans, em domainlanguage.com.
- Doc oficial: Documentação do Python sobre dataclasses para modelar agregados e eventos, em docs.python.org.
