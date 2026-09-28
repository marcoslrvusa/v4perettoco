# STANDARD: Serverless Event-Driven

Standard da trilha 03 (Modelagem de dados / Full Stack) para qualquer serviço que receba carga de entrada em rajada e a transforme em escrita durável no banco.

1. Upload nunca processa no request. Grava no store e publica `file.uploaded`.
2. Concorrência limitada no consumer (ex.: 10).
3. Idempotência: dedup = hash(arquivo + tenant).
4. DLQ após N tentativas.
5. Payload carrega só metadados (URL).

## Escopo e não-escopo

**Escopo:** caminho de ingestão assíncrona (upload de planilha, webhook, evento de terceiro) que termina em escrita em banco relacional. Cobre fila, função, dedup, lote de escrita, DLQ, índices da tabela-alvo e a API que expõe o status.

**Não-escopo:** jobs de longa duração acima de 60 s (usa fila de tarefas dedicada, não função), streaming contínuo, processamento em lote noturno com janela garantida (aí worker fixo costuma ser melhor) e qualquer coisa com transação distribuída entre dois banços.

## Termos

| Termo | Significado operacional |
| --- | --- |
| `file.uploaded` | Mensagem com URL, `tenant_id` e `content_hash`; nunca o arquivo |
| Dedup | Chave `tenant_id:content_hash` verificada antes do efeito |
| Backpressure | Limite fixo de execuções simultâneas que empurra a pressão para a fila |
| Mensagem veneno | Mensagem que falha sempre e reentra até travar o consumo |
| DLQ | Fila de exceção com replay manual e triagem |
| `visibility_timeout` | Janela em que a mensagem fica invisível enquanto é processada |
| Lote | Conjunto de linhas gravadas numa única transação |

## Regra canônica

Todo caminho de ingestão satisfaz cinco invariantes, na ordem:

1. **Receber barato:** o request grava o objeto e publica a mensagem em uma transação lógica, respondendo em milissegundos.
2. **Segurar:** a fila absorve a rajada e a concorrência fixa define quantas estações de trabalho existem.
3. **Proteger:** antes de qualquer efeito, a chave de dedup é verificada e reservada.
4. **Escrever em lote:** upserts deduplicados dentro do lote, uma transação por lote.
5. **Soltar:** sucesso commita a dedup; falha devolve a mensagem à fila com `NACK`; três falhas mandam para a DLQ.

Fórmula de capacidade que sustenta a regra 2:

$$\mu = \frac{C}{S}$$

onde $C$ é a concorrência (número fixo de execuções simultâneas) e $S$ o tempo de serviço médio por mensagem, ambos em unidades coerentes (mensagens/s quando $C$ é adimensional e $S$ em segundos).

**Exemplo numérico:** $C = 10$ execuções, $S = 15$ s por planilha de 50k linhas. $\mu = 10/15 = 0{,}67$ msg/s. Se a chegada sustentada é 0,5 msg/s, a folga é 33% e a fila converge. Se a chegada chega a 1 msg/s, a fila cresce a 0,33 msg/s indefinidamente e o alerta de idade da mensagem dispara (meta: acionar em 10 min). Para voltar a convergir: $C = \lceil \lambda \times S \rceil = \lceil 1 \times 15 \rceil = 15$, arredondado para 20 por causa da variabilidade.

## Tabela de decisão

| Se X | E Y | Então Z |
| --- | --- | --- |
| Chegada é rajada | Há ociosidade no vale | Fila + função serverless com concorrência fixa |
| Chegada é constante e alta | Utilização acima de 60% o tempo todo | Worker always-on, serverless é o erro |
| Processamento passa de 60 s | O efeito ainda é idempotente | Quebra em etapas com fila entre elas |
| Processamento passa de 60 s | O efeito é irreversível | Fila de tarefas dedicada com acompanhamento |
| Retry do mesmo evento | Chave de conteúdo estável | Dedup por `tenant:hash` |
| Retry do mesmo evento | Chave instável (timestamp) | Dedup por `event_id` do emissor, senão nunca deduplica |
| Falha é transitória | Erro de rede/banco | Deixa voltar à fila, backoff da plataforma |
| Falha é permanente | Payload malformado | DLQ na terceira tentativa com triagem |
| Dois consumers no mesmo tenant | Escrita em tabela única | Restrição única no banco, sempre |
| API lista entidades | Volume cresce | Paginação por cursor composto, nunca `OFFSET` |

## Exemplo numérico de ponta a ponta

