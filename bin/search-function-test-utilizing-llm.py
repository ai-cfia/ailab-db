import ailab.db as db

projectname_db = db.connect_db()

# Random chunk query
random_chunk_query = "SELECT * FROM chunks ORDER BY RAND() LIMIT 1"

# Well-scored chunk query (assuming a score threshold of 8)
well_scored_chunk_query = "SELECT * FROM chunks WHERE score >= 8 ORDER BY score DESC LIMIT 1"

# Executing random chunk query
with projectname_db.cursor() as cursor:
    cursor.execute(random_chunk_query)
    random_chunk = cursor.fetchone()
    print("Random Chunk:", random_chunk)

# Executing well-scored chunk query
with projectname_db.cursor() as cursor:
    cursor.execute(well_scored_chunk_query)
    well_scored_chunk = cursor.fetchone()
    print("Well Scored Chunk:", well_scored_chunk)
