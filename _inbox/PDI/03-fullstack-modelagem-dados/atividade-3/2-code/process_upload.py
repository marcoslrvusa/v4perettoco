import hashlib, json
PROCESSED = set()
def handler(event, ctx):
    rec = json.loads(event["body"])
    key = f"{rec['tenant']}:{hashlib.sha256(rec['url'].encode()).hexdigest()}"
    if key in PROCESSED:
        return {"status": "skipped", "reason": "duplicate"}
    rows = read_sheet(rec["url"])
    for r in rows: upsert_lead(r, tenant=rec["tenant"])
    PROCESSED.add(key)
    return {"status": "ok", "rows": len(rows)}
# Em prod, PROCESSED vive em Redis/DynamoDB.
