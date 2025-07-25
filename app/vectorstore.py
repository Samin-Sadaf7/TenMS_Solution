from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load FAISS index
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
faiss_store = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
