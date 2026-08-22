from llm import LocalLLM


def main():

    llm = LocalLLM()

    response = llm.generate(
        system_prompt=(
            "You are a helpful customer support "
            "assistant."
        ),
        user_prompt=(
            "Write one short sentence saying "
            "hello to a customer."
        ),
    )

    print("\nMODEL RESPONSE:")
    print(response)


if __name__ == "__main__":
    main()