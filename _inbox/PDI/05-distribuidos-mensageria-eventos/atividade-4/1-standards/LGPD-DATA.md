# LGPD: Padrão de Dados e Eventos

1. **Minimização**: só o necessário para a finalidade.
2. **Consentimento por finalidade**: campanha != score.
3. **Anonimização em log/trace**: e-mail/CNPJ viram hash.
4. **Retenção definida**: PII tem TTL.
5. **Esquecimento**: delete em cascata por subject_id.

## Regra de ouro
Nunca PII em log, trace ou cache. Use hash(subject) para correlação.

---

## Escopo e não-escopo

**Escopo deste standard**

- Payloads de eventos que trafegam por tópico ou fila e podem conter dado pessoal.
- Campos catalogados com `pii:true` no schema (`lead_event.avsc`) e o caminho deles até o
  consumidor.
- Chaves de correlação (`subject_id`, hash) usadas em log, trace e métrica.
- Ciclo de vida do dado pessoal: coleta, uso, retenção e apagamento, incluindo as cópias em
  cache, índice de busca e réplica.

**Não-escopo**

- Dado pessoal digitado em formulário e guardado só no sistema de origem (aí aplica-se o
  cadastro do setor responsável, não este padrão de eventos).
- Dado agregado ou estatístico sem possibilidade de reidentificação: é resultado analítico,
  não PII, e não precisa de consentimento por evento.
- Segredos de infraestrutura (credenciais, chaves): seguem o padrão de gestão de segredos, que
  proíbe segredo no repositório e em variável de ambiente de aplicação.

## Termos

| Termo | Significado operacional neste padrão |
| --- | --- |
| PII | Qualquer campo que identifique pessoa física ou jurídica de forma direta: CPF, CNPJ, e-mail, telefone, nome completo, endereço |
| `subject_id` | Chave opaca (UUID) do titular; é a única chave aceita em comando de exclusão |
| Pseudonimização | Trocar o identificador por token reversível apenas pelo dono da chave (Fernet no `encrypt_pii.py`) |
| Anonimização | Transformar em hash não reversível na prática (`anon.py`), usado em log, trace e métrica |
| Consentimento (`consent_id`) | Registro de base legal por finalidade, com início, escopo e vigência |
| Finalidade | O propósito declarado do tratamento: `campanha`, `score`, `analitico`; um consentimento não cobre outro |
| Minimização | Cada etapa do pipeline recebe só os campos de que precisa para a finalidade que executa |
| Cascata de exclusão | Remoção por `subject_id` em todos os destinos catalogados, com prova em `audit_log` |
| Recuperação para frente | Falha no meio do apagamento é retomada do ponto parado, nunca desfeita |

## Regra canônica

Um evento com dado pessoal só existe se as quatro condições abaixo forem verdadeiras ao mesmo
tempo. Se qualquer uma falhar, o payload sai minimizado (sem PII), e não "sai assim mesmo".

```text
eventos_com_pii = { e | marca_pii(e) AND consent_ativo(e.subject, e.finalidade)
                        AND campos_minimizados(e) AND ttl_definido(e) }
```

- `marca_pii(e)`: todo campo sensível está declarado `pii:true` no schema e passa pelo
  codificador.
- `consent_ativo(...)`: existe registro vigente para a finalidade exata; consentimento para
  `campanha` **não** vale para `score`.
- `campos_minimizados(e)`: o downstream recebe `subject_id` ou hash, nunca o valor cru.
- `ttl_definido(e)`: o destino tem prazo declarado no `mapa-dados.md`.

**Corolário 1 (ordem)**: a checagem acontece **antes** da publicação. Validar no consumidor é
tarde demais, porque o dado já foi copiado por quem assinou o tópico.

**Corolário 2 (falha)**: quando a checagem não responde (gateway indisponível), o sistema
falha **fechado**: publica sem dado pessoal. Disponibilidade de publicação é negociável;
conformidade não.

**Corolário 3 (correlação)**: para juntar duas pontas de um fluxo sem levar PII, usa-se
`subject_id` quando o destino é interno e controlado, e `hash(salt + valor)` quando o destino é
log, trace ou métrica, onde a linha vai viver por meses.

## Tabela de decisão

