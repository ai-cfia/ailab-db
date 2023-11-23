import os
from azure.storage.blob import BlobServiceClient

# Load environment variables
container_name = os.getenv("AZURE_CONTAINER_NAME")
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

# Delete all blobs in the container
blobs = container_client.list_blobs()
for blob in blobs:
    container_client.delete_blob(blob.name)

print(f"All blobs in '{container_name}' have been deleted.")
