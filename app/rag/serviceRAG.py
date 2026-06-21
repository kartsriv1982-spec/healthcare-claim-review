from fastapi import FastAPI  

from RAG import (ingest,query)

from config.loadConfig import (RAG_INGEST_API_PATH, RAG_HEALTH_API_PATH,RAG_INSPECT_API_PATH,RAG_QUERY_API_PATH)

from inspectRAG import inspect

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

@app.post(RAG_QUERY_API_PATH)
def query_API(request: query_request):

    results = query(request.question, request.plan_name, request.rule_type, request.top_k)

    return {
        "status": "Query Completed",
        "result": results
    }