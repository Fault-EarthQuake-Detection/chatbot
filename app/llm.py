import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print(f"Loading {MODEL_NAME} to GPU (4-bit mode)...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Konfigurasi Kompresi 4-bit (Hemat VRAM banget!)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# Load Model dengan Config di atas
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config, # <--- Masukkan config 4-bit
    device_map="auto",              # Biarkan library atur posisi GPU otomatis
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