**Parâmetros declarados:** 200 uploads em 5 minutos, planilha média de 20k linhas, 2 ms/linha de parsing, $C = 10$, $S = 40$ s, 100% de sucesso.

- Demanda: $200 \times 40\ s = 8.000$ s de serviço em 300 s de janela → 26,7 núcleos equivalentes.
- Com $C = 10$: capacidade $= 300\ s \times 10 / 40 = 75$ mensagens concluídas na janela; as 125 restantes esperam na fila.
- Tempo de residência médio (Little): $L = 125$ mensagens em fila, $\lambda = 0{,}67$ msg/s → $W = L/\lambda = 187$ s. Soma com o serviço: p95 projetado abaixo de 60 s só se a fila começar vazia (meta).
- Custo do pico: 200 × 40 s × 0,5 GB = 4.000 GB-s, a parâmetro R$ 0,0000166/GB-s dá R$ 0,066 (meta) pelo pico inteiro.

Conclusão do exemplo: dobrar $C$ para 20 corta $W$ pela metade e custa o dobro de conexões simultâneas. A escolha entre as duas é uma decisão de banco (pool) antes de decisão de nuvem.

## Modelagem mínima exigida

```sql
CREATE TABLE import_batch (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id    bigint      NOT NULL,
  object_key   text        NOT NULL,
  content_hash char(64)    NOT NULL,
  status       text        NOT NULL DEFAULT 'received',
  row_count    integer,
  created_at   timestamptz NOT NULL DEFAULT now(),
  processed_at timestamptz,
  CONSTRAINT uq_import_dedup UNIQUE (tenant_id, content_hash)
);

CREATE INDEX CONCURRENTLY idx_import_tenant_created
  ON import_batch (tenant_id, created_at DESC);
```

Regras de modelagem que acompanham o standard:

1. A dedup durável é a restrição `UNIQUE (tenant_id, content_hash)`. O store rápido (Redis/DynamoDB) é aceleração, nunca autoridade: se ele reiniciar e perder o estado, o banco ainda segura a duplicata.
2. Toda tabela de efeito tem restrição única que espelha a regra de negócio (por exemplo `UNIQUE (tenant_id, email)` em `lead`), não só índice de apoio.
3. Índice de suporte usa `CONCURRENTLY` para não bloquear escrita durante o `CREATE`.
4. Índices são pagos na escrita. **Exemplo numérico:** com 3 índices além do heap, cada linha gravada custa 4 unidades de escrita; um lote de 50k linhas vira 200k unidades. Antes de criar o quarto índice, medir o `EXPLAIN (ANALYZE, BUFFERS)` da consulta que ele atende.

## Contrato da mensagem

```json
{
  "event": "file.uploaded",
  "tenant_id": 4211,
  "object_key": "uploads/2026/09/abc123.csv",
  "content_hash": "b1946ac92492d2347c6235b4d2611184b1946ac92492d2347c6235b4d2611184",
  "received_at": "2026-09-28T14:03:11.120Z",
  "trace_id": "6f1c0f2a9c4d4b1e"
}
```

Campos obrigatórios: `tenant_id`, `object_key`, `content_hash`, `trace_id`. Campo proibido: qualquer binário, CSV embutido ou dado pessoal. Versão do contrato: campo `event` sempre presente, consumidor ignora campos desconhecidos (adição é compatível, remoção não é).

## Handler canônico (TypeScript)

```ts
type UploadEvent = {
  tenantId: number;
  objectKey: string;
  contentHash: string;
  traceId: string;
};

type Outcome = { status: "ok" | "skipped"; rows?: number; reason?: string };

export async function handler(msg: UploadEvent): Promise<Outcome> {
  const key = `${msg.tenantId}:${msg.contentHash}`;

  const lease = await dedup.acquire(key);        // 1. proteger
  if (!lease.acquired) {
    return { status: "skipped", reason: "duplicate" };
  }

  try {
    const rows = await readSheet(msg.objectKey); // 2. buscar objeto por URL
    const batch = dedupeBatch(rows, msg.tenantId); // 3. limpar o lote interno
    const written = await runBatch(batch, 500);  // 4. transação por lote
    await importBatch.markDone(msg, written);    // 5. estado durável
    await dedup.commit(lease.key);               // 6. commitar a dedup
    return { status: "ok", rows: written };
  } catch (err) {
    await dedup.release(lease.key);              // devolve para o retry
    throw err;                                   // NACK: mensagem volta à fila
  }
}
```

