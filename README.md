# Aster & Row Customer Support AI Agent

A local AI-powered customer support agent that uses Retrieval-Augmented Generation (RAG), a local LLM, order lookup tools, conversation memory, source citations, and safe escalation to human support.

---

## 1. Setup and Run Instructions

### Requirements

- Python 3.11+
- Git
- Internet connection for downloading the required Hugging Face models on first run

### Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd ASSIGNMENT
```

### Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Run the Application

From the project root:

```powershell
python -m app.main
```

The support agent runs directly in the terminal.

### Run the Evaluation Suite

```powershell
python -m pytest -v
```

---

## 2. Environment Variables

The project uses a local LLM and does not require an OpenAI API key.

A Hugging Face token is optional and can be used for higher download limits.

Create a `.env` file:

```text
HF_TOKEN=your_huggingface_token_here
```

### .env.example

The repository includes an `.env.example` file:

```text
HF_TOKEN=
```

No real credentials or API keys should be committed to the repository.

---

## 3. Model and Technology Choices

### Language

Python

### LLM

The project uses:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The model is loaded locally using Hugging Face Transformers.

### Embeddings

A local sentence-embedding model is used to convert knowledge-base documents into vector embeddings.

These embeddings allow the system to retrieve relevant information based on semantic similarity.

### RAG

The project uses Retrieval-Augmented Generation (RAG).

The system retrieves relevant knowledge-base information before generating the final customer-support response.

### Vector Database

ChromaDB is used for local vector storage and semantic retrieval.

### Order Storage

Order information is stored locally in:

```text
data/orders.json
```

### Testing

Pytest is used for automated evaluation and regression testing.

---

## 4. Architecture

The system follows this general flow:

```text
                     CUSTOMER
                         |
                         v
                  +--------------+
                  | SupportAgent |
                  +--------------+
                         |
              +----------+----------+
              |                     |
              v                     v
       Order-related          Knowledge-related
          request                 request
              |                     |
              v                     v
        +-----------+          +---------+
        | OrderTool |          |   RAG   |
        +-----------+          +---------+
              |                     |
              v                     v
        orders.json              ChromaDB
                                    |
                                    v
                           Retrieved Context
                                    |
                                    v
                              Local LLM
                                    |
                                    v
                             Final Response
                                    |
                                    v
                              Citations
```

### Main Components

```text
app/
├── __init__.py
├── agent.py
├── llm.py
├── main.py
├── order_tool.py
├── rag.py
└── index_kb.py

