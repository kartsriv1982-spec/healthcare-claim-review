def query_collection(
        collection,
        embeddings,
        query,
        top_k=5
):

    query_embedding = embeddings.embed_query(
        query
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results