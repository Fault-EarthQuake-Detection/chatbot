---
title: GeoValid Chatbot (Generative)
emoji: 🌋
colorFrom: orange
colorTo: red
sdk: docker
pinned: false
---

# GeoValid Chatbot (Generative Edition)

Chatbot ini adalah asisten virtual cerdas yang didedikasikan untuk edukasi seputar **Geologi, Gempa Bumi, dan Sesar/Patahan**.

Berbeda dengan versi sebelumnya, versi ini menggunakan **Google Gemini API** (Generative AI) yang telah diinstruksikan secara khusus (System Prompting) untuk menjawab dengan cepat, akurat, dan tetap dalam konteks geologi.

### Fitur Utama:
* **Super Cepat:** Respon dalam hitungan detik menggunakan Gemini Flash Model.
* **Topic Guardrail:** Otomatis menolak pertanyaan di luar topik (misal: resep masakan, politik).
* **Smart Persona:** Memiliki identitas sebagai ahli geologi yang ramah.

### Teknologi:
* **Framework:** FastAPI (Python)
* **AI Engine:** Google Gemini API (`google-genai`)
* **Deployment:** Docker Container

---
*Dibuat untuk Capstone Project GeoValid.*