from app.memory import memory
from app.prompt_template import prompt_template
from app.retrieval import retrieve_with_scores
from app.clients.cohere_client import co
from app.clients.llm_client import llm
from langchain.schema import HumanMessage

def rag_chat_with_memory(query: str) -> str:
    # Add user question to memory
    memory.chat_memory.add_user_message(query)

    # Step 1: Retrieve documents with BM25 scores (using fixed retrieval function)
    bm25_results = retrieve_with_scores(query, k=10)
    
    # Step 2: Extract text contexts from BM25 results
    candidate_texts = [res["context"] for res in bm25_results]
    
    # Step 3: Rerank with Cohere to get top-3
    rerank_res = co.rerank(
        query=query,
        documents=candidate_texts,
        top_n=3,
        return_documents=True
    )
    
    # Step 4: Extract final contexts
    final_texts = [res.document.text for res in rerank_res.results]
    
    # Step 5: Build context string
    context = "\n".join(final_texts)
    
    # Step 6: Generate answer
    prompt = prompt_template.format(context=context, question=query)
    answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    
    # Add AI response to memory and return
    memory.chat_memory.add_ai_message(answer)
    return answer