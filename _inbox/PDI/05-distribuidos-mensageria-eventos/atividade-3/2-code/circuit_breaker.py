import time
class CircuitBreaker:
    def __init__(self, threshold=5, cooldown=30):
        self.fails=0; self.threshold=threshold; self.cooldown=cooldown; self.opened=0
    def call(self, fn, *a, fallback=None, **k):
        if self.opened and time.time()-self.opened < self.cooldown:
            return fallback() if fallback else None
        try:
            r=fn(*a,**k); self.fails=0; return r
        except Exception:
            self.fails+=1
            if self.fails>=self.threshold: self.opened=time.time()
            return fallback() if fallback else None
