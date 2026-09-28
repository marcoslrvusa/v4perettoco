# ROTEIRO-DOMINIO: Queries Complexas e Indexação no Supabase (PostgreSQL)

5 perguntas de coordenador + respostas curtas para defesa da atividade 1.

## 1. Por que exigir EXPLAIN antes de qualquer query em produção?

Sem plano, a query da fila `mt_jobs` varria 2,4M linhas com Seq Scan e removia 2,38M por filtro. O `EXPLAIN (ANALYZE, BUFFERS)` mostra o plano real e é a única prova aceita na revisão.

**Aprofundamento:** o custo é baixo (um comando a mais no MR) e o risco de não ter é
alto (1,8 s de pick e 3 timeouts de webhook por dia). A regra não é burocracia: é o
único ponto do fluxo onde a regressão de plano é visível antes do usuário sentir.

## 2. Por que o índice composto segue a ordem igualdade, range e ORDER BY?

Nessa ordem um único B-tree cobre filtro e ordenação num Index Scan sem Sort. Foi assim que o pick do worker saiu de 1,8s para 4ms com `(queue, status, scheduled_at)`.

**Aprofundamento:** o B-tree só consegue pular faixas a partir de prefixos fixos. Com
`(queue, status, ...)`, o prefixo `queue='crm-sync'` reduz 2,4M para 40.000 entradas e o
`status` reduz para 10.000. Na ordem invertida, o planner precisa varrer o índice inteiro
para filtrar, que é quase tão caro quanto varrer a tabela.

## 3. Quando usar BRIN em vez de B-tree?

Em série temporal fisicamente ordenada por tempo (logs, sync, eventos), o BRIN fica 10x menor que o B-tree equivalente. Se a ordem física não acompanha o tempo, ele não serve e o B-tree volta a ser a escolha.

**Aprofundamento:** o BRIN não guarda chave por linha: guarda resumo por bloco de
página. Se os blocos estão ordenados por tempo, o resumo elimina blocos inteiros. Se a
ordem foi quebrada por restore ou `VACUUM FULL`, o resumo mente e o scan fica caro. Por
isso a regra é: BRIN sempre acompanhado de uma checagem de ordenação.

## 4. Por que particionar tabelas de eventos em vez de só indexar?

Índice não resolve tabela que cresce sem limite: o planner continua avaliando partições antigas. Com particionamento por range e TTL, o pruning ignora o passado e o dashboard com agregação materializada saiu de 8,4s para 1,1s.

**Aprofundamento:** índice reduz custo por linha, particionamento reduz quantidade de
linhas candidatas. São alavancas diferentes. E o particionamento ainda permite retenção
por `DETACH` em vez de `DELETE` massivo, que geraria dead tuples e não devolveria espaço.

## 5. Como aplicar índice em produção sem derrubar a escrita?

Sempre `CREATE INDEX CONCURRENTLY`, fora da janela de pico: não segura `AccessExclusiveLock`. A criação é mais lenta e não roda em transação, então a janela de deploy precisa prever isso. Nenhum índice desta atividade foi aplicado em produção, apenas documentado e provado.

**Aprofundamento:** o `CONCURRENTLY` faz duas varreduras e atualiza o catálogo ao vivo;
se a segunda varredura falhar, o índice fica "inválido" e precisa ser recriado. Por isso
o runbook inclui conferir `pg_index.indisvalid` depois da criação.

## 6. Quanto custa manter esses índices na prática?

**Resposta curta:** `WAL` e espaço. **Exemplo numérico (parâmetros declarados):** fila
com 500 escritas/s e índice de 3 colunas de ~60 bytes dá 500 × 60 × 2,5 = 75.000 bytes/s
≈ 75 kB/s de `WAL` extra, ou 6,48 GB por dia. O ganho correspondente é de 1,8 s por
leitura × 5.760 leituras/dia ≈ 2,8 h de espera evitada por dia.

**Aprofundamento:** o índice é caro em escrita e barato em leitura. Por isso a regra
prática é medir `pg_stat_user_indexes.idx_scan` por 7 dias: índice com menos de 100
scans na janela é candidato a remoção. Também por isso a atividade não criou índice
"por precaução": cada um deles está ligado a uma query com plano medido.

