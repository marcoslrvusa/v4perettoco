# STANDARD: Observabilidade de Sync n8n -> CRM

Aplicável a toda integração n8n que escreve em CRM da operação. Este documento é o contrato normativo: o que é obrigatório, o que é proibido, como se prova que o padrão está sendo seguido.

## Escopo e não-escopo

**Escopo**: eventos emitidos por nós do n8n que criam, atualizam, aplicam (upsert) ou deletam registros em qualquer um dos 4 CRMs; a view SQL de correlação; o roteamento de alertas; a política de retenção de log.

**Não-escopo**: logs de aplicação interna que não tocam CRM, logs de infraestrutura (Docker, rede), métricas de negócio do painel de BI, e traces distribuídos multi-serviço, que ficam para a evolução com OTel.

## Termos

| Termo | Definição operacional |
| --- | --- |
| `trace_id` | UUID v4 gerado no webhook de entrada; identifica uma tentativa de sincronização de ponta a ponta |
| Evento | Uma linha do log estruturado, sempre com schema conhecido |
| Assinante | Um CRM que recebe o evento publicado no barramento |
| `settled` | Estado em que todos os assinantes responderam, sucesso ou falha permanente |
| DLQ | Fila de mensagens envenenadas (`poison pill`), isolada do fluxo normal |
| Idempotência | Propriedade de aplicar a mesma operação duas vezes sem alterar o resultado final |
| Idempotency key | Chave composta `trace_id + crm + op` usada para deduplicar |

## Contrato (obrigatório em toda saída)

Todo nó que escreve em CRM deve emitir log estruturado:

```json
{"ts":"2026-08-27T10:00:00Z","level":"warn","trace_id":"abc123",
 "integration":"hubspot","op":"upsert_lead","status":"error",
 "code":"401","lead_id":"L-9","msg":"token expirado"}
```

Campos obrigatórios (o evento é inválido sem eles): `ts`, `level`, `trace_id`, `integration`, `op`, `status`, `code`, `msg`. Campos opcionais mas recomendados: `lead_id`, `entity`, `duration_ms`, `attempt`, `schema_version`.

Schema versionado, para que mudança de formato não quebre leitores antigos:

```json
{"schema_version":2,"ts":"2026-08-27T10:00:00Z","level":"info",
 "trace_id":"a1b2c3d4","integration":"rdstation","op":"upsert_lead",
 "status":"ok","code":"200","entity":"lead","lead_id":"L-4412",
 "duration_ms":318,"attempt":1,"msg":"upsert confirmado pelo servidor"}
```

Validação obrigatória na fronteira: se a linha não validar contra o schema, ela é gravada em tabela de rejeição e o evento original é reprocessado, nunca silenciosamente descartado.

## Níveis

- `info`: sucesso de sincronização (1 por lote).

- `warn`: falha recuperável (retry depois).

- `error`: falha persistente -> alerta.

Regra de desempate para quem está em dúvida:

| Situação | Nível |
| --- | --- |
| Escrita confirmada pelo servidor | `info` |
| Timeout, 429, 503: retry será tentado | `warn` |
| 401/403, payload inválido, 3 falhas seguidas | `error` |
| Evento descartado por falta de e-mail | `warn` com `msg` explicando o descarte |
| Falha no próprio coletor de log | `error` com o máximo de contexto disponível |

`debug` existe, mas está proibido em produção: só é liberado por janela temporária, com hora de desligamento anotada no chamado.

## Proibido

- Logar PII cru (e-mail/CNPJ) sem mascarar.

- Swallow de erro sem registro (falha silenciosa).

Outras proibições de igual peso:

- Imprimir o payload completo do CRM, mesmo mascarando só o e-mail (restam CPF, telefone, endereço).
- Usar `console.log` solto sem o schema; o padrão é uma função única de log.
- Gerar `trace_id` depois do primeiro nó de negócio (perde a correlação justamente onde é mais necessária).
- Marcar `status: "ok"` com base em "nenhuma exceção lançada" em vez de confirmação do servidor.
- Duplicar eventos idênticos na mesma execução sem reutilizar a `idempotency key`.

## Regra canônica

Todo evento de sync tem exatamente um `trace_id` por tentativa, e o `status` final só pode ser gravado após resposta registrada de todos os assinantes:

$$\forall e \in Eventos:\ |\{trace\_id(e)\}| = 1 \quad \land \quad status(e) \in \{pending,\ settled,\ poison\}$$

A transição de `pending` para `settled` exige resposta de cada assinante $i \in A$:

$$settled(e) \iff \forall i \in A,\ resposta_i(e) \in \{ok,\ erro\_permanente\}$$

E a probabilidade de perda silenciosa, que é o que a atividade quer zerar, é o produto das taxas de falha não observadas:

$$P_{perda} = P_{falha} \times P_{não\text{-}observada}$$

Se o contrato derruba $P_{não\text{-}observada}$ de cerca de 0,95 para 0,05 (Exemplo numérico), com $P_{falha}$ de 0,10, o risco cai de $0{,}10 \times 0{,}05 = 0{,}005$, ou seja, 0,5% dos eventos.

## Tabela de decisão

