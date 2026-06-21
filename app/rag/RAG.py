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

from config.loadConfig import (COVERAGE_RAG_PATH,COVERAGE_DOC_PATH)

from embeddings.embeddingProvider import (get_embedding_model)
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

def query(question,
          plan_name =None,
          rule_type = None,
          top_k=5):
    embeddings = get_embedding_model()

    # Query Coverage 

    client = chromadb.PersistentClient(
        path=COVERAGE_RAG_PATH
    )
    
    coverage_collection = (
            client.get_collection(
                "COVERAGE_COLLECTION"
            )
        )   
    
    query_embedding = (
        embeddings.embed_query(
            question
        )
    )

    where_clause = []

    if plan_name:
        where_clause.append({"plan_name": plan_name})
        

    if rule_type:
        where_clause.append({"rule_type": rule_type})
        
    
    if where_clause:

        results = coverage_collection.query(

            query_embeddings=[
                query_embedding
            ],

            where={"$and": where_clause},

            n_results=top_k
        )

    else:

        results = coverage_collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k
        )

    return results["documents"]
    
    

## if __name__ == "__main__":
    ingest()