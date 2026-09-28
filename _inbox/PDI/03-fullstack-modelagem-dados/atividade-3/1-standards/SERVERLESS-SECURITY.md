# STANDARD: Serverless Seguro

Escopo: toda função serverless que lê arquivo de terceiro, escreve em banco multi-tenant e usa segredo. Não-escopo: segurança de aplicação web genérica (autenticação de UI, CSRF), que vive no padrão de API.

## Regras canônicas

- **Secrets:** nunca em env var hardcoded → usar Secret Manager / AWS Secrets Manager.
- **Conexão DB:** via connection pooler (PgBouncer) com TLS; não abrir por IP público.
- **IAM:** função com política mínima (only `cloudfunctions.invoker` + secret accessor).
- **Timeout:** <= 60s; jobs longos → Cloud Tasks / fila.
- **Idempotência:** chave de evento para não reprocessar duplicado.

## Modelo de ameaça (o que de fato pode dar errado)

| Ameaça | Vetor | Impacto | Controle |
| --- | --- | --- | --- |
| Vazamento de segredo | Log de depuração, env em imagem, repositório público | Acesso total ao banco | Secret Manager + rotação + varredura de histórico |
| Injeção de SQL | Coluna de CSV concatenada em `INSERT` | Leitura/exclusão de dados de todos os tenants | Somente query parametrizada, zero de concatenação |
| Escapar do tenant | `tenant_id` vindo do payload confiado ao cliente | Um cliente lê dados do outro | Restrição de linha (RLS) + validação de posse do objeto |
| CSV injection | Célula iniciando com `=` ou `+` abrindo planilha do operador | Execução de comando na estação de quem abre o relatório | Sanitizar célula com prefixo `'` na exportação |
| Arquivo hostil | Zip bomb, CSV de 2 GB, content-type mentiroso | Custo estourado e negação de serviço | Limite de bytes + contagem de linhas + tempo de execução |
| Negação de serviço por custo | Rajada de uploads que nunca terminam | Fatura de nuvem disparada | Limite de taxa por tenant + concorrência fixa |
| Replay malicioso | Reenvio de evento antigo já consumido | Dado regravado com versão velha | Dedup + validade do `received_at` |
| Escrita fora do contrato | Payload alterado por emissor não confiável | Estado corrompido | Validação de esquema da mensagem (JSON Schema) |

## Segredos

```python
# ERRADO: segredo em env var fixa e versionada
DB_URL = "postgres://app:senha@host/db"

# CERTO: segredo resolvido por invocação, com identidade da função
from google.cloud import secretmanager

def get_conn():
    client = secretmanager.SecretManagerServiceClient()
    db_url = client.access_secret_version(
        name=os.getenv("DB_SECRET")).payload.data.decode()
    return pg8000.connect(dsn=db_url)   # dsn já exige sslmode=require
```

Regras derivadas:

1. Variável de ambiente guarda o *nome* do segredo, nunca o valor.
2. Cada função tem segredo próprio ou política de acesso ao mesmo segredo, revogada por função.
3. Rotação: trocar o segredo no Secret Manager e reiniciar a função; nunca editar código. Cadência: a cada troca de time ou suspeita, no mínimo a cada 180 dias (meta).
4. Nenhum segredo em mensagem de fila, log, `trace_id` ou variável de ambiente de build.
5. Revogação de emergência: apagar a versão do segredo derruba a função (falha visível) em vez de deixar credencial vazando.

## Identidade e permissão mínima

Política da função cobre exatamente três coisas: invocação pelo emissor autorizado, leitura do objeto que o evento aponta e escrita no bucket/tabela do seu escopo. Nada de `*` em recurso. Separação por ambiente: `dev` e `prod` em projetos/contas distintos, porque vazamento de credencial de homologação não pode alcançar produção.

Revisão de política em checklist: (1) algum `Resource: "*"`? (2) permissão de administrador de banco? (3) permissão de escrever em fila de outro serviço? (4) permissão de listar todos os objetos do bucket? Se sim em qualquer item, volta para revisão.

## Conexão e rede

- TLS obrigatório no DSN (`sslmode=require`), sem exceção de ambiente.
- Pooler na frente do banco: a função abre e fecha conexão a cada invocação, e sem pooler cada execução paga handshake + TLS (~**Exemplo numérico:** 20 ms × 10 execuções simultâneas = 200 ms de CPU de rede por ciclo).
- Banco não exposto à internet pública. Acesso via IP privado + pooler, ou via provedor gerenciado com lista de IPs autorizados.
- Timeout da conexão menor que o timeout da função: 10 s de conexão contra 60 s de função (meta), para que a falha de rede vire retry rápido em vez de espera morta.
- Tempo de vida da conexão curto; a função é efêmera e não existe garantia de reúso.

## Validação da entrada (arquivo e mensagem)

