import logging
import ailab.db.finesse as finesse
import ailab.db as db


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    """Get the individual scoring of each documents"""
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        print(finesse.get_individual_scoring(cursor))
