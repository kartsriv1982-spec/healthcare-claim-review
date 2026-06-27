import chromadb

from .config.loadConfig import (
    COVERAGE_RAG_PATH,
)

client = chromadb.PersistentClient(
    path=COVERAGE_RAG_PATH
)

def inspect():
    collections = client.list_collections()
    result = ""
    result = result + "\nCollections\n"

    for collection in collections:

        result = result + collection.name + "\n"
        collection = client.get_collection(
        collection.name)
        results = collection.get()

        result = result + "Total Chunks: " + str(len(results['ids'])) + "\n"

        for id in range(
        len(results['ids'])
        ):

            result = result + (
                f"\nChunk {id+1}\n"
                f"ID: {results['ids'][id]}\n"
                f"Document: {results['documents'][id]}\n"
                f"Metadata: {results['metadatas'][id]}\n"
            )
        
        return result 

