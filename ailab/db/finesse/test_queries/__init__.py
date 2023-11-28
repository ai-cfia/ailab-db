def get_random_chunk(cursor):
    query = """
        SELECT dc.score AS score, cr.id AS crawl_id, ch.id AS chunk_id, ch.title, cr.url AS crawl_url, ch.text_content
        FROM Chunk ch
        INNER JOIN html_content_to_chunk hctc ON ch.id = hctc.chunk_id
        INNER JOIN html_content hc ON hctc.md5hash = hc.md5hash
        INNER JOIN crawl cr ON hc.md5hash = cr.md5hash
        INNER JOIN documents dc ON ch.id = dc.chunk_id
        WHERE dc.score > 0.0 
        AND EXISTS (
            SELECT 1 
            FROM score sc
            WHERE sc.entity_id = ch.id
            AND sc.score_type = 'current' 
            AND sc.score > 0.0
        )
        ORDER BY RANDOM()
        LIMIT 1;
    """
    cursor.execute(query)
    return cursor.fetchall()

def chunk_test_quality(cursor):
    query = """
        SELECT
            ch.id AS chunk_score_id,
            hc.md5hash AS md5hash_content_to_chunk,
            hc.content AS html_content
        FROM
            louis_006.chunk_score ch
        LEFT JOIN
            louis_006.html_content_to_chunk hctc ON ch.id = hctc.chunk_id
        LEFT JOIN
            louis_006.html_content hc ON hctc.md5hash = hc.md5hash
        WHERE
            ch.score > 0.9
        LIMIT
            1;
    """
    cursor.execute(query)
    return cursor.fetchall()