Ordem importa: dedup commitada depois do efeito durável. Se fosse ao contrário, um crash entre os dois passos deixaria a mensagem marcada como consumida sem efeito nenhum no banco, e o lead nunca seria criado. O inverso (efeito antes da dedup) aceita duplicata em caso de crash, mas o banco com restrição única ainda pega: é o único arranjo com duas barreiras.

## Anti-padrões (o que o sênior reprovaria em review)

1. **Dedup em `set` de memória em produção.** Reinício da função perde o histórico e reabre a duplicata. Aceitável só em PoC com aviso explícito.
2. **`SELECT` antes do `INSERT` como proteção.** Corrida clássica entre dois consumidores: ambos veem a ausência, ambos inserem. Só `ON CONFLICT` + restrição única resolve.
3. **`DELETE` em massa para expirar dados.** Deixa a tabela inchada, devolve espaço devagar ao disco e obriga `VACUUM` longo com lock de análise. A alternativa certa é particionamento por tempo com `DROP` da partição, que libera tudo de uma vez.
4. **`OFFSET` em página de lista.** Custo crescente e página que pula/repete linha quando chega registro novo no meio.
5. **Processar 50k linhas numa única transação.** Transação longa segura `xmin` antigo, infla VACUUM e transforma qualquer retry em retrabalho inteiro.
6. **Concorrência ilimitada "porque a fila segura".** A fila segura a espera, não a contenção de banco: 200 execuções simultâneas viram 200 conexões.
7. **`visibility_timeout` menor que o pior caso.** A mensagem volta visível enquanto ainda processa, e dois workers fazem o mesmo trabalho.
8. **Sem `trace_id` do upload ao upsert.** Impossível reconstruir o caminho de uma planilha que sumiu.
9. **Retry infinito em falha permanente.** É assim que se cria fila infinita e conta de nuvem inflada.
10. **Contar linha do CSV sem normalizar.** `Ana@Loja.com`, `ana@loja.com` e ` ana@loja.com ` são três linhas distintas para o banco e um lead para o cliente.
11. **Aceitar a primeira coluna do CSV como coluna canônica.** Mapear por nome normalizado, com relatório de colunas desconhecidas.
12. **Publicar métrica com cardinalidade alta.** `tenant_id` em rótulo de métrica de milhares de tenants explode a memória do coletor; tenant vira dimensão em log/trace, não em rótulo.

## Telemetria

| Métrica | Cardinalidade | Alerta |
| --- | --- | --- |
| Idade da mensagem mais antiga | 1 por fila | > 10 min (meta) |
| Tamanho da DLQ | 1 por fila | > 0 por 15 min |
| Duração da função p95 | 1 por função | > 45 s |
| Taxa de erro (`NACK`) | 1 por função | > 2% em 15 min |
| `rows_written` somado | 1 por função | queda de 50% contra média de 7 dias (meta) |
| Custo GB-s/dia | 1 por função | projeção acima do orçamento (meta) |
| Duplicatas detectadas | 1 por função | > 0 em 24 h |

`trace_id` entra em log estruturado, nunca em rótulo de métrica. Amostragem de trace: 100% das falhas, 10% das sucessas.

## Plano de teste

| # | Caso | Passo | Critério de aceite |
| --- | --- | --- | --- |
| 1 | Caminho feliz | Enviar 1 planilha de 1k linhas | `status = done`, `row_count = 1000` |
| 2 | Rajada | 200 planilhas em 5 min | Todas resolvidas, p95 < 60 s (meta) |
| 3 | Idempotência | Reenviar o mesmo objeto 3 vezes | 1 processamento, 2 `skipped`, contagem de `lead` estável |
| 4 | Payload ruim | Arquivo binário renomeado para `.csv` | 3 tentativas, ida à DLQ, demais seguem |
| 5 | Concorrência | Amostrar `pg_stat_activity` no pico | Nunca mais que 10 conexões da função |
| 6 | Crash no meio | Matar a função após escrita e antes do commit de dedup | Retry reexecuta, banco não duplica (restrição única) |
| 7 | Borda de lote | Planilha com e-mails repetidos no próprio arquivo | Sem erro de `ON CONFLICT`, linhas deduplicadas |
| 8 | Borda de dados | Coluna vazia, acento, emoji, `NULL`, linha em branco | Importa sem erro, relatório de rejeitados |
| 9 | Consistência de leitura | Listar status durante o pico | Página estável, sem item pulado |
| 10 | Rollback | Reverter alias para versão anterior | Fila intacta, consumo retoma em < 2 min |

