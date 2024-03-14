import time
import semver
import math


def get_random_chunk(cursor, schema_version, seed=None):
    assert (
        semver.compare(schema_version, "0.0.6") >= 0
    ), "Schema version must be >= 0.0.6"
    schema_version = "louis_" + schema_version

    if seed is None:
        seed = math.sin(time.time())

    # Execute the SET commands separately
    cursor.execute(f'SET SEARCH_PATH TO "{schema_version}", public;')
    cursor.execute(f"SET SEED TO {seed};")

    query = """
        SELECT
            dc.score AS score, cr.id AS crawl_id, ch.id AS chunk_id, ch.title, cr.url, ch.text_content
        FROM
            Chunk ch
        INNER JOIN
            documents dc ON ch.id = dc.chunk_id
        INNER JOIN
            html_content_to_chunk hctc ON ch.id = hctc.chunk_id
        INNER JOIN
            html_content hc ON hctc.md5hash = hc.md5hash
        INNER JOIN
            crawl cr ON hc.md5hash = cr.md5hash
        WHERE
            dc.score > 0.01
        ORDER BY
            floor(random() * (
                SELECT
                    COUNT(*)
                FROM
                    Chunk
            ))
        LIMIT
            1;
    """

    cursor.execute(query)
    return cursor.fetchall()


def get_random_document_score(cursor, schema_version, seed=None):
    if seed is None:
        seed = math.sin(time.time())

    # Execute the SET commands separately
    cursor.execute(f'SET SEARCH_PATH TO "{schema_version}", public;')
    cursor.execute(f"SET SEED TO {seed};")

    query = """
        WITH random_crawl AS (  
            SELECT id  
            FROM crawl  
            ORDER BY
                floor(random() * (
                    SELECT
                        COUNT(*)
                    FROM
                        Chunk
                ))
            LIMIT
                1  
        )  
        SELECT  
            cr.id AS crawl_id, cr.url AS crawl_url, sc.score, sc.score_type   
        FROM  
            crawl cr  
        INNER JOIN  
            score sc ON cr.id = sc.entity_id  
        WHERE  
            cr.id = (SELECT id FROM random_crawl)  
    """

    cursor.execute(query)
    return cursor.fetchall()