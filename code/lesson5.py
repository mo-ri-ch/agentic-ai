import re

# Tools: a pretend shop, and the calculator
def shop(item):
    prices = {"cake for 10 at cake house": "₹1800", "snacks for 10": "₹1500"}
    if "sweet spot" in item.lower():
        return "Error: Sweet Spot is closed today"
    return prices.get(item.lower(), f"Error: no price found for {item}")

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

TOOLS = {"shop": shop, "calculator": calculator}

INSTRUCTIONS = """You are an agent. TOOLS you can use:
shop(item) - the price of an item at a shop. Give it the item and the shop.
calculator(math) - works out math exactly.
First write PLAN: and your steps, one per line, numbered.
Then do one step at a time: ACT: tool(input)
If a step fails, write a new PLAN:.
When you're done, write: ANSWER: your answer"""

# Read the numbered steps out of a plan
def read_plan(reply):
    return re.findall(r"^\d+\. (.+)$", reply, re.MULTILINE)

# A fake LLM with a plan, a failed step and a new plan
fake_replies = [
    "PLAN:\n1. Find a cake for 10 at Sweet Spot\n2. Find snacks for 10\n3. Add up the cost",
    "ACT: shop(cake for 10 at Sweet Spot)",
    "THINK: Step 1 failed. A new plan.\nPLAN:\n1. Find a cake for 10 at Cake House\n2. Find snacks for 10\n3. Add up the cost",
    "ACT: shop(cake for 10 at Cake House)",
    "ACT: shop(snacks for 10)",
    "ACT: calculator(1800 + 1500)",
    "ANSWER: A Cake House cake and snacks: ₹3300 in all, under ₹5000.",
]
def fake_llm(text):
    return fake_replies.pop(0)

# The loop, now keeping track of the plan
def run_agent(question, llm, step_limit=8):
    text = INSTRUCTIONS + "\n\nQuestion: " + question + "\n"
    plan, done = [], 0
    for step in range(step_limit):
        reply = llm(text)
        print(reply)
        text += reply + "\n"
        if "PLAN:" in reply:
            plan, done = read_plan(reply), 0
            print(f"(a plan with {len(plan)} steps)")
        if "ANSWER:" in reply:
            return reply.split("ANSWER:")[1].strip()
        act = re.search(r"ACT: (\w+)\((.*)\)", reply)
        if act is None:
            continue
        elif act.group(1) not in TOOLS:
            look = f"Error: no tool called {act.group(1)}"
        else:
            look = TOOLS[act.group(1)](act.group(2).strip('"'))
        if not look.startswith("Error"):
            done += 1
        print("LOOK:", look, f"(done {done} of {len(plan)})")
        text += "LOOK: " + look + "\n"
    return "Stopped: the step limit was reached."

print(run_agent("Order a cake and snacks for 10 people, under ₹5000.", fake_llm))