tests/
├── test_agent.py
├── test_llm.py
├── test_order_tool.py
└── test_rag.py
```

### SupportAgent

`agent.py` coordinates the main support workflow.

It handles:

- Customer questions
- Knowledge-base retrieval
- Order lookup
- Conversation memory
- Source citations
- Safe responses and escalation

### RAGSystem

`rag.py` handles:

- Knowledge-base loading
- Embedding generation
- ChromaDB storage
- Semantic retrieval

### LocalLLM

`llm.py` loads and runs the local Qwen model.

### OrderTool

`order_tool.py` performs order lookups from the local order data.

The order tool also handles different order ID formats such as:

```text
ORD-1001
ord-1001
ORD 1001
ORD_1001
```

### Main Application

`main.py` provides the terminal-based interface.

---

## 5. Evaluation Command

Run the complete automated evaluation suite with:

```powershell
python -m pytest -v
```

The final evaluation result is:

```text
10 passed, 1 warning
```

---

## 6. Baseline and Final Evaluation Results

### Baseline Result

During development, the first complete evaluation produced:

```text
9 passed
1 failed
```

The failed test was:

```text
test_return_window_retrieval
```

The RAG system retrieved related return-policy information but did not retrieve the passage containing the required return-window information.

### Final Result

After fixing the retrieval issue:

```text
10 passed
1 warning
```

### Evaluation Breakdown

| Category | Tests | Baseline | Final |
|---|---:|---:|---:|
| Conversation Memory | 1 | PASS | PASS |
| Local LLM | 1 | PASS | PASS |
| Order Lookup | 3 | PASS | PASS |
| RAG Retrieval | 5 | 4 PASS / 1 FAIL | 5 PASS |
| **Total** | **10** | **9 PASS / 1 FAIL** | **10 PASS** |

### Final Pass Rate

```text
10 / 10 = 100%
```

The remaining warning is a ChromaDB dependency deprecation warning and does not cause a test failure.

---

---

## 7. Bug Diary

### Bug 1 — Return Window Retrieval Failure

#### Reproduced Failure

During development, running:

```powershell
python -m pytest -v
```

produced:

```text
tests/test_rag.py::test_return_window_retrieval FAILED
```

The test expected the retrieved knowledge-base results to contain either:

```text
30 calendar days
```

or:

```text
45-calendar-day
```

However, the retrieved results contained related return-policy information but did not contain the actual return-window statement.

#### Root Cause

The semantic retrieval results were related to returns, but the most relevant return-window passage was not included in the top retrieved results.

#### Fix

The RAG retrieval/policy handling was adjusted so that the relevant return-window information is retrieved for the query.

#### Regression Test

The test:

```text
tests/test_rag.py::test_return_window_retrieval
```

was rerun after the fix.

Result:

```text
PASSED
```

---

### Bug 2 — Test Import Errors After Moving Tests

#### Reproduced Failure

The test files were moved from:

```text
app/
```

to:

```text
tests/
```

After moving them, running:

```powershell
python -m pytest -v
```

produced errors such as:

```text
ModuleNotFoundError: No module named 'agent'
ModuleNotFoundError: No module named 'llm'
ModuleNotFoundError: No module named 'order_tool'
```

#### Root Cause

The test files were still using imports designed for when the tests were located inside the `app` directory.

For example:

```python
from llm import LocalLLM
```

When pytest collected tests from the separate `tests/` directory, Python could not find the application modules using those imports.

#### Fix

The project was converted to use the `app` directory as a Python package.

An:

```text
app/__init__.py
```

file was added.

The imports were changed to:

```python
from app.agent import SupportAgent
from app.llm import LocalLLM
from app.order_tool import OrderTool
from app.rag import RAGSystem
```

#### Regression Test

The complete evaluation suite was run again:

```powershell
python -m pytest -v
```

Result:

```text
10 passed
```

---

### Bug 3 — Application Launch Import Error

#### Reproduced Failure

Running:

```powershell
python -m app.main
```

initially produced:

```text
ModuleNotFoundError: No module named 'agent'
```

#### Root Cause

`app/main.py` originally imported the agent using:

```python
from agent import SupportAgent
```

This worked when running the file directly from the `app` directory but failed when launching the application as a Python module from the project root.

#### Fix

The import was changed to:

```python
from app.agent import SupportAgent
```

The application imports were updated to use the package structure consistently.

#### Regression Test

The application can now be started from the project root with:

```powershell
python -m app.main
```

The evaluation suite also confirms that the application modules can be imported correctly:

```text
10 passed, 1 warning
```

---

## 8. Known Limitations and Future Improvements

### Known Limitations

1. The local LLM can be slow when running on CPU.
2. The first run takes longer because the embedding model and LLM need to be downloaded and loaded.
3. The Qwen 0.5B model is relatively small and may produce less detailed responses than larger models.
4. RAG retrieval can sometimes return related information instead of the exact most relevant passage.
5. Orders are stored in a local JSON file rather than a live order-management system.
6. The agent cannot actually issue refunds, replacements, or cancellations.
7. Some customer cases require human review.
8. The application currently runs as a terminal application.
9. Hugging Face may display an unauthenticated-request warning when `HF_TOKEN` is not configured.

### Future Improvements

Before production, I would:

- Use a stronger production-grade LLM.
- Improve retrieval using hybrid keyword and semantic search.
- Add a reranking step for retrieved documents.
- Add more adversarial and edge-case evaluation tests.
- Connect the order tool to a real order-management API.
- Add authentication and authorization.
- Add monitoring and structured logging.
- Improve response latency and model inference performance.
- Add stronger hallucination prevention.
- Add continuous integration for automated regression testing.

---

## 9. AI Coding Tools Used

AI coding assistance was used during development to help with:

- Python debugging.
- Project structure.
- Moving test files from `app/` into `tests/`.
- Fixing Python import errors.
- Debugging RAG retrieval.
- Improving test coverage.
- Reviewing assignment requirements.
- Preparing README documentation.

### Example of an Incorrect or Incomplete AI Suggestion

During development, the tests were moved from:

```text
app/
```

to:

```text
tests/
```

The test files initially used imports such as:

```python
from llm import LocalLLM
```

After moving the tests, this caused:

```text
ModuleNotFoundError: No module named 'llm'
```

Similar errors occurred with:

```text
agent
order_tool
rag
```

The issue was that the imports did not account for the changed Python package structure.

The imports were changed to:

```python
from app.llm import LocalLLM
from app.agent import SupportAgent
from app.order_tool import OrderTool
from app.rag import RAGSystem
```

An `app/__init__.py` file was also added.

After the fix, the complete evaluation suite passed:

```text
10 passed, 1 warning
```

This demonstrates an example where an AI-assisted coding suggestion was incomplete because it did not account for the changed project directory structure.

---

## 10. Demo Video / GIF

A 2–4 minute demonstration is included in the repository.

The demonstration covers all required scenarios:

1. Knowledge-base question with citations.
2. Order lookup.
3. Multi-turn conversation.
4. Correct refusal to guess or recommendation for human help.
5. Evaluation suite running.

### Demo

### Demo Video

[▶️ Watch the Aster & Row Support Agent Demo — ASSISTANT.mp4](ASSISTANT.mp4)
### Demo 1 — Knowledge-Base Question with Citations

```text
CUSTOMER:
What is the standard return window?

