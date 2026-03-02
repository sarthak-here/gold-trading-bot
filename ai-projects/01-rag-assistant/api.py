from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="RAG Assistant Starter")


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/ask")
def ask(req: AskRequest):
    # Placeholder: retrieval + generation pipeline will be wired next
    return {
        "question": req.question,
        "answer": "Stub response: retrieval pipeline not connected yet.",
        "sources": [],
    }
