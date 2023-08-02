""""Fetch embeddings from the Microsoft Azure OpenAI API"""
import os
import openai
import tiktoken

# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=python

def safe_get(key):
    value = os.environ.get(key)
    if not value:
        raise Exception(f"Environment variable {key} not defined")
    return value

OPENAI_API_KEY = safe_get("OPENAI_API_KEY")
AZURE_OPENAI_SERVICE = safe_get("AZURE_OPENAI_SERVICE")

openai.api_type = "azure"
openai.api_key = OPENAI_API_KEY
openai.api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"
openai.api_version = "2023-05-15"

enc = tiktoken.get_encoding("cl100k_base")

def fetch_embedding(tokens):
    """Fetch embedding for a list of tokens from the Microsoft Azure OpenAI API"""
    response = openai.Embedding.create(
        input=tokens,
        engine="ada"
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
