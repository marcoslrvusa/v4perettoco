# Design Patterns — Notas (Python/JS)

## Quando usar
- **Adapter**: sempre que chamar API de terceiro.
- **Strategy**: variacao de algoritmo (modelo de LLM por custo).
- **Observer**: reagir a eventos sem acoplar.
- **Command**: acoes de agente re-jogaveis.
- **Singleton**: NAO. Use DI.

```python
class Cheap:  def complete(self, p): ...
class Smart:  def complete(self, p): ...
def model_for(task): return Smart() if task.get("hard") else Cheap()
```