| Dado | Finalidade | Consentimento | Forma no evento | Forma em log | TTL |
| --- | --- | --- | --- | --- | --- |
| E-mail para disparo | `campanha` | exigido e vigente | cifrado (Fernet) no campo `contact.email` | `anon:` + hash de 12 hex | 365 dias |
| E-mail para enriquecimento | `score` | exigido, escopo diferente | `subject_id` somente | não loga o campo | 365 dias |
| CPF/CNPJ | qualquer | exigido | cifrado + marcado `pii:true` | hash de 12 hex | 365 dias |
| Telefone | `campanha` | exigido | cifrado | não loga o campo | 365 dias |
| Métrica de campanha | `analitico` | não aplicável (sem identificação) | agregado por dia | valor agregado | conforme política analítica |
| Traço de depuração | interno | não aplicável | nunca | `subject_id` (UUID) apenas | 30 dias |

Como usar a tabela numa revisão de código: ache o campo novo, ache a linha correspondente. Se
não existir linha, o campo não pode entrar no schema sem decisão registrada no ADR-054.

## Exemplo numérico: o custo de deixar o e-mail cru no log

**Exemplo numérico:** um serviço loga `10.000` linhas/dia com `3%` delas contendo e-mail
(`300 e-mails/dia`). Em `90` dias são `27.000` ocorrências em arquivo de log, com retenção de
`180` dias, o que dá `54.000` registros com e-mail vivo em disco (`300 * 180`). A cascata de
exclusão por `subject_id` **não alcança o arquivo de log**: ele é texto, não tem chave. Para
remover, seria preciso reescrever o arquivo com `anon.py` e reprocessar `180` dias de histórico.
Com `log_safe()` aplicado na origem, o número é `0` e a operação de exclusão do titular vira
uma linha em `audit_log`, não um trabalho de reescrita. A conta mostra por que a regra de ouro
é "nunca PII em log" e não "apague o log depois": o depois custa dias, o nunca custa um review.

**Exemplo numérico: colisão do hash truncado.** Com `sha256[:12]` (48 bits) e `n = 1.000.000`
de titulares, `P(colisão) ≈ n² / (2 · 2^48) = 0,0018`, ou `0,18%`. Serve para correlação em
log; **não** serve como identificador único de pessoa. Por isso a chave de exclusão é sempre o
UUID `subject_id`, nunca o hash.

## Anti-padrões (o que o sênior reprova na revisão)

1. **`logger.info(payload)` genérico**: imprime o evento inteiro no log de informação. Um único
   `logger.info("lead salvo subject=%s", subject_id)` resolve.
2. **Máscara parcial como se fosse anonimização**: `j***@***.com` continua sendo dado pessoal e
   não atende ao direito ao esquecimento.
3. **Consentimento genérico**: um booleano `aceitou_termos` usado para todas as finalidades.
   A pergunta certa é "para quê", não "se aceitou".
4. **Delete em uma tabela só**: apagar no CRM e deixar no Analytics, que é o estado que gera
   autuação.
5. **Chave de exclusão por e-mail**: se o titular trocar de e-mail, a exclusão vira caça ao
   antigo. Usa-se `subject_id`.
6. **Hash sem salt**: `sha256(e-mail)` é reversível por dicionário em minutos; o salt fica no
   cofre, fora do código, e é o que torna a transformação praticamente irreversível.
7. **Campo novo de PII sem marcação `pii:true`**: entra no schema, passa reto pelo
   codificador e vaza. O gate de schema na esteira falha o build.
8. **Cachear PII com TTL longo**: o cache sobrevive à exclusão e serve dado apagado.
9. **Chave de criptografia no repositório**: qualquer acesso ao código vira leitura em massa.
10. **Exclusão sem linha de auditoria**: não há como provar à ANPD que a remoção ocorreu.
11. **Retry de exclusão sem idempotência**: dois consumidores processando o mesmo comando com
    efeitos colaterais (por exemplo, notificar o titular) disparam mensagem duplicada.
12. **Ordem de evento sem chave de partição por titular**: `subject.delete` pode ser processado
    antes de `lead.criado` e o dado volta a existir.

## Telemetria

