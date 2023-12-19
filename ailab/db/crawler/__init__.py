import psycopg
import numpy as np

import ailab.db as db

def link_pages(cursor, source_url, destination_url):
    """Link two pages together in the database."""
    data = {
        'source_url': source_url,
        'destination_url': destination_url,
    }
    cursor.execute(
        """SELECT id FROM crawl
           WHERE url = %(source_url)s ORDER BY last_updated DESC LIMIT 1""",
        data
    )
    data['source_crawl_id'] = cursor.fetchone()['id']
    cursor.execute(
        """SELECT id FROM crawl
           WHERE url = %(destination_url)s ORDER BY last_updated DESC LIMIT 1""",
        data
    )
    data['destination_crawl_id'] = cursor.fetchone()['id']
    cursor.execute(
        "INSERT INTO link (source_crawl_id, destination_crawl_id)"
        " VALUES (%(source_crawl_id)s, %(destination_crawl_id)s)"
        " ON CONFLICT DO NOTHING",
        data
    )


def fetch_links(cursor, url):
    """Fetch all links from a given url."""
    data = {
        'source_url': url
    }
    cursor.execute(
        "SELECT url FROM link"
        " JOIN crawl ON link.destination_crawl_id = crawl.id"
        " WHERE source_crawl_id = ("
            " SELECT id FROM crawl WHERE url = %(source_url)s"
            " ORDER BY last_updated DESC LIMIT 1)",
        data
    )
    data['destination_urls'] = [r['url'] for r in cursor.fetchall()]
    return data['destination_urls']

def get_md5hash(cursor, data):
    cursor.execute(
        """SELECT md5hash FROM crawl WHERE url = %(url)s
           ORDER BY last_updated DESC LIMIT 1""",
        data
    )
    return cursor.fetchone()['md5hash']

def get_chunk_id(cursor, data):
    cursor.execute(
        """
        WITH e as(
            INSERT INTO chunk (title, text_content)
                VALUES(%(title)s, %(text_content)s)
            ON CONFLICT DO NOTHING
            RETURNING id
        )
        SELECT id FROM e
        UNION ALL
        SELECT id FROM chunk WHERE text_content = %(text_content)s
        """,
        data
    )
    row = cursor.fetchone()
    return row['id'] if row is not None else None

def insert_html_content_to_chunk(cursor, data):
    cursor.execute(
        """
        INSERT INTO html_content_to_chunk (md5hash, chunk_id)
        VALUES(%(md5hash)s, %(chunk_id)s::UUID)
        ON CONFLICT DO NOTHING
        """,
        data)

def get_token_id(cursor, data):
    cursor.execute(
        """
        WITH e as(
            INSERT INTO token (chunk_id, tokens, encoding)
                VALUES (%(chunk_id)s::UUID, %(tokens)s, %(encoding)s)
            ON CONFLICT DO NOTHING
            RETURNING *
        )
        SELECT id FROM e
        UNION ALL
        SELECT id FROM token
            WHERE chunk_id = %(chunk_id)s::UUID
            and tokens = %(tokens)s::INTEGER[]
            and encoding = %(encoding)s
        """,
        data
    )
    res = cursor.fetchone()
    return res['id'] if res is not None else None

def store_chunk_item(cursor, item):
    """Process a ChunkItem and insert it into the database."""
    try:
        data = {
                'url': item["url"],
                'title': item["title"],
                'text_content': item["text_content"],
                'tokens': item["tokens"],
                'encoding': 'cl100k_base'
        }
        data['md5hash'] = get_md5hash(cursor, data)
        data['chunk_id'] = get_chunk_id(cursor, data)
        insert_html_content_to_chunk(cursor, data)
        data['token_id'] = get_token_id(cursor, data)
        return data
    except psycopg.IntegrityError as e:
        raise db.DBError("Error storing chunk item for %s" % item['url']) from e

