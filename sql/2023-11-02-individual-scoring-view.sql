CREATE VIEW individual_score AS
SELECT entity_id,
       CASE WHEN s.score_type = 'current' THEN s.score END AS current,
       CASE WHEN s.score_type = 'recency' THEN s.score END AS recency,
       CASE WHEN s.score_type = 'traffic' THEN s.score END AS traffic,
       CASE WHEN s.score_type = 'typicality' THEN s.score END AS typicality,
       CASE WHEN s.score_type = 'similarity' THEN s.score END AS similarity,
       COALESCE(CASE WHEN s.score_type = 'current' THEN s.score END, 0) + 
       COALESCE(CASE WHEN s.score_type = 'recency' THEN s.score END, 0) +
       COALESCE(CASE WHEN s.score_type = 'traffic' THEN s.score END, 0) + 
       COALESCE(CASE WHEN s.score_type = 'typicality' THEN s.score END, 0) +
       COALESCE(CASE WHEN s.score_type = 'similarity' THEN s.score END, 0) AS avg
FROM score s;