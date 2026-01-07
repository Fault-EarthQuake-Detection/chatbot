from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import answer_question
from app.llm import generate_answer
from app.guard import is_about_bot, is_geology_related

app = FastAPI(title="GeoValid Chatbot")

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    q = query.question.lower()

    if is_about_bot(q):
        return {
            "answer": (
                "Saya adalah chatbot geologi pada aplikasi GeoValid "
                "yang berfokus pada patahan sesar berdasarkan jurnal ilmiah."
            )
        }

    if not is_geology_related(q):
        return {
            "answer": "Maaf, saya tidak memiliki pengetahuan mengenai topik tersebut."
        }

    context = answer_question(q)

    if not context:
        return {
            "answer": "Maaf, saya tidak menemukan informasi terkait di dataset jurnal."
        }

    answer = generate_answer(q, context)
    return {"answer": answer}
