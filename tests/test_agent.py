from app.agent import SupportAgent


def test_conversation_memory():
    agent = SupportAgent()

    session_id = "memory-test"

    question1 = "What is the standard return window?"

    result1 = agent.answer(
        question1,
        session_id=session_id
    )

    assert result1["response"]
    assert "30" in result1["response"]
    assert result1["sources"]

    question2 = "What about TrailPlus members?"

    result2 = agent.answer(
        question2,
        session_id=session_id
    )

    assert result2["response"]
    assert "45" in result2["response"]
    assert result2["sources"]