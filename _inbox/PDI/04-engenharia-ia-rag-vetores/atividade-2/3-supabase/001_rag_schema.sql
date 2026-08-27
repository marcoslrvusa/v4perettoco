CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE docs (
  id bigserial PRIMARY KEY,
  content text,
  tsv tsvector GENERATED ALWAYS AS (to_tsvector('portuguese', content)) STORED,
  embedding vector(1536)
);
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops);
