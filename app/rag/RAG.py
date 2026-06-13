from xmlrpc import client

import chromadb

from langchain_community.document_loaders import (
    PyPDFLoader
)

import os
from langchain_openai import OpenAIEmbeddings

from chunkers import (
    CHUNKING_STRATEGIES
)

from storage import store_documents

from evaluate import evaluate_query

from config.loadConfig import (OPENAI_API_KEY,OPENAI_EMBEDDING_MODEL,
    COVERAGE_RAG_PATH,
    COVERAGE_DOC_PATH,
    CLAIMS_HISTORY_RAG_PATH
)

from embeddings.embedding_provider import (get_embedding_model)
from policyChunker import (policy_coverage_chunking)

def load_pdf_document(file_path):
    loader = PyPDFLoader(file_path)

    return loader.load()

def ingest_coverage_docs(
        coverage_folder,
        collection,
        embeddings
):

    total_chunks = 0

    for file_name in os.listdir(
            coverage_folder
    ):

        file_path = os.path.join(
            coverage_folder,
            file_name
        )
        print (f"Ingesting {file_path}...")
        
        documents = (
            load_pdf_document(
                file_path
            )
        )

        chunks = (
            policy_coverage_chunking(
                documents
            )
        )

        store_documents(
            collection,
            chunks,
            embeddings
        )

        total_chunks += len(
            chunks
        )


        
    

def ingest():

    embeddings = get_embedding_model()

    # Ingest Coverage 

    client = chromadb.PersistentClient(
        path=COVERAGE_RAG_PATH
    )
    
    try:
        client.delete_collection(
                "COVERAGE_COLLECTION"
            )
    except:
        pass

    coverage_collection = (
            client.create_collection(
                "COVERAGE_COLLECTION"
            )
        )   
    ingest_coverage_docs(COVERAGE_DOC_PATH, coverage_collection, embeddings)
    
    return {
        "status": "Ingestion Completed"
           }

    

## if __name__ == "__main__":
    ingest()