from langchain_cohere import ChatCohere 

import os
# Load from environment
COHERE_API_KEY = os.getenv("cohere_api_key")

llm = ChatCohere(
    cohere_api_key=COHERE_API_KEY, 
    model="command-r", 
    streaming=True
) 