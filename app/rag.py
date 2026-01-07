from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.llm import llm_pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "vectorstore" / "faiss_index"

print("🔎 Loading FAISS from:", DB_PATH)
print("📂 Exists?", DB_PATH.exists())
print("📄 Files:", list(DB_PATH.glob("*")))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

def answer_question(question: str) -> str:
    docs = db.similarity_search(question, k=3)

    if not docs:
        return "Maaf, saya tidak menemukan informasi terkait di jurnal."

    context = "\n".join(d.page_content for d in docs)

    prompt = f"""
Kamu adalah chatbot geologi khusus patahan sesar.
Jawablah HANYA berdasarkan konteks jurnal berikut.

Konteks:
{context}

Pertanyaan:
{question}

Jawaban:
"""

    response = llm_pipeline(prompt)[0]["generated_text"]
    return response.split("Jawaban:")[-1].strip()
