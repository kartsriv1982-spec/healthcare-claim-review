from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
RAG_PATH = os.getenv("RAG_PATH")
DOC_PATH = os.getenv("DOC_PATH")

