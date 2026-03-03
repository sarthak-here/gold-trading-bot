from fastapi import FastAPI
from pydantic import BaseModel

from retriever import retrieve_top_k


app = FastAPI(title="RAG Assistant Starter")


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/ask")
def ask(req: AskRequest):
    chunks = retrieve_top_k(req.question, k=3)
    sources = [{"text": c.text, "score": c.score} for c in chunks]

    if not sources:
        answer = "No relevant context found."
    else:
        top = sources[0]["text"]
        answer = f"Based on retrieved context: {top}"

    return {
        "question": req.question,
        "answer": answer,
        "sources": sources,
    }
