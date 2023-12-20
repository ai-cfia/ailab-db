import os
import random
import uuid
import dotenv
dotenv.load_dotenv()

def raise_error(message):
    raise Exception(message)

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

# Generate a random UUID
test_uuid = uuid.uuid4()
test_item = {
                "id": test_uuid,
                "title": "Title exemple",
                "text_content": "This is an example content.",
                }


def generate_random_embedding(dimensions=100):
    return [random.uniform(0, 100000) for _ in range(dimensions)]
