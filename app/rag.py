from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# Import fungsi generate_answer yang sudah diperbaiki
from app.llm import generate_answer  

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "vectorstore"

print("Loading Embedding Model to CPU...") # Ubah log jadi CPU
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-small",
    model_kwargs={'device': 'cpu'},         # <--- GANTI 'cuda' JADI 'cpu'
    encode_kwargs={'normalize_embeddings': True}
)

print("Loading Vector Database...")
db = FAISS.load_local(
    str(DB_PATH), 
    embeddings, 
    allow_dangerous_deserialization=True
)

def answer_question(question: str) -> str:
    # 1. Cari dokumen relevan (Retrieval)
    print(f"\n🔍 Mencari konteks untuk: '{question}'...")
    docs = db.similarity_search(question, k=3)

    if not docs:
        print("❌ Tidak ada dokumen yang cocok ditemukan.")
        return "Maaf, saya tidak menemukan informasi terkait di database jurnal."

    # Debug: Tampilkan judul dokumen yang ketemu
    print(f"✅ Ditemukan {len(docs)} potongan konteks.")
    for i, d in enumerate(docs):
        # Preview sedikit isinya biar yakin
        print(f"   - Dokumen {i+1}: {d.page_content[:100].replace(chr(10), ' ')}...")

    # 2. Gabungkan konten dokumen jadi satu string teks
    context_text = "\n\n".join([d.page_content for d in docs])

    # 3. Panggil LLM
    print("🤖 Sedang berpikir...")
    final_answer = generate_answer(question, context_text)
    
    return final_answer