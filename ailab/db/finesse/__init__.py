import dotenv
# This is used to load the .env file
dotenv.load_dotenv()

def get_individual_scoring(cursor):
    """Creating a view with each individual scoring of documents"""
    cursor.execute("SELECT * FROM individual_score")
    return cursor.fetchall()

