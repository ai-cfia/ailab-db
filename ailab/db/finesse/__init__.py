import dotenv

# This is used to load the .env file
dotenv.load_dotenv()


def get_individual_scoring(cursor):
    """Creating a view with each individual scoring of documents by first reading the
    SQL file and then executing a SELECT on it."""
    with open("sql/2023-11-02-individual-scoring-view.sql", "r") as file:
        sql_command = file.read()
    cursor.execute(sql_command)
    cursor.execute("SELECT * FROM individual_score")
    return cursor.fetchall()
