import re

# The loop from Lesson 3, but each agent brings its own instructions and tools
def run_agent(instructions, question, tools, llm, step_limit=6):
    text = instructions + "\n\nQuestion: " + question + "\n"
    for step in range(step_limit):
        reply = llm(text)
        text += reply + "\n"
        if "ANSWER:" in reply:
            return reply.split("ANSWER:")[1].strip()
        act = re.search(r"ACT: (\w+)\((.*)\)", reply)
        if act is None or act.group(1) not in tools:
            look = "Error: write ACT: tool(input) with a tool you have"
        else:
            look = tools[act.group(1)](act.group(2))
        text += "LOOK: " + look + "\n"
    return "Stopped: the step limit was reached."

# Make an agent: a name, its instructions, its tools, and its (fake) LLM's replies
def make_agent(name, instructions, tools, replies):
    def agent(task):
        print(f"  {name} gets: {task}")
        answer = run_agent(instructions, task, tools, lambda text: replies.pop(0))
        print(f"  {name} answers: {answer}")
        return answer
    return agent

def search(words):
    return "Cherai Beach: calm water, 25 km from Kochi. Fort Kochi Beach: rocky."

researcher = make_agent("researcher", "You find facts. Tool: search(words).", {"search": search}, [
    "ACT: search(beaches near Kochi)",
    "ANSWER: Cherai Beach is best: calm water, 25 km from Kochi.",
])
writer = make_agent("writer", "You write short, friendly text. No tools.", {}, [
    "ANSWER: Cherai Beach is the best beach near Kochi: calm, and only 40 km away.",
    "ANSWER: Cherai Beach is the best beach near Kochi: calm, and only 25 km away.",
])
checker = make_agent("checker", "You check a draft against the facts. Answer OK, or FIX: and what's wrong.", {}, [
    "ANSWER: FIX: the facts say 25 km, not 40 km.",
    "ANSWER: OK",
])

# The manager: its tools are the other agents
manager_replies = [
    "ACT: ask_researcher(Find the best beach near Kochi)",
    "ACT: ask_writer(Write one sentence: Cherai Beach, calm water, 25 km from Kochi)",
    "ACT: ask_checker(Facts: 25 km from Kochi. Draft: calm, and only 40 km away.)",
    "ACT: ask_writer(Fix it: the beach is 25 km away, not 40 km)",
    "ACT: ask_checker(Facts: 25 km from Kochi. Draft: calm, and only 25 km away.)",
    "ANSWER: Cherai Beach is the best beach near Kochi: calm, and only 25 km away.",
]
manager = make_agent("manager", "You lead a team. Tools: ask_researcher, ask_writer, ask_checker.",
                     {"ask_researcher": researcher, "ask_writer": writer, "ask_checker": checker},
                     manager_replies)

print(manager("Write one sentence about the best beach near Kochi."))
