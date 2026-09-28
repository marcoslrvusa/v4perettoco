# Idempotência: Padrão

## Premissa
Brokers são at-least-once. Duplicata VAI acontecer. O consumidor torna o efeito único.

## Técnica
1. Cada evento tem event_id (UUID).
2. Tabela processed_events(event_id, ts) com PK única.
3. INSERT event_id antes de processar; duplicata -> pula.
4. OU upsert por chave de negócio (CNPJ).

```sql
INSERT INTO processed_events(id) VALUES ($1) ON CONFLICT DO NOTHING;
```

## Escopo e não-escopo

**Escopo**: qualquer handler cujo efeito seja irreversível ou financeiro (cobrança, débito, emissão de fatura, criação de lead, movimentação de estoque, disparo de e-mail transacional). Também entram no escopo os relays que leem outbox e os consumidores que fazem replay de histórico, porque ambos podem reenviar o que já foi aplicado.

**Não-escopo**: leituras puras sem efeito (consulta de saldo), eventos de telemetria onde duplicar métrica é aceitável, e fluxos que já são naturalmente únicos por construção (comando HTTP com `PUT` idempotente por definição). Registrar o não-escopo importa: sem ele, a revisão discute caso a caso e o padrão morre de exaustão.

## Termos

| Termo | Definição operacional |
| --- | --- |
| `event_id` | identificador único atribuído na origem; identifica a MENSAGEM |
| `idempotency_key` | identificador do EFEITO pretendido; combina `event_id` com a chave de negócio |
| Dedup | descarte de entrega repetida consultando a tabela de processados |
| Upsert | gravação que insere ou atualiza em uma única instrução |
| Reentrega | nova entrega da mesma mensagem após falha de `ack` ou reinício de sessão |
| Poison pill | mensagem que nunca processa e bloqueia a partição se não for descartada |
| Effectively-once | comportamento observado pelo negócio quando dedup + at-least-once se combinam |
| Retenção (`T`) | janela em que a chave permanece na tabela de processados |

## Regra canônica

Ordem obrigatória das operações no consumidor, sem exceção:

```
receber -> extrair chave -> INSERT da chave (ON CONFLICT DO NOTHING)
        -> se conflitou: descartar e fazer ack
        -> se inseriu: aplicar efeito -> fazer ack
```

Qualquer variação que aplique o efeito antes de gravar a chave viola o padrão. A fórmula que resume a garantia é:

$$T_{dedup} > T_{reentrega\_max} + margem$$

Se a retenção da chave for menor que a janela máxima de reentrega do broker, existe uma faixa temporal em que a chave já sumiu e a mensagem velha ainda pode chegar. Essa faixa é onde as duplicatas "misteriosas" de semanas depois nascem.

```sql
-- Garantia imposta pelo banco, não pela aplicação
CREATE TABLE processed_events (
  id TEXT PRIMARY KEY,
  ts TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON processed_events (ts);  -- suporta o expurgo por idade
```

## Tabela de decisão

| `event_id` já existe? | Chave de negócio já existe? | Efeito já aplicado? | Ação |
| --- | --- | --- | --- |
| Não | Não | Não | inserir chave, aplicar efeito, fazer `ack` |
| Sim | Sim | Sim | descartar silenciosamente, fazer `ack` |
| Sim | Não | Não | evento novo do mesmo cliente: aplicar efeito com upsert |
| Não | Sim | Sim | reentrega com `event_id` novo (regenerado por retry no produtor): descartar por chave de negócio |
| Sim | Sim | Não | quedou entre chave e efeito: reprocessar o efeito, não inserir chave de novo |
| Qualquer | Qualquer | Indeterminado | enviar para DLQ com payload completo para inspeção |

A linha 4 é a que quase todo mundo esquece: alguns produtos geram `event_id` novo a cada tentativa de envio, então dedup só por `event_id` nunca pegaria essa duplicata. Por isso a chave combinada com identificador de negócio é obrigatória, não opcional.

## Exemplo numérico

**Exemplo numérico:** pico de $\lambda = 120$ eventos/s, retenção $T = 48$ h (172.800 s), linha de 104 B.

- Linhas retidas: $120 \times 172.800 = 20.736.000$.
- Volume: $20.736.000 \times 104 \text{ B} \approx 2,2$ GB.
- Checagem por evento: 1 round-trip de 2,4 ms sobre handler de 18 ms, acréscimo de 13,3% no caminho crítico.
- Se o TTL subir para 7 dias, o volume sobe para $120 \times 604.800 = 72.576.000$ linhas, cerca de 7,5 GB. A retenção é decisão de custo, não de conveniência.

