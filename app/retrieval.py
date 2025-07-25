from rank_bm25 import BM25Okapi
from app.vectorstore import faiss_store
from app.utils import bm25_tokenizer

def retrieve_with_scores(query: str, k: int = 10):
    # Use public method instead of private method
    retriever = faiss_store.as_retriever(search_kwargs={"k": k})
    candidate_docs = retriever.get_relevant_documents(query)  # Public method
    
    candidate_texts = [doc.page_content for doc in candidate_docs]

    tokenized_query = bm25_tokenizer(query)
    tokenized_candidates = [bm25_tokenizer(text) for text in candidate_texts]
    bm25 = BM25Okapi(tokenized_candidates)
    scores = bm25.get_scores(tokenized_query)

    results = [{"context": text, "score": float(score)} for text, score in zip(candidate_texts, scores)]
    return sorted(results, key=lambda x: x["score"], reverse=True)