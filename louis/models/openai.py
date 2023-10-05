""""Fetch embeddings from the Microsoft Azure OpenAI API"""
import os
import openai
import tiktoken

import dotenv
dotenv.load_dotenv()

# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=python

def safe_get(key):
    value = os.environ.get(key)
    if not value:
        raise Exception(f"Environment variable {key} not defined")
    return value

OPENAI_API_KEY = safe_get("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = safe_get("AZURE_OPENAI_ENDPOINT")
OPENAI_API_ENGINE = safe_get('OPENAI_API_ENGINE')

openai.api_type = "azure"
openai.api_key = OPENAI_API_KEY
openai.api_base = f"{AZURE_OPENAI_ENDPOINT}"
openai.api_version = "2023-05-15"

enc = tiktoken.get_encoding("cl100k_base")

def fetch_embedding(tokens):
    """Fetch embedding for a list of tokens from the Microsoft Azure OpenAI API"""
    response = openai.Embedding.create(
        input = tokens,
        engine = OPENAI_API_ENGINE
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

# def fetch_tokens_embeddings(text):
#     tokens = get_tokens_from_text(text)
#     embeddings = fetch_embedding(tokens)
#     return (tokens, embeddings)

def get_tokens_from_text(text):
    tokens = enc.encode(text)
    return tokens
