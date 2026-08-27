# DEPOIS — Clean Architecture + SOLID
from typing import Protocol
from dataclasses import dataclass
from unittest import mock

class LeadRepository(Protocol):
    def pending(self, camp_id: int) -> list: ...
    def mark_sent(self, lead_id: str, conn) -> None: ...
class Notifier(Protocol):
    def notify(self, lead: dict, body: str) -> None: ...

@dataclass
class CampaignService:
    repo: LeadRepository
    notifier: Notifier
    def run(self, camp_id: int, body: str) -> None:
        for lead in self.repo.pending(camp_id):
            try:
                self.notifier.notify(lead, body)
                self.repo.mark_sent(lead["id"], None)
            except Exception as e:
                raise

def test_service_notifies_and_marks():
    repo = mock.Mock(); repo.pending.return_value = [{"id": "1", "email": "a@b.com"}]
    notif = mock.Mock()
    CampaignService(repo, notif).run(1, "oi")
    notif.notify.assert_called_once()
    repo.mark_sent.assert_called_once()