ASSISTANT:
The standard return window is 30 calendar days from delivery.

SOURCES:
- 01-returns-policy-current.md
- 09-trailplus-membership.md
- 04-damaged-or-wrong-items.md
- 03-final-sale-and-promotions.md
```

This demonstrates that the agent retrieves information from the knowledge base and provides source citations.

---

### Demo 2 — Order Lookup

```text
CUSTOMER:
What is the status of ORD-1001?

ASSISTANT:
Order ORD-1001 status: pending.

SOURCES:
- orders.json
```

This demonstrates the order lookup tool.

---

### Demo 3 — Multi-Turn Conversation

```text
CUSTOMER:
What is the standard return window?

ASSISTANT:
The standard return window is 30 calendar days from delivery.

CUSTOMER:
What about TrailPlus members?

ASSISTANT:
TrailPlus members receive a 45-calendar-day return window from delivery for eligible items, provided membership was active when the order was placed.
```

This demonstrates that the agent maintains context across multiple turns.

---

### Demo 4 — Refusal / Human Help

```text
CUSTOMER:
My item has a manufacturing defect. Can you guarantee that I will get a replacement?

ASSISTANT:
I can't guarantee that a refund or replacement has been approved. This case requires review under the warranty/support policy and may require human assistance.
```

The agent does not invent an approval or guarantee an outcome that it cannot verify.

---

### Demo 5 — Evaluation Suite

Run:

```powershell
python -m pytest -v
```

Final result:

```text
10 passed, 1 warning
```

The evaluation suite covers:

- Conversation memory
- Local LLM response generation
- Order lookup
- Invalid order handling
- Missing-order handling
- Return-policy retrieval
- Return-window retrieval
- Shipping retrieval
- Warranty retrieval
- Membership retrieval

---

## Project Summary

The Aster & Row Support Agent demonstrates:

- Local LLM inference
- Retrieval-Augmented Generation
- Semantic knowledge-base search
- Source citations
- Order lookup
- Order ID normalization
- Multi-turn conversation memory
- Safe refusal and human escalation
- Automated evaluation
- Regression testing

### Final Evaluation

```text
10 / 10 tests passed
100% pass rate
```