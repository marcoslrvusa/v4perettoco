from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")
def embed(texts): return model.encode(texts, normalize_embeddings=True)
def chunk(doc, size=512, overlap=64):
    toks = doc.split()
    return [" ".join(toks[i:i+size]) for i in range(0, len(toks), size-overlap)]
def retrieve(q, chunks, k=5):
    qv = embed([q])[0]; cv = embed(chunks)
    idx = np.argsort(-(cv @ qv))[:k]
    return [chunks[i] for i in idx]
def answer(q, ctx, llm):
    return llm(f"Responda usando SO o contexto. Cite o trecho.\nContexto: {ctx}\nP: {q}")
