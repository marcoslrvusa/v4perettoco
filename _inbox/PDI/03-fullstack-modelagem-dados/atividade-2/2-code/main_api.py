from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Core API", version="1")
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

def paginate(qs, page: int = 1, size: int = 50):
    total = qs.count()
    items = qs.offset((page-1)*size).limit(size).all()
    return {"items": items, "page": page, "size": size, "total": total}

@app.get("/v1/leads")
@limiter.limit("100/minute")
def list_leads(request: Request, page: int = 1, size: int = 50):
    # cache via Redis em produção
    return paginate(Lead.query, page, size)
