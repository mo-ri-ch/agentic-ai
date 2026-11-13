import re

# Tools: plain Python functions. Text in, text out.
def calculator(math):
    for ch in math:
        if ch not in "0123456789+-*/(). ":
            return "Error: the calculator only takes numbers and + - * / ( )"
    if "**" in math:   # ** is power: 9 ** 999999 would never finish
        return "Error: the calculator only takes numbers and + - * / ( )"
    try:
        return str(eval(math))
    except Exception:
        return "Error: that math doesn't work out"

def weather(city):
    today = {"kochi": "29°C, sunny", "delhi": "18°C, foggy", "pune": "24°C, light rain"}
    return today.get(city.lower(), f"Error: no city called {city}")

TOOLS = {"calculator": calculator, "weather": weather}
print(TOOLS["weather"]("Kochi"))

# The tool list, at the top of the text, every time
# (""" … """ is a string over several lines)
INSTRUCTIONS = """You are an agent. TOOLS you can use:
calculator(math) - works out math exactly. Give it the math, like 12 * 7.
weather(city) - the weather right now in a city. Give it the city name.
To use a tool, write one line: ACT: tool(input)
Then stop. The result will come back on a LOOK: line.
When you know the answer, write: ANSWER: your answer"""

# A fake LLM: it just hands back the next reply from a list
fake_replies = [
    "THINK: Exact math. I'll use the calculator.\nACT: calculator(4817 * 263)",
    "ANSWER: 4,817 × 263 = 1,266,871.",
]
def fake_llm(text):
    return fake_replies.pop(0)

# The loop: think, act, look, until ANSWER: or the step limit
def run_agent(question, llm, step_limit=5):
    text = INSTRUCTIONS + "\n\nQuestion: " + question + "\n"
    for step in range(step_limit):
        reply = llm(text)
        print(reply)
        text += reply + "\n"
        if "ANSWER:" in reply:
            return reply.split("ANSWER:")[1].strip()
        act = re.search(r"ACT: (\w+)\((.*)\)", reply)
        if act is None:
            look = "Error: write ACT: tool(input) or ANSWER: your answer"
        elif act.group(1) not in TOOLS:
            look = f"Error: no tool called {act.group(1)}"
        else:
            look = TOOLS[act.group(1)](act.group(2).strip('"'))
        print("LOOK:", look)
        text += "LOOK: " + look + "\n"
    return "Stopped: the step limit was reached."

print(run_agent("What is 4,817 × 263?", fake_llm))
