# ADR-001: Nó de Validação Humana

**Data:** 2026-07-24
**Status:** Decidido
**Contexto:** Hub de Agentes OpenCode

## Contexto

Tínhamos uma task pendente chamada "Nó de validação humana": *o ponto onde o rascunho fica parado esperando alguém aprovar antes de qualquer ação.*

A pergunta era: isso é necessário? O OpenCode já tem? Como implementar no hub?

## Análise

### O que o OpenCode oferece hoje

| Mecanismo | O que faz | É um gate? |
|---|---|---|
| Permissões (allow/deny) | Controla acesso a tools por modo (plan vs build) | Não — é binário, não tem checkpoint |
| Agentes de revisão (@revisor, @copy-revisor) | Revisam e reportam qualidade | Não — o orquestrador pode ignorar |
| Question tool | Pergunta algo ao usuário no meio da execução | Sim, mas é manual e não escalado |
| Pipeline-conteudo | `rascunho → para_aprovacao → aprovado` | Parcial — humano precisa ir no Drive ver |

**Conclusão: OpenCode NÃO tem um nó de validação humana built-in.** Não existe um mecanismo nativo de "trava workflow até aprovação explícita".

### O que já existe no hub que se aproxima

- **@compartilhar-skill**: usa PR no GitHub como gate — humano precisa aprovar antes de mergear. É o padrão mais robusto.
- **@pipeline-conteudo**: envia draft pro Drive com status `para_aprovacao`. Mas não bloqueia o agente — o humano precisa saber que tem algo pra revisar.
- **@flag-okr**: detecta desvio de premissa e *diz* que precisa aprovação humana. Mas não consegue se segurar — confia no humano lendo a flag.

### O dilema

Criar um "nó de validação humana" genérico — uma entidade separada que todo fluxo precisa consultar antes de prosseguir — é **overengineering** pro nosso contexto atual.

Motivos:
1. A maioria dos agentes do hub **não produz dano real** se executar sem validação (pesquisa, análise, rascunho de copy, relatório)
2. Onde o dano existe (compartilhar skill no hub público, campanhas reais, automações n8n em produção), já temos padrões que funcionam
3. Um nó genérico adiciona complexidade de manutenção sem contrapartida de valor

## Decisão

**Não criar um nó de validação humana genérico.**

Em vez disso, adotamos um **padrão leve por orquestrador** onde o risco justifica:

```
orquestrador → gera draft → question("Aprova antes de executar?") → se sim, executa / se não, ajusta
```

Esse padrão usa a tool `question` do próprio OpenCode — zero infra nova, zero dependência externa.

### Onde aplicar o padrão

| Contexto | Tem gate? | Mecanismo |
|---|---|---|
| Compartilhar skill | ✅ Sim | PR review (já existe) |
| Pipeline de conteúdo | ✅ Sim | Google Drive + status (já existe) |
| Agentes de pesquisa/análise | ❌ Não | Desnecessário — sem risco de dano |
| Automação n8n em produção | ⚠️ Sim | Usar `question` no orquestrador |
| Campanhas de mídia (execução real) | ⚠️ Sim | Usar `question` no orquestrador |
| Draft de copy/design | ❌ Não | Revisor já cobre |

## Consequências

- **Positivas:** zero infra nova, padrão simples, cada orquestrador decide onde faz sentido travar
- **Positivas:** usa ferramenta nativa do OpenCode (`question`), sem acoplamento externo
- **Negativas:** não resolve casos onde o agente roda headless (CI, agendado) — nesses, o gate precisa ser PR ou webhook
- **Negativas:** exige disciplina na escrita dos prompts dos orquestradores — não é imposto por configuração

## Alternativas rejeitadas

1. **Serviço externo de approval (webhook + banco + dashboard):** complexidade alta, benefício baixo pro volume atual de workflows que precisariam de gate
2. **Nó genérico como sub-agente separado:** criaria um passeio adicional desnecessário na maioria dos fluxos; viraria ruído
3. **Modo OpenCode customizado com permissões graduais:** OpenCode não suporta per-skill ou per-step permission override — só allow/deny global
