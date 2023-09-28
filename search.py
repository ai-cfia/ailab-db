# Name of this file: search.py
# Location: at the root of the project
# How to execute: python3 -m search.py
 

#This is used to load the .env file

import dotenv
dotenv.load_dotenv()

import louis.db as db

def search(cursor, query_embedding, text, JSONB):
    """Match documents with a given query."""
    data = {
        'text': text,
        'query_embedding': query_embedding,
        'match_threshold': 0.5,
        'match_count': 10,
        'weights': JSONB
    }

    # cursor.callproc('search', data)
    cursor.execute(
        "SELECT * FROM search",
        "(%(text)s, %(query_embedding)s::vector, %(match_threshold)s, %(match_count)s, %(weights)s)",
        data)
    
    # turn into list of dict now to preserve dictionaries
    return [dict(r) for r in cursor.fetchall()]

if __name__ == '__main__':
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        search(cursor, 'what are the cooking temperatures for e.coli?')