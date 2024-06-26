import ailab.models.openai as openai
import os
import json
import sys
import ailab.db as db
import dotenv
# This is used to load the .env file
dotenv.load_dotenv()

FINESSE_WEIGHTS = os.environ.get("FINESSE_WEIGHTS") \
    or db.raise_error("FINESSE_WEIGHTS is not set")


if FINESSE_WEIGHTS:
    try:
        with open(FINESSE_WEIGHTS, 'r') as json_file:
            json_data = json_file.read()
        FINESSE_JSON_PARSED_WEIGHTS = json.loads(json_data)
    except OSError:
        FINESSE_JSON_PARSED_WEIGHTS=json.loads(FINESSE_WEIGHTS)
else:
    db.raise_error("FINESSE_WEIGHTS is not set")

def match_documents(cursor, query_embedding):
    """Match documents with a given query."""
    data = {
        # TODO: use of np.array to get it to recognize the vector type
        # is there a simpler way to do this? only reason we use this
        # dependency
        # 'query_embedding': np.array(query_embedding),
        'query_embedding': query_embedding,
        'match_threshold': 0.5,
        'match_count': 10
    }

    # cursor.callproc('match_documents', data)
    cursor.execute(
        "SELECT * FROM match_documents"
        "(%(query_embedding)s::vector, %(match_threshold)s, %(match_count)s)",
        data)

    # turn into list of dict now to preserve dictionaries
    return [dict(r) for r in cursor.fetchall()]

def match_documents_from_text_query(cursor, query):
    data = {
        'query': query,
        'tokens': openai.get_tokens_from_text(query)
    }
    results = cursor.execute("""
        SELECT *
        FROM query
        WHERE tokens = %(tokens)s::integer[]
    """, data)
    db_data = results.fetchone()
    if not db_data:
        data['embedding'] = openai.fetch_embedding(data['tokens'])
        results = cursor.execute(
            "INSERT INTO query(query, tokens, embedding)"
            " VALUES(%(query)s, %(tokens)s, %(embedding)s) RETURNING id", data)
        data['query_id'] = results.fetchone()['id']
    else:
        data.update(db_data)
    docs = match_documents(cursor, data['embedding'])

    return docs

def search(cursor, query_embedding):
    """Search matching documents with a given query and return a dict."""
    data = {
        'text': ' '.join(sys.argv[1:]),
        'query_embedding': query_embedding,
        'match_threshold': 0.5,
        'match_count': 10,
        'weights': json.dumps(FINESSE_JSON_PARSED_WEIGHTS)
    }

    cursor.execute("""
        SELECT * 
        FROM search(%(text)s, %(query_embedding)s::vector, %(match_threshold)s,
                   %(match_count)s, %(weights)s::JSONB)
    """, data)
    # turn into list of dict now to preserve dictionaries
    return [dict(r) for r in cursor.fetchall()[0]["search"]]

def search_from_text_query(cursor, query):
    """Encode the query before doing the search and return a dict."""
    data = {
        'query': query,
        'tokens': openai.get_tokens_from_text(query)
    }
    results = cursor.execute("""
        SELECT *
        FROM query
        WHERE tokens = %(tokens)s::integer[]
    """, data)
    db_data = results.fetchone()
    if not db_data:
        data['embedding'] = openai.fetch_embedding(data['tokens'])
        results = cursor.execute("""
            INSERT INTO query(query, tokens, embedding)
            VALUES(%(query)s, %(tokens)s, %(embedding)s) RETURNING id
        """, data)
        data['query_id'] = results.fetchone()['id']
    else:
        data.update(db_data)
    docs = search(cursor, data['embedding'])
    return docs
