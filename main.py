from fastapi import FastAPI
from app import api

app = FastAPI(title="Bangla RAG API")
app.include_router(api.router)
