# Standard: Expressões Avançadas no n8n

> **Objetivo:** padrão para expressões `={{ ... }}` em parâmetros de nós n8n:
> referências entre nós, JSONata, condicionais e cache: para payloads pesados.

## Escopo e não-escopo

**Escopo:** expressões avaliadas pelo motor de expressões do n8n em parâmetros de
nós (`={{ ... }}`), incluindo referências entre nós (`$('Node')`), acesso ao item
corrente (`$json`), operadores ternários e de coalescência, funções JSONata
(`$filter`, `$count`, `$sum`) e persistência de estado com
`$getWorkflowStaticData`.

**Não-escopo:** lógica de negócio reutilizável com mais de duas condições ou com
laço: isso vai para `3-lib/` e vira nó Code. Também ficam de fora expressões que
dependam de dados sensíveis (token, senha), que pertencem a credenciais do n8n e
nunca a texto colado em parâmetro.

## Termos

| Termo | Significado operacional neste standard |
|---|---|
| Expressão | Trecho avaliado em tempo de execução entre `{{` e `}}` |
| Referência entre nós | `$('Nome do Nó')`, que busca um nó da execução atual |
| Item corrente | O objeto `json` do item que está atravessando o nó |
| JSONata | Linguagem de consulta e transformação usada pelo n8n em alguns parâmetros |
| Coalescência | `a || b`: usa `a` se existir, senão `b` |
| Memoização | Valor estável gravado em `$getWorkflowStaticData('global')` e reúso entre execuções |
| Custo de avaliação | Número de vezes que a expressão é reavaliada por execução |

## Quando usar expressão vs nó Code

| Situação | Use |
|---|---|
| Pegar um campo de outro nó na mesma execução | Expressão `$('Node').item.json.campo` |
| Transformação simples (formatação, concat) | Expressão |
| Dedupe / agregação / normalização em lote | Nó Code (JS/Python) |
| Referenciar dados da execução anterior | `$getWorkflowStaticData()` |
| Consultar por caminho/condição em payload grande | JSONata (`.$filter()`) |
| Mais de duas condições aninhadas | Nó Code ou nó IF encadeado |
| Qualquer coisa com laço sobre 1.000 itens | Nó Code |
| Valor calculado que só muda por configuração | Memoização com chave versionada |

## Referências entre nós

```text
// Último item de outro nó
{{ $('HTTP Request').item.json.leads }}

// Primeiro item
{{ $('HTTP Request').first().json.leads }}

// Todos os itens (cuidado com memória em payload pesado!)
{{ $('HTTP Request').all() }}
```

> **Regra:** `$('Node').all()` materializa o array inteiro. Em payloads pesados,
> prefira processar via nó Code e expor só o que precisa via `item`.

**Custo de `all()`:** cada chamada devolve uma referência ao array de itens daquele
nó na execução. Se a expressão está dentro de um parâmetro que o n8n avalia por item
(ex.: um campo de um nó que processa 100k itens), a mesma chamada é reavaliada 100k
vezes.

**Exemplo numérico:** nó com 100.000 itens avaliando `{{ $('HTTP Request').all().length }}`
por item: 100.000 avaliações de referência, cada uma percorrendo o array de nós
anteriores para localizá-lo. No mínimo isso duplica o trabalho da etapa. A forma
correta é calcular o valor uma vez num nó Code e referenciar o resultado:

```javascript
// Nó Code "Prepara Referência": calcula UMA vez
const origem = $('HTTP Request').all();
return [{ json: { origemCount: origem.length, origem: origem[0].json } }];
```

```text
// Depois, nos nós downstream (acesso pontual, não all())
{{ $json.origemCount }}
```

**Referência segura vs referência custosa:**

| Forma | Custo por execução | Uso aceito |
|---|---|---|
| `$('Node').item.json.campo` | 1 resolução | Padrão |
| `$('Node').first().json.campo` | 1 resolução | Quando só o primeiro importa |
| `$('Node').last().json.campo` | 1 resolução | Quando só o último importa |
| `$('Node').all()` | Materializa o array | Só em nó de preparação, uma vez |
| `$('Node').all()` dentro de laço ou por item | Repetido n vezes | Proibido |

## JSONata para consulta em payload grande

```text
{{ $json.leads.$filter($, function($v) { $v.score >= 70 }).$count() }}
```

Vantagem: consulta e agregação diretas no payload sem nó Code extra.

**Limites práticos do JSONata neste contexto:** a avaliação é feita por item quando
a expressão está num parâmetro de item, e a linguagem mantém o resultado intermediário
em memória até a última função da cadeia. Cadeias com `$filter` seguido de `$map`
seguido de `$sort` criam três estruturas intermediárias equivalentes ao tamanho do
array.

| Se | E | Então |
|---|---|---|
| O filtro é simples e o array é pequeno | < 1.000 itens | JSONata direto no parâmetro |
| O filtro é simples e o array é grande | >= 1.000 itens | Nó Code com passada única |
| Precisa contar/summarizar | Qualquer tamanho | Nó Code com `Map`/`Counter`, métrica explícita |
| A expressão aparece em vários nós | Sempre | Extraia para nó Code ou para a `3-lib/` |

## Expressões condicionais e coalescência

```text
{{ $json.fallback || $('HTTP Request').item.json.valor }}
{{ $json.tipo == 'B2B' ? 'entrada' : 'pipeline' }}
```

Regras de composição:

1. **No máximo um ternário por expressão.** Dois ternários aninhados já indicam que
   a regra de negócio merece um nó Code nomeado, testável isoladamente.
2. **Coalescência para valor ausente, ternário para regra.** `a || b` cobre o caso
   "não veio"; `cond ? x : y` cobre o caso "veio, mas a regra muda".
