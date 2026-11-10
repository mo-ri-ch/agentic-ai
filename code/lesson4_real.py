# A real LLM: a small, free model that runs inside Colab
# (faster with a GPU: Runtime → Change runtime type → T4 GPU)
import torch
from transformers import pipeline
chat = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct",
                device=0 if torch.cuda.is_available() else -1)

def real_llm(text):
    out = chat([{"role": "user", "content": text}], max_new_tokens=120, do_sample=False)
    reply = out[0]["generated_text"][-1]["content"]
    kept = []
    for line in reply.split("\n"):
        kept.append(line)
        if line.startswith("ACT:") or line.startswith("ANSWER:"):
            break   # cut here: the program writes the LOOK: line, not the LLM
    return "\n".join(kept)

# The same memory, now with a real LLM
print(run_agent("My favourite colour is green. Please remember that.", real_llm))
print(notes)
print(run_agent("What's my favourite colour?", real_llm))
