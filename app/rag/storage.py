import uuid


def store_documents(
        collection,
        chunks,
        embeddings
):

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    metadatas = [
        chunk.metadata
        for chunk in chunks
    ]

    vectors = embeddings.embed_documents(
        texts
    )

    collection.add(
        ids=[
            str(uuid.uuid4())
            for _ in chunks
        ],
        documents=texts,
        embeddings=vectors,
        metadatas=metadatas
    )