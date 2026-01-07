from app.rag import answer_question

print("💬 GeoValid Chat")
print("Ketik pertanyaan (ketik 'exit' untuk keluar)\n")

while True:
    q = input(">> ")

    if q.lower() in ["exit", "quit"]:
        print("👋 Sampai jumpa")
        break

    try:
        answer = answer_question(q)
        print("\n🤖", answer, "\n")
    except Exception as e:
        print("❌ Error:", e)
