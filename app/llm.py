import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

# --- BAGIAN INI DIUBAH UNTUK CPU DEPLOYMENT ---
print(f"Loading {MODEL_NAME} to CPU (Standard Mode)...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Kita HAPUS config 4-bit (bitsandbytes) karena CPU Hugging Face punya RAM 16GB (Cukup banget!)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="cpu",       # Paksa ke CPU
    torch_dtype=torch.float32, # Pakai float32 biar stabil di CPU
    low_cpu_mem_usage=True,
    trust_remote_code=True
)

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.3,
    top_k=50,
    top_p=0.95,
    repetition_penalty=1.1
)

def generate_answer(question: str, context: str) -> str:
    messages = [
        {"role": "system", "content": (
            "Kamu adalah asisten ahli geologi yang membantu menjawab pertanyaan berdasarkan jurnal ilmiah. "
            "PENTING: Jawablah hanya dalam BAHASA INDONESIA. "
            "Gunakan informasi dari 'Konteks' di bawah ini untuk menjawab. "
            "Jika jawaban tidak ada di konteks, katakan jujur 'Informasi tidak ditemukan di jurnal'."
        )},
        {"role": "user", "content": f"Konteks:\n{context}\n\nPertanyaan: {question}"}
    ]
    
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )

    outputs = llm_pipeline(prompt)
    raw_output = outputs[0]["generated_text"]
    
    if "<|im_start|>assistant" in raw_output:
        return raw_output.split("<|im_start|>assistant")[-1].strip()
    
    return raw_output.replace(prompt, "").strip()