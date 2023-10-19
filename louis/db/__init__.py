"""Database functions for the Louis project."""
import hashlib
import logging
import os
import urllib

import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

import dotenv
dotenv.load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class DBError(Exception):
    pass

class DBMissingEnvironmentVariable(DBError):
    pass

def raise_error(message):
    raise DBMissingEnvironmentVariable(message)

LOUIS_DSN = os.environ.get("LOUIS_DSN") or raise_error("LOUIS_DSN is not set")
LOUIS_SCHEMA = os.environ.get("LOUIS_SCHEMA") or raise_error("LOUIS_SCHEMA is not set")

def connect_db():
    """Connect to the postgresql database and return the connection."""
    logger.info(f"Connecting to {LOUIS_DSN}")
    connection = psycopg.connect(
        conninfo=LOUIS_DSN,
        row_factory=dict_row,
        autocommit=False,
        options=f"-c search_path={LOUIS_SCHEMA},public")
    assert connection.info.encoding == 'utf-8', (
        'Encoding is not UTF8: ' + connection.info.encoding)
    # psycopg.extras.register_uuid()
    register_vector(connection)
    return connection

def cursor(connection):
    """Return a cursor for the given connection."""
    return connection.cursor()

def create_postgresql_url(dbname, tablename, entity_id, parameters=None):
    if parameters is None:
        return f'postgresql://{dbname}/{LOUIS_SCHEMA}/{tablename}/{entity_id}'
    return f'postgresql://{dbname}/{LOUIS_SCHEMA}/{tablename}/{entity_id}?{urllib.parse.urlencode(parameters)}'


def parse_postgresql_url(url):
    """Parse a postgresql url and return a dictionary with the parameters."""
    parsed = urllib.parse.urlparse(url)
    path_split = parsed.path.split('/')
    return {
        'dbname': parsed.hostname,
        'schema': path_split[1],
        'tablename': path_split[2],
        'id': path_split[3],
        'parameters': urllib.parse.parse_qs(parsed.query)
    }

def hash(text):
    """Return the hash of the given text.

    We hash using the Python library to remove a roundtrip to the database
    """
    return hashlib.md5(text.encode()).hexdigest()