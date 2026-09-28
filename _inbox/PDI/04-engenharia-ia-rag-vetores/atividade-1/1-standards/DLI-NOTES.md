# NVIDIA DLI: Notas

- **Embeddings**: normalizar antes de coseno.
- **Chunking**: 512 tokens + overlap 64.
- **Retrieval**: top-k=20 + rerank para top-5.
- **Evaluation**: faithfulness + answer relevance.

## Por que normalizar antes do cosseno

A similaridade de cosseno mede o ângulo entre dois vetores, não o tamanho deles. Se o vetor não for normalizado, a norma entra na conta e o score passa a refletir uma mistura de direção e comprimento, o que quebra a comparação entre um trecho de 50 palavras e outro de 500. Com normalização prévia, o denominador da fórmula vira 1 e a similaridade vira produto escalar puro.

$$\text{sim}(a, b) = \frac{a \cdot b}{\|a\| \|b\|} \xrightarrow{\ \|a\|=\|b\|=1\ } a \cdot b$$

Consequência prática: o threshold 0,82 só significa alguma coisa se a norma dos vetores for constante. Sem normalização, o mesmo corte bloqueia texto longo e libera texto curto sem relação com relevância.

```python
import numpy as np

def similaridade(a: np.ndarray, b: np.ndarray) -> float:
    """Similaridade de cosseno entre dois vetores, com normalização defensiva."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0                      # vetor vazio não é similar a nada
    return float(a @ b / (na * nb))
```

## Por que 512 tokens com overlap 64

Chunk grande enche a janela de contexto com material que só parcialmente responde à pergunta, e o modelo dilui a atenção. Chunk pequeno corta a evidência no meio e entrega duas metades que, sozinhas, não sustentam a resposta. O par 512/64 é o ponto de coesão com custo aceitável: passo de 448 tokens entre chunks e 12,5 por cento de tokens duplicados na fronteira.

| Tamanho | Efeito no prompt | Efeito na indexação | Veredito |
| --- | --- | --- | --- |
| 64 tokens | muitos fragmentos, contexto pobre | índice barato, recall ruim | reprovado |
| 512 tokens | coeso, orçamento previsível | acréscimo de 12,5 por cento com overlap | ESCOLHIDO |
| 2048 tokens | ruído domina o contexto | índice pequeno, custo alto por consulta | reprovado |

Regra de bolso do curso: o chunk deve ser maior que o maior trecho de evidência esperado no domínio, e o overlap deve cobrir o travessão de frase mais comum do texto.

## Por que 20 candidatos e 5 no fim

A busca vetorial é barata e explora: devolver 20 custa pouco e protege contra vizinhança errada. O rerank é caro e extrai: avalia cada candidato contra a pergunta, parágrafo por parágrafo, e só os 5 melhores entram no prompt. Pagar 20 passes de rerank para descartar 15 é latência sem ganho.

```python
def recuperar(pergunta: str, chunks: list[str], k_bruto: int = 20, k_final: int = 5) -> list[str]:
    """Busca em duas fases: exploração vetorial barata e extração com rerank."""
    candidatos = busca_vetorial(pergunta, k=k_bruto)          # ordem por cosseno
    pontuados = [(c, reranker.score(pergunta, c)) for c in candidatos]
    pontuados.sort(key=lambda par: par[1], reverse=True)       # reordenação
    return [c for c, _ in pontuados[:k_final]]
```

Sinal de que a arquitetura está errada: se subir `k_bruto` e o recall@5 não melhorar, o problema não é o número de candidatos, é o embedding ou o chunking.

## Evaluation: faithfulness e answer relevance

Duas perguntas diferentes. **Faithfulness**: a resposta está fiel ao que o contexto recuperado diz? **Answer relevance**: a resposta responde o que foi perguntado? Uma resposta fiel a um trecho errado reprova em relevance; uma resposta relevante inventando número reprova em faithfulness.

- Medir faithfulness por similaridade de cosseno entre resposta e evidência, com corte em 0,8.
- Medir answer relevance comparando resposta com a pergunta, com o mesmo tipo de corte.
- Rodar as duas sobre o golden set de 50 pares em cada build de CI.
- Registrar o score por pergunta, não só a média: a média esconde uma pergunta que quebra sempre.

```python
def avaliar(pergunta: str, resposta: str, contexto: str, limiar: float = 0.82) -> dict:
    """Devolve os dois escores e o veredito de aprovação da resposta."""
    fid = similaridade(emb(resposta), emb(contexto))
    rel = similaridade(emb(resposta), emb(pergunta))
    return {"faithfulness": fid, "relevance": rel, "aprovado": fid >= limiar and rel >= limiar}
```

## Anti-padroes
- Chunk gigante sem overlap -> ruído.
- Resposta sem citar fonte -> hallucination invisible.

Demais anti-padrões que o curso insiste em corrigir:

- Consulta indexada com um modelo e buscada com outro -> espaços vetoriais diferentes, resultado aleatório.
- Avaliação feita no olhômetro -> nenhuma mudança é comparável com a anterior.
- Threshold tirado de intuição sem curva de exemplo -> falso positivo e falso negativo sem ninguém saber.
- Contexto montado sem ordem de relevância -> o modelo lê primeiro o trecho menos provável.
- Prompt sem instrução de citar o trecho -> alucinação passa despercebida porque não há rastro para conferir.
- Reindexação apagando o índice anterior antes de validar -> sem rollback no momento mais crítico.
- Medir só a resposta final sem medir o recall -> impossível saber se o erro é de busca ou de geração.

## Sequência de verificação antes de dizer pronto

1. Vetores normalizados conferidos em amostra.
2. Mesmo modelo em indexação e consulta.
3. recall@5 medido no lote de validação.
4. Faithfulness >= 0,8 em 10 perguntas.
5. Citação obrigatória presente em todas as respostas do golden set.
6. Guardrail de saída testado com caso tóxico, caso PII e caso fora de domínio.
7. Custo por consulta contado antes da chamada.
8. Reprocessamento do mesmo corpus sem duplicidade no índice.
