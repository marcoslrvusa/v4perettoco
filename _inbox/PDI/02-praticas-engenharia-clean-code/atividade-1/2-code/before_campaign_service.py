# ANTES — modulo legado (didatico; NAO usar em prod)
import psycopg2, smtplib, requests, os
class CampaignService:
    def run(self, camp):
        conn = psycopg2.connect(os.getenv("DB"))
        rows = conn.cursor().execute(f"SELECT * FROM leads WHERE camp={camp.id}")  # injection
        for r in rows:
            requests.post("https://api.crm/v1", json=r)
            smtplib.sendmail("relay", r["email"], camp.body)
            print("enviado", r["email"])
