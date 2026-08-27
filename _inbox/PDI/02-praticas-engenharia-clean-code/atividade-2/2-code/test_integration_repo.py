import pytest
from unittest import mock
class FakeRepo:
    def __init__(self): self._store = {}
    def pending(self, camp_id): return [{"id": "1", "email": "a@b.com"}]
    def mark_sent(self, lead_id, conn): self._store[lead_id] = True
class SpyNotifier:
    def __init__(self): self.sent = []
    def notify(self, lead, body): self.sent.append(lead["email"])
def test_integration_happy_path():
    repo, notif, log = FakeRepo(), SpyNotifier(), mock.Mock()
    CampaignService(repo, notif, log).run(1, "oi")
    assert notif.sent == ["a@b.com"] and repo._store.get("1") is True
def test_integration_marca_falha_sem_silenciar():
    repo = FakeRepo(); notif = mock.Mock(side_effect=RuntimeError("crm down")); log = mock.Mock()
    with pytest.raises(RuntimeError):
        CampaignService(repo, notif, log).run(1, "oi")
    log.error.assert_called_once()
