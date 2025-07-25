import cohere
import os
from dotenv import load_dotenv
# Load from environment
load_dotenv()  

COHERE_API_KEY = os.getenv("cohere_api_key")

co = cohere.Client(COHERE_API_KEY)
