-- Correlacao registro -> causa via trace_id
CREATE VIEW v_sync_errors AS
SELECT trace_id, integration, op, code, lead_id, ts
FROM sync_logs
WHERE level IN ('warn','error')
ORDER BY ts DESC;

SELECT integration,
       count(*) FILTER (WHERE level='error')::float / nullif(count(*),0) AS err_rate
FROM sync_logs
WHERE ts > now() - interval '5 min'
GROUP BY integration;