```python
MAX_BYTES = 25 * 1024 * 1024      # 25 MB
MAX_ROWS = 200_000
FORBIDDEN_PREFIXES = ("=", "+", "-", "@", "\t", "\r")

def sanitize_cell(value: str) -> str:
    """Neutraliza CSV injection em células exportadas."""
    if value.startswith(FORBIDDEN_PREFIXES):
        return "'" + value
    return value
```

Critérios de aceite da validação: arquivo acima de 25 MB recusado antes do parse; contagem de linhas acima de 200k recusada com status `failed` explicando o limite; célula iniciada por `=` nunca chega crua ao arquivo de exportação; mensagem sem `trace_id` ou sem `content_hash` é rejeitada por validação de esquema e cai na DLQ como `payload_ruim`.

Observação sobre limite: validar **antes** do parse é o que mantém o custo previsível. Validar durante o parse significa deixar o atacante decidir quanto custo ele gera.

## Isolamento multi-tenant

Duas camadas, porque uma só falha silenciosamente:

1. **Na aplicação:** todo `SELECT`/`UPDATE` carrega `WHERE tenant_id = $1`, com `tenant_id` derivado da sessão autenticada, nunca do corpo da mensagem.
2. **No banco (RLS):**

```sql
ALTER TABLE lead ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON lead
  USING (tenant_id = current_setting('app.tenant_id')::bigint);
```

A função define a variável de conexão logo após conectar e nunca mais trafega com outra. Teste obrigatório: conectar como `app.tenant_id = 1` e tentar ler linha do tenant 2; retorno precisa ser vazio, não erro (erro indicaria que a política está sendo burlada por outro caminho e não pela política).

## Idempotência e validade temporal

- Chave de dedup: `tenant_id:content_hash`, com duas barreiras (store rápido + `UNIQUE` no banco).
- Idade máxima do evento: `received_at` com mais de 24 h é descartado com log, porque replay de evento velho regrava estado que já foi corrigido por outro caminho.
- Replay da DLQ sempre em lote pequeno (10 mensagens) com dedup ativa, para não reinjetar de uma vez o problema inteiro.

## Observabilidade de segurança

| Sinal | O que indica | Ação |
| --- | --- | --- |
| Pico de arquivos rejeitados por tamanho | Tentativa de abuso ou cliente com exportação errada | Bloqueio temporário por tenant |
| Erro de restrição única em massa | Fila reprocessando demais | Pausar consumer, investigar dedup |
| Acesso a segredo negado | Rotação incompleta | Corrigir política antes de reativar |
| Consulta com tempo anormal | Falta de índice ou tentativa de extração | Amostrar `EXPLAIN (ANALYZE, BUFFERS)` e log de origem |
| Custo por execução subindo sem mudar volume | Payload inflado ou loop de retry | Auditoria de tamanho e contagem de `NACK` |

## Plano de teste de segurança

1. Enviar planilha com célula `=cmd|' /C calc'!A0` e conferir que a exportação sai com aspas.
2. Enviar arquivo de 200 MB e conferir recusa antes do parse, com resposta abaixo de 1 s.
3. Forçar mensagem sem `content_hash` e conferir ida à DLQ, não sucesso silencioso.
4. Conectar com tenant A e tentar ler tenant B: resultado vazio.
5. Tentar logar o DSN e conferir que o valor do segredo não aparece em log algum.
6. Simular queda do Secret Manager: a função falha com erro claro e a fila segura a demanda, sem derrubar a API de ingestão.
7. Rodar varredura no repositório procurando token, senha e chave conhecida; nenhum hit.

## Checklist de adesão

- [ ] Nenhum valor de segredo em código, env fixa ou repositório.
- [ ] Variável de ambiente guarda só o identificador do segredo.
- [ ] TLS exigido na conexão com o banco.
- [ ] Pooler entre função e banco.
- [ ] Política de função sem `*` e sem permissão administrativa.
- [ ] Timeout de conexão menor que timeout da função.
- [ ] Limite de bytes e de linhas aplicado antes do parse.
- [ ] Sanitização de CSV injection na exportação.
- [ ] `trace_id` e `content_hash` obrigatórios por validação de esquema.
- [ ] `tenant_id` derivado da sessão, nunca do payload.
- [ ] RLS habilitada e testada com leitura cruzada vazia.
- [ ] Apenas queries parametrizadas, sem concatenação de SQL.
- [ ] Idade máxima de evento definida e logada no descarte.
- [ ] Replay da DLQ em lote pequeno com dedup ativa.
- [ ] Rotação de segredo agendada com dono nomeado.
- [ ] Métricas de segurança no dashboard com alerta dono.

## Referências de estudo

- Curso: AWS Lambda e Serverless na prática (Alura)
- Vídeo: Serverless em 100 segundos (Fireship, YouTube)
- Doc oficial: Cloud Run functions, https://cloud.google.com/functions/docs (verificada em 2026-09-28)
- Doc oficial: Terraform, https://developer.hashicorp.com/terraform/docs (verificada em 2026-09-28)
