# ANTES — acoplado (exemplo didático)
class CampaignService:
    def run(self, camp):
        rows = psycopg2.connect(os.getenv('DB')).execute(f"SELECT * FROM leads WHERE camp={camp.id}")
        for r in rows:
            requests.post('https://api.crm/v1', json=r)          # CRM
            smtp.sendmail('relay', r.email, camp.body)            # e-mail
            print('enviado', r.email)                             # log
