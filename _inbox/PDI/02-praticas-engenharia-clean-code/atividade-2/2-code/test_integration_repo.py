import pytest
from src.repo import LeadRepository

def test_integration_pending(db_container):
    repo = LeadRepository(db_container.url)
    assert repo.pending(1)  # popula fixture no container

def test_integration_notifier(notifier_spy):
    notifier_spy.notify({"email":"a@b.com"}, "oi")
    assert notifier_spy.sent == [{"email":"a@b.com"}]
