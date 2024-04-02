""""Fetch embeddings from the Microsoft Azure OpenAI API"""

import os

import tiktoken
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=python


def safe_get(key):
    value = os.environ.get(key)
    if not value:
        raise Exception(f"Environment variable {key} not defined")
    return value


OPENAI_API_KEY = safe_get("OPENAI_API_KEY")
OPENAI_ENDPOINT = safe_get("OPENAI_ENDPOINT")

client = AzureOpenAI(
    api_key=OPENAI_API_KEY, azure_endpoint=OPENAI_ENDPOINT, api_version="2023-05-15"
)
enc = tiktoken.get_encoding("cl100k_base")


def fetch_embedding(tokens):
    """Fetch embedding for a list of tokens from the Microsoft Azure OpenAI API"""
    OPENAI_API_ENGINE = safe_get("OPENAI_API_ENGINE")

    response = client.embeddings.create(input=tokens, model=OPENAI_API_ENGINE)
    return response.data[0].embedding


# def fetch_tokens_embeddings(text):
#     tokens = get_tokens_from_text(text)
#     embeddings = fetch_embedding(tokens)
#     return (tokens, embeddings)


def get_tokens_from_text(text):
    tokens = enc.encode(text)
    return tokens


def get_chat_answer(system_prompt, user_prompt, max_token):
    OPENAI_API_ENGINE = safe_get("OPENAI_API_ENGINE")

    response = client.chat.completions.create(
        engine=OPENAI_API_ENGINE,
        temperature=0,
        max_tokens=max_token,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": (user_prompt)},
        ],
    )
    return response
