from dataclasses import dataclass, field
from typing import Any
@dataclass
class Handoff:
    frm: str; to: str; intent: str; payload: dict[str, Any]; trace_id: str; hops: int = 0
    def next(self, to: str, payload: dict) -> "Handoff":
        return Handoff(self.frm, to, self.intent, payload, self.trace_id, self.hops + 1)
