from fastapi import FastAPI, HTTPException

from .RAG import ingest, query

from .config.loadConfig import (
    RAG_INGEST_API_PATH,
    RAG_HEALTH_API_PATH,
    RAG_INSPECT_API_PATH,
    RAG_QUERY_API_PATH,
)

from .inspectRAG import inspect

from pydantic import BaseModel

class query_request(
    BaseModel
):
    question: str

    plan_name: str = None

    rule_type: str = None

    top_k: int = 5

    

app = FastAPI(
    title="Insurance Claims RAG Ingestion API"
)

@app.post(RAG_INGEST_API_PATH)
def ingest_API():
    try:
        result = ingest()
        return result
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@app.get(RAG_HEALTH_API_PATH)
def health_API():
    return {
        "status": "UP",
        "message": "RAG service is running. Set OPENAI_API_KEY to enable ingest and query endpoints."
    }

@app.post(RAG_INSPECT_API_PATH)
def inspect_API():

    result = inspect()

    return {
        "status": "Inspection Completed",
        "result": result
    }

@app.post(RAG_QUERY_API_PATH)
def query_API(request: query_request):
    try:
        results = query(request.question, request.plan_name, request.rule_type, request.top_k)
        return results
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc