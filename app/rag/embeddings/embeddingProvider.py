import os

from langchain_openai import OpenAIEmbeddings

from ..config.loadConfig import OPENAI_EMBEDDING_MODEL


def get_embedding_model():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    return OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=api_key,
    )