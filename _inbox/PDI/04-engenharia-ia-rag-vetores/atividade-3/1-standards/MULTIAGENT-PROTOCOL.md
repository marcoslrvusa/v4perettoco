# Protocolo Multi-Agente Assíncrono

- **Comunicação:** fila de mensagens (asyncio.Queue / Redis Streams).
- **Memória:** cada agente tem `MemoryStore` (curto + longo prazo).
- **Autoaperfeiçoamento:** loop de reflexão: após cada Run, um `CriticAgent`
  avalia a saída e escreve melhoria em `lessons.md`.
- **Supervisão:** `Orchestrator` roteia tarefas por capacidade.

## 1. Por que assíncrono

O caminho síncrono de requisição e resposta funciona até a primeira falha lenta. Se o worker de consulta demora
4 s, o HTTP da borda fica segurando conexão por 4 s; se demora 40 s, o proxy corta e o usuário vê erro mesmo
com o trabalho rodando. A fila separa o aceite da execução: a borda devolve `accepted` com `trace_id` em
milissegundos e o orquestrador trabalha no seu ritmo. Isso também cria o ponto natural de retomada, de retry e
de deduplicação, coisas que não existem numa chamada direta.

## 2. Contrato de mensagem

```python
from dataclasses import dataclass, field
from typing import Literal
import json, hashlib

@dataclass(frozen=True)
class Handoff:
    trace_id: str
    seq: int                      # ordem do salto dentro da tarefa
    origin: str
    dest: str
    intent: Literal["triagem", "consulta", "proposta", "fallback"]
    payload: dict
    produced_at: float            # epoch em segundos
    ttl_s: int = 15

    @property
    def idempotency_key(self) -> str:
        """Chave estável: repetir a mesma mensagem não duplica efeito."""
        base = f"{self.trace_id}:{self.seq}:{self.intent}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()[:32]

    def validate(self) -> None:
        """Valida contrato antes de enfileirar. Falha cedo, não no worker."""
        faltando = [c for c in ("trace_id", "seq", "origin", "dest", "intent", "payload")
                    if getattr(self, c, None) in (None, "")]
        if faltando:
            raise ValueError(f"handoff invalido, campos ausentes: {faltando}")
        if self.intent not in ("triagem", "consulta", "proposta", "fallback"):
            raise ValueError(f"intent desconhecido: {self.intent}")
        if len(json.dumps(self.payload, ensure_ascii=False)) > 8_192:
            raise ValueError("payload acima do teto de 8 KB, resumir antes do salto")
```

O campo `seq` é o que permite descartar mensagem atrasada: se chegar um salto com `seq` menor ou igual ao
último aplicado para o mesmo `trace_id`, ele é ignorado, não processado.

## 3. Fila e garantia de entrega

- **Transporte:** `asyncio.Queue` no processo único de desenvolvimento e Redis Streams em produção, com
  consumer group por papel.
- **Garantia:** at-least-once. A entrega é repetida em caso de falha do consumidor, então deduplicação por
  `idempotency_key` é obrigatória, não opcional.
- **Ordem:** ordenação garantida por chave de partição igual a `trace_id`, o que mantém os saltos de uma tarefa
  na mesma partição e na mesma ordem, sem globalizar a ordenação de todas as tarefas.
- **Confirmação:** `XACK` só depois da persistência do estado da tarefa. Reconhecimento antes de gravar perde
  trabalho em caso de queda do processo.
- **Poison pill:** mensagem que falha três vezes vai para a fila de erro e para de consumir ciclo de CPU.
- **Backpressure:** o consumidor só faz `XREADGROUP` com lote limitado; se a fila cresce acima do teto, a
  borda passa a devolver sobrecarga em vez de aceitar trabalho que não vai terminar.

