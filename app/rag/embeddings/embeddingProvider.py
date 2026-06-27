from langchain_openai import OpenAIEmbeddings

from ..config.loadConfig import (OPENAI_EMBEDDING_MODEL)
from ..config.loadSecrets import (OPENAI_API_KEY)


def get_embedding_model():

    api_key = OPENAI_API_KEY

    return OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=api_key
    )