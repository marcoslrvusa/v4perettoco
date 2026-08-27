import time
class CircuitBreaker:
    def __init__(self, fail=5, reset=30):
        self.fails = 0; self.fail_max = fail; self.reset = reset
        self.state = "CLOSED"; self.opened_at = 0
    def allow(self):
        if self.state == "OPEN":
            if time.time() - self.opened_at > self.reset:
                self.state = "HALF_OPEN"; return True
            return False
        return True
    def success(self): self.fails = 0; self.state = "CLOSED"
    def failure(self):
        self.fails += 1
        if self.fails >= self.fail_max:
            self.state = "OPEN"; self.opened_at = time.time()
def call_with_breaker(breaker, fn, fallback):
    if not breaker.allow(): return fallback()
    try:
        r = fn(); breaker.success(); return r
    except Exception:
        breaker.failure(); return fallback()
