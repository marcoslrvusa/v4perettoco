CREATE TABLE subject (id TEXT PRIMARY KEY, consent JSONB, created_at TIMESTAMPTZ DEFAULT now());
DELETE FROM leads WHERE subject_id = $1;
DELETE FROM activities WHERE subject_id = $1;
DELETE FROM traces WHERE subject_id = $1;
DELETE FROM subject WHERE id = $1;
