from app.agent import SupportAgent


def main():
    print("=" * 70)
    print("ASTER & ROW SUPPORT ASSISTANT")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 70)

    agent = SupportAgent()

    session_id = "terminal-session"

    while True:
        try:
            question = input("\nCUSTOMER: ").strip()

            if question.lower() in {"exit", "quit"}:
                print("\nGoodbye!")
                break

            if not question:
                print("Please enter a question.")
                continue

            result = agent.answer(
                question,
                session_id=session_id
            )

            print("\nASSISTANT:")
            print(result.get("response", ""))

            sources = result.get("sources", [])

            if sources:
                print("\nSOURCES:")
                for source in sources:
                    print(f"- {source}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        except Exception as error:
            print(f"\nERROR: {error}")


if __name__ == "__main__":
    main()