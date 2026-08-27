import numpy as np
from rank_bm25 import BM25Okapi
def rrf(ranks, k=60):
    s = {}
    for r in ranks:
        for i, doc in enumerate(r):
            s[doc] = s.get(doc, 0) + 1/(k + i + 1)
    return sorted(s, key=s.get, reverse=True)
def hybrid_retrieve(q, chunks, emb_model, k=10):
    tok = [c.split() for c in chunks]
    bm = BM25Okapi(tok)
    bm25_rank = bm.get_top_n(q.split(), chunks, n=k)
    qv = emb_model.encode([q], normalize_embeddings=True)[0]
    cv = emb_model.encode(chunks, normalize_embeddings=True)
    vec_rank = [chunks[i] for i in np.argsort(-(cv @ qv))[:k]]
    return rrf([bm25_rank, vec_rank])[:k]
def relation_query(tx, client_id):
    return tx.run("MATCH (c:Cliente {id:$id})-[:TEM]->(ct)-[:GERA]->(f) RETURN f", id=client_id)