3. **Cuidado com coalescência e zero:** `{{ $json.score || 70 }}` troca `0` por `70`.
   Use coalescência explícita de presença, não de verdade:

```text
{{ $json.score !== undefined && $json.score !== null ? $json.score : 70 }}
```

Esse é um dos erros silenciosos mais comuns: um lead com score `0` passa a valer o
limiar padrão e entra no filtro errado, sem nenhum erro de execução para denunciar.

## Cache entre execuções (memoização)

```javascript
// Em nó Code:
const staticData = $getWorkflowStaticData('global');
if (!staticData.taxaCambio) {
  staticData.taxaCambio = 5.4; // busca uma vez, reusa nas próximas execuções
}
return [{ json: { taxa: staticData.taxaCambio } }];
```

**Versão versionada, que é a que este standard adota:** a chave muda quando a
semântica do valor muda, para que uma configuração nova não seja mascarada pelo
cache antigo.

```javascript
const staticData = $getWorkflowStaticData('global');
const CHAVE = 'limiar:v2';          // incrementa ao mudar a regra de negócio
const PADRAO = 70;

if (staticData[CHAVE] === undefined) {
  staticData[CHAVE] = PADRAO;        // ou busca externa, calculada 1x
}
return [{ json: { limiar: staticData[CHAVE], cachedAt: staticData[CHAVE + ':ts'] } }];
```

| Propriedade | Comportamento |
|---|---|
| Alcance | Global ao workflow (não por execução, não por usuário) |
| Persistência | Sobrevive a execuções enquanto o workflow não for reconfigurado |
| Invalidação | Manual: trocar a chave ou limpar o static data no UI |
| Custo de leitura | Um acesso a objeto, desprezível |
| Risco principal | Valor defasado servido como verdade |

**Quando NÃO memoizar:** valor que muda a cada execução (timestamp, ID de execução),
valor por usuário (exige partição por chave, fora do escopo do `global`) e valor cuja
obteneção já é barata (memoizar uma leitura de constante só adiciona risco de
defasagem).

## Anti-patterns

| Anti-pattern | Problema |
|---|---|
| `$('Node').all()` dentro de loop | Materializa arrays gigantes repetidamente |
| Expressão complexa com múltiplas chamadas de nó | Re-avalia a cada execução |
| JSONata pesado em payload enorme | Melhor chunking no nó Code |
| Expressão para lógica de negócio reutilizável | Duplicação: vai para `3-lib/` |
| Ternários aninhados em parâmetro | Ilegível e não testável |
| `||` com valores que podem ser `0` ou `''` | Coalescência silenciosa trocando dado legítimo |
| Static data sem chave versionada | Cache impossível de invalidar de forma cirúrgica |
| Expressão referenciando nó removido/renomeado | Referência quebrada só aparece em tempo de execução |
| Credencial ou token escritos na expressão | Vazamento em log de workflow exportado |

## Telemetria

Expressões não emitem métrica por natureza, então o monitoring observa o **nós que
consomem** a expressão. Os sinais úteis são:

| Sinal | O que indica | Onde olhar |
|---|---|---|
| `durationMs` alto só em um nó | Expressão cara avaliada por item | Execução do nó no n8n UI |
| Execução falha com "undefined" | Referência a nó renomeado ou campo ausente | Mensagem de erro do nó |
| Valor constante quando deveria mudar | Static data defasado | `cachedAt` exposto na saída |
| Contagem de itens processados menor que o esperado | Coalescência ou filtro errado | `processedItems` vs `totalItems` |

## Plano de teste

| # | Caso | Entrada | Critério de aceite |
|---|---|---|---|
| T1 | Referência a nó inexistente | Nó renomeado | Falha visível em teste, não em produção |
| T2 | Campo ausente | `json` sem a chave | Coalescência aplica o padrão |
| T3 | Valor `0` e valor `''` | Payload com zero e vazio | Não são substituídos pelo padrão |
| T4 | Ternário simples | `tipo` B2B e B2C | Saída correta para os dois ramos |
| T5 | JSONata `.$filter` + `.$count` | 500 leads | Contagem correta |
| T6 | Memoização 1ª execução | Static data limpo | `cachedAt` preenchido |
| T7 | Memoização 2ª execução | Static data aquecido | `cachedAt` idêntico ao anterior |
| T8 | Troca de versão da chave | `limiar:v2` novo | Cache novo é criado, antigo ignorado |
| T9 | `all()` em nó de preparação | Payload grande | Chamada única, não por item |
| T10 | Payload 100k com expressão leve | Nó downstream | Sem regressão de `durationMs` |

**Critério de aceite geral:** T1 a T10 passam, nenhuma expressão contém mais de um
ternário e nenhuma chamada `all()` aparece em parâmetro avaliado por item.

## Checklist de adesão (antes de publicar o workflow)

- [ ] `$('Node').all()` só onde absolutamente necessário
- [ ] Expressões simples o suficiente para leitura rápida
- [ ] Lógica reutilizável movida para `3-lib/` (payload-lib)
- [ ] Valores estáveis cacheados com `$getWorkflowStaticData`
- [ ] Nenhum ternário aninhado em parâmetro de nó
- [ ] Nenhuma coalescência `||` sobre valor que pode ser `0` ou vazio
- [ ] Toda chave de static data versionada (`chave:vN`)
- [ ] Toda referência entre nós aponta para nó existente e estável
- [ ] Nenhum token, senha ou URL sensível dentro de expressão
- [ ] JSONata limitada a arrays pequenos ou a consulta pontual
- [ ] Casos T1 a T10 executados
- [ ] `npx --yes n8nac skills validate` verde
