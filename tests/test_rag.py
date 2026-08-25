from app.rag import RAGSystem


def test_return_policy_retrieval():

    rag = RAGSystem()

    results = rag.search(
        "What is the return policy?",
        n_results=3
    )

    assert results

    filenames = [
        result["metadata"].get("filename")
        for result in results
    ]

    assert "01-returns-policy-current.md" in filenames


def test_return_window_retrieval():

    rag = RAGSystem()

    results = rag.search(
        "How long do I have to return an item?",
        n_results=3
    )

    assert results

    filenames = [
        result["metadata"].get("filename")
        for result in results
    ]

    assert any(
        filename in [
            "01-returns-policy-current.md",
            "03-final-sale-and-promotions.md",
            "09-trailplus-membership.md",
        ]
        for filename in filenames
    )


def test_shipping_retrieval():

    rag = RAGSystem()

    results = rag.search(
        "What are the shipping options?",
        n_results=3
    )

    assert results

    filenames = [
        result["metadata"].get("filename")
        for result in results
    ]

    assert "05-domestic-shipping.md" in filenames


def test_warranty_retrieval():

    rag = RAGSystem()

    results = rag.search(
        "What is the warranty policy?",
        n_results=3
    )

    assert results

    filenames = [
        result["metadata"].get("filename")
        for result in results
    ]

    assert "07-warranty.md" in filenames


def test_membership_retrieval():

    rag = RAGSystem()

    results = rag.search(
        "How does membership work?",
        n_results=3
    )

    assert results

    filenames = [
        result["metadata"].get("filename")
        for result in results
    ]

    assert "09-trailplus-membership.md" in filenames