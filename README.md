# Agentic Corrective RAG

An intelligent Retrieval-Augmented Generation (RAG) system that dynamically decides whether to answer from uploaded documents or perform web search when local knowledge is insufficient.

Unlike traditional PDF chatbots that fail when information is unavailable in uploaded documents, this system evaluates retrieval quality and automatically switches to web search, providing more reliable and grounded responses.

---

## Features

- Multi-PDF upload and semantic search
- Dynamic local vs web routing
- Retrieval quality evaluation
- Automatic query rewriting for better search performance
- Web fallback using Tavily Search API
- Grounded answer generation using Llama 3.3 70B
- Source identification for every response
- Temporary vector database generation for uploaded files
- Dockerized deployment
- Public deployment via Hugging Face Spaces

---

## System Architecture

```text
                           User Query
                                │
                                ▼
                    ┌────────────────────┐
                    │    Retrieve Node   │
                    │ Chroma Similarity  │
                    │ Search on Uploaded │
                    │    PDF Chunks      │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │  Retrieval Grader  │
                    │ Evaluate Similarity│
                    │      Score         │
                    └───────┬─────┬──────┘
                            │     │
              High Score    │     │ Low Score
                            │     │
                            ▼     ▼
                    ┌──────────┐ ┌──────────────┐
                    │ Generate │ │ Rewrite Query│
                    │ Response │ └──────┬───────┘
                    └────┬─────┘        │
                         │              ▼
                         │      ┌──────────────┐
                         │      │ Tavily Search│
                         │      │  Web Search  │
                         │      └──────┬───────┘
                         │             │
                         └──────┬──────┘
                                ▼
                      ┌──────────────────┐
                      │ Llama 3.3 70B    │
                      │ Response         │
                      │ Generation       │
                      └──────────────────┘
```

---

## Workflow

### 1. Document Upload and Indexing

Uploaded PDFs are:

- Parsed using PyMuPDF
- Split into semantic chunks
- Embedded using BGE Base Embeddings
- Stored temporarily in ChromaDB

```text
PDF Upload
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Temporary Chroma Vector Store
```

---

### 2. Retrieval

The user's query is converted into embeddings and compared with stored document embeddings using cosine similarity.

```text
Question
   ↓
Embedding
   ↓
Similarity Search
   ↓
Top-K Relevant Chunks
```

---

### 3. Retrieval Grading

The system evaluates the retrieval score:

- **Above threshold → Local Generation**
- **Below threshold → Web Search Pipeline**

This prevents hallucinations and improves answer reliability.

---

### 4. Query Rewriting

If retrieval confidence is low, the query is rewritten into a concise search query optimized for web retrieval.

Example:

```text
Original:
Where is Chennai located?

Rewritten:
Chennai location
```

---

### 5. Web Search

The rewritten query is sent to Tavily Search API.

Retrieved web snippets are converted into LangChain Documents and forwarded to the generation node.

---

### 6. Response Generation

Responses are generated using **Llama 3.3 70B Versatile** hosted on Groq using only the retrieved context.

This ensures:

- Grounded responses
- Reduced hallucinations
- Better factual accuracy

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Workflow Orchestration | LangGraph |
| Vector Database | ChromaDB |
| Embedding Model | BAAI/bge-base-en-v1.5 |
| PDF Processing | PyMuPDF |
| Web Search | Tavily API |
| LLM | Llama 3.3 70B via Groq |
| Deployment | Docker + Hugging Face Spaces |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/agentic-corrective-rag.git
cd agentic-corrective-rag
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run Locally

```bash
streamlit run app.py
```

---

### Web Retrieval

```text
Who won the FIFA World Cup in 2022?
```

Source:

```text
Web Search
```

---

## Future Improvements

- Hybrid Retrieval (BM25 + Dense Retrieval)
- Cross-Encoder Re-ranking
- Multi-modal PDF understanding
- Citation generation with URLs
- Persistent vector storage
- Conversational memory
- Multi-agent planning workflows

---

## Author

**Varunesh V**

---
