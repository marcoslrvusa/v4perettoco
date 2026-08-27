import pytest
from src.agent import AgentPipeline

def test_unit_parse_prompt():
    a = AgentPipeline()
    assert a.parse("envie para Maria")["action"] == "send"

def test_unit_retry_backoff(monkeypatch):
    calls = []
    monkeypatch.setattr("src.agent.sleep", lambda s: calls.append(s))
    AgentPipeline().with_retry(lambda: (_ for _ in ()).throw(Exception), tries=3)
    assert len(calls) == 2
