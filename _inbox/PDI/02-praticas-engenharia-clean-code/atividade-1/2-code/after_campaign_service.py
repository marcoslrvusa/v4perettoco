# DEPOIS — Clean Architecture + SOLID
from typing import Protocol

class LeadRepository(Protocol):
    def pending(self, camp_id: int) -> list[dict]: ...

class Notifier(Protocol):
    def notify(self, lead: dict, body: str) -> None: ...

class CampaignService:
    def __init__(self, repo: LeadRepository, notifier: Notifier, log):
        self.repo, self.notifier, self.log = repo, notifier, log
    def run(self, camp_id: int, body: str) -> None:
        for lead in self.repo.pending(camp_id):
            self.notifier.notify(lead, body)
            self.log.info("notificado", lead=lead["email"])
