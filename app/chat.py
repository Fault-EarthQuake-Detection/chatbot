# app/chat.py
from app.rag import answer_question
from app.guard import (
    is_about_bot, 
    is_geology_related, 
    is_gratitude,            # <--- Tambah ini
    get_identity_response, 
    get_fallback_response,
    get_gratitude_response   # <--- Tambah ini
)

print("💬 GeoValid Chat")
print("Ketik pertanyaan (ketik 'exit' untuk keluar)\n")

while True:
    q = input(">> ")

    if q.lower() in ["exit", "quit"]:
        print("👋 Sampai jumpa")
        break

    # 1. Cek Identitas Bot
    if is_about_bot(q):
        print(f"\n🤖 {get_identity_response()}\n")
        continue

    # 2. Cek Terima Kasih (Baru)
    if is_gratitude(q):
        print(f"\n🤖 {get_gratitude_response()}\n")
        continue

    # 3. Cek Apakah Topik Geologi?
    if not is_geology_related(q):
        print(f"\n🤖 {get_fallback_response()}\n")
        continue

    # 4. Jika Lolos, Masuk ke RAG
    try:
        answer = answer_question(q)
        print("\n🤖", answer, "\n")
    except Exception as e:
        print("❌ Error:", e)