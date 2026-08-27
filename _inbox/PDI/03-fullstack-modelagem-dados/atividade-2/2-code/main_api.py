from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Core API", version="1")
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
@app.exception_handler(Exception)
async def handle(req, exc):
    return JSONResponse(500, {"error": {"code": "INTERNAL", "message": "erro interno",
                                         "trace_id": req.headers.get("x-trace-id")}})
def paginate_cursor(qs, after: str | None, limit: int = 50):
    if after: qs = qs.filter(id > int(after))
    page = qs.limit(limit + 1).all()
    nxt = page[-1].id if len(page) > limit else None
    return {"items": page[:limit], "next_cursor": str(nxt) if nxt else None, "limit": limit}
@app.get("/v1/leads")
@limiter.limit("100/minute")
async def list_leads(request: Request, after: str | None = None):
    cached = redis.get(f"leads:{after}")
    if cached: return json.loads(cached)
    data = paginate_cursor(Lead.query, after)
    redis.setex(f"leads:{after}", 30, json.dumps(data))
    return data
