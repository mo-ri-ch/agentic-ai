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

# Now you're the person: type y or n when the agent wants to send an email
def ask_person(name, details):
    answer = input(f"Allow {name}({details})? y or n: ")
    return answer == "y"

print(run_agent("Find a cheap flight to Goa.", real_llm, allowed={"search", "send_email"}))
print(log)
