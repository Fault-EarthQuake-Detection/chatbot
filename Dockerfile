# Gunakan Python 3.10 yang stabil
FROM python:3.10-slim

# Set folder kerja
WORKDIR /app

# Buat folder cache untuk Hugging Face (wajib permission 777)
RUN mkdir -p /app/.cache && chmod -R 777 /app/.cache
ENV HF_HOME="/app/.cache"

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download data NLTK (agar tidak error saat evaluation/tokenizing)
RUN python -m nltk.downloader punkt punkt_tab

# Copy seluruh kode project
COPY . .

# Beri izin eksekusi ke user Hugging Face
RUN chmod -R 777 /app

# Expose port standar HF
EXPOSE 7860

# Jalankan aplikasi (Main Entry Point)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]