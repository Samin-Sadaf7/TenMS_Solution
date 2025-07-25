from fastapi import APIRouter, Query
from models import QueryRequest
from core import rag_chat_with_memory
from memory import memory
from retrieval import retrieve_with_scores

router = APIRouter()

@router.post("/query")
def answer_query(request: QueryRequest):
    answer = rag_chat_with_memory(request.query)
    return {"query": request.query, "answer": answer}

@router.get("/last-messages")
def get_last_two_messages():
    messages = memory.chat_memory.messages[-4:]
    return [{"role": msg.type, "content": msg.content} for msg in messages]

@router.get("/relevant-contexts")
def get_contexts(query: str = Query(...)):
    results = retrieve_with_scores(query)
    return results
