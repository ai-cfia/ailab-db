def get_random_chunk(cursor):
    query = """
        SELECT
            dc.score AS score, cr.id AS crawl_id, ch.id AS chunk_id, ch.title, cr.url, ch.text_content
        FROM
            "louis_0.0.6".Chunk ch
        INNER JOIN
            "louis_0.0.6".documents dc ON ch.id = dc.chunk_id
        INNER JOIN
            "louis_0.0.6".html_content_to_chunk hctc ON ch.id = hctc.chunk_id
        INNER JOIN
            "louis_0.0.6".html_content hc ON hctc.md5hash = hc.md5hash
        INNER JOIN
            "louis_0.0.6".crawl cr ON hc.md5hash = cr.md5hash
        WHERE
            dc.score > 0.01
        ORDER BY
            RANDOM()
        LIMIT
            1;
    """
    cursor.execute(query)
    return cursor.fetchall()
