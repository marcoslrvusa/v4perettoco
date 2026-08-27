from dataclasses import dataclass
from datetime import datetime
@dataclass
class DomainEvent:
    type: str; aggregate_id: str; ts: datetime = field(default_factory=datetime.utcnow)
@dataclass
class LeadCreated(DomainEvent):
    email: str
    def __post_init__(self): self.type = "crm.lead.created"
def on_lead_created(ev: LeadCreated):
    publish("crm.lead.created", ev)
