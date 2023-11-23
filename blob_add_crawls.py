import logging
import os
import pickle
import re
from urllib.parse import quote

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from dotenv import load_dotenv
from psycopg import OperationalError, connect
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

# Connection strings and table names
database_connection_string = os.getenv("DATABASE_URL")
table_html_content = os.getenv("TABLE_HTML_CONTENT")
table_crawl = os.getenv("TABLE_CRAWL")

# Connect to Azure Blob Storage
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)


def sanitize(input):
    return quote(input)


# Function to upload a single blob with retries
def upload_blob_with_retries(
    blob_client: BlobClient, content_bytes, metadata, max_retries=3
):
    try:
        for _ in range(max_retries):
            blob_client.upload_blob(
                content_bytes, blob_type="BlockBlob", overwrite=True
            )
            blob_client.set_blob_metadata(metadata)
            return True
    except Exception as e:
        logging.error(metadata)
        raise e


# Function to process
def process(rows, container_client: ContainerClient, num_rows=None):
    if num_rows is not None:
        rows = rows[:num_rows]

    for row in tqdm(rows, desc="Uploading blobs"):
        (
            content,
            url,
            crawl_id,
            title,
            lang,
            last_crawled,
            last_updated,
            last_updated_date,
            md5hash,
        ) = row
        title = sanitize(title)

        # Convert the HTML content to bytes if not already in bytes
        content_bytes = (
            content if isinstance(content, bytes) else content.encode("utf-8")
        )
        blob_name = f"{title}"
        blob_client = container_client.get_blob_client(blob_name)

        # Metadata for the blob
        metadata = {
            "id": str(crawl_id),
            "url": url,
            "title": title,
            "language": lang,
            "last_crawled": last_crawled
            if isinstance(last_crawled, str)
            else last_crawled.isoformat()
            if last_crawled
            else "",
            "last_updated": last_updated
            if isinstance(last_updated, str)
            else last_updated.isoformat()
            if last_updated
            else "",
            "last_updated_date": last_updated_date
            if isinstance(last_updated_date, str)
            else last_updated_date.isoformat()
            if last_updated_date
            else "",
            "md5hash": md5hash,
        }

        if upload_blob_with_retries(blob_client, content_bytes, metadata):
            logging.info(f"Successfully uploaded blob {blob_name}")
        else:
            logging.error(f"Failed to upload blob {blob_name} after retries")


try:
    # with connect(database_connection_string) as conn:
    #     with conn.cursor() as cursor:
    #         query = f"""
    #         SELECT hc.content, c.url, c.id, c.title, c.lang, c.last_crawled, c.last_updated, c.last_updated_date, c.md5hash
    #         FROM {table_html_content} as hc
    #         JOIN {table_crawl} as c ON hc.md5hash = c.md5hash
    #         """
    #         cursor.execute(query)
    #         rows = cursor.fetchall()
    #         with open("rows.pkl", "wb") as file:
    #             pickle.dump(rows, file)

    with open("rows.pkl", "rb") as file:
        rows = pickle.load(file)
    process(rows, container_client)
except OperationalError as e:
    logging.error(f"Database operation failed: {e}")
except Exception as e:
    logging.exception("An unexpected error occurred: ")

logging.info("Operation completed")
