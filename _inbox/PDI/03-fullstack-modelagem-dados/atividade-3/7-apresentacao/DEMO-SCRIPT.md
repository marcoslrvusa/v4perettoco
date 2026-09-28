# Roteiro de Demo: Arquitetura Serverless para Processamento Assíncrono (event-driven)

Abra o deck (index.html) e percorra os slides na ordem.

## Pré-requisitos

- Acesso de leitura ao repositório e ao painel de filas da nuvem.
- Seed disponível: 200 planilhas sintéticas em `seed/uploads/` (1k, 5k, 20k e 50k linhas) e 1 arquivo corrompido em `seed/uploads/_corrompido.bin`.
- Função e fila implantadas a partir de `infra/terraform_serverless.tf`, com `reserved_concurrent_executions = 10` e DLQ anexada.
- Comandos abaixo rodam na raiz do projeto. Saída esperada é literal; desvio é critério de falha do passo.

## Passos da demo

1. **Slide de Resumo: abra com o problema de negócio e o blast radius.**
   Fala: custo fixo pago 24/7 contra entrada variável de 1k-50k linhas.
   Saída esperada: plateia entende os três números (90% ocioso, 200 uploads no pico, R$ 0,20 por mil como alvo).
   Falha: se pedirem o número de antes e ele não existir, volte ao slide 2 e declare o exemplo numérico do README como parâmetro, não como medição.

2. **Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).**
   Fala: quatro critérios iguais para as três alternativas.
   Saída esperada: `Lambda direto no upload` rejeitada por falta de backpressure; `worker com auto-scaling` rejeitada por custo no vale.
   Falha: se a objeção for "e se a fila atrasar?", responda com a conta do slide 12 (fila de 100 mensagens em 5 min) e a ação de subir concorrência.

3. **Slide de Validação/Rollout: mostre como provamos em produção.**
   Fala: as três provas (volume, falha forçada, isolamento) e os critérios de aceite marcados.
   Saída esperada: todos os itens do checklist de aceite do README marcados.
   Falha: item desmarcado não se discute como pronto; ele volta para a lista de pendências antes do deploy.

4. **Slide de Riscos: apresente o plano de mitigação.**
   Fala: cold start com concorrência provisionada; fila sem limite com DLQ desde o primeiro deploy.
   Saída esperada: cada risco com mitigação e dono.
   Falha: risco sem dono vira ação na retro.

5. **Abra o terminal e mostre a infra como código.**
   Comando: `grep -n "reserved_concurrent_executions\|maxReceiveCount\|visibility_timeout" infra/terraform_serverless.tf`
   Saída esperada: `reserved_concurrent_executions = 10`, `maxReceiveCount = 3`, `visibility_timeout_seconds = 300`.
   Falha: qualquer valor ausente significa que o backpressure ou a DLQ saíram do padrão. Não siga: corrija o plano antes de qualquer execução.

6. **Abra o handler e aponte as seis etapas canônicas.**
   Comando: `cat 2-code/process_upload.py`
   Saída esperada: leitura do evento, chave `tenant:hash`, checagem de dedup, upsert por lote, commit de dedup, retorno `skipped` em duplicata.
   Falha: se `PROCESSED.add(key)` vier antes dos upserts, a ordem está invertida e o crash no meio perde o lead. Pare a demo e explique o bug.

7. **Mostre a modelagem que sustenta a idempotência.**
   Comando: `grep -n "UNIQUE" -A2 README.md`
   Saída esperada: `CONSTRAINT uq_import_dedup UNIQUE (tenant_id, content_hash)` e `UNIQUE (tenant_id, email)` em `lead`.
   Falha: restrição ausente significa que a segurança final depende só do store em memória, que reinicia. Risco inaceitável em produção.

8. **Rode o modo de autoverificação do handler (PoC em memória).**
   Comando: `python3 2-code/process_upload.py --self-test`
   Saída esperada: `ok caminho feliz`, `ok duplicata detectada`, `ok borda: linha vazia`, `ok borda: unicode`, total de casos conforme o script.
   Falha: qualquer caso `FAIL` derruba a demo; reporte a causa e volte ao passo 6.

9. **Envie 1 planilha de 1k linhas e acompanhe o status.**
   Comando: `python3 scripts/enviar.py seed/uploads/planilha_1k.csv --tenant 4211`
   Saída esperada: resposta imediata com `accepted` e `trace_id`; status muda de `received` para `done` com `row_count = 1000`.
   Falha: status preso em `received` por mais de 10 minutos significa evento perdido; mostre a varredura de republicação (passo 15) em vez de esconder.

10. **Reenvie o mesmo arquivo três vezes para provar idempotência.**
    Comando: `python3 scripts/enviar.py seed/uploads/planilha_1k.csv --tenant 4211` (executar 3×).
    Saída esperada: 1× `done`, 2× `{"status":"skipped","reason":"duplicate"}`; contagem de `lead` do tenant estável entre as execuções.
    Falha: contagem aumentando é duplicata em produção. Interrompa, pause o consumer e corrija a dedup antes de continuar.

