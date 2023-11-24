CREATE VIEW individual_score AS
SELECT entity_id,
       COALESCE(SUM(CASE WHEN s.score_type = 'current' THEN s.score END), 0) AS current,
       COALESCE(SUM(CASE WHEN s.score_type = 'recency' THEN s.score END), 0) AS recency,
       COALESCE(SUM(CASE WHEN s.score_type = 'traffic' THEN s.score END), 0) AS traffic,
       COALESCE(SUM(CASE WHEN s.score_type = 'typicality' THEN s.score END), 0) AS typicality,
       COALESCE(AVG(s.score), 0) AS avg
FROM score s
GROUP BY entity_id;
