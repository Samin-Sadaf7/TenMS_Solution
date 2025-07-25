from app.memory import memory
from app.prompt_template import prompt_template
from app.retrieval import retrieve_with_scores
from app.clients.cohere_client import co
from app.clients.llm_client import llm
from langchain.schema import HumanMessage

def rag_chat_with_memory(query: str) -> str:
    memory.chat_memory.add_user_message(query)

    bm25_results = retrieve_with_scores(query)
    top_texts = [res["context"] for res in bm25_results[:10]]

    rerank_res = co.rerank(query=query, documents=top_texts, top_n=3, return_documents=True)
    final_texts = [
        res.document.text if hasattr(res.document, "text") else res.document
        for res in rerank_res.results
    ]
    context = "\n".join(final_texts)
    prompt = prompt_template.format(context=context, question=query)

    answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    memory.chat_memory.add_ai_message(answer)
    return answer
