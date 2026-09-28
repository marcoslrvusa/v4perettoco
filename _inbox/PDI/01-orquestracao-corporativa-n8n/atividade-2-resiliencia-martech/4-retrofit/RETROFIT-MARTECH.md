# RETROFIT: Como adaptar workflows MarTech existentes ao padrão PDI-MARTECH

> Objetivo: transformar workflows síncronos frágeis em pipelines assincronos
> resilientes SEM reescrever a lógica de negócio existente.

## 1. Workflows MarTech comuns que precisam de retrofit

| Workflow atual | Problema | Mudança |
|----------------|----------|---------|
| Importação de pedidos (SPA → CRM) | Síncrono, trava em payload grande | Gateway + Worker + Heavy Payload |
| Sincronização de contatos (CRM push) | Falha some, cliente descobre | Envelope padrão → Observabilidade |
| Enriquecimento de leads (API externa) | Rate limit derruba a execução | Fila com backoff + circuit |
| Exportação de relatórios (grandes) | Timeout do webhook | Job assíncrono + status polling |

## 2. Passo a passo genérico

### 2.1 Queue Gateway

```ts
// Antes (workflow atual)
Webhook → [lógica pesada 1] → [lógica pesada 2] → Respond

// Depois
Webhook → [CC] MT Queue Gateway  (enfileira + ACK 202)
        → [CC] MT - Queue Worker  (delega)
        → [CC] MT - Heavy Payload Processor (lógica pesada)
```

### 2.2 Camada de observabilidade

O workflow que fala com o CRM passa a chamar o webhook `/mt/crm-sync`
ao FINAL, com o envelope padrão:

```json
{
  "syncId": "job-123",
  "object": "order",
  "direction": "push",
  "client": "genics",
  "expected": 120,
  "synced": 118,
  "http_status": 200,
  "execution_url": "https://n8n.../executions/...",
  "payload": "<opcional>",
  "response": "<opcional>"
}
```

O Observabilidade calcula hash, drift e atualiza `mt_crm_health`.

## 3. Regras de retrofit

1. **Não mudar a lógica de negócio** no retrofit: só o transporte.
2. **Job keys estáveis**: `queue:object:id` para idempotência.
3. **Checkpoint em jobs > 5 min**: `mt_job_progress` com chunk_index.
4. **Sempre enviar envelope** ao Observabilidade (mesmo em erro).
5. **Backoff exponencial** no retry (30s → 1m → 2m), max 3 tentativas.
6. **Circuit breaker** (atividade 1) protege a integração externa.

## 4. Checklist por workflow retrofitado

- [ ] Fluxo passa pelo Gateway (ACK 202)
- [ ] Payload > 100 itens usa chunks com progresso
- [ ] Envelope de sync enviado ao `/mt/crm-sync`
- [ ] `mt_sync_log` registra done/error
- [ ] Drift detectado gera `mt_sync_delta`
- [ ] Erros entram no Error Handler Central (atividade 1)
- [ ] Workflow continua ativo com mesmo trigger

## 5. Exemplo completo (Sincronização de pedidos Kommo)

```
Kommo Webhook (novo pedido)
  → [retrofit] Envelope padrão montado no Code node
  → [CC] MT Queue Gateway      (job: pedido:sync:123, ACK 202)
  → [CC] MT - Queue Worker     (slot 1/5, running)
  → [CC] MT - Heavy Payload    (normaliza itens, enriquece, progresso)
  → Kommo API (push)           (circuit protegido)
  → [CC] MT - CRM Sync Obs     (mt_sync_log done, health +1)
  └── drift? → mt_sync_delta → alerta 15 min (antecipando cliente)
```

## 6. Esforço por tipo de retrofit

Estimativas com parâmetros declarados, para planejar a fila de trabalho:

| Tipo | Toques no workflow | Esforço (meta) | Risco |
|------|--------------------|----------------|-------|
| Só transporte (fila + ACK) | Trocar o caminho antes do trabalho pesado | 1 a 2 h | Baixo |
| Fila + observabilidade | Transporte mais envelope no final | 2 a 4 h | Baixo |
| Fila + observabilidade + chunking | Acrescenta SplitInBatches e checkpoint | 4 a 8 h | Médio |
| Caso completo (tudo acima + circuit) | Refaz o fluxo de erro da integração | 8 a 12 h | Alto |

**Exemplo numérico:** retrofit de quatro workflows (dois simples, um médio, um
completo) dá $2 + 2 + 6 + 10 = 20$ horas de esforço (meta). Com dois dias úteis
de foco, a fila inteira cabe em uma semana de trabalho, sem considerar
homologação.

## 7. Erros clássicos de retrofit

1. **Trocar o transporte e manter o trabalho pesado no webhook.** O Gateway
   precisa ser o primeiro node depois do Webhook, senão nada mudou.
2. **Gerar `job_key` com timestamp.** Quebra a idempotência e permite que o mesmo
   evento vire três jobs distintos.
3. **Esquecer o envelope no ramo de erro.** É exatamente quando o CRM falha que a
   trilha é mais necessária; enviar só no sucesso cria viés de sobrevivência nos
   dados.
4. **Mover o `expected` para depois da confirmação.** Se o valor esperado é
   calculado com base no que o CRM retornou, o drift nunca dispara.
5. **Manter dois caminhos em paralelo (antigo e novo).** Dupla escrita e métrica
   corrompida; o retrofit troca o caminho, não duplica.

## 8. Critérios de aceite do retrofit

- [ ] Latência do ACK abaixo de 2 s medida com o fluxo real.
- [ ] Nenhum node de negócio antes do Gateway.
- [ ] `job_key` determinístico e testado com dois eventos iguais.
- [ ] Payload acima de 100 itens percorrendo chunks com progresso visível.
- [ ] Envelope enviado nos ramos de sucesso **e** de erro.
- [ ] Linha criada em `mt_sync_log` para cada tentativa de sync.
- [ ] `error_class` preenchido no caminho de falha.
- [ ] Disjuntor de circuito da atividade 1 protegendo a chamada externa.
- [ ] Workflow legado desativado no mesmo dia da ativação do novo.
- [ ] Backfill histórico decidido: migrar, reprocessar ou aceitar lacuna.
- [ ] Rollback documentado em uma linha: qual botão desligar.