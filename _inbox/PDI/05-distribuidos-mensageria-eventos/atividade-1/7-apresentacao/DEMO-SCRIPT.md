# Roteiro de Demo: Sistemas Distribuídos com Mensageria (fila, tópico, DLQ)

Abra o deck (index.html) e percorra os slides na ordem.

Duração total: (meta) 12 minutos, sendo 7 de demonstração e 5 de defesa.

## Pré-requisitos

1. Docker ativo e porta 5672 (AMQP) livre no host.
2. `python3` com `boto3`/cliente do broker instalado, conforme `2-code/consumer.py`.
3. Credenciais do broker já no ambiente; nenhuma senha digitada em tela.
4. Arquivo `2-code/topic_contracts.json` presente (contrato dos tópicos).

## Seed (preparação de dados)

```bash
# 1. subir o broker declarado em infra/broker.tf (ambiente de homologação)
terraform -chdir=infra init && terraform -chdir=infra apply -auto-approve
```

- **Saída esperada:** `Apply complete! Resources: N added`.
- **Se falhar:** porta 5672 ocupada ou daemon do Docker parado; derrube o processo que ocupa a
  porta e reexecute. Não siga com a demo sem broker de pé, senão todos os passos seguintes
  falham em cascata.
- **Rollback:** `terraform -chdir=infra destroy -auto-approve`.

## Passos da demo

1. **Slide de Resumo:** abra com o problema de negócio e o blast radius.
   - Fala: um serviço cai e três times param.
   - Critério de falha: não citar o `>= 200 msg/s` do SLO. Se esquecer, volte ao Slide 20
     (Métricas e SLO).

2. **Slide do ADR:** defenda a opção escolhida vs as rejeitadas (trade-offs).
   - Fala: fila para trabalho exclusivo, tópico para evento difundido, HTTP síncrono rejeitado
     por cascata.
   - Critério de falha: não nomear a perda de cada opção. Se perguntarem "e o que você perde?",
     responda "operação e plantão".

3. **Publicar 1.000 mensagens de teste** (início da demo técnica).
   ```bash
   python3 2-code/consumer.py --publish --count 1000 --topic venda.criada
   ```
   - **Saída esperada:** `publicadas=1000 em 4.8s` (Exemplo numérico de saída; o tempo real
     depende da máquina).
   - **Se falhar:** contraste de tópico ou credencial; confira o contrato em
     `2-code/topic_contracts.json` antes de seguir.

4. **Derrubar o consumer** no meio do lote.
   ```bash
   pkill -f "consumer.py --consume" ; sleep 2
   ```
   - **Saída esperada:** processo encerrado e `queue.depth` estável acima de zero no painel.
   - **Critério de falha:** se `queue.depth` for a zero, ou o processo não morreu, ou o ACK está
     sendo enviado antes do commit (erro grave). Corrija antes de continuar.

5. **Confirmar represamento sem perda:** meça a fila com o consumer fora.
   ```bash
   python3 2-code/consumer.py --stats --queue cobranca.v1
   ```
   - **Saída esperada:** `depth >= 1000`, `unacked=0`.
   - **Se falhar (depth=0):** mensagens sumiram; trate como incidente e interrompa a demo. Esse
     é exatamente o cenário que a atividade existe para evitar.

6. **Religar o consumer** e observar o reprocessamento.
   ```bash
   python3 2-code/consumer.py --consume --prefetch 10 --queue cobranca.v1 &
   ```
   - **Saída esperada:** contagem final `processadas=1000` e `queue.depth=0`.
   - **Critério de aceite C1:** processadas igual a publicadas, mesmo havendo reentrega.
   - **Rollback deste passo:** `pkill -f "consumer.py --consume"` e reexecutar o item 4.

7. **Mostrar a duplicata sendo absorvida:** consulte a tabela de dedup.
   ```bash
   python3 2-code/consumer.py --stats --dedup
   ```
   - **Saída esperada:** `entregas > 1000`, `efeitos_unicos = 1000`.
   - **Fala:** entrega é at-least-once, efeito é único porque a chave foi registrada na mesma
     transação. É a ponte para a Atividade 2 (`05-A2`).

8. **Injetar payload inválido** para provar a DLQ.
   ```bash
   python3 2-code/consumer.py --publish --topic venda.criada --payload-file /tmp/msg-invalida.json
   ```
   - **Saída esperada:** `dlq.depth = 1` e `queue.depth = 0`; no log,
     `motivo=parse: campo obrigatorio ausente`.
   - **Critério de falha:** se a mensagem voltar para a fila em laço (`requeue`), o `Nack` está
     errado. Interrompa e corrija para `requeue=False`.

