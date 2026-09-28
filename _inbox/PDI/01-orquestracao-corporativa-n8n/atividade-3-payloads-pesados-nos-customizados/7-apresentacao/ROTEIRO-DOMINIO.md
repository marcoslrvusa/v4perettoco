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

## 6. Por que não publicar um custom node TypeScript compilado?
Porque exige build, versionamento de pacote e ciclo de release próprio do n8n, atrasando a entrega em semanas. O padrão de copiar as funções da 3-lib para dentro do nó Code entrega o mesmo ganho de performance em horas, e a sincronização é garantida pela regra de que a lib é a fonte da verdade. Se a duplicação entre workflows virar problema real no futuro, aí sim o custom node entra como revisão de arquitetura, com a matriz de tradeoff já escrita no slide 19 do deck.

## 7. Quanto custa manter isso rodando?
Custo de infraestrutura zero: a instância n8n Enterprise já existe, os três workflows novos são autônomos, só usam nós Code, e não criam tabela obrigatória no Supabase. O custo real é de manutenção: sincronizar a 3-lib com as cópias embutidas a cada mudança de função, algo da ordem de minutos por alteração. O monitoring é opcional e aditiva: a tabela mt_payload_metrics só é criada se quisermos histórico de durationMs e itemsPerSecond.

## 8. E se o payload cair no meio da noite, quem aciona?
O runbook do README define: checagem diária pelas queries §2 e §3 do 5-monitoring, mitigação por redução de chunk_size e rollback por arquivo com git checkout e n8nac push daquele arquivo apenas. O Tech Lead da trilha de Automação decide rollback; a coordenação do PDI é notificada quando o SLI de execuções bem-sucedidas ficar abaixo da meta por duas janelas de 24 h consecutivas. Como cada workflow é independente e não altera schema, a recuperação é por workflow, nunca "desfazer tudo".

## 9. Qual é o SLO dessa atividade?
Três SLIs: execuções de payload >= 100k itens terminando com success true, com meta de 99% em janela de 7 dias; durationMs p95 por workflow com meta de até 60.000 ms na mesma janela; disponibilidade dos webhooks /nos/* com meta de 99,5% em 30 dias. O orçamento de erro é de 1% das execuções do período sem gerar postmortem. Todos os valores são meta: ainda não há baseline medida, porque nada foi publicado antes da homologação.

## 10. Como você prova que funciona?
Quatro evidências nesta ordem: primeiro, npx --yes n8nac skills validate acusando Workflow is valid nos três workflows; segundo, smoke test de 10 itens com dedupe conferido (processedItems e deduped); terceiro, carga de 100k itens gerada pelo próprio script do manual, com durationMs e itemsPerSecond registrados e worker sem reiniciar; quarto, memoização confirmada na segunda execução do Playground, com cachedAt idêntico. A quinta evidência, que só existe depois do retrofit, é a comparação de durationMs do mesmo workflow antes e depois com o mesmo payload.

## 11. O que você deixaria para trás nesta entrega?
Três coisas: (a) o particionamento externo do payload no produtor, porque o webhook ainda aceita 100k num POST só e a resolução definitiva é o produtor enviar em lotes menores; (b) a retomada automática ponto a ponto com mt_job_progress nesta atividade, que ficou apenas esboçada no diagrama de chunking, pois pertence à camada de checkpoint da atividade 2; (c) a criação e alimentação da tabela mt_payload_metrics, que depende de homologação. Também deixaria um self-test executável por função da lib, que hoje é validado por inspeção e por teste manual.

## 12. Qual a alternativa mais barata que resolveria o mesmo?
Escrever duas linhas de orientação no wiki e revisar código manualmente. Resolve por algumas semanas e não tem custo, mas não muda ordem de grandeza: o O(n²) continua lá dentro de cada nó, esperando um payload maior para aparecer. A segunda alternativa barata seria restringir o tamanho máximo de payload no webhook, o que empurra o problema para o produtor e quebra integração quando o volume crescer. A terceira seria migrar a transformação para fora do n8n, num serviço próprio, o que resolve performance e custa um serviço novo para manter. A opção escolhida fica no meio: padroniza o código dentro do n8n já existente, com esforço de retrofit de cerca de 1 h 30 para os quatro workflows com sintoma.

## 13. E se um item inválido derrubar o lote inteiro?
Não derruba, por construção: o filtro barato roda antes de qualquer transformação e todo acumulador de Python usa try/except por item, contando a exceção em skipped. O caso T3 do standard JS e o T5 do standard Python cobrem exatamente isso. A violação apareceria como run em error com mensagem de campo, e a mitigação é inverter a ordem: filtro primeiro, transformação depois. Como o dedupe é por chave, a reexecução é idempotente: rodar de novo não duplica nada.

## 14. Por que o webhook responde antes de terminar o processamento?
Porque responseMode 'onReceived' devolve o reconhecimento imediato ao chamador. Com 100k itens, a resposta ao fim do processamento seguraria a conexão HTTP do cliente por dezenas de segundos e provavelmente esgotaria o timeout dela. O tradeoff é que o chamador não recebe o resultado no corpo da resposta: quem precisa do resultado consulta a métrica gravada pelo próprio pipeline ou chama um nó de saída separado.

## 15. Qual o impacto em horas para o negócio?
Somando o plano: cerca de 1 h 30 de execução de retrofit nos quatro workflows (ADPLAN 30 min, PRO ANÁLISES 10 min, CC Collector 20 min, CC Metrics 20 min), mais 2 h de revisão e homologação dos padrões, mais 1 h de configuração de monitoring. O ganho é eliminar o timeout de 25 min observado no ADPLAN e manter o pico de memória abaixo de 2 GB sem trocar de máquina. Com Little's Law, reduzir o tempo de execução por payload reduz o número de execuções residentes na mesma janela, que é o que segura o pico de memória da instância.
