# Modelos de domínio (DDD) — raízes de agregado
from dataclasses import dataclass, field

@dataclass
class Lead:
    id: str
    email: str
    activities: list = field(default_factory=list)

@dataclass
class Campaign:
    id: str
    segments: list = field(default_factory=list)

@dataclass
class Agent:
    id: str
    tasks: list = field(default_factory=list)
