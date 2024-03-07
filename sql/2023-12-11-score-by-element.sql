-- Set the search path to the louis_0.0.6 schema
SET
    search_path TO "louis_0.0.6";
    
WITH tr_counts AS (
    SELECT
        id,
        (LENGTH(h.content) - LENGTH(REPLACE(h.content, '<tr>', ''))) / LENGTH('<tr>') AS tr_count
    FROM
        crawl c
        INNER JOIN html_content h ON c.md5hash = h.md5hash
),
tr_stats AS (
    SELECT
        id,
        tr_count,
        MAX(tr_count) OVER () AS max_tr_count,
        MIN(tr_count) OVER () AS min_tr_count
    FROM
        tr_counts
)
SELECT
    id,
    tr_count,
    -- Normalize tr_count into a score between 1 and 0, with higher tr_count getting lower score
    CASE
        WHEN max_tr_count = min_tr_count THEN 0.0 -- Avoid division by zero, assign lowest score
        ELSE 1.0 - ((tr_count - min_tr_count)::FLOAT / (max_tr_count - min_tr_count))
    END AS score
FROM
    tr_stats
ORDER BY
    score ASC;
