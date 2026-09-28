# Multi-Agente: Padrão

```
Supervisor (roteia)
  |-> Triagem
  |-> Consulta (RAG)
  |-> Proposta
```
1. Handoff explícito: {from, to, intent, payload, trace_id}.
2. Contexto isolado: cada agente só recebe o payload.
3. Timeout por agente (15s) -> volta ao supervisor.
4. Max hops: impede loop.
5. Supervisor leve (modelo barato).

## 1. Escopo e não-escopo

**Escopo.** Este padrão cobre a orquestração de tarefas compostas de duas a quatro etapas em que cada etapa tem
papel, ferramenta e tolerância a falha diferentes. Cobre o contrato de handoff, o isolamento de contexto, o
teto de tempo por etapa, o limite de saltos, a retomada por estado e a telemetria mínima para operar tudo
isso em produção.

**Não-escopo.** Não cobre treino ou ajuste fino de modelo. Não define o conteúdo dos prompts individuais de
cada worker, que fica com a trilha de avaliação. Não substitui o protocolo assíncrono descrito em
`MULTIAGENT-PROTOCOL.md`, que cuida de fila, ordem e entrega. Não decide a política de retenção de dados,
que é assunto de segurança.

## 2. Termos

- **Supervisor:** componente stateless que classifica intenção, monta handoff, conta saltos e nunca executa
  ferramenta.
- **Worker (agente especialista):** executa um único papel com ferramentas privativas e contexto próprio.
- **Handoff:** mensagem tipada que atravessa a fronteira entre dois papéis.
- **Hops:** quantidade de handoffs consumidos na execução atual de uma tarefa.
- **Criticador:** agente que avalia a saída de cada execução e escreve lição consolidada.
- **Recall@k:** fração de documentos relevantes presentes nos `k` primeiros resultados de uma busca vetorial,
  métrica de aceite do worker de consulta.
- **Reranking:** reordenação dos candidatos da busca por um modelo de pontuação, sempre depois da busca bruta.

## 3. Regra canônica

A regra é simples e verificável: **o custo de um salto é o tamanho do payload, e o custo de um erro é o tamanho
do contexto compartilhado.** Portanto o padrão minimiza os dois ao mesmo tempo ao proibir contexto global.

Fórmula de orçamento de salto:

```text
H_max = floor((L_tarefa - L_roteio) / (L_etapa_p95 + L_handoff))
```

com $H_{max}$ igual a máximo de saltos permitidos, $L_{tarefa}$ o teto ponta a ponta em segundos,
$L_{roteio}$ a sobra do supervisor por decisão, $L_{etapa_p95}$ a latência esperada da etapa mais lenta e
$L_{handoff}$ o custo de serializar e validar a mensagem.

**Exemplo numérico:** parâmetros declarados: $L_{tarefa} = 30$ s, $L_{roteio} = 0,4$ s por decisão com duas
decisões, $L_{etapa\_p95} = 3,2$ s e $L_{handoff} = 0,15$ s. Então $H_{max} = \lfloor (30 - 0,8) / (3,2 + 0,15)
\rfloor = \lfloor 8,72 \rfloor = 8$. Com teto de hops igual a 8, um loop de re-rota custa no máximo 8 saltos
antes de abortar, e o pior caso de tempo gasto é de aproximadamente 8 x 3,35 s + 0,8 s = 27,6 s, ainda dentro
do teto de 30 s.

Fórmula de orçamento de payload:

```text
tokens(handoff) = tokens(entidade) + tokens(resumo) + tokens(contrato)
```

O contrato é fixo (cerca de 80 tokens). O resumo tem teto rígido. A entidade é o dado de negócio mínimo. O
payload que estourar o teto é cortado na origem, com erro de validação, e nunca comprimido às cegas pelo
supervisor.

## 4. Tabela de decisão

| Condição A | Condição B | Decisão |
| --- | --- | --- |
| Tarefa tem mais de 2 etapas | Etapas têm ferramentas distintas | Supervisor + workers isolados |
| Tarefa tem 1 etapa | Sem dependência entre partes | Worker único, sem supervisor |
| Etapa falha por timeout | Existe worker de reserva do mesmo papel | Re-rota imediata para a reserva |
| Etapa falha por timeout | Não existe reserva | Retorno com erro tipado e estado preservado |
| Payload excede o teto | Resumo já foi gerado | Cortar e validar na origem, abortar o salto |
| Salto excede `max_hops` | Sempre | Abortar com erro `loop_detectado` |
| Consulta vetorial devolve 0 citações | Sempre | Status `sem_suporte`, sem geração de texto |
| Entrada do usuário contém instrução de sistema | Sempre | Tratar como dado, nunca como instrução |
| Efeito externo é irreversível | Sempre | Confirmação humana antes de executar |

