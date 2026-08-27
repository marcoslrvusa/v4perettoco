import contextlib, signal, time
from dataclasses import dataclass
@dataclass
class Handoff:
    frm: str; to: str; intent: str; payload: dict; trace_id: str; hops: int = 0
AGENTS = {"triage": None, "consult": None, "proposal": None}
TIMEOUT = 15; MAX_HOPS = 5
def route(intent): return {"triagem":"triage","consulta":"consult","proposta":"proposal"}[intent]
@contextlib.contextmanager
def timeout(sec):
    def h(s, f): raise TimeoutError()
    signal.signal(signal.SIGALRM, h); signal.alarm(sec)
    try: yield
    finally: signal.alarm(0)
def run(intent, payload, trace_id, hops=0):
    if hops > MAX_HOPS: return {"error": "loop", "fallback": True}
    target = route(intent)
    try:
        with timeout(TIMEOUT): result = AGENTS[target].handle(payload)
    except TimeoutError:
        return run("triage", {"note":"timeout"}, trace_id, hops+1)
    return Handoff("supervisor", target, intent, result, trace_id, hops)
