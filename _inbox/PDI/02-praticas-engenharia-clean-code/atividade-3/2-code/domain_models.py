from dataclasses import dataclass, field
class DomainError(Exception): pass
@dataclass
class Lead:
    id: str; email: str; qualified: bool = False
    activities: list = field(default_factory=list)
    def contact(self, channel: str) -> "Contact":
        if not self.qualified:
            raise DomainError("lead nao qualificado nao pode ser contatado")
        return Contact(lead_id=self.id, channel=channel)
@dataclass
class Contact:
    lead_id: str; channel: str
