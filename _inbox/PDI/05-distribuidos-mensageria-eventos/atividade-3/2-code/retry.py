import random, time
def backoff(attempt, base=0.2, cap=5.0):
    return min(cap, base * (2 ** attempt)) + random.uniform(0, 0.1)
def retry(fn, tries=4, fallback=None):
    for i in range(tries):
        try: return fn()
        except Exception:
            if i == tries - 1: return fallback() if fallback else (_ for _ in ()).throw(RuntimeError("esgotado"))
            time.sleep(backoff(i))
