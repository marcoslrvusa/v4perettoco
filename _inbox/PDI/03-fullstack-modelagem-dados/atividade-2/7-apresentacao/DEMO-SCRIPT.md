# Roteiro de Demo: APIs Modulares de Missão Crítica (FastAPI) com Paginação, Cache e Rate Limiting

Abra o deck (index.html) e percorra os slides na ordem.

## Pré-requisitos

- Ambiente de homologação com a API instalada a partir de `2-code/requirements.txt`.
- PostgreSQL com a tabela de exemplo carregada e índice composto criado.
- Redis local respondendo a `redis-cli PING` com `PONG`.
- Ferramenta de carga k6 instalada.
- Coletor de métricas ligado para exibir p95 e hit rate em tela.
- Seed de ao menos 80.000 linhas para a demonstração de página profunda ser honesta.

## Comandos de seed e verificação de base

```bash
# 1) Confirmar Redis vivo
redis-cli PING
# Saída esperada: PONG
# Se falhar: o demo de cache não roda; suba o Redis antes de continuar.

# 2) Contar linhas de exemplo
psql -c "SELECT count(*) FROM leads;"
# Saída esperada: 80000 (Exemplo numérico do seed)
# Se falhar: não há volume para provar página profunda; carregue o seed.

# 3) Confirmar o índice
psql -c "\d leads" | grep idx_leads_created_id
# Saída esperada: idx_leads_created_id
# Se falhar: crie com CREATE INDEX CONCURRENTLY antes de qualquer carga.

# 4) Zerar contador de cache para a demonstração ficar limpa
redis-cli FLUSHDB
# Saída esperada: OK
# Se falhar: pare e corrija o Redis; sem isso o HIT/MISS é inconclusivo.
```

## Passos da demo

1. **Abra o deck (index.html)** e percorra os slides na ordem. Fale o problema de negócio antes de qualquer detalhe técnico.
2. **Slide de Resumo:** abra com o problema de negócio e o blast radius. Critério: o ouvinte entende que o alvo é o Postgres compartilhado.
3. **Demonstre a página profunda sem cursor.** Comando: `curl -s "http://localhost:8000/v1/leads_old?offset=79950&limit=50" | jq '.items | length'`. Saída esperada: `50` com latência alta (Exemplo numérico: ordem de segundos). Se falhar: confirme o seed de 80k. Se der rápido demais, o volume está baixo, acrescente linhas.
4. **Colete o plano da query antiga.** Comando: `psql -c "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM leads ORDER BY created_at DESC OFFSET 79950 LIMIT 50;"`. Saída esperada: linhas lidas na casa de dezenas de milhares. Se aparecer índice cobrindo o descarte, é esperado: o índice não elimina a leitura das linhas anteriores, só a ordenação em memória.
5. **Demonstre a mesma página com cursor.** Comando: `curl -s "http://localhost:8000/v1/leads?after=<cursor>&limit=50" -w '%{time_total}\n'`. Saída esperada: `50` itens e tempo na casa de milissegundos. Se falhar: confirme o índice composto e o formato do cursor.
6. **Slide de Modelo mental:** explique os três portões baratos antes do banco. Critério: o ouvinte repete a ordem (identidade, balde, cache).
7. **Slide de Arquitetura:** percorra o diagrama mermaid do fluxo. Fale por que o rate limit vem antes do cache.
8. **Slide do ADR:** defenda a opção escolhida vs as rejeitadas (trade-offs). Use a tabela de alternativas descartadas.
9. **Slide de Matemática:** apresente a conta `50.050` contra `51` linhas lidas e o fator `981`. Critério: ninguém pergunta "de onde saiu esse número", porque os parâmetros estão declarados.
10. **Slide de Token bucket:** apresente a recarga com `Δs = 48` dando `80` tokens. Critério: o ouvinte entende o `Retry-After` como consequência do balde, não como número fixo.
11. **Demonstre o primeiro acesso à lista.** Comando: `curl -i "http://localhost:8000/v1/leads?limit=50" | grep -i x-cache`. Saída esperada: `X-Cache: MISS`. Se falhar: confirme que o Redis está limpo (passo 4 do seed).
12. **Demonstre o segundo acesso.** Comando: repita o mesmo `curl`. Saída esperada: `X-Cache: HIT` e resposta em milissegundos. Se falhar: verifique se a chave inclui o mesmo cliente e o mesmo cursor, e se o TTL não venceu entre as chamadas.
13. **Prove a invalidação por escrita.** Comando: `curl -X POST http://localhost:8000/v1/leads -H 'Content-Type: application/json' -d '{"nome":"demo"}'` e, em seguida, repita o `curl` do passo 12. Saída esperada: `X-Cache: MISS` depois da escrita. Se falhar: o caminho de escrita não está invalidando o prefixo; corrija antes de mostrar em produção.
14. **Demonstre o estouro de quota.** Comando: `for i in $(seq 1 101); do curl -s -o /dev/null -w '%{http_code}\n' "http://localhost:8000/v1/leads?limit=10"; done | sort | uniq -c`. Saída esperada: 100 vezes `200` e 1 vez `429`. Se falhar: confirme que nenhuma outra requisição consumiu tokens na janela e que o balde está no Redis.
15. **Confirme o cabeçalho de recarga.** Comando: `curl -i "http://localhost:8000/v1/leads?limit=10" | grep -i retry-after`. Saída esperada: `Retry-After` com número de segundos coerente com a recarga de um token. Se falhar: a configuração do balde não está devolvendo o cabeçalho.
16. **Slide de Validação/Rollout:** mostre como provamos em produção, com o plano de 12 casos e o critério de aceite de cada um.
17. **Demonstre o envelope de erro.** Comando: `curl -s "http://localhost:8000/v1/leads?after=abc" | jq .`. Saída esperada: objeto com `code`, `message` e `trace_id`, sem stack trace. Se aparecer stack: bloqueie a publicação, o handler global não está cobrindo essa exceção.
18. **Demonstre a degradação com Redis fora.** Comando: `redis-cli shutdown nosave`, e em seguida repita o `curl` do passo 11. Saída esperada: `200` pelo caminho do banco. Se falhar: o fallback não está ativo, corrija antes de sair do modo contingência.
19. **Restaure o Redis.** Comando: suba o serviço e confirme com `redis-cli PING` retornando `PONG`. Saída esperada: `PONG`. Se falhar: pare a demo e comunique; sem Redis o hit rate não pode ser mostrado.
20. **Slide de Métricas:** exiba p95 do hit, hit rate e proporção de 429. Compare com as metas (`p95 < 200 ms`, `hit rate >= 90%`).
21. **Slide de Modos de falha:** apresente a tabela com sintoma, causa, detecção, mitigação e tempo de recuperação.
22. **Slide de Riscos:** apresente o plano de mitigação, incluindo os riscos adicionais de backoff ausente e limpeza de índice.
23. **Slide de Orçamento de erro:** feche com `0,005 × 30 × 24 × 60 = 216` minutos e a regra de congelar mudanças ao passar de 50%.
24. **Slide de Próximos Passos:** gateway com OAuth2 e tracing OTel, explicando a ordem entre eles.

## Rollback da demo

- Para desfazer o seed: `psql -c "TRUNCATE leads;"` somente em ambiente de demonstração.
- Para zerar o balde de rate limit: `redis-cli DEL` da chave do cliente de teste, nunca `FLUSHDB` em ambiente compartilhado.
- Para voltar a versão da API: apontar o consumidor para `/v1` anterior, sem alteração de dado.

Material de apoio: pdi-fullstack-modelagem-dados-a2-report.pdf (dossiê completo).
