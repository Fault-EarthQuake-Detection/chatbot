# evaluation.py
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from app.rag import answer_question  # Kita pakai fungsi RAG utama

# Download tokenizer jika belum ada
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# --- DATASET UJIAN (Ground Truth) ---
# Isi dengan pertanyaan dan jawaban ideal yang kamu harapkan (dari jurnal)
test_data = [
    {
        "question": "Apa itu sesar lembang?",
        "reference": "Sesar Lembang adalah patahan geser aktif yang terletak di Kecamatan Lembang, Kabupaten Bandung Barat, Jawa Barat."
    },
    {
        "question": "Bagaimana mekanisme sesar mendatar?",
        "reference": "Sesar mendatar atau strike-slip fault terjadi ketika dua blok batuan bergeser secara horizontal satu sama lain."
    },
    {
        "question": "Apa dampak gempa akibat sesar aktif?",
        "reference": "Gempa akibat sesar aktif dapat menyebabkan kerusakan bangunan, tanah longsor, dan retakan pada permukaan tanah."
    }
    # Tambahkan 5-10 pertanyaan lagi agar hasil evaluasi lebih valid
]

def calculate_evaluation():
    print("\n📊 --- MEMULAI EVALUASI MODEL (BLEU SCORE) ---")
    print(f"Jumlah Pertanyaan Uji: {len(test_data)}")
    print("-" * 70)
    print(f"{'PERTANYAAN':<30} | {'BLEU':<10} | {'STATUS'}")
    print("-" * 70)

    total_score = 0
    chencherry = SmoothingFunction() # Smoothing agar nilai tidak 0 jika kalimat pendek

    for item in test_data:
        q = item['question']
        ref_text = item['reference']
        
        # 1. Dapatkan jawaban dari Chatbot
        # Kita gunakan try-except agar evaluasi tidak berhenti jika ada error satu soal
        try:
            candidate_text = answer_question(q)
        except Exception as e:
            print(f"Error pada pertanyaan '{q}': {e}")
            candidate_text = ""

        # 2. Preprocessing (Lowercase & Tokenizing)
        ref_tokens = nltk.word_tokenize(ref_text.lower())
        cand_tokens = nltk.word_tokenize(candidate_text.lower())
        
        # 3. Hitung BLEU Score
        # Weights (0.5, 0.5) artinya kita menilai kecocokan kata per kata (1-gram) 
        # dan kecocokan frasa 2 kata (2-gram).
        score = sentence_bleu(
            [ref_tokens], 
            cand_tokens, 
            weights=(0.5, 0.5), 
            smoothing_function=chencherry.method1
        )
        
        total_score += score
        
        # Tampilkan status sederhana
        status = "✅ Bagus" if score > 0.3 else "⚠️ Kurang"
        print(f"{q[:27]+'...':<30} | {score:.4f}     | {status}")

    # Rata-rata
    avg_score = total_score / len(test_data)
    
    print("-" * 70)
    print(f"RATA-RATA BLEU SCORE: {avg_score:.4f}")
    print("-" * 70)
    
    if avg_score > 0.4:
        print("Kesimpulan: Model menjawab CUKUP AKURAT sesuai referensi.")
    elif avg_score > 0.2:
        print("Kesimpulan: Model menjawab RELEVAN tapi redaksi kalimat berbeda.")
    else:
        print("Kesimpulan: Jawaban model masih kurang mirip dengan referensi.")

if __name__ == "__main__":
    calculate_evaluation()