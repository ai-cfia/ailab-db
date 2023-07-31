""""Fetch embeddings from the Microsoft Azure OpenAI API"""
import os
import openai
import tiktoken

# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=python

def raise_error(message):
    raise Exception(message)

OPENAPI_API_KEY = os.environ.get("OPENAI_API_KEY") or raise_error("OPENAI_API_KEY not defined")
AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE") or raise_error("AZURE_OPENAI_SERVICE not defined") 

openai.api_type = "azure"
openai.api_key = OPENAPI_API_KEY
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
