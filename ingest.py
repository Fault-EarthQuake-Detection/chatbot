import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 

DATA_DIR = "data/journals"
DB_PATH = "vectorstore"

all_docs = []

print("🔍 Scanning PDF files...")
# Pastikan folder ada
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    raise RuntimeError(f"❌ Folder {DATA_DIR} tidak ditemukan. Silakan buat folder dan isi dengan PDF.")

pdf_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]

if not pdf_files:
    raise RuntimeError("❌ Tidak ada file PDF di folder data/journals")

for pdf in pdf_files:
    try:
        print(f"📄 Loading {os.path.basename(pdf)}")
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        
        # CLEANING: Hapus baris baru yang bikin teks putus-putus
        for d in docs:
            d.page_content = d.page_content.replace("\n", " ")
            
        all_docs.extend(docs)
        print(f"   ✅ {len(docs)} pages loaded")
    except Exception as e:
        print(f"   ❌ Gagal memuat {pdf}: {e}")

if not all_docs:
    raise RuntimeError("❌ Tidak ada dokumen yang berhasil dimuat")

# Chunking diperbesar biar konteks tidak terpotong di tengah kalimat
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)
chunks = splitter.split_documents(all_docs)

print(f"✂️ Total chunks: {len(chunks)}")

# GANTI EMBEDDING KE MULTILINGUAL (Mode CPU)
print("🧠 Membuat Embedding Multilingual (Mode CPU)...")
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-small", 
    model_kwargs={'device': 'cpu'},  # <--- SUDAH DIGANTI KE CPU
    encode_kwargs={'normalize_embeddings': True}
)

print("💾 Menyimpan Vector Database...")
db = FAISS.from_documents(chunks, embeddings)
db.save_local(DB_PATH)

print("🎉 Vectorstore berhasil dibuat! Siap digunakan.")