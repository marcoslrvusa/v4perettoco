# Design Patterns: Notas (Python/JS)

## Quando usar
- **Adapter**: sempre que chamar API de terceiro.
- **Strategy**: variação de algoritmo (modelo de LLM por custo).
- **Observer**: reagir a eventos sem acoplar.
- **Command**: ações de agente re-jogaveis.
- **Singleton**: NÃO. Use DI.

```python
class Cheap:  def complete(self, p): ...
class Smart:  def complete(self, p): ...
def model_for(task): return Smart() if task.get("hard") else Cheap()
```