| Se | E | Então |
| --- | --- | --- |
| HTTP 401/403 | token expirado | `error` + parar retry + alerta de credencial |
| HTTP 429 | header `Retry-After` presente | `warn` + esperar o valor do header + retry |
| HTTP 429 | header ausente | `warn` + backoff exponencial 1-2-4 s com jitter |
| HTTP 5xx | tentativa < 3 | `warn` + retry |
| HTTP 5xx | tentativa >= 3 | `error` + envio para DLQ |
| Payload inválido no mapeamento | campo obrigatório ausente | `warn` + descarte com `msg` explicando |
| Escrita devolve 200 sem body | leitura de confirmação disponível | `info` apenas após confirmação lida |
| Erro de rede (ECONNRESET) | qualquer tentativa | `warn` + retry, nunca `error` de primeira |

## Exemplo numérico

**Exemplo numérico:** 1.200 eventos em 5 min, 24 falhas na mesma janela. `error_rate = 24 / 1200 = 0,02`, exatamente no limiar, logo o alerta dispara (a regra é estritamente maior que 0,02, então neste caso exato ele não dispara: `24/1200 = 0,02` é igual, portanto permanece abaixo). Com 25 falhas: `25/1200 = 0,0208 > 0,02`, alerta dispara.

Backoff exponencial: tentativas em 0 s, 1 s, 2 s (com jitter de até 500 ms), total de espera de 3,5 s + jitter. Se três eventos falharem simultaneamente e sincronizarem, geram 9 requisições no mesmo instante; com jitter, elas se espalham em uma janela de 1,5 s, reduzindo o pico contra a API do CRM.

## Anti-padrões (o que o sênior reprovaria)

1. **Log decorativo**: emitir linha com `level: "info"` antes de chamar a API, e nunca mais um registro depois. O leitor acredita que deu certo.
2. **Contador solto**: incrementar um número no nó sem `trace_id`. Diz quantos erros houve, nunca quais registros.
3. **Retry cego**: repetir 5 vezes sem backoff e sem jitter. Transforma uma falha pontual em tempestade contra o CRM.
4. **PII disfarçada**: trocar `@` por `***` no e-mail e manter telefone e CPF inteiros.
5. **Trace que não atravessa**: gerar `trace_id` em um nó e não repassar aos filhos, quebrando a corrente.
6. **Alerta sem dono**: canal de Slack com dezenas de mensagens e ninguém nomeado como responsável.
7. **JSON colado em string**: serializar o log como texto único, quebrando a consulta SQL por coluna.

## Telemetria

| Métrica | Cardinalidade | Fonte | Alerta |
| --- | --- | --- | --- |
| Taxa de erro por CRM | baixa (4 valores) | `crm_sync_logs` | > 2% em 5 min |
| Cobertura de `trace_id` | baixa | coluna nula | < 100% |
| Latência p95 por entidade | média | `duration_ms` | > 30 s em 24 h |
| Idade do evento mais antigo em `pending` | 1 | fila | > 5 min |
| Tamanho da DLQ | 1 | `crm_sync_dlq` | > 0 |
| Volume de eventos por integração | 12 | contagem | queda > 50% vs. média |

Regra de cardinalidade: nunca agrupar alerta por `trace_id`. Um alerta por minuto com `trace_id` diferente é ruído garantido; agrupe sempre por `crm` ou `integration`.

## Plano de teste

| # | Caso | Entrada esperada | Critério de aceite |
| --- | --- | --- | --- |
| T1 | Sucesso | API devolve 200 com body | 1 linha `info` com `trace_id` e `duration_ms` |
| T2 | Token expirado | API devolve 401 | 1 linha `error`, zero retries, alerta em < 1 min |
| T3 | Limite de taxa | API devolve 429 com `Retry-After` | `warn` e nova tentativa após o header |
| T4 | Payload sem e-mail | Campo ausente | `warn` de descarte, evento não publicado |
| T5 | Reinjeção do mesmo evento | Mesmo `trace_id` duas vezes | 1 escrita efetiva, 2ª detectada como duplicata |
| T6 | CRM fora do ar | Timeout em 1 dos 3 assinantes | Os outros 2 concluem, evento vai para DLQ |
| T7 | Log sem schema | Linha fora do formato | Gravada em tabela de rejeição, alerta de integridade |

Critério de aceite geral: todos os sete casos passando em ambiente de homologação, com a saída SQL conferindo coluna a coluna.

## Checklist de adesão

- [ ] Nó de entrada gera `trace_id` antes de qualquer lógica de negócio.
- [ ] Todos os nós propagam `trace_id` para os filhos.
- [ ] Função única de log é usada, sem `console.log` direto.
- [ ] Schema validado na fronteira, com rejeição registrada.
- [ ] Níveis `info`/`warn`/`error` aplicados conforme a tabela de decisão.
- [ ] PII mascarada: e-mail e CNPJ, sem exceção.
- [ ] Retry com backoff exponencial e jitter, máximo de 3 tentativas.
- [ ] DLQ implementada e com alerta ligado.
- [ ] Escrita confirmada pelo servidor antes do `status: "ok"`.
- [ ] View de correlação acessível e testada com `trace_id` real.
- [ ] Alerta com piso de volume e dono nomeado.
- [ ] Alerta de silêncio configurado (ausência de eventos).
- [ ] Política de retenção definida (90 dias) e limpeza automática ativa.
- [ ] Código aprovado em code review com este checklist anexado.

## Referências

- Doc: n8n Docs, Logging and observability, na plataforma n8n Docs.
- Doc: PostgreSQL Docs, Views and JSON functions, na plataforma PostgreSQL Docs.
- Curso: Observabilidade na Prática, logs, métricas e traces, na Alura.
