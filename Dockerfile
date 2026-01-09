# Gunakan Python 3.10 slim (versi ringan)
FROM python:3.10-slim

# Set folder kerja
WORKDIR /app

# Copy requirements dan install
# Pastikan requirements.txt sudah bersih (hanya fastapi, uvicorn, google-generativeai, python-dotenv)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode project ke dalam image
COPY . .

# Beri izin eksekusi ke user Hugging Face (untuk menghindari permission error)
RUN chmod -R 777 /app

# Expose port standar HF
EXPOSE 7860

# Jalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]