11. **Dispare a rajada de 200 planilhas.**
    Comando: `python3 scripts/enviar.py --burst seed/uploads/ --count 200 --window 300`
    Saída esperada: 200 aceites em até 300 s; consumo visivelmente limitado a 10 execuções simultâneas.
    Falha: mais de 10 conexões simultâneas da função (verifique com amostragem de `pg_stat_activity`) significa concorrência não aplicada. Cancele a carga.

12. **Meça paralelismo e custo durante a rajada.**
    Comando: `python3 scripts/medir.py --janela 300`
    Saída esperada: execuções simultâneas máximas ≤ 10, p95 do `upload` até `done` abaixo de 60 s (meta), GB-s do período impressos.
    Falha: p95 acima de 60 s por duas janelas seguidas encerra a validação e vira tarefa de otimização.

13. **Force falha parcial e confirme retry sem duplicata.**
    Comando: `python3 scripts/falhar.py --modo rede --taxa 0.3 --janela 120`
    Saída esperada: mensagens voltam à fila, tentativas sobem, conclusão final com `done` ou `skipped`, zero duplicatas.
    Falha: qualquer linha repetida em `lead` para o mesmo `tenant_id` e e-mail.

14. **Prove isolamento com o arquivo corrompido.**
    Comando: `python3 scripts/enviar.py seed/uploads/_corrompido.bin --tenant 4211`
    Saída esperada: exatamente 3 tentativas e mensagem na DLQ; as demais planilhas do lote seguem `done`.
    Falha: arquivo ruim parando o consumo dos demais significa ausência de isolamento por mensagem; verifique `maxReceiveCount`.

15. **Mostre a DLQ e o replay controlado.**
    Comando: `python3 scripts/dlq.py listar` e depois `python3 scripts/dlq.py replay --lote 10`
    Saída esperada: 1 mensagem listada com classificação `payload_ruim`; replay de 10 mensagens no máximo, com dedup ativa.
    Falha: replay em volume ilimitado está fora do padrão; aborte e explique o risco de reinjetar o problema inteiro.

16. **Abra o `EXPLAIN` da API de status.**
    Comando: `psql "$DB_URL" -c "EXPLAIN (ANALYZE, BUFFERS) SELECT id, status, row_count, created_at FROM import_batch WHERE tenant_id = 4211 ORDER BY created_at DESC, id DESC LIMIT 50;"`
    Saída esperada: plano usando `idx_import_tenant_created`, linhas retidas ≈ 50, sem varredura completa da tabela.
    Falha: `Seq Scan` em tabela grande significa índice ausente ou seletividade ruim; não prometa p95 sem corrigir.

17. **Teste a paginação por cursor em duas páginas.**
    Comando: `python3 scripts/listar.py --tenant 4211 --cursor "2026-09-28T14:03:11.120Z"` (executar 2× encadeando o cursor).
    Saída esperada: nenhuma linha repetida nem pulada entre as páginas, mesmo com importação nova chegando no meio.
    Falha: item repetido indica paginação por `OFFSET`; isso é anti-padrão do standard.

18. **Demonstre rollback cronometrado.**
    Comando: `aws lambda update-alias --function-name process_upload --name live --function-version 3` e em seguida a troca de volta para a versão anterior.
    Saída esperada: consumo retoma em menos de 2 minutos (meta) com a fila intacta.
    Falha: rollback acima de 5 minutos ou fila perdida significa deploy com estado compartilhado; reavalie o ADR.

19. **Feche com os quatro números do dashboard.**
    Comando: `python3 scripts/dashboard.py`
    Saída esperada: idade da mensagem mais antiga, tamanho da DLQ, duração p95 e custo do dia, com status verde/amarelo/vermelho.
    Falha: dashboard sem os quatro sinais significa observabilidade incompleta; o handoff não pode ser dado.

20. **Encerre nos próximos passos e abra para perguntas.**
    Fala: `trace_id` ponta a ponta, dedup persistente no lugar do `set` em memória, molde repetido nos workers de agentes.
    Saída esperada: perguntas do roteiro de domínio respondidas em menos de 1 minuto cada.
    Falha: pergunta sem resposta vira item de estudo registrado no PDI na própria hora.

## Rollback geral da demo

Se qualquer passo falhar de forma estrutural: `terraform apply -replace` não é caminho. Restaure a versão anterior da função pelo alias, pause o consumer (`aws lambda update-event-source-mapping --maximum-batching-window 0` somente em ambiente de teste), limpe os dados de seed com `python3 scripts/limpar_seed.py --tenant 4211` e registre o motivo da parada no relatório da demo.

Material de apoio: pdi-fullstack-modelagem-dados-a3-report.pdf (dossiê completo).
