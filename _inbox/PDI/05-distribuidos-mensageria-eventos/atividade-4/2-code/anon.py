import hashlib, re
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
CNPJ = re.compile(r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}")
def anon(text, salt):
    def h(m): return "anon:" + hashlib.sha256((salt + m.group(0)).encode()).hexdigest()[:12]
    text = EMAIL.sub(h, text)
    return CNPJ.sub(h, text)
def log_safe(msg, salt): return anon(msg, salt)
