from .retrieval import query_collection


def evaluate_query(
        query,
        collections,
        embeddings
):

    print("\n")
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    for strategy, collection in collections.items():

        print("\n")
        print(f"STRATEGY: {strategy}")
        print("-" * 50)

        results = query_collection(
            collection,
            embeddings,
            query
        )

        docs = results["documents"][0]

        for idx, doc in enumerate(docs):

            print(f"\nResult {idx+1}")

            print(doc[:500])