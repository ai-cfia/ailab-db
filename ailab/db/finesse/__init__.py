def get_individual_scoring(cursor):
    """Returning each individual scoring of documents by doing 
    a SELECT on the individual_score view. Require louis_v006."""
    cursor.execute("SELECT * FROM individual_score")
    return cursor.fetchall()
