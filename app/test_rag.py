from rag import RAGSystem


def main():
    rag = RAGSystem()

    questions = [
        "What is the return policy?",
        "How long do I have to return an item?",
        "What are the shipping options?",
        "What is the warranty policy?",
        "How does membership work?",
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print("QUESTION:", question)
        print("=" * 70)

        results = rag.search(
            question,
            n_results=3
        )

        for number, result in enumerate(
            results,
            start=1
        ):

            metadata = result["metadata"]

            print(f"\nRESULT {number}")
            print("-" * 50)

            print(
                "File:",
                metadata.get("filename")
            )

            print(
                "Heading:",
                metadata.get("heading")
            )

            print(
                "Status:",
                metadata.get("status")
            )

            print(
                "Distance:",
                round(result["distance"], 4)
            )

            print("\nText:")
            print(result["text"][:500])


if __name__ == "__main__":
    main()