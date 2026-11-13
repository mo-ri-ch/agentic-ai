import re

# Long-term memory: notes kept outside the text, in a list
notes = []

def save_note(note):
    notes.append(note)
    return "Saved."

TOOLS = {"save_note": save_note}

# The instructions now end with every note saved so far
def instructions():
    rules = """You are an agent. TOOLS you can use:
save_note(note) - remember something for next time. Give it the note.
To use a tool, write one line: ACT: tool(input)
When you know the answer, write: ANSWER: your answer
NOTES from earlier tasks:"""
    for note in notes:
        rules += "\n- " + note
    return rules

# A fake LLM that reads the text, so you can see the notes matter
def fake_llm(text):
    if "Question: I'm vegetarian" in text:
        if "LOOK:" not in text:
            return "THINK: That's worth remembering.\nACT: save_note(The person is vegetarian.)"
        return "ANSWER: Got it. I'll remember that."
    if "- The person is vegetarian." in text:
        return "ANSWER: How about paneer tikka? It's vegetarian, like you."
    return "ANSWER: How about butter chicken?"

# The same loop as Lesson 3. It also shows how long the text has grown.
def run_agent(question, llm, step_limit=5):
    text = instructions() + "\n\nQuestion: " + question + "\n"
    for step in range(step_limit):
        reply = llm(text)
        print(reply)
        text += reply + "\n"
        print("(the text is now", len(text.split()), "words)")
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

# Task 1, before any notes
print(run_agent("Suggest a dinner for me.", fake_llm))
# Task 2: tell it something worth remembering
print(run_agent("I'm vegetarian. Please remember that.", fake_llm))
print(notes)
# Task 3: a brand new text, but the note is at the top
print(run_agent("Suggest a dinner for me.", fake_llm))
