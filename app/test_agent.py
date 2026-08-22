from agent import SupportAgent


def main():

    agent = SupportAgent()

    session_id = "memory-test"

    print("=" * 70)
    print("CONVERSATION MEMORY TEST")
    print("=" * 70)

    question1 = "What is the standard return window?"

    print("\nCUSTOMER:")
    print(question1)

    result1 = agent.answer(
        question1,
        session_id=session_id
    )

    print("\nASSISTANT:")
    print(result1["response"])

    print("\nSOURCES:")
    print(result1["sources"])

    question2 = "What about TrailPlus members?"

    print("\nCUSTOMER:")
    print(question2)

    result2 = agent.answer(
        question2,
        session_id=session_id
    )

    print("\nASSISTANT:")
    print(result2["response"])

    print("\nSOURCES:")
    print(result2["sources"])


if __name__ == "__main__":
    main()