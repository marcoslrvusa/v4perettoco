# Roteiro de Dominio: Atividade 3, Nos Customizados e Expressoes Avancadas

Perguntas que um coordenador faria no presencial, com respostas curtas para estudo.

## 1. Por que O(n) muda o jogo em payload de 100k itens?
Porque o padrao antigo com .find e indexOf em loop vira O(n²) e custa bilhoes de operacoes, com OOM e event loop bloqueado. Com indice em Set e passada unica, cai para centenas de milhares de operacoes com pico abaixo de 2 GB.

## 2. Qual e a regra de ouro do parse de JSON no pipeline?
Parse 1x na entrada e chunk default de 1000, no no Parse and Chunk. Nunca repetir JSON.parse dentro de loop ou por etapa, pois cada re-parse multiplica custo de CPU e memoria.

## 3. Por que Python so com stdlib no n8n?
Porque collections, itertools, Counter e defaultdict resolvem enriquecimento e agregacao sem pandas e sem pip. Isso evita quebra por versao de pacote e mantem deploy simples no Code node.

## 4. Onde fica a fonte da verdade do codigo reutilizavel?
Na 3-lib, com payload-lib.js e payload-lib.py e funcoes chunk, dedupe, aggregate, normalizeStream, memoizeGlobal e toOutput. Os workflows embutem copias, entao nunca se edita um no sem atualizar a lib.

## 5. Como evitar recalculo caro entre execucoes?
Com memoizacao via $getWorkflowStaticData global para limiar e config estaveis, calculados 1x e reutilizados. Na segunda execucao o cachedAt nao muda, e a base de metricas sai em processedItems, deduped, durationMs e itemsPerSecond.