## 5. Exemplo numérico de jornada completa

**Exemplo numérico:** parâmetros declarados: intenção "montar proposta para cliente X", três etapas.
Triagem consome 1,8 s e 900 tokens de entrada. Handoff 0,15 s e 400 tokens. Consulta RAG consome 3,2 s,
recupera 8 candidatos, reranking reduz para 3, consome 2.400 tokens. Handoff 0,15 s e 500 tokens. Proposta
consome 2,6 s e 2.100 tokens. Total de tempo: 1,8 + 0,15 + 3,2 + 0,15 + 2,6 = 7,9 s, contra teto de 30 s.
Total de tokens de entrada: 900 + 400 + 2.400 + 500 + 2.100 = 6.300, ou 79 por cento dos 8.000 do antigo
prompt monolítico, mas distribuídos em prompts que cada modelo enxerga inteiro e em isolamento. Hops usados:
2 de um máximo de 8.

## 6. Anti-padrões

O que o sênior reprovaria na revisão:

- **Contexto global "por enquanto".** Passar o histórico inteiro para economizar uma chamada de resumo troca
  privacidade por conveniência e é a causa clássica de vazamento entre etapas.
- **Timeout por tentativa sem contador.** Retry infinito disfarçado de resiliência transforma um worker lento
  em fila infinita.
- **Supervisor com ferramenta.** No momento em que o supervisor executa ação, a fronteira de permissão some e
  o teste deixa de isolar papéis.
- **Handoff em JSON livre.** Sem esquema validado, o worker seguinte aceita lixo e devolve alucinação coerente.
- **Memória só em prompt.** Se a retomada depende de replay de conversa, qualquer corte de contexto perde o
  estado da tarefa.
- **Métrica só de sucesso final.** Sem latência por etapa e tokens por salto, o incidente só aparece quando o
  usuário reclama.
- **Avaliação visual "parece bom".** Sem conjunto-ouro e critério de aceite numérico, regressão de prompt passa
  despercebida.
- **Reindexar junto com troca de prompt.** Duas variáveis mudando ao mesmo tempo tornam a queda de recall
  inexplicável.

## 7. Telemetria

| Métrica | Tipo | Cardinalidade | Alerta |
| --- | --- | --- | --- |
| `handoff_latency_ms` | histograma | origem, destino | p95 acima de 400 ms por 5 min |
| `worker_duration_ms` | histograma | papel | p95 acima de 15 s por 1 ciclo |
| `handoff_total` | contador | origem, destino, resultado | queda brusca de volume |
| `hops_consumed` | histograma | intenção | cauda acima de 6 saltos |
| `fallback_triggered` | contador | motivo | qualquer ocorrência em produção |
| `ctx_isolation_violation` | contador | teste | zero tolerado, incidente P0 |
| `rag_citations_count` | histograma | coleção | massa em zero |
| `rag_recall_at_k` | gauge | coleção | abaixo da meta de avaliação |
| `tokens_per_hop` | histograma | papel | crescimento sustentado entre versões |

Regra de cardinalidade: proibido usar `trace_id` como rótulo de métrica. `trace_id` vai para log estruturado e
trace distribuído, nunca para a base de séries, senão o custo de observabilidade explode.

## 8. Plano de teste

O plano cobre três eixos: contrato, degradação e conteúdo. Contrato prova que mensagem inválida não entra.
Degradação prova que o sistema falha bonito, com estado preservado e tempo conhecido. Conteúdo prova que o
worker de consulta devolve suporte e não opinião. Todo caso tem saída esperada e critério de aceite, porque
teste sem critério vira confirmação de que o código roda.

| Caso | Entrada esperada | Critério de aceite |
| --- | --- | --- |
| Jornada feliz de 3 etapas | Intenção válida | Concluí em <= 30 s com 2 saltos |
| Timeout forçado no worker de consulta | Worker que não responde | Re-rota em <= 15 s, estado preservado |
| Cadeia cíclica entre dois workers | Classificador brigando | Aborta em `max_hops` com erro tipado |
| Payload acima do teto | Handoff inchado | Rejeição na origem, sem envio |
| Base vetorial vazia | Consulta sem correspondência | Status `sem_suporte`, zero texto gerado |
| Reentrega da mesma mensagem | Mesmo `trace_id` duas vezes | Efeito externo executado 1 vez |
| Entrada com prompt injection | Texto com ordem de sistema | Tratado como dado, sem mudança de papel |
| Retomada após corte de processo | Processo morto no meio | Retoma do último handoff válido |
| Unicode e texto vazio | Acentos, emoji, string vazia | Validação responde sem exceção vazada |
| PII no payload | CPF e e-mail no texto | Não aparece no worker seguinte nem no log |

