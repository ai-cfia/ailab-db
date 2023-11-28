-- Set the search path to the louis_006 schema
SET search_path TO louis_006;

CREATE TABLE IF NOT EXISTS chunk_score (
    id UUID,
    score FLOAT,
    score_type VARCHAR(50)
);

TRUNCATE TABLE chunk_score;

INSERT INTO chunk_score (id, score, score_type)
SELECT
    ch.id, -- Use the id column from the chunk table
    ROUND(
        (
            LENGTH(hc.content) - length_values.min_val
        ) * 1.0 / (length_values.max_val - length_values.min_val),
        1
    ) AS tr_proportion,
    'didactic' AS score_type
FROM
    louis_006.chunk ch
INNER JOIN louis_006.html_content_to_chunk hctc ON ch.id = hctc.chunk_id
INNER JOIN louis_006.html_content hc ON hctc.md5hash = hc.md5hash
CROSS JOIN (
    SELECT
        MIN(LENGTH(content)) AS min_val,
        MAX(LENGTH(content)) AS max_val
    FROM
        louis_006.chunk ch
    INNER JOIN louis_006.html_content_to_chunk hctc ON ch.id = hctc.chunk_id
    INNER JOIN louis_006.html_content hc ON hctc.md5hash = hc.md5hash
) AS length_values
ORDER BY
    tr_proportion DESC;
