-- Set the search path to the louis_0.0.6 schema
SET
    search_path TO "louis_0.0.6";

WITH tr_counts AS (
    SELECT
        c.id,
        (
            LENGTH(h.content) - LENGTH(REPLACE(h.content, '<tr>', ''))
        ) / LENGTH('<tr>') AS tr_count
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
),
histogram AS (
    SELECT
        bucket_min,
        bucket_max,
        COUNT(t.score) AS freq,
        REPEAT(
            '■',
            (
                COUNT(t.score) :: FLOAT / GREATEST(MAX(COUNT(t.score)) OVER(), 1) * 30
            ) :: INT
        ) AS bar
    FROM
        (
            SELECT
                CAST(generate_series(0, 9) AS FLOAT) / 10.0 AS bucket_min,
                CAST(generate_series(1, 10) AS FLOAT) / 10.0 AS bucket_max
        ) AS buckets
        LEFT JOIN (
            SELECT
                id,
                tr_count,
                CASE
                    WHEN max_tr_count = min_tr_count THEN 0.0
                    ELSE 1.0 - (
                        (tr_count - min_tr_count) :: FLOAT / (max_tr_count - min_tr_count)
                    )
                END AS score
            FROM
                tr_stats
        ) t ON t.score >= buckets.bucket_min
        AND (
            t.score < buckets.bucket_max
            OR (
                buckets.bucket_max = 1.0
                AND t.score <= buckets.bucket_max
            )
        )
    GROUP BY
        buckets.bucket_min,
        buckets.bucket_max
    ORDER BY
        buckets.bucket_min,
        buckets.bucket_max
)
SELECT
    bucket_min,
    bucket_max,
    freq,
    bar
FROM
    histogram;

