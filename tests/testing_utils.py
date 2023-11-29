import os
import logging
import dotenv
dotenv.load_dotenv()

def raise_error(message):
    raise Exception(message)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.info("Connecting to " + os.getenv("LOUIS_SCHEMA"))
LOUIS_SCHEMA = os.getenv("LOUIS_SCHEMA") or raise_error("LOUIS_SCHEMA is not set")
LOUIS_DSN = os.getenv("LOUIS_DSN") or raise_error("LOUIS_DSN is not set")
MATCH_THRESHOLD = 0.5
MATCH_COUNT = 10

embedding_table = """
create table if not exists "{embedding_model}" (
	id uuid default uuid_generate_v4 (),
	token_id uuid references token(id),
	embedding vector(1536),
	primary key(id),
	unique(token_id)
);
"""
