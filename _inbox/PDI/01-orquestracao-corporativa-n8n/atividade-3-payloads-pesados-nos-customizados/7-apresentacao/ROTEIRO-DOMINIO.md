# Roteiro de Domínio: Atividade 3, Nos Customizados e Expressões Avançadas

Perguntas que um coordenador faria no presencial, com respostas curtas para estudo.

## 1. Por que O(n) muda o jogo em payload de 100k itens?
Porque o padrão antigo com .find e indexOf em loop vira O(n²) e custa bilhões de operações, com OOM e event loop bloqueado. Com índice em Set e passada única, cai para centenas de milhares de operações com pico abaixo de 2 GB.

## 2. Qual e a regra de ouro do parse de JSON no pipeline?
Parse 1x na entrada e chunk default de 1000, no nó Parse and Chunk. Nunca repetir JSON.parse dentro de loop ou por etapa, pois cada re-parse multiplica custo de CPU e memória.

## 3. Por que Python só com stdlib no n8n?
Porque collections, itertools, Counter e defaultdict resolvem enriquecimento e agregação sem pandas e sem pip. Isso evita quebra por versão de pacote e mantém deploy simples no Code node.

## 4. Onde fica a fonte da verdade do código reutilizável?
Na 3-lib, com payload-lib.js e payload-lib.py e funções chunk, dedupe, aggregate, normalizeStream, memoizeGlobal e toOutput. Os workflows embutem cópias, então nunca se edita um nó sem atualizar a lib.

## 5. Como evitar recálculo caro entre execuções?
Com memoização via $getWorkflowStaticData global para limiar e config estáveis, calculados 1x e reutilizados. Na segunda execução o cachedAt não muda, e a base de métricas sai em processedItems, deduped, durationMs e itemsPerSecond.
