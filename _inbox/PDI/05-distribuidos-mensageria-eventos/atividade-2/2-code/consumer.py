import pg8000
def handle(conn, event):
    try:
        conn.run("INSERT INTO processed_events(id) VALUES(:e)", e=event["id"])
    except pg8000.errors.IntegrityError:
        return  # já processado -> idempotente
    conn.run(
        """INSERT INTO leads(id,email) VALUES(:i,:e)
           ON CONFLICT (id) DO NOTHING""",
        i=event["id"], e=event["email"])
