from fastapi import FastAPI
from pydantic import BaseModel
from app.llm import generate_response

app = FastAPI(title="GeoValid Generative Chatbot")

class Query(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "GeoValid Generative is Running 🚀"}

@app.post("/chatbot-generative")
def chat(query: Query):
    # Langsung kirim ke Gemini (Logic pembatasan sudah ada di System Prompt Gemini)
    answer = generate_response(query.question)
    
    return {"answer": answer}