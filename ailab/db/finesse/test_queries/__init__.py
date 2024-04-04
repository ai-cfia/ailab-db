import random
import time
import math


def get_random_chunk(cursor, schema_version, seed=None):
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


def get_random_crawl(cursor, schema_version):
    # Execute the SET commands separately
    cursor.execute(f'SET SEARCH_PATH TO "{schema_version}", public;')

    # Get the count of eligible rows
    cursor.execute("""
        SELECT count(*) AS total_count
        FROM crawl cr
        WHERE cr.id IN (
            SELECT entity_id
            FROM score
            WHERE score_type = 'current' AND score = 1
        )
        AND cr.id IN (
            SELECT entity_id
            FROM score
            WHERE score_type = 'recency' AND score > 0.5
        )
    """)
    row = cursor.fetchone()
    if row and row.get('total_count'):
        total_count = row['total_count']
    else:
        return None  # No eligible rows found

    # Get a random offset within the count
    random_offset = random.randint(0, total_count - 1)

    # Fetch the random crawl using the offset
    cursor.execute("""
        SELECT  
            cr.id AS crawl_id, cr.url AS crawl_url, sc.score, sc.score_type, hc.content as html_content
        FROM  
            crawl cr  
        INNER JOIN  
            score sc ON cr.id = sc.entity_id
        INNER JOIN  
            html_content hc ON cr.md5hash = hc.md5hash  
        WHERE  
            cr.id IN (
                SELECT entity_id
                FROM score
                WHERE score_type = 'current' AND score = 1
            )
        AND cr.id IN (
            SELECT entity_id
            FROM score
            WHERE score_type = 'recency' AND score > 0.5
        )
        OFFSET %s LIMIT 1
    """, (random_offset,))

    return cursor.fetchall()


def print_schema_tables_and_variables(cursor, schema_version):
    # Execute the SET commands separately
    cursor.execute(f'SET SEARCH_PATH TO "{schema_version}", public;')

    # Execute the query to retrieve all tables and variables from the schema
    cursor.execute(
        "SELECT * FROM information_schema.tables WHERE table_schema = %s;",
        (schema_version,),
    )

    # Fetch all results
    return cursor.fetchall()
