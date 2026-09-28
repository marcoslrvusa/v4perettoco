# 3-lib: Biblioteca Reutilizável (payload-lib)

Biblioteca de funções JS/Python para nós `Code` do n8n. **Esta é a fonte única
de lógica de transformação**: em vez de copiar/colar código entre workflows,
referencie estas funções.

## Arquivos

| Arquivo | Linguagem | Funções |
|---|---|---|
| `payload-lib.js` | JavaScript | `chunk` · `normalizeStream` · `dedupe` · `aggregate` · `memoizeGlobal` · `toOutput` |
| `payload-lib.py` | Python (stdlib) | `chunk` · `dedupe` · `aggregate` · `parse_payload` · `to_output` |

## Como usar

O n8n não importa arquivos externos em nós Code: a prática é **copiar as funções
necessárias** para dentro do nó, mantendo este arquivo como fonte de verdade.
Cada função vem com exemplo de uso no final do arquivo.

## Regras

1. Nunca editar a lógica de um nó Code e esquecer de atualizar a lib: **a lib é
   a fonte da verdade**.
2. Manter apenas stdlib no Python (sem pandas/numpy).
3. Funções novas vão primeiro na lib, depois nos workflows.

## Contrato função a função

| Função | Linguagem | Assinatura | Complexidade | Efeito colateral |
|---|---|---|---|---|
| `chunk` | JS (gerador) | `chunk(items, size = 100)` | O(n) | Nenhum: usa `yield`, não materializa |
| `normalizeStream` | JS | `normalizeStream(items, { dedupeKey, filter, map })` | O(n) | Nenhum: retorna array novo |
| `dedupe` | JS | `dedupe(items, keyFn)` | O(n) | Mantém a primeira ocorrência |
| `aggregate` | JS | `aggregate(items, keyFn, reduce)` | O(n) | Retorna `[...]` dos valores do `Map` |
| `memoizeGlobal` | JS | `memoizeGlobal(key, computeFn)` | O(1) amortizado | **Grava** em `$getWorkflowStaticData('global')` |
| `toOutput` | JS | `toOutput(rows)` | O(n) | Converte para `{ json }` |
| `chunk` | Python | `chunk(iterable, size=100)` | O(n) | `itertools.islice`, gerador |
| `dedupe` | Python | `dedupe(rows, key='id')` | O(n) | Mantém a primeira ocorrência |
| `aggregate` | Python | `aggregate(rows, key='tipo', value=None)` | O(n) | `TypeError` do acumulador é engolido |
| `parse_payload` | Python | `parse_payload(payload)` | O(1) + parse | **Mutata** `payload['rows']` quando é string |
| `to_output` | Python | `to_output(data)` | O(1) | Sempre devolve lista de um elemento |

Duas assinaturas merecem atenção em revisão:

- `normalizeStream` aceita `filter` e `map` como funções. Isso mantém a passada
  única (a lib faz o laço) sem congelar a regra de negócio dentro da lib. Se a
  regra for usada em mais de um workflow, ela vira função nomeada em `3-lib/`, não
  um lambda colado no nó.
- `parse_payload` muta o objeto recebido. É intencional (evita cópia do documento
  inteiro) e por isso está documentado: quem chama duas vezes recebe o mesmo
  resultado sem repagar o `json.loads`.

## Padrões de teste mínimos

Antes de promover uma função nova da lib para os workflows, ela precisa passar
destes casos, executáveis fora do n8n (o n8n não importa módulo externo):

```javascript
// Casos de borda da função normalizeStream
normalizeStream([], { dedupeKey: 'id' });                       // vazio
normalizeStream([{ json: null }], { dedupeKey: 'id' });         // json nulo
normalizeStream([{ json: { id: 'São Paulo' } }], { dedupeKey: 'id' });  // unicode
normalizeStream([{ json: { id: 1 } }, { json: { id: '1' } }],
  { dedupeKey: 'id' });                                        // colisão de tipo
```

O último caso é o mais importante: `1` e `'1'` produzem a mesma chave se a lib
converter com `String(...)`. Se o domínio trata essas duas formas como o mesmo
registro, isso é desejável; se trata como registros distintos, a conversão precisa
sair da chave. A decisão é do contrato de dados do produtor e deve estar escrita
no comentário da função.

```python
# Casos de borda da função aggregate
aggregate([], key='tipo')                              # vazio
aggregate([{'tipo': None}], key='tipo')                # chave nula
aggregate([{'tipo': 'B2B', 'score': 'abc'}], 'tipo', 'score')  # score inválido
```

## Fluxo de mudança

1. Edite a função aqui, em `payload-lib.js` ou `payload-lib.py`.
2. Rode os casos de borda correspondentes fora do n8n.
3. Copie a função atualizada para cada nó Code que a use.
4. Valide o workflow com `npx --yes n8nac skills validate`.
5. Registre a mudança no README desta pasta.

O passo 3 é o que a regra 1 protege. Ele é manual porque o n8n não carrega módulo
externo em `Code node`; a alternativa seria um custom node TypeScript compilado,
descartado nesta atividade por custo de build e release (ver README da atividade,
Decisões e tradeoffs).

## Limites conhecidos

- Sem versionamento por assinatura: quem consome a lib compara texto, não hash.
  Enquanto o número de workflows for pequeno, comparação textual basta.
- Sem self-test embutido: os casos acima são documentados, não automatizados.
  Automatizá-los é passo natural para a próxima iteração.
- `memoizeGlobal` usa o escopo `global` do workflow. Não serve para valor por
  usuário nem para valor que precise expirar sozinho.
