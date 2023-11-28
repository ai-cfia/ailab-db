SELECT
  score,
  count(*) as count
FROM louis_006.chunk_score
GROUP BY score
ORDER BY score;
