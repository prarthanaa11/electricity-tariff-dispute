from app.services.retrieval import RegulationRetriever


def main():
    retriever = RegulationRetriever()

    queries = [
        "Definition of domestic electricity tariff category",
        "Premises used partly for commercial purposes",
        "Change of use of an electricity connection",
    ]

    for query in queries:
        print("\n" + "=" * 80)
        print("QUERY:", query)
        print("=" * 80)

        results = retriever.search(
            query,
            top_k=5,
        )

        for result in results:
            print(
                f'\nDocument: {result["document_name"]}'
            )
            print(
                f'Page: {result["page"]}'
            )
            print(
                f'Similarity: {result["similarity"]:.3f}'
            )
            print(result["text"][:800])


if __name__ == "__main__":
    main()