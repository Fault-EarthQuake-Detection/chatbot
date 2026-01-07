# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import answer_question
# Import fungsi baru is_gratitude dan get_gratitude_response
from app.guard import (
    is_about_bot, 
    is_geology_related, 
    is_gratitude,           # <--- Tambah ini
    get_identity_response, 
    get_fallback_response,
    get_gratitude_response  # <--- Tambah ini
)

app = FastAPI(title="GeoValid Chatbot")

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    q = query.question

    # 1. Cek Identitas
    if is_about_bot(q):
        return {"answer": get_identity_response()}

    # 2. Cek Terima Kasih (Baru)
    if is_gratitude(q):
        return {"answer": get_gratitude_response()}

    # 3. Cek Konteks Geologi
    # Penting: Cek geologi dilakukan SETELAH cek terima kasih, 
    # karena kata "terima kasih" tidak mengandung kata "sesar/geologi"
    if not is_geology_related(q):
        return {"answer": get_fallback_response()}

    # 4. Proses RAG (Jika lolos semua pengecekan)
    final_answer = answer_question(q)
    
    return {"answer": final_answer}