## 9. Checklist de adesão

1. Esquema de handoff versionado e validado na entrada de todo worker.
2. Teto de timeout por papel configurado e monitorado, com valor de 15 s como padrão.
3. `max_hops` derivado da fórmula de orçamento, não escolhido a olho.
4. Contexto construído por função pura que aceita apenas o payload declarado.
5. Supervisor sem ferramentas registradas.
6. Estado persistido por salto, permitindo retomada sem replay de conversa.
7. Efeito externo protegido por chave de idempotência.
8. Worker de consulta como único detentor da credencial de leitura do índice.
9. Citação obrigatória na resposta final, com teste automatizado.
10. Métricas de latência, hops, tokens por salto e fallback emitidas.
11. Conjunto-ouro por papel com critério de aceite numérico antes de publicar prompt.
12. Runbook de timeout, fila e índice acessível e testado.
13. Decisão arquitetural registrada com alternativas descartadas.
14. Varredura de PII na saída de cada worker em ambiente de homologação.

## 10. Fluxo de execução do supervisor

O supervisor é uma função previsível: entra intenção, sai salto. Ele não tem memória própria, não tem
ferramenta e não conhece o conteúdo do payload além do tamanho, que é o que ele precisa para validar o teto.

```python
MAX_HOPS = 8          # derivado da fórmula de orçamento de latência
TIMEOUT_S = 15        # teto por worker
TETO_PAYLOAD = 8_192  # bytes de payload serializado

async def supervisor(tarefa: dict, estado: Estado | None = None) -> Resultado:
    """Roteia, conta salto e devolve. Nunca executa ferramenta."""
    estado = estado or Estado.trace_novo(tarefa)
    if estado.hops >= MAX_HOPS:
        raise LoopDetectado(trace_id=estado.trace_id, hops=estado.hops)

    intencao = await classificar(tarefa, estado.resumo)
    destino = MAPA_PAPEL[intencao]
    if not await saudavel(destino):
        destino = MAPA_FALLBACK[intencao]   # worker de reserva do mesmo papel

    handoff = Handoff(
        trace_id=estado.trace_id,
        seq=estado.hops + 1,
        origin="supervisor",
        dest=destino,
        intent=intencao,
        payload=resumir(estado, teto=TETO_PAYLOAD),
    )
    handoff.validate()

    try:
        saida = await executar_com_timeout(destino, handoff, TIMEOUT_S)
    except TimeoutError:
        await metrica("fallback_triggered", motivo="timeout", papel=destino)
        raise                                    # estado ja persistido, re-rota decide
    await gravar_estado(estado.trace_id, saida)
    return saida
```

Pontos que a revisão deve procurar nesse trecho: `validate()` antes de qualquer envio, contagem de saltos no
começo e não no fim, persistência de estado antes de tratar erro, e nenhuma chamada de ferramenta em lugar
algum.

## 11. Avaliação por papel

Cada papel tem o seu próprio conjunto-ouro e o seu próprio critério de aceite. Média agregada de "acurácia do
sistema" esconde a regressão de um único worker atrás do desempenho dos outros, e é justamente esse o erro
mais comum em avaliação de sistema multi-agente.

| Papel | Métrica principal | Critério de aceite | Janela |
| --- | --- | --- | --- |
| Supervisor | Acerto de intenção | >= 95 por cento | por release |
| Triagem | F1 na classificação de urgência | >= 0,90 | por release |
| Consulta RAG | Recall@k no conjunto-ouro | >= 0,85 com `ef_search` declarado | por release |
| Proposta | Ausência de afirmação sem citação | 100 por cento das frases factuais citadas | por release |
| Global | Sucesso de tarefa composta | >= 95 por cento | 30 dias rolantes |

Regras de avaliação:

1. O conjunto-ouro é versionado no repositório e muda por revisão explícita, nunca junto com o prompt.
2. Toda rodada registra a versão do prompt, o valor de `ef_search`, o `top_k` e a data, para que a comparação
   seja entre configurações conhecidas.
3. Variável por vez: trocar prompt e reindexar na mesma janela torna a queda de recall inexplicável.
4. Caso de borda obrigatório em toda rodada: texto vazio, unicode, acentuação pesada e payload no limite do
   teto.
5. Regressão em qualquer papel bloqueia a publicação, mesmo que a média agregada esteja acima da meta.

## 12. Referências de estudo

- Curso: Multi-AI Agent Systems with LangGraph, plataforma DeepLearning.AI.
- Vídeo: Padrões de orquestração com supervisor e handoff, plataforma YouTube, canal LangChain.
- Doc oficial: Documentação do LangGraph para grafos de agentes, documentação oficial LangChain.
- Doc oficial: Guia de function calling e structured outputs, documentação oficial OpenAI.
