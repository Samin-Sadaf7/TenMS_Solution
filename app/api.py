from fastapi import APIRouter, Query
from app.models.QueryRequest import QueryRequest
from app.models.QueryInput import QueryInput
from app.core import rag_chat_with_memory
from app.memory import memory
from app.retrieval import retrieve_with_scores

router = APIRouter()

@router.post("/query")
def answer_query(request: QueryRequest):
    answer = rag_chat_with_memory(request.query)
    return {"query": request.query, "answer": answer}

@router.get("/last-messages")
def get_last_two_messages():
    messages = memory.chat_memory.messages[-4:]
    return [{"role": msg.type, "content": msg.content} for msg in messages]

@router.post("/relevant-contexts")
def get_contexts(request: QueryInput):
    results = retrieve_with_scores(request.query)
    return results
