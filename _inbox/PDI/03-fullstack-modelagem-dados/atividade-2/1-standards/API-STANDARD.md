# STANDARD: API Modular (FastAPI)

## Escopo e não-escopo

**Escopo:** endpoints de listagem e detalhe em FastAPI voltados a dados de missão crítica, autenticados por `api_key`, com estado no Redis e banco PostgreSQL. Aplica-se a qualquer rota `GET` que devolva coleção de registros e a qualquer rota de escrita que altere uma coleção listável.

**Fora de escopo:** endpoints de upload binário, streaming de arquivo, webhooks de saída e rotas de relatório que exportam planilha. Esses casos têm perfil de latência e de corpo diferente e merecem standard próprio. Também ficam de fora as APIs públicas externas, que exigem cota por plano, faturamento e contrato legal de nível de serviço.

**Termos:**

| Termo | Significado neste standard |
| --- | --- |
| Cursor | valor opaco que marca a posição de leitura na ordenação estável; o cliente repassa sem interpretar |
| Keyset | técnica de paginação que localiza a página pela chave de ordenação, não pelo deslocamento |
| Balde | estrutura token bucket: capacidade máxima de requisições e taxa de recarga |
| Prefixo de cliente | segmento inicial de toda chave de cache, igual ao identificador do `api_key` |
| Envelope | formato único de erro: `code`, `message`, `trace_id` |
| HIT/MISS | resultado da leitura de cache: encontrado no Redis / precisou do banco |
| Varredura | leitura sequencial completa de uma coleção feita por um consumidor em lote |

## Paginação: SEMPRE cursor-based
`?after=<cursor>&limit=50`. Cursor = id criptografado.
Resposta: `{ items, next_cursor, limit }`. Nunca `offset` em tabelas > 10k.

### Regra canônica

A listagem ordena sempre por um par estável e busca por esse par. A fórmula é:

$$WHERE (created\_at,\ id) < (c_{ts},\ c_{id})\ ORDER\ BY\ created\_at\ DESC,\ id\ DESC\ LIMIT\ L + 1$$

O `+ 1` é obrigatório: é a linha extra que diz se existe página seguinte, sem segunda consulta. Se o banco devolveu `L + 1` linhas, descarta a última, monta `next_cursor` a partir dela e devolve `L` itens. Se devolveu `L` ou menos, `next_cursor` é `null`.

Ordenar por `created_at` sozinho é proibido: empates de timestamp fazem itens pular ou repetir entre páginas. O segundo campo do par, `id`, quebra o empate e torna a ordenação uma permutação total dos registros.

Cursor é valor opaco, codificado em base64 com um prefixo de versão e devolvido intacto. O servidor valida o formato antes de qualquer uso. Valor malformado responde `422`, nunca chega ao banco.

**Implementação de referência (extraída de `main_api.py`):**

```python
def paginate_cursor(qs, after: str | None, limit: int = 50):
    """Devolve página por keyset com linha extra para detectar próxima página."""
    if after:
        qs = qs.filter(id > int(after))
    page = qs.limit(limit + 1).all()
    nxt = page[-1].id if len(page) > limit else None
    return {
        "items": page[:limit],
        "next_cursor": str(nxt) if nxt else None,
        "limit": limit,
    }
```

**SQL correspondente com o par estável completo:**

```sql
SELECT id, created_at, nome, status
FROM leads
WHERE (created_at, id) < (:c_ts, :c_id)
ORDER BY created_at DESC, id DESC
LIMIT :limit_plus_one;
```

**Índice que sustenta a regra:**

```sql
CREATE INDEX CONCURRENTLY idx_leads_created_id
    ON leads (created_at DESC, id DESC);
```

`CONCURRENTLY` é obrigatório em produção: sem ele, a criação do índice trava as escritas da tabela inteira durante a execução.

### Tabela de decisão

| Ordenação | Cursor tem par estável | Existe índice composto | Limite <= 200 | Então |
| --- | --- | --- | --- | --- |
| Sim | Sim | Sim | Sim | cursor, `limit + 1`, retorno `next_cursor` |
| Sim | Sim | Sim | Não | rejeitar na validação Pydantic com `422` |
| Sim | Sim | Não | Sim | criar índice `CONCURRENTLY` antes de publicar |
| Sim | Não (só data) | qualquer | qualquer | corrigir a ordenação, bloquear merge |
| Não (ordenado por coluna não única sem desempate) | qualquer | qualquer | qualquer | bloquear merge |
| Qualquer | qualquer | qualquer | Sim mas pede salto direto | expor `/v2` com busca por faixa, nunca `OFFSET` |

## Cache
`Cache-Control: max-age=30, stale-while-revalidate=60`. Invalidar no write.

### Regra canônica

A chave é montada de forma determinística e sempre carrega o prefixo do cliente:

```
{recurso}:{api_key}:{cursor|inicio}:{limit}
```

