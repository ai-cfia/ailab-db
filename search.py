# Name of this file: search.py
# Location: at the root of the project
# How to execute: python3 -m search.py query
import os
import json
import sys
import dotenv
import louis.models.openai as openai
import louis.db as db
from microbench import MicroBench
    


# This is used to load the .env file
dotenv.load_dotenv()
basic_bench = MicroBench()
RECENCY_WEIGHTS = os.environ.get("RECENCY_WEIGHTS") or \
    db.raise_error("RECENCY_WEIGHTS is not set")
TRAFFIC_WEIGHTS = os.environ.get("TRAFFIC_WEIGHTS") or \
    db.raise_error("TRAFFIC_WEIGHTS is not set")
CURRENT_WEIGHTS = os.environ.get("CURRENT_WEIGHTS") or \
    db.raise_error("CURRENT_WEIGHTS is not set")
TIPICALITY_WEIGHTS = os.environ.get("TIPICALITY_WEIGHTS") or \
    db.raise_error("TIPICALITY_WEIGHTS is not set")
SIMILARITY_WEIGHTS = os.environ.get("SIMILARITY_WEIGHTS") or \
    db.raise_error("SIMILARITY_WEIGHTS is not set")

# Execute the SQL search function 
@basic_bench
def search(cursor, query_embedding):
    """Match documents with a given query."""
    data = {
        'text': ' '.join(sys.argv[1:]),
        'query_embedding': query_embedding,
        'match_threshold': 0.5,
        'match_count': 1,
        'weights': json.dumps({
            'recency': RECENCY_WEIGHTS,
            'traffic': TRAFFIC_WEIGHTS, 
            'current': CURRENT_WEIGHTS,
            'typicality': TIPICALITY_WEIGHTS,
            'similarity': SIMILARITY_WEIGHTS
        })
    }

    cursor.execute("""
                   explain analyze
        SELECT * 
        FROM search(%(text)s, %(query_embedding)s::vector, %(match_threshold)s,
                   %(match_count)s, %(weights)s::JSONB)
    """, data)
    
    # turn into list of dict now to preserve dictionaries
    return [dict(r) for r in cursor.fetchall()]

# Encode the query before doing the search
def search_from_text_query(cursor, query):
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

if __name__ == '__main__':
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        results = search_from_text_query(cursor, ' '.join(sys.argv[1:]))
        print(results)