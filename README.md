# Healthcare Insurance Claim Review Assistant

## RAG Docker container

Build and run the dedicated RAG service separately:

```bash
docker compose -f deployment/docker-compose.yaml build rag-service
docker compose -f deployment/docker-compose.yaml up -d rag-service
```

The service will be available at:
- http://localhost:8001/rag/health

Required environment variable:
- OPENAI_API_KEY
