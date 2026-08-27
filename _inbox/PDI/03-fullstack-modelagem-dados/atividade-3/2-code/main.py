import functions_framework, os, json, pg8000, google.auth
from google.cloud import secretmanager

def get_conn():
    client = secretmanager.SecretManagerServiceClient()
    db_url = client.access_secret_version(
        name=os.getenv("DB_SECRET")).payload.data.decode()
    return pg8000.connect(dsn=db_url)

@functions_framework.http
def export_report(request):
    conn = get_conn()
    rows = conn.run("SELECT id, email FROM leads LIMIT 1000")
    return json.dumps({"rows": len(rows)})
