# 3-lib — Biblioteca Reutilizável (payload-lib)

Biblioteca de funções JS/Python para nós `Code` do n8n. **Esta é a fonte única
de lógica de transformação** — em vez de copiar/colar código entre workflows,
referencie estas funções.

## Arquivos

| Arquivo | Linguagem | Funções |
|---|---|---|
| `payload-lib.js` | JavaScript | `chunk` · `normalizeStream` · `dedupe` · `aggregate` · `memoizeGlobal` · `toOutput` |
| `payload-lib.py` | Python (stdlib) | `chunk` · `dedupe` · `aggregate` · `parse_payload` · `to_output` |

## Como usar

O n8n não importa arquivos externos em nós Code — a prática é **copiar as funções
necessárias** para dentro do nó, mantendo este arquivo como fonte de verdade.
Cada função vem com exemplo de uso no final do arquivo.

## Regras

1. Nunca editar a lógica de um nó Code e esquecer de atualizar a lib — **a lib é
   a fonte da verdade**.
2. Manter apenas stdlib no Python (sem pandas/numpy).
3. Funções novas vão primeiro na lib, depois nos workflows.