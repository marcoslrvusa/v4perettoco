CREATE TABLE processed_events (id TEXT PRIMARY KEY, ts TIMESTAMPTZ DEFAULT now());
CREATE INDEX ON processed_events (ts);
