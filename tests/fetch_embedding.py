import os
import sys

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


client = AzureOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    azure_endpoint=f"https://{os.environ['AZURE_OPENAI_SERVICE']}.openai.azure.com",
    api_version="2023-05-15",
)


def fetch_embedding(text):
    """Fetch embedding for a list of tokens from the Microsoft Azure OpenAI API"""
    response = client.embeddings.create(input=text, model="ada")
    embeddings = response.data[0].embedding
    return embeddings


if __name__ == "__main__":
    text = " ".join(sys.argv[1:])
    if len(text) == 0:
        print("Please provide a text to embed")
        raise SystemExit
    print(fetch_embedding(text))
