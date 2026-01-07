from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="cpu"
)

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    temperature=0.2,
)

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
Kamu adalah chatbot geologi khusus patahan sesar.
Jawablah HANYA berdasarkan konteks berikut.
Jika jawabannya tidak ada, katakan "Saya tidak tahu".

Konteks:
{context}

Pertanyaan:
{question}

Jawaban:
"""
    output = llm_pipeline(prompt)[0]["generated_text"]
    return output.split("Jawaban:")[-1].strip()
