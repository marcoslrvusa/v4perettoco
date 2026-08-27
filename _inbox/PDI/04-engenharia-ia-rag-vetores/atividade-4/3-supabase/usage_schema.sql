CREATE TABLE llm_usage (
  id bigserial PRIMARY KEY,
  agent text, model text,
  prompt_tokens int, completion_tokens int,
  cost_usd numeric(10,4), created_at timestamptz DEFAULT now()
);
CREATE INDEX ON llm_usage (agent, created_at);
