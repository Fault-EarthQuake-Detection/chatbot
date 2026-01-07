def is_about_bot(question: str) -> bool:
    keywords = ["kamu siapa", "chatbot apa", "ini chatbot apa"]
    return any(k in question for k in keywords)

def is_geology_related(question: str) -> bool:
    keywords = [
        "sesar", "patahan", "fault",
        "strike-slip", "normal fault",
        "reverse fault", "tektonik"
    ]
    return any(k in question for k in keywords)
