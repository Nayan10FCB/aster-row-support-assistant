# Aster & Row Support Assistant

A simple customer support assistant built using Retrieval-Augmented Generation (RAG).

The system retrieves relevant information from the Aster & Row knowledge base and uses a local Large Language Model (LLM) to generate customer-support responses.

The project also includes an order lookup tool, conversation memory, basic safety handling, and a simple Flask web interface.

## Features

- Retrieval-Augmented Generation (RAG)
- Local text embeddings
- ChromaDB vector database
- Local Large Language Model (LLM)
- Knowledge-base document retrieval
- Active-document filtering
- Order lookup tool
- Conversation memory using sessions
- Basic safety handling
- Human handoff handling
- Simple Flask web interface
- No OpenAI API key required

## Technologies Used

- Python
- Flask
- ChromaDB
- Sentence Transformers
- Hugging Face Transformers
- PyTorch
- PyYAML

## Project Structure

```text
ASSIGNMENT/
│
├── app/
│   ├── agent.py
│   ├── index_kb.py
│   ├── llm.py
│   ├── main.py
│   ├── order_tool.py
│   ├── rag.py
│   ├── web.py
│   ├── test_agent.py
│   ├── test_llm.py
│   ├── test_order_tool.py
│   ├── test_rag.py
│   └── templates/
│       └── index.html
│
├── data/
│   ├── orders.json
│   └── orders-data-dictionary.md
│
├── evaluation/
│   └── visible-cases.json
│
├── knowledge-base/
│   ├── 01-returns-policy-current.md
│   ├── 02-returns-policy-legacy.md
│   ├── 03-final-sale-and-promotions.md
│   ├── 04-damaged-or-wrong-items.md
│   ├── 05-domestic-shipping.md
│   ├── 06-international-shipping.md
│   ├── 07-warranty.md
│   ├── 08-order-changes-and-cancellations.md
│   ├── 09-trailplus-membership.md
│   ├── 10-gift-cards-and-price-adjustments.md
│   ├── 11-product-care.md
│   ├── 12-breeze-tumbler-product-card.md
│   ├── 13-support-escalation.md
│   └── 14-internal-content-migration-notes.md
│
├── tests/
├── templates/
├── logs/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md