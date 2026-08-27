import functools
PROCESSED = set()
def idempotent(event_id_getter):
    def deco(fn):
        @functools.wraps(fn)
        def wrap(msg, *a, **k):
            eid = event_id_getter(msg)
            if eid in PROCESSED: return {"status": "duplicate"}
            PROCESSED.add(eid)
            return fn(msg, *a, **k)
        return wrap
    return deco
def upsert_lead(lead): pass  # INSERT ... ON CONFLICT (cnpj) DO UPDATE
