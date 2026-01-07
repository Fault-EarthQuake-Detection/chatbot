import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DATA_DIR = "data/journals"
DB_PATH = "vectorstore"

all_docs = []

print("🔍 Scanning PDF files...")
pdf_files = [
    os.path.join(DATA_DIR, f)
    for f in os.listdir(DATA_DIR)
    if f.lower().endswith(".pdf")
]

if not pdf_files:
    raise RuntimeError("❌ Tidak ada file PDF di folder data/journals")

for pdf in pdf_files:
    try:
        print(f"📄 Loading {os.path.basename(pdf)}")
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        all_docs.extend(docs)
        print(f"   ✅ {len(docs)} pages loaded")
    except Exception as e:
        print(f"   ❌ Gagal memuat {pdf}: {e}")

if not all_docs:
    raise RuntimeError("❌ Tidak ada dokumen yang berhasil dimuat")

print(f"📚 Total pages loaded: {len(all_docs)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(all_docs)

print(f"✂️ Total chunks: {len(chunks)}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(chunks, embeddings)
db.save_local(DB_PATH)

print("🎉 Vectorstore berhasil dibuat")