def store_crawl_item(cursor, item):
    """Process a CrawlItem and insert it into the database."""
    try:
        item['html_content_md5hash'] = db.hash(item["html_content"])
        cursor.execute(
            """INSERT INTO html_content (content, md5hash)
               VALUES(%(html_content)s, %(html_content_md5hash)s)
               ON CONFLICT DO NOTHING""",
            item)
        cursor.execute(
            """INSERT INTO crawl
               (url, title, lang, md5hash, last_crawled, last_updated)
               VALUES (
                %(url)s, %(title)s, %(lang)s, %(html_content_md5hash)s,
                %(last_crawled)s, %(last_updated)s)
            """,
            item
        )
        cursor.execute("""SELECT * FROM crawl 
                       WHERE url = %(url)s ORDER BY last_updated DESC LIMIT 1""", item)
        return cursor.fetchone()
    except psycopg.IntegrityError as e:
        raise db.DBError("Error storing crawl item for %s" % item['url']) from e


def store_embedding_item(cursor, item):
    """Process an EmbeddingItem and insert it into the database."""
    try:
        data = {
            'token_id': item["token_id"],
            # TODO: shouldn't python-pgvector support casting from smallint[] to vector?
            'embedding': np.array(item["embedding"]),
            'embedding_model': item["embedding_model"],
        }
        query = psycopg.sql.SQL(
                'INSERT INTO {embedding_model} (token_id, embedding)'
                ' VALUES (%(token_id)s, %(embedding)s::vector)'
            ).format(
                embedding_model=psycopg.sql.Identifier(
                data['embedding_model'])
            ).as_string(cursor)
        cursor.execute(
           query,
            data
        )
        return data['token_id']
    except psycopg.IntegrityError as e:
        raise db.DBError(
            "Error storing embedding item for token %s" % item['token_id']) from e

def fetch_crawl_ids_without_chunk(cursor):
    """Fetch all crawl ids without an embedding."""
    query = psycopg.sql.SQL(
        """
        SELECT crawl.id FROM crawl
         LEFT JOIN html_content_to_chunk
         ON crawl.md5hash = html_content_to_chunk.md5hash
         WHERE chunk_id IS NULL
        """
    ).as_string(cursor)
    cursor.execute(query)
    return [crawl_id['id'] for crawl_id in cursor.fetchall()]

def fetch_chunk_id_without_embedding(cursor, embedding_model='ada_002'):
    """Fetch all chunk ids without an embedding."""
    query = psycopg.sql.SQL(
        "SELECT chunk_id FROM chunk"
        " JOIN token ON chunk.id = token.chunk_id"
        " LEFT JOIN {embedding_model} ON token.id = {embedding_model}.token_id"
        " WHERE {embedding_model}.embedding IS NULL"
    ).format(embedding_model=psycopg.sql.Identifier(embedding_model)).as_string(cursor)
    cursor.execute(query)
    return [chunk_id['chunk_id'] for chunk_id in cursor.fetchall()]

def fetch_crawl_row(cursor, url):
    """Fetch the most recent crawl row for a given url."""
    if url.startswith('postgresql://'):
        data = db.parse_postgresql_url(url)

        cursor.execute(
            """SELECT *, content as html_content FROM crawl
                INNER JOIN html_content on crawl.md5hash = html_content.md5hash
                WHERE id = %(id)s ORDER BY last_updated DESC LIMIT 1""",
            data
        )
    else:
        data = {'url': url}
        cursor.execute(
            """SELECT *, content as html_content FROM crawl
                INNER JOIN html_content on crawl.md5hash = html_content.md5hash
                WHERE url = %(url)s ORDER BY last_updated DESC LIMIT 1""",
            data
        )
    if cursor.rowcount == 0:
        raise db.DBError("No crawl found for id: {}".format(data))
    row = cursor.fetchone()
    assert 'html_content' in row.keys()
    return row

def fetch_chunk_token_row(cursor, id):
    """Fetch the most recent chunk token for a given chunk id."""
    data = {'id': id}
    cursor.execute(
        """SELECT chunk.id as chunk_id, token.id as token_id, tokens FROM chunk
        JOIN token ON chunk.id = token.chunk_id
        WHERE chunk.id = %(id)s LIMIT 1""",
        data
    )
    return cursor.fetchone()
