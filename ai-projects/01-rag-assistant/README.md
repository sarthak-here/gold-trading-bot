# 01 — RAG Assistant

## Goal
Document Q&A assistant over local files/web docs.

## Stack
- Python, FastAPI
- LangChain / LlamaIndex style pipeline
- FAISS or ChromaDB for vector search
- sentence-transformers embeddings

## Math / Core concepts
- Cosine similarity: `sim(a,b)=a·b/(||a|| ||b||)`
- Chunking and retrieval top-k
- Prompt grounding to reduce hallucination

## Planned files
- `ingest.py`
- `retriever.py`
- `api.py`
