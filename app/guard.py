# app/guard.py

def is_about_bot(question: str) -> bool:
    """Mendeteksi apakah user bertanya tentang identitas bot."""
    keywords = [
        "kamu siapa", "siapa kamu", "bot apa", "chatbot apa", 
        "ini apa", "perkenalkan diri", "tugasmu apa"
    ]
    question_lower = question.lower()
    return any(k in question_lower for k in keywords)

def is_gratitude(question: str) -> bool:
    """Mendeteksi ucapan terima kasih."""
    keywords = [
        "terima kasih", "makasih", "thanks", "thank you", 
        "trims", "suwun", "hatur nuhun"
    ]
    question_lower = question.lower()
    return any(k in question_lower for k in keywords)

def is_geology_related(question: str) -> bool:
    """
    Mendeteksi apakah pertanyaan relevan dengan Geologi/Sesar.
    Jika False, berarti Out of Context.
    """
    keywords = [
        "sesar", "patahan", "fault", "gempa", "bumi", 
        "tektonik", "geologi", "lempeng", "seismik",
        "magnitudo", "geser", "strike-slip", "subduksi",
        "geovalid", "tanah", "batuan"
    ]
    question_lower = question.lower()
    return any(k in question_lower for k in keywords)

# --- Response Templates ---

def get_identity_response() -> str:
    return "Saya adalah chatbot geologi yang membahas seputar patahan sesar. Ada yang bisa saya bantu terkait topik tersebut?"

def get_gratitude_response() -> str:
    return "Sama-sama. Semoga informasi yang saya berikan bermanfaat untuk menambah wawasan Anda mengenai geologi."

def get_fallback_response() -> str:
    return "Maaf saya tidak memiliki pengetahuan atas itu, tanya saya seputar geologi khususnya patahan sesar."