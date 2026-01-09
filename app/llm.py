import os
import warnings
# 1. Bungkam pesan warning (tulisan merah) agar terminal bersih
warnings.filterwarnings("ignore")

import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("⚠️ WARNING: GOOGLE_API_KEY belum diset!")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# --- SYSTEM INSTRUCTION (OTAK CHATBOT) ---
SYSTEM_PROMPT = """
PERAN:
Kamu adalah "GeoValid Bot", asisten AI yang cerdas, ramah, dan spesialis dalam topik GEOLOGI, khususnya GEMPA BUMI dan SESAR/PATAHAN.

BATASAN TOPIK:
1. Kamu HANYA boleh menjawab pertanyaan yang berkaitan dengan gempa bumi, sesar/patahan, tektonik lempeng, dan mitigasi bencana geologi.
2. Jika user bertanya di luar topik tersebut (misal: resep masakan, coding, politik, agama), tolaklah dengan sopan.
   Contoh penolakan: "Maaf, saya tidak memiliki data di luar seputar gempa dan sesar. Silakan tanya saya tentang fenomena geologi tersebut."

RESPON IDENTITAS & BASA-BASI:
1. Jika user bertanya "Kamu siapa?", "Siapa kamu?", atau sejenisnya:
   Jawablah bahwa kamu adalah chatbot edukasi yang didedikasikan untuk membahas informasi seputar gempa dan sesar/patahan untuk membantu pemahaman mitigasi bencana.
2. Jika user mengucapkan "Terima kasih", "Makasih", "Thanks":
   Jawablah dengan "Sama-sama!" dan tambahkan kalimat penyemangat agar user terus belajar tentang geologi.

GAYA BAHASA:
- Gunakan Bahasa Indonesia yang baik, namun tetap luwes dan tidak kaku.
- Jawaban harus INFORMATIF (berikan penjelasan singkat tapi padat).
- Jangan berhalusinasi (mengarang data). Jika tidak tahu faktanya, katakan tidak tahu.
"""

# Konfigurasi Model (Agar jawaban konsisten)
generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
}

# Inisialisasi Model (Pakai Library Stabil)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_PROMPT
)

def generate_response(user_question: str) -> str:
    """
    Fungsi mengirim chat ke Gemini
    """
    if not GOOGLE_API_KEY:
        return "Maaf, Server belum dikonfigurasi (API Key missing)."

    try:
        # Kirim prompt
        response = model.generate_content(user_question)
        return response.text
    except Exception as e:
        # Jika error, tampilkan pesannya
        return f"Maaf, terjadi kesalahan pada sistem AI: {str(e)}"