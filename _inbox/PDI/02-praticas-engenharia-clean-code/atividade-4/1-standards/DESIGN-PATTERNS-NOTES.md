# Design Patterns — Notas de Estudo (Python/JS)

## Criacionais
- **Factory:** criar `Notifier` (email/sms/crm) sem acoplar o caller.
- **Singleton (cuidado):** usar apenas para clients de DB/LLM (prefira DI).

## Estruturais
- **Adapter:** `CrmAdapter` traduz API de terceiro para porta interna.
- **Decorator:** `RetryDecorator` envolve chamadas de API.

## Comportamentais
- **Strategy:** seleção de modelo de LLM por custo/qualidade.
- **Observer:** eventos de domínio (Lead criado → dispara campanha).
- **Command:** cada ação de agente vira um Command replayable.

## Exemplo Strategy (Python)
```python
class CheapModel:  def complete(self,p): ...
class SmartModel: def complete(self,p): ...
def model_for(task): return SmartModel() if task.hard else CheapModel()
```