Exemplo: `leads:ak_9f2:inicio:50`. Dois clientes com a mesma listagem nunca compartilham chave, porque o filtro de permissão pode diferir e um vazamento de cache entre contas é falha de segurança, não falha de performance.

Gravação usa `SETEX` com TTL de 30 segundos. Leitura é feita antes de tocar no banco. A resposta expõe `X-Cache: HIT` ou `X-Cache: MISS`, que é o SLI de acerto.

**Invalidação no write:** toda rota de escrita que altera o recurso executa, depois do commit, a limpeza do prefixo do cliente. Ordem importa: commit antes da invalidação. Se invalidar antes do commit, um leitor concorrente pode regravar no cache a versão antiga e o dado fica defasado até o TTL.

```python
# Pseudocódigo do caminho de escrita
async def upsert_lead(payload):
    async with db.transaction() as tx:          # 1) grava primeiro
        row = await tx.execute(INSERT_LEAD, payload)
    await cache.invalidate_prefix(f"leads:{api_key}:")   # 2) invalida depois
    return row
```

Invalidação global por recurso (`DEL leads:*`) é proibida: derruba o cache de todos os clientes a cada escrita e zera a taxa de acerto no pico de gravação.

O header `Cache-Control` também é enviado, para que consumidores com proxy próprio economizem banda. Ele é complemento, nunca substituto do cache no servidor.

**Leitura do cache com proteção contra estouro de contagem (thundering herd):** quando a chave vence e 20 requisições chegam juntas, todas farão `MISS` ao mesmo tempo. A mitigação é trava de registro: a primeira requisição grava `SETNX` com TTL curto de 2 segundos e as demais aguardam ou servem a versão em revalidação. Sem trava, o pico de banco duplica exatamente no momento em que a taxa de acerto cai.

## Rate limiting (token bucket)
100 req/min por api_key -> 429 + Retry-After.

### Regra canônica

Baldinho com capacidade `B = 100` e recarga `r = 100/min`, compartilhado no Redis para valer igual em todas as instâncias. Cada requisição tenta consumir um token; sem token, responde `429` com `Retry-After` em segundos e `X-RateLimit-Remaining: 0`.

Fórmula de recarga ao consultar:

$$tokens = \min(B,\ tokens + \lfloor \Delta s \times r / 60 \rfloor)$$

**Exemplo numérico:** cliente gasta os 100 tokens em 12 segundos. Ao minuto seguinte, `Δs = 48`, recarga = $\lfloor 48 \times 100 / 60 \rfloor = 80$ tokens. Ele pode fazer 80 requisições imediatamente e as 20 restantes no minuto seguinte.

O balde fica **antes** do cache na cadeia. Se ficasse depois, um cliente abusivo consumiria CPU e rede montando chaves e lendo Redis antes de ser barrado.

`Retry-After` nunca é aleatório: é o tempo real de recarga de um token, o que torna o retry do consumidor eficiente em vez de uma loteria.

Rate limit local por processo (memória do worker) só é aceito em contingência de Redis, com flag e janela curta, porque cada instância teria seu próprio balde e a quota efetiva seria `r × instâncias`.

## Erros
`{ "error": { "code": "...", "message": "...", "trace_id": "..." } }`
4xx = cliente (não retentar). 5xx = nosso (retry com backoff).

### Tabela de decisão

| Status | `code` de exemplo | Retentar? | Backoff sugerido | Quem age |
| --- | --- | --- | --- | --- |
| 400 | `INVALID_PARAM` | não | nenhum | cliente corrige a chamada |
| 401 | `UNAUTHORIZED` | não | nenhum | cliente renova credencial |
| 403 | `FORBIDDEN` | não | nenhum | cliente pede permissão |
| 404 | `NOT_FOUND` | não | nenhum | cliente confere o id |
| 409 | `CONFLICT` | às vezes | nenhum | cliente resolva o conflito de versão |
| 422 | `VALIDATION_ERROR` | não | nenhum | cliente corrige corpo ou parâmetro |
| 422 | `BAD_CURSOR` | não | nenhum | cliente reinicia a varredura do início |
| 429 | `RATE_LIMITED` | sim | igual a `Retry-After` + jitter | cliente espera e repete |
| 500 | `INTERNAL` | sim | exponencial com jitter | cliente retenta; time investiga pelo `trace_id` |
| 503 | `UNAVAILABLE` | sim | exponencial com jitter | cliente retenta; time mitiga |

`trace_id` é gerado na entrada da requisição, devolvido no envelope e gravado em log estruturado com o mesmo valor. É a única ponte entre o consumidor e o processo interno.

Nenhum handler pode devolver `str(exc)`. Exceção vira `code` genérico na resposta e detalhe completo apenas no log.

## Anti-padrões (o que o sênior reprovaria na revisão)

