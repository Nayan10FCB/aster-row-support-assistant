# Aster & Row Support Assistant

A simple customer support assistant built using Retrieval-Augmented Generation (RAG).

The system retrieves relevant information from the Aster & Row knowledge base and uses a local Large Language Model (LLM) to generate customer-support responses.

The project also includes an order lookup tool, conversation memory, basic safety handling, and a simple Flask web interface.

---

## Features

- Retrieval-Augmented Generation (RAG)
- Local text embeddings
- ChromaDB vector database
- Local Large Language Model (LLM)
- Knowledge-base document retrieval
- Active-document filtering
- Order lookup tool
- Conversation memory using sessions
- Basic prompt-injection/safety handling
- Human handoff handling
- Simple Flask web interface
- No OpenAI API key required

---

## Technologies Used

- Python
- Flask
- ChromaDB
- Sentence Transformers
- Hugging Face Transformers
- PyTorch
- PyYAML

---

## Project Structure

```text
ASSIGNMENT/
│
├── app/
│   ├── agent.py
│   ├── rag.py
│   ├── llm.py
│   ├── order_tool.py
│   ├── web.py
│   ├── index_kb.py
│   ├── test_rag.py
│   ├── test_agent.py
│   ├── test_order_tool.py
│   └── templates/
│       └── index.html
│
├── knowledge-base/
├── data/
├── evaluation/
├── tests/
├── logs/
├── templates/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md