import pytest
from unittest import mock
class AgentPipeline:
    def parse(self, text: str) -> dict:
        if "envie para" in text:
            return {"action": "send", "target": text.split("envie para")[-1].strip()}
        return {"action": "none"}
    def with_retry(self, fn, tries=3):
        for i in range(tries):
            try: return fn()
            except Exception:
                if i == tries - 1: raise
def test_unit_parse_prompt():
    assert AgentPipeline().parse("envie para Maria") == {"action": "send", "target": "Maria"}
def test_unit_retry_backoff(monkeypatch):
    calls = []
    monkeypatch.setattr("time.sleep", lambda s: calls.append(s))
    with pytest.raises(Exception):
        AgentPipeline().with_retry(lambda: (_ for _ in ()).throw(RuntimeError("x")), tries=3)
    assert len(calls) == 2
