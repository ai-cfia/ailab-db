import logging
import ailab.db.finesse as finesse
import ailab.db as db
import pandas as pd
import dotenv

# This is used to load the .env file
dotenv.load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def create_individual_scoring(cursor):
    """Create individual scoring view."""
    with open("sql/2023-11-02-individual-scoring-view.sql", "r") as file:
        sql_command = file.read()
    cursor.execute(sql_command)

if __name__ == "__main__":
    """Get the individual scoring of each documents and write the results in a csv file."""
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        create_individual_scoring(cursor)
        results = finesse.get_individual_scoring(cursor)
    file = 'tests/output/individual_scoring.csv'
    dataframe = pd.DataFrame(results)
    logger.info("Creating " + file)
    dataframe.to_csv(file, index=False)