## Checklist de adesão

- [ ] Request de upload não executa parsing nem escrita de negócio.
- [ ] Mensagem contém URL, `tenant_id`, `content_hash` e `trace_id`.
- [ ] Concorrência fixada em infraestrutura, com valor revisado.
- [ ] Dedup com duas barreiras: store rápido e restrição única.
- [ ] Ordem correta: efeito durável antes do commit de dedup.
- [ ] Lotes com transação e deduplicação interna do lote.
- [ ] `visibility_timeout` ≥ pior caso de processamento.
- [ ] DLQ configurada com `maxReceiveCount` e playbook de replay.
- [ ] Índices criados com `CONCURRENTLY` e cobrindo a API.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` registrado para as consultas principais.
- [ ] Paginação por cursor composto.
- [ ] Migração em expand/contract quando houver mudança de schema.
- [ ] Métricas das sete linhas da telemetria no dashboard.
- [ ] Custo por mil unidades medido e abaixo da meta.
- [ ] Modo de autoverificação executável no código (`--self-test`).
- [ ] Rollback testado cronometrado em homologação.

## Migração de schema sem downtime

Mudança em tabela com produção é sequência de fases com janela de confirmação entre elas. O princípio é um: a reversibilidade só existe enquanto a fase anterior continua válida.

| Fase | O que muda | Rollback |
| --- | --- | --- |
| 1. Expand | Coluna nova nullable criada, sem uso pelo código | Descarta a coluna, custo zero |
| 2. Backfill | Atualização em lotes de 10k com pausa entre lotes | Para o backfill e reexecuta do ponto |
| 3. Dual write | Código grava nas duas colunas, lê da antiga | Volta a gravar só a antiga |
| 4. Dual read | Código lê da nova e confere contra a antiga | Volta a ler a antiga |
| 5. Contract | Remoção da coluna antiga após janela de confirmação | Sem rollback: por isso espera |

Regras que acompanham as fases:

1. `CREATE INDEX CONCURRENTLY` em produção, sempre. O `CREATE INDEX` comum segura escrita durante a construção e, com 50k linhas por lote chegando, a janela de bloqueio vira incidente.
2. Backfill em lotes pequenos com `WHERE id > $1 AND id <= $2`, porque `UPDATE` em massa segura `xmin` antigo e atrasa o `VACUUM` das demais tabelas.
3. Janela de confirmação do contract: no mínimo um ciclo de negócio completo, porque é o tempo em que o dado errado (se existir) aparece para alguém.
4. Migração de dado sensível: escrever a coluna nova, conferir contagem e amostra, e só então trocar o leitor. Nunca apagar a fonte junto com a troca.
5. Rollback de contrato de mensagem é diferente de rollback de schema: mensagem tem versão no campo `event` e o consumidor ignora campo desconhecido, então adição é compatível sem deploy coordenado.

## Rollout e observabilidade do rollout

1. Implantar em ambiente de teste com o mesmo plano de Terraform.
2. Rodar o modo de autoverificação do handler e o plano de teste da seção anterior.
3. Publicar a versão nova em paralelo, movendo o alias canônico em 10% do tráfego.
4. Observar por 15 minutos (meta): duração p95, taxa de `NACK`, tamanho da DLQ e duplicatas detectadas.
5. Promover para 100% ou reverter por troca de alias, cronometrando os dois caminhos.
6. Registrar o tempo de rollback no dossiê; rollback não cronometrado é rollback não testado.

Critério de parada: qualquer sinal vermelho por duas janelas consecutivas de 15 minutos encerra a promoção e devolve o tráfego à versão anterior. A fila não precisa ser tocada em nenhum dos dois caminhos, porque o contrato da mensagem permanece o mesmo.

## Quando NÃO usar

- Carga constante alta (worker always-on sai mais barato).
- Job acima de 60 s com efeito não idempotente.
- Processamento que exige transação distribuída entre dois banços.
- Pico previsível e calendado: nesse caso provisionar antecipadamente custa menos que provisionar por surpresa.

## Referências de estudo

- Curso: AWS Lambda e Serverless na prática (Alura)
- Vídeo: Serverless em 100 segundos (Fireship, YouTube)
- Doc oficial: Cloud Run functions, https://cloud.google.com/functions/docs (verificada em 2026-09-28)
- Doc oficial: Terraform, https://developer.hashicorp.com/terraform/docs (verificada em 2026-09-28)