## 7. E se isso cair no meio da noite, qual é o plano?

Runbook em 4 tempos: checagem diária (5 min) do p95 e do `dead_pct`; diagnóstico com
`EXPLAIN (ANALYZE, BUFFERS)` da query lenta (15 min); rollback com
`DROP INDEX CONCURRENTLY` do índice que piorou (30 min); e aceleração de contingência
subindo `work_mem` da sessão do worker para eliminar `temp file`. O acionamento é do
responsável pelo módulo de dados, registrado no chamado com o plano antes e depois.

**Aprofundamento:** o rollback é sempre o mesmo e sempre disponível, porque toda mudança
de índice entra com o seu `DROP` documentado. Nenhuma mudança desta atividade exige
retornar de migration.

## 8. Qual é o SLO e o que acontece quando ele estoura?

Pick da fila com p95 < 10 ms medido em janela de 5 min; sync CRM < 250 ms em 15 min;
dashboard < 1,5 s em 15 min; `dead_pct` < 10% por hora; zero timeout de webhook por dia.
Orçamento de erro: no máximo 1 janela de 10 min por mês acima do meta. Estourou, a
mudança causadora é revertida antes de investigar causa raiz, porque a fila é caminho
crítico do SDR IA.

**Aprofundamento:** a ordem importa: reverter primeiro, entender depois. Em fila de
trabalho, cada minuto de lentidão vira backlog que persiste mesmo depois do fix.

## 9. Como você prova que isso funciona, e não que é só um relatório bonito?

Com critério de aceite escrito antes de rodar o teste: os três casos precisam reproduzir
pelo menos 80% do ganho documentado (450×, 23× e 22×) e nenhum `INSERT` pode sofrer mais
que 15% de queda de throughput. Os planos são capturados com
`EXPLAIN (ANALYZE, BUFFERS)` em staging com a volumetria de referência, e a saída fica
anexada ao `06-planos-antes-depois.md`.

**Aprofundamento:** o critério é declarado antes para não adaptar a conclusão ao
resultado. Se 80% não sair, a mudança não vai a produção, mesmo que o relatório fique
bonito.

## 10. O que você deixaria para trás e reavaliaria primeiro?

Três coisas: (a) a ordem exata das colunas do índice composto, que ficou decidida por
medida no staging e não por teoria de cardinalidade; (b) o BRIN, que depende de
ordenagem física e precisa de checagem automática em cada `VACUUM FULL` ou restore;
(c) o refresh da MV, que hoje é manual e deveria virar job agendado com alerta de
atraso. Nenhuma das três bloqueia a publicação, mas as três têm dono e prazo na
homologação.

## 11. Qual é a alternativa mais barata que você descartou, e por quê?

**Descartada: trocar o Supabase por outro banco.** Custo: migração de schema, de client
e de operação, semanas de risco, e nenhum dos três gargalos era do motor. Os três eram
de plano de execução, que qualquer Postgres escolheria igual. **Descartada: subir
`work_mem` globalmente.** Custo: mais memória por operação simultânea, risco de OOM em
pico, e resolve só o `Sort`/spill, não o `Seq Scan`. Ficou como contingência de sessão,
não como correção.

**Aprofundamento:** antes de trocar de ferramenta, é obrigatório mostrar que a solução
dentro da ferramenta foi tentada e medida.

## 12. Pergunta de negócio: qual o impacto em R$ ou horas?

**Exemplo numérico (parâmetros declarados):** 3 timeouts de webhook por dia × (meta) R$
25 por lead descartado = R$ 75/dia, ou (meta) R$ 2.250/mês. Em horas: o tempo de
consulta das duas rotinas monitoradas cai de 12.164 s/dia para 101 s/dia, uma economia
de ≈ 3,35 h/dia, ou ≈ 100 h/mês de CPU e de espera. Contra isso, o custo da atividade é
de 25 h de trabalho interno e zero licença nova. **Payback projetado com (meta):** menos
de um mês, mesmo se apenas metade do ganho se confirmar em produção.

**Aprofundamento:** o argumento de negócio não é "query mais rápida". É disponibilidade
do funil SDR: webhook que não dá 504, fila que não acumula backlog invisível, dashboard
que o gestor abre e acredita.
