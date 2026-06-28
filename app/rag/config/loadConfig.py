from dotenv import load_dotenv
import os
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent
load_dotenv(CONFIG_DIR / ".env")

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
COVERAGE_RAG_PATH = os.getenv("COVERAGE_RAG_PATH")
COVERAGE_DOC_PATH = os.getenv("COVERAGE_DOC_PATH")
CLAIMS_HISTORY_RAG_PATH = os.getenv("CLAIMS_HISTORY_RAG_PATH")
RAG_INGEST_API_PATH = os.getenv("RAG_INGEST_API_PATH")
RAG_QUERY_API_PATH = os.getenv("RAG_QUERY_API_PATH")
RAG_HEALTH_API_PATH = os.getenv("RAG_HEALTH_API_PATH")
RAG_INSPECT_API_PATH = os.getenv("RAG_INSPECT_API_PATH")