```python
async def consumidor(stream: str, grupo: str, papel: str, max_lote: int = 8):
    """Lê um lote, aplica deduplicação e só confirma após gravar estado."""
    while True:
        lote = await ler_stream(stream, grupo, max_lote)
        if not lote:
            continue
        for msg in lote:
            if await ja_aplicado(msg.idempotency_key):
                await confirmar(msg)          # descarte silencioso do duplicado
                continue
            try:
                resultado = await executar(papel, msg)
                await gravar_estado(msg.trace_id, resultado)
            except TimeoutError:
                await reencaminhar(msg, tentativa=msg.tentativa + 1)
            except Exception:
                await enviar_erro(msg)        # vai para DLQ depois de 3 tentativas
            else:
                await confirmar(msg)
        if await tamanho_fila(stream) > 5_000:
            await sinalizar_backpressure()
```

## 4. Memória com dois horizontes

`MemoryStore` separa o que é fato do turno do que é aprendizado entre turnos. O curto prazo guarda o estado da
tarefa: último `handoff` aplicado, saltos consumidos, resultado parcial de cada papel. É por ele que a retomada
acontece. O longo prazo guarda lições consolidadas pelo `CriticAgent`, com janela de avaliação e teto de
itens para não virar lixo acumulado.

| Camada | Chave | TTL | Escrita | Leitura |
| --- | --- | --- | --- | --- |
| Curto prazo (turno) | `trace_id` | 30 min | worker, após cada salto | supervisor, antes de rotear |
| Longo prazo (lição) | `papel + topico` | 90 dias | somente o crítico | montagem de prompt do papel |

Regra de escrita no longo prazo: nenhuma lição entra sem evidência de execução anterior, ou seja, sem
`trace_id` associado e sem contagem mínima de recorrência. Lição única vira hipótese, não regra.

## 5. Loop de autoaperfeiçoamento

Após cada execução, o `CriticAgent` avalia a saída contra o contrato do papel e escreve melhoria em
`lessons.md`. O ciclo é curto e propositalmente conservador:

1. Execução termina e o resultado vai para o crítico com o `trace_id`.
2. O crítico classifica: `ok`, `suspeito` ou `falhou`, sempre com motivo tipado.
3. Em `suspeito` ou `falhou`, ele redige uma lição candidata com a evidência.
4. Lição que se repete em N execuções é promovida para `lessons.md`; as demais ficam descartadas.
5. `lessons.md` é lido na montagem do prompt do papel, com teto de linhas para não inflar contexto.

```python
def licao_promovida(candidatas: list[dict], n_min: int = 3) -> list[dict]:
    """Só promove lição recorrente. Evita transformar azar em regra."""
    por_tema: dict[str, int] = {}
    for c in candidatas:
        por_tema[c["tema"]] = por_tema.get(c["tema"], 0) + 1
    return [c for c in candidatas if por_tema[c["tema"]] >= n_min]
```

## 6. Roteamento por capacidade

O `Orchestrator` não escolhe o worker pela ordem da lista. Escolhe por capacidade disponível, que combina
ocupação da fila, latência recente do papel e estado de saúde. Worker em degradação recebe peso zero até
voltar, em vez de continuar drenando requisição e envenenando a métrica de latência de toda a trilha.

## 7. Critérios de aceite do protocolo

1. Mensagem inválida é rejeitada na origem, com erro de contrato, e nunca chega ao worker.
2. Reentrega da mesma mensagem não repete efeito externo.
3. Perda de consumidor no meio de um lote não perde trabalho já gravado.
4. Fila acima do teto gera sobrecarga na borda e não fila infinita.
5. Mensagem que falha três vezes vai para a fila de erro e para de reprocessar.
6. Retomada após queda do processo reconstitui o estado pelo `trace_id`.
7. Lição de execução única não entra em `lessons.md`.
8. Worker degradado sai do roteamento antes de estourar o teto de latência.

## 8. Referências de estudo

- Curso: Multi-AI Agent Systems with LangGraph, plataforma DeepLearning.AI.
- Doc oficial: Documentação do LangGraph para grafos de agentes, documentação oficial LangChain.
- Doc oficial: Guia de function calling e structured outputs, documentação oficial OpenAI.
