from app.llm import LocalLLM


def test_llm_generates_response():

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

    assert response
    assert isinstance(response, str)
    assert len(response.strip()) > 0
