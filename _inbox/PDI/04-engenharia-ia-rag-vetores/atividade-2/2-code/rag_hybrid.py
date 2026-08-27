import pg8000
def hybrid_search(conn, query_emb, text, k=10):
    return conn.run(
        """SELECT id, content,
           0.7*(1-(embedding <=> :q)) + 0.3*ts_rank(tsv, websearch_to_tsquery(:t)) AS score
           FROM docs ORDER BY score DESC LIMIT :k""",
        q=query_emb, t=text, k=k)
