from fastapi import FastAPI  

from RAG import ingest

from config.loadConfig import (RAG_INGEST_API_PATH, RAG_HEALTH_API_PATH,RAG_INSPECT_API_PATH)

from inspectRAG import inspect

app = FastAPI(
    title="Insurance Claims RAG Ingestion API"
)
@app.post(RAG_INGEST_API_PATH)
def ingest_API():

    result = ingest()

    return result

@app.get(RAG_HEALTH_API_PATH)
def health_API():

    return {
        "status": "UP"
    }

@app.post(RAG_INSPECT_API_PATH)
def inspect_API():

    result = inspect()

    return {
        "status": "Inspection Completed",
        "result": result
    }