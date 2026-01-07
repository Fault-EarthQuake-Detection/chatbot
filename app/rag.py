from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.llm import generate_answer

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "vectorstore"

# Inisialisasi Model Embedding (Mode Silent)
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-small",
    model_kwargs={'device': 'cpu'}, 
    encode_kwargs={'normalize_embeddings': True}
)

# Load Vector Database
db = FAISS.load_local(
    str(DB_PATH), 
    embeddings, 
    allow_dangerous_deserialization=True
)

def answer_question(question: str) -> str:
    """
    Mencari konteks relevan dari vector store dan mengirimkannya ke LLM.
    Output langsung berupa string jawaban bersih.
    """
    # 1. Cari dokumen relevan (Retrieval)
    docs = db.similarity_search(question, k=3)

    # Jika tidak ada dokumen yang relevan
    if not docs:
        return "Maaf, informasi terkait tidak ditemukan dalam referensi jurnal yang tersedia."

    # 2. Gabungkan konten dokumen jadi satu string teks konteks
    context_text = "\n\n".join([d.page_content for d in docs])

    # 3. Panggil LLM untuk generate jawaban
    final_answer = generate_answer(question, context_text)
    
    return final_answer