| Métrica | Rótulos (cardinalidade controlada) | O que indica | Alerta |
| --- | --- | --- | --- |
| `eventos_sem_consentimento_total` | `topico`, `finalidade` | vazamento de dado pessoal sem base legal | `> 0` por 5 min: P1 |
| `pii_em_log_total` | `servico` | ocorrência cru em log | `> 0` diário: P2 com correção no mesmo dia |
| `deletion_pending` | `destino` | exclusão travada em algum destino | `> 0` por 5 min: P2 |
| `deletion_duration_seconds` | `destino` | duração da cascata | p95 acima de 1 dia: alerta (teto do SLO) |
| `consent_cache_hit_ratio` | `servico` | saúde do cache do gateway | `< 90%`: investigar gateway |
| `dlq_comandos_depth` | `topico` | comandos de exclusão parados | `> 0` por 24 h: revisita obrigatória |
| `schema_sem_marcacao_pii_total` | `schema`, `campo` | campo sensível sem proteção | `> 0`: build falha |

Regra de cardinalidade: **nenhum rótulo leva `subject_id`, `email`, `cpf` ou `trace_id`**.
Métrica com identificador pessoal é PII dentro de ferramenta de monitoramento, que não tem
ferramenta de exclusão. Para investigação pontual, usa-se `trace_id` no log (cujo trace já é
anonimizado), nunca na métrica.

## Plano de teste

| Caso | Procedimento | Critério de aceite |
| --- | --- | --- |
| P1 Varredura de log | rodar `anon.py` sobre 24 h de log de produção | `0` e-mail e `0` CNPJ cru |
| P2 Falha do gateway | parar o serviço de consentimento e publicar 1.000 eventos | `1.000` payloads minimizados, `0` com PII |
| P3 Cascata de exclusão | executar `retention_policy.sql` com `subject_id` de teste | `count(*) = 0` nas 4 tabelas + linha em `audit_log` |
| P4 Idempotência | publicar `subject.delete` 3 vezes | estado final idêntico a 1 execução, sem erro |
| P5 Ordem | `lead.criado` e `subject.delete` para o mesmo titular, com rebalanceamento no meio | estado final "apagado" em 100% das execuções |
| P6 TTL | rodar o expurgo sobre lote de 12 milhões de linhas (Exemplo numérico) | janela concluída sem lock acima de 5 s (meta) |
| P7 Gate de schema | inserir campo de e-mail sem `pii:true` | build falha antes do deploy |
| P8 Anonimização | conferir que `anon:` + 12 hex é determinístico para o mesmo salt e não revelã o valor | mesmo valor, mesmo hash; salt diferente, hash diferente |

## Checklist de adesão

- [ ] Todo campo sensível está declarado `pii:true` no schema e revisado na esteira.
- [ ] A checagem de `consent_id` acontece antes da publicação, no caminho do evento.
- [ ] O gateway está em modo de falha fechada.
- [ ] Consentimento é registrado por finalidade, com vigência, e não como booleano único.
- [ ] O downstream recebe `subject_id` ou hash; nunca valor cru.
- [ ] Log, trace e métrica passam por `anon.py`/`log_safe` e não têm rótulo identificador.
- [ ] A chave de partição de evento e de comando é `subject_id`.
- [ ] A cascata de exclusão cobre todas as tabelas listadas no `mapa-dados.md`.
- [ ] O estado `pending` é gravado antes do primeiro `DELETE` (recuperação para frente).
- [ ] Comando de exclusão é idempotente em todos os destinos.
- [ ] Auditoria da exclusão é gravada na mesma transação e não contém PII.
- [ ] Chave de criptografia vive em cofre, fora do repositório e do ambiente da aplicação.
- [ ] Janela de retenção de backup é declarada e a mídia é criptografada.
- [ ] Testes P1 a P8 executados nesta versão, com resultado anexado ao ticket.
- [ ] Dono e prazo definidos para cada linha do `mapa-dados.md`.

## Referências

- Documento oficial: Lei n. 13.709/2018 (planalto.gov.br).
- Documento oficial: Guia Orientativo da ANPD (gov.br/anpd).
- Curso: "LGPD na Prática" (Udemy).
- Vídeo: "O que é a LGPD?" (YouTube, SEBRAE).
