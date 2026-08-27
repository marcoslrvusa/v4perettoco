from typing import Protocol
class CrmPort(Protocol):
    def upsert(self, lead: dict) -> None: ...
class HubSpotAdapter:
    def upsert(self, lead): print("hubspot", lead)
class Cheap:  def complete(self, p): return "cheap"
class Smart:  def complete(self, p): return "smart"
def model_for(task): return Smart() if task.get("hard") else Cheap()
class Bus:
    def __init__(self): self._s = {}
    def on(self, t, f): self._s.setdefault(t, []).append(f)
    def emit(self, t, p): [f(p) for f in self._s.get(t, [])]
if __name__ == "__main__":
    b = Bus(); b.on("lead.created", lambda p: print("ouvinte:", p))
    b.emit("lead.created", {"id": 1})
    print(model_for({"hard": True}).complete(None))
