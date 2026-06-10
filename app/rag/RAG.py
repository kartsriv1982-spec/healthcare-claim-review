import chromadb

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_openai import OpenAIEmbeddings

from chunkers import (
    CHUNKING_STRATEGIES
)

from storage import store_documents

from evaluate import evaluate_query

from config.loadConfig import (RAG_PATH, DOC_PATH)

from embeddings.embedding_provider import (get_embedding_model)


def load_document():
    print(DOC_PATH)
    loader = PyPDFLoader(DOC_PATH)

    return loader.load()


def main():

    documents = load_document()

    embeddings = get_embedding_model()

    client = chromadb.PersistentClient(
        path=RAG_PATH
    )

    collections = {}

    for name, chunker in (
            CHUNKING_STRATEGIES.items()
    ):

        print(
            f"\nRunning chunker: {name}"
        )

        chunks = chunker(documents)

        collection_name = (
            f"policy_{name}"
        )

        try:
            client.delete_collection(
                collection_name
            )
        except:
            pass

        collection = (
            client.create_collection(
                collection_name
            )
        )

        store_documents(
            collection,
            chunks,
            embeddings
        )

        collections[name] = collection

        print(
            f"Stored {len(chunks)} chunks"
        )

    evaluation_queries = [

        "What is the waiting period?",

        "Is knee replacement covered?",

        "What are the exclusions?",

        "What documents are required for reimbursement?"
    ]

    for query in evaluation_queries:

        evaluate_query(
            query,
            collections,
            embeddings
        )


if __name__ == "__main__":
    main()