## Anti-padrões (o que o sênior reprovaria)

1. **`SELECT` antes do `INSERT` sem unicidade no banco**: dois consumidores passam pelo mesmo `SELECT` ao mesmo tempo e os dois aplicam o efeito. A correção é `INSERT ... ON CONFLICT`, que faz a arbitragem dentro do banco.
2. **Dedup só em memória**: cai no reinício do processo, que é um dos gatilhos clássicos de reentrega. Aceitável em teste unitário, inaceitável como garantia.
3. **Aplicar efeito e depois gravar a chave**: queda nessa janela deixa efeito sem registro, e a reentrega cobra de novo. É a falha mais cara do padrão.
4. **Chave igual a `event_id` puro**: não cobre reenvio com identificador regenerado nem duplicata de domínio.
5. **Sem política de expurgo**: a tabela cresce sem limite e a checagem degrada, transformando uma solução de latência num problema de armazenamento.
6. **Retry infinito sem DLQ**: um payload quebrado trava a partição inteira e transforma duplicata em indisponibilidade.
7. **Dedup sem métrica**: se ninguém mede contagem de efeito por `event_id`, o padrão pode regredir silenciosamente e ninguém percebe.

## Telemetria

| Métrica | Cardinalidade | O que alerta |
| --- | --- | --- |
| `efeitos_por_event_id > 1` | alta (por evento), agregar em janela | duplicata real, severidade alta |
| `descartos_por_duplicata` | baixa (contador) | confirma que retry está sendo absorvido |
| `linhas_processed_events` | sem etiqueta | crescimento anormal, risco de store cheio |
| `idade_minima_processed_events` | sem etiqueta | expurgo prematuro, invariante violada |
| `lag_por_particao` | média (nº de partições) | backpressure e head of line blocking |
| `entrada_em_dlq` | média (por motivo) | poison pill e payload inválido |

Regra de cardinalidade: nunca usar `event_id` como etiqueta de métrica, isso estoura a memória do coletor em minutos. Contar por janela e expor o detalhe em tabela de consultas.

## Plano de teste

| Caso | Passo | Critério de aceite |
| --- | --- | --- |
| Reentrega simples | injetar o mesmo evento 3x | exatamente 1 efeito, 2 descartes |
| Reentrega em lote | injetar o mesmo evento 5x | 1 cobrança, contagem por `event_id` = 1 |
| Concorrência | 2 processos consumindo o mesmo lote | 1 aplicação por `event_id` |
| Queda no meio | matar o processo entre efeito e `ack` | após reentrega, 0 efeitos adicionais |
| Replay | reprocessar 1 h de histórico | nenhum estado de negócio alterado |
| Poison pill | enviar payload inválido | vai para DLQ, partição segue drenando |
| Expurgo | expirar chave e reenviar mensagem antiga | não ocorre: retenção maior que janela de reentrega |
| Cobertura | rodar a consulta de handlers | 100% dos handlers com teste de reentrega |

Critério de aceite global: nenhum caso acima pode falhar em CI, e o merge fica bloqueado enquanto algum falhar.

## Checklist de adesão

1. O handler declara explicitamente sua `idempotency_key` (event_id + chave de negócio).
2. A unicidade é garantida por `PRIMARY KEY` ou `UNIQUE`, nunca só por `SELECT`.
3. A instrução de gravação usa `ON CONFLICT` para não virar erro sob concorrência.
4. A chave é gravada antes do `ack`, com teste que cobre a janela de queda.
5. A chave de partição é o identificador de negócio.
6. O `T` de dedup é maior que a janela máxima de reentrega do broker.
7. Existe índice em `ts` para o expurgo não fazer varredura completa.
8. Existe DLQ e limite máximo de tentativas.
9. Métrica de contagem de efeito por `event_id` está no dashboard.
10. Os oito casos do plano de teste rodam no CI.
11. O runbook registra rollback e quem aciona.
12. O replay sobre histórico já processado já foi executado uma vez.
13. A consulta de cobertura reporta 100% dos handlers.
14. A ADR registra as alternativas descartadas.

## Referências

- Documento oficial: PostgreSQL Documentation, INSERT ON CONFLICT (postgresql.org).
- Documento oficial: Apache Kafka Documentation, Exactly-once Semantics (kafka.apache.org).
- Vídeo: "What is Idempotency?" (YouTube, Hussein Nasser).
- Curso: "Event-Driven Architecture: From Theory to Practice" (Udemy).
