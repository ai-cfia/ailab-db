-- Set the search path to the louis_006 schema
SET
    search_path TO "louis_0.0.6";
    
INSERT INTO
    chunk_score (id, score, score_type)
SELECT
    s.id,
    s.score,
    s.score_type
FROM
    score s;

CREATE
OR REPLACE FUNCTION count_tr_in_chunk(chunk_id UUID) RETURNS INTEGER AS $ $ DECLARE tr_count INTEGER;

BEGIN
SELECT
    COUNT(*) INTO tr_count
FROM
    "louis_0.0.6".chunk
WHERE
    id = chunk_id
    AND html_content LIKE '%<tr>%';

-- Replace 'html_content' with your column name
RETURN tr_count;

END;

$ $ LANGUAGE plpgsql;