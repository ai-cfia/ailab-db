import ailab.db as db
import dotenv
# This is used to load the .env file
dotenv.load_dotenv()

def individual_scoring_view():
    """Creating a view with each individual scoring of documents"""
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        cursor.execute("SELECT * FROM individual_score")
        return cursor.fetchall()
