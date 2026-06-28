FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY app /app/app
COPY app/rag/requirements.txt /tmp/rag-requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /tmp/rag-requirements.txt \
    && mkdir -p /app/app/rag/COVERAGE_RAG_DB /app/app/rag/CoverageDocs

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "app.rag.serviceRAG:app", "--host", "0.0.0.0", "--port", "8001"]
