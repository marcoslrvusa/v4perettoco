CREATE TABLE processed_events (
  id text PRIMARY KEY,
  created_at timestamptz DEFAULT now()
);
