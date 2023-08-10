import psycopg
import numpy as np

import louis.db as db

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
        cursor.execute(
            """SELECT id FROM crawl WHERE url = %(url)s
               ORDER BY last_updated DESC LIMIT 1""",
            data
        )
        data['crawl_id'] = cursor.fetchone()['id']
        cursor.execute(
            "INSERT INTO chunk (crawl_id, title, text_content)"
                " VALUES(%(crawl_id)s::UUID, %(title)s, %(text_content)s)"
            " RETURNING id",
            data
        )
        data['chunk_id'] = cursor.fetchone()['id']
        cursor.execute(
            "INSERT INTO token (chunk_id, tokens, encoding)"
                " VALUES (%(chunk_id)s::UUID, %(tokens)s, %(encoding)s)"
            " RETURNING id",
            data
        )
        data['token_id'] = cursor.fetchone()['id']

        return item
    except psycopg.IntegrityError as e:
        raise db.DBError("Error storing chunk item for %s" % item['url']) from e

def store_crawl_item(cursor, item):
    """Process a CrawlItem and insert it into the database."""
    try:
        cursor.execute(
            """INSERT INTO crawl
               (url, title, lang, html_content, last_crawled, last_updated)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                item["url"],
                item["title"],
                item["lang"],
                item["html_content"],
                item["last_crawled"],
                item["last_updated"],
            )
        )
        return item
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
            ).format(embedding_model=psycopg.sql.Identifier(data['embedding_model'])).as_string(cursor)
        cursor.execute(
           query,
            data
        )
        return item
    except psycopg.IntegrityError as e:
        raise db.DBError("Error storing embedding item for token %s" % item['token_id']) from e

def fetch_crawl_ids_without_chunk(cursor):
    """Fetch all crawl ids without an embedding."""
    query = psycopg.sql.SQL(
        "SELECT crawl.id FROM crawl"
        " LEFT JOIN chunk ON crawl.id = chunk.crawl_id"
        " WHERE chunk.crawl_id IS NULL"
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

def fetch_crawl_row_by_url(cursor, url):
    """Fetch the most recent crawl row for a given url."""
    data = {
        'url': url
    }
    cursor.execute(
        "SELECT * FROM crawl WHERE url = %(url)s ORDER BY last_updated DESC LIMIT 1",
        data
    )
    if cursor.rowcount == 0:
        raise db.DBError("No crawl found for url: {}".format(url))
    return cursor.fetchone()

def fetch_crawl_row(cursor, url):
    """Fetch the most recent crawl row for a given url."""
    data = db.parse_postgresql_url(url)

    cursor.execute(
        "SELECT * FROM crawl WHERE id = %(id)s ORDER BY last_updated DESC LIMIT 1",
        data
    )
    if cursor.rowcount == 0:
        raise db.DBError("No crawl found for id: {}".format(id))
    return cursor.fetchone()

def fetch_chunk_token_row(cursor, url):
    """Fetch the most recent chunk token for a given chunk id."""

    # TODO: eventually we could generalize the use of these postgresql
    # url to data but for now keep it simple
    data = db.parse_postgresql_url(url)
    cursor.execute(
        "SELECT chunk.id as chunk_id, token.id as token_id, tokens FROM chunk"
        " JOIN token ON chunk.id = token.chunk_id"
        " JOIN crawl ON chunk.crawl_id = crawl.id"
        " WHERE chunk.id = %(id)s LIMIT 1",
        data
    )
    # psycopg.extras.DictRow is not a real dict and will convert
    # to string as a list so we force convert to dict
    return dict(cursor.fetchone())
