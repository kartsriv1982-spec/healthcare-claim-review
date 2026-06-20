import chromadb

from embeddings.embedding_provider import (get_embedding_model)

client = chromadb.PersistentClient(
    path="./Health_Insurance_RAG_DB"
)

collection = client.get_collection(
    name="policy_fixed"
)

embeddings = get_embedding_model()
query_embedding = embeddings.embed_query(
        "What is the coverage for pre-existing conditions?"
    )
results = collection.query(query_embeddings=[query_embedding],
        n_results=5
    )
print(results)

