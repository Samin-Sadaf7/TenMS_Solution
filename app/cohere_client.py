import cohere
import os

# Load from environment
COHERE_API_KEY = os.getenv("cohere_api_key")

co = cohere.Client(COHERE_API_KEY)
