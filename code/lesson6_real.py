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

# The same team, now with a real LLM for every agent
RULES = "\nTo use a tool, write one line: ACT: tool(input)\nWhen you're done, write: ANSWER: your answer"

def make_real_agent(name, instructions, tools):
    def agent(task):
        print(f"  {name} gets: {task}")
        answer = run_agent(instructions + RULES, task, tools, real_llm)
        print(f"  {name} answers: {answer}")
        return answer
    return agent

researcher = make_real_agent("researcher", "You find facts. Tool: search(words).", {"search": search})
writer = make_real_agent("writer", "You write short, friendly text. No tools.", {})
checker = make_real_agent("checker", "You check a draft against the facts. Answer OK, or FIX: and what's wrong.", {})
manager = make_real_agent("manager", "You lead a team. Tools: ask_researcher(task), ask_writer(task), ask_checker(task).",
                          {"ask_researcher": researcher, "ask_writer": writer, "ask_checker": checker})
print(manager("Write one sentence about the best beach near Kochi."))
