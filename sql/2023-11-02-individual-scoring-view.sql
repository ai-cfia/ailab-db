CREATE VIEW individual_scoring AS
SELECT entity_id,
       CASE WHEN score_type = 'current' THEN score END AS current,
       CASE WHEN score_type = 'recency' THEN score END AS recency,
       CASE WHEN score_type = 'traffic' THEN score END AS traffic,
       CASE WHEN score_type = 'typicality' THEN score END AS typicality,
       CASE WHEN score_type = 'similarity' THEN score END AS similarity
FROM score;