1. `OFFSET` em consulta de listagem, mesmo pequeno "por enquanto".
2. Ordenação por `created_at` sem campo desempatador.
3. Chave de cache sem o prefixo do cliente.
4. Invalidar cache antes do commit da escrita.
5. `KEYS leads:*` para invalidar: varredura bloqueante no Redis; usar prefixo rastreável ou `SCAN`.
6. Rate limit por IP atrás de proxy, que faz todos parecerem a mesma origem.
7. Rate limit implementado com `sleep` no caminho da requisição, que segura a conexão e amplia o pico.
8. Devolver `str(exc)` ou stack trace no corpo.
9. `create_engine` dentro da função da rota, criando conexão a cada chamada.
10. Label de métrica com `api_key` ou `cursor`, que explode a cardinalidade da base de séries.
11. Teste que só verifica a primeira página, deixando a varredura completa sem prova.
12. Limite de `limit` apenas no cliente, sem teto no servidor.
13. Tratar `429` como erro interno no monitoramento, poluindo a taxa de 5xx.

## Telemetria

| Métrica | Tipo | Cardinalidade | Observação |
| --- | --- | --- | --- |
| `api_request_duration_seconds` | histograma | baixa (`rota`, `metodo`, `cache`) | é daqui que sai o p95 do SLO |
| `api_requests_total` | contador | baixa (`rota`, `status`) | alimenta disponibilidade e taxa de 5xx |
| `api_rate_limit_total` | contador | baixa (`resultado`) | `allow` e `deny` |
| `api_cache_result_total` | contador | baixa (`recurso`, `resultado`) | hit rate por recurso |
| `db_pool_in_use` | gauge | mínima | alerta acima de 90% |
| `redis_up` | gauge | mínima | alerta em 0 por 60 s |

Cardinalidade proibida como label: `api_key`, `cursor`, `trace_id`, `id` de registro. Identidade detalhada vai para log estruturado, não para métrica.

Alertas: p95 de lista > 200 ms por 10 min; 5xx > 1% por 5 min; 429 > 5% por 15 min; hit rate < 70% por 15 min; `redis_up` = 0 por 1 min.

## Plano de teste

| # | Caso | Passo | Critério de aceite |
| --- | --- | --- | --- |
| P1 | Varredura completa | paginar até `next_cursor = null` | contagem igual ao total, sem duplicado e sem pulado |
| P2 | Empate de timestamp | inserir 50 linhas com o mesmo `created_at` | varredura sem repetição nem omissão |
| P3 | Página profunda | paginação até a 1.000ª página com `EXPLAIN (ANALYZE, BUFFERS)` | linhas lidas próximas de `limit + 1` |
| P4 | Cursor inválido | `?after=abc` | `422 BAD_CURSOR`, zero consulta ao banco |
| P5 | Teto de limite | `?limit=100000` | `422`, mensagem aponta o teto |
| P6 | HIT em seguida de MISS | duas chamadas idênticas | primeira `MISS`, segunda `HIT` |
| P7 | Invalidação | gravar e ler em seguida | leitura pós-escrita é `MISS` |
| P8 | Redis parado | desligar Redis e repetir P1 | `200`, caminho banco ativo |
| P9 | Estouro de quota | 101ª requisição no minuto | `429` com `Retry-After` |
| P10 | Exceção não tratada | forçar erro interno | envelope completo, sem stack |
| P11 | Carga | 200 req/s por 5 min | p95 hit < 200 ms, zero 5xx |
| P12 | Memória | observar RSS na P11 | sem crescimento contínuo |

## Checklist de adesão

1. A rota tem `limit` com teto servidor-side e default explícito.
2. A ordenação usa par estável `(created_at, id)` e o índice cobre essa ordem.
3. Existe `EXPLAIN` armazenado para a consulta profunda e o plano usa o índice.
4. O cursor é opaco, versionado e validado antes do banco.
5. A chave de cache começa com o prefixo do `api_key`.
6. Toda escrita no recurso invalida o prefixo depois do commit.
7. O rate limit está antes do cache e usa o Redis como fonte única.
8. O `429` carrega `Retry-After` real.
9. Todo erro passa pelo envelope com `trace_id`.
10. Nenhuma resposta contém stack trace ou caminho interno.
11. O pool de conexões é único e fixo, sem criação por requisição.
12. Existe teste de varredura completa e teste com Redis desligado.
13. Métricas sem label de identidade de alto volume.
14. Runbook cobre pool esgotado, índice perdido, Redis fora e 429 em massa.
15. As metas de SLO têm janela de medição e alarme configurado.

## Referências

- Doc oficial: Documentação do FastAPI, https://fastapi.tiangolo.com/ (verificada em 2026-09-28)
- Doc oficial: Redis, https://redis.io/ (site oficial com link para a documentação, verificado em 2026-09-28)
- Curso: FastAPI Beyond CRUD (TalkPython Training)