9. **Reprocessar a DLQ pelo runbook.**
   ```bash
   python3 2-code/consumer.py --dlq-replay --queue cobranca.v1.dlq --dry-run
   ```
   - **Saída esperada:** `dry_run: 1 mensagem seria reprocessada`, sem efeito aplicado.
   - **Fala:** primeiro `dry_run`, depois execução real. Replay sem `dry_run` é como deploy sem
     teste.
   - **Rollback:** não aplicar; a mensagem permanece na DLQ.

10. **Demonstrar backpressure:** reduza o `prefetch` e deixe o produtor correr mais rápido.
    ```bash
    python3 2-code/consumer.py --consume --prefetch 2 --queue cobranca.v1
    ```
    - **Saída esperada:** `queue.depth` sobe, `rss_mb` do consumer estável (variação < 10%).
    - **Critério de falha:** se `rss_mb` subir junto com a fila, o backpressure está no lugar
      errado. Não siga; explique o anti-padrão e corrija o `prefetch`.

11. **Medir o throughput** contra a meta de 200 msg/s.
    ```bash
    python3 2-code/consumer.py --bench --duration 60 --prefetch 30
    ```
    - **Saída esperada:** `throughput >= 200 msg/s` sustentado por 60 s.
    - **Se ficar abaixo:** aumente a concorrência (workers) e não o `prefetch`; a conta
      `$capacidade = workers / W$` diz o limite real.

12. **Mostrar a ordem por chave:** publique 100 eventos da mesma `entity_id`.
    ```bash
    python3 2-code/consumer.py --publish --count 100 --key cliente-42 --version-seq
    ```
    - **Saída esperada:** consumidor registra versões `1, 2, 3, ... 100` sem inversão.
    - **Critério de falha:** qualquer inversão de `entity_version` significa partição errada ou
      consumidor paralelo sobre a mesma chave.

13. **Quebrar a ordem propositalmente** (o que não devemos fazer).
    ```bash
    python3 2-code/consumer.py --publish --count 100 --key-null
    ```
    - **Saída esperada:** versões fora de ordem no consumidor.
    - **Fala:** sem chave, o produtor faz round-robin e a ordem por entidade desaparece. Esse é
      o teste que convence quem diz "ordem não importa".

14. **Slide de Validação/Rollout:** mostre como provamos em produção.
    - Fala: os três testes T1 (perda), T3 (DLQ) e T4 (backpressure) rodam na esteira antes de
      qualquer troca de versão do consumer.
    - Critério de falha: não citar o critério de aceite numérico de cada teste.

15. **Slide de falha e recuperação:** abra o modo de falha real.
    - Fala: consumer cai, fila cresce, ACK não foi dado, reentrega acontece sozinha; recuperação
      em minutos.
    - Evidência: a tabela de modos de falha do `README.md`.

16. **Slide de Riscos:** apresente o plano de mitigação.
    - Fala: duplicata (mitigada em `05-A2`), DLQ esquecida (mitigada com alerta e dono),
      `prefetch` mal calibrado (mitigado por Little's Law).
    - Critério de falha: risco sem dono nomeado. Se não houver dono, o item não está fechado.

17. **Mostrar a telemetria** que sustenta o SLO.
    - Verifique `queue.depth`, `consumer.unacked`, `dlq.depth`, `redelivery.rate`,
      `e2e.latency.p95`.
    - Critério de falha: métrica com rótulo de `entity_id` ou `order_id` (cardinalidade
      descontrolada). Sinalize como melhoria antes de ir a produção.

18. **Rodar o checklist de domínio** junto do público.
    - Percorra os 15 itens do `README.md` e marque os executados nesta demo (T1, T3, T4, T10).
    - Critério de falha: item marcado sem evidência de execução.

19. **Fecho com números.**
    - `>= 200 msg/s`, `0` perdidas, p95 `< 5 s` (meta), DLQ revisada em `< 24 h`.
    - Critério de falha: prometer número que não apareceu no teste da demo. Diga "meta", não
      "resultado".

20. **Encerramento e rollback final.**
    ```bash
    pkill -f "consumer.py --consume" ; terraform -chdir=infra destroy -auto-approve
    ```
    - **Saída esperada:** broker destruído, portas liberadas.
    - **Se falhar:** deixe o ambiente declarado e registre o pendente; nunca finalize a demo com
      processo órfão consumindo fila.

## Material de apoio

Material de apoio: pdi-distribuidos-mensageria-eventos-a1-report.pdf (dossiê completo).

Também usados nesta demo: `1-standards/MESSAGING.md` (regras), `1-standards/MESH-ARCHITECTURE.md`
(topologia), `README.md` (SLO, invariantes e checklist) e `infra/broker.tf` (seed).
