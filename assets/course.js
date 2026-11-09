// course.js — everything that belongs to this course only.
// The shared look and features come from study-notebook-design (loaded after this file),
// which reads the settings below.

const COURSE_LESSONS = [
  // n: lesson number used for saved progress (never change it) · label: the number students see
  { n: 1, label: "0", step: "basics", title: "What an LLM does", file: "lesson0.html", ready: true, test: 5,
    summary: "A next-word guesser. It reads text and writes text, one word at a time.",
    leaves: "An LLM can only write text. How can writing text make something happen?" },
  { n: 2, label: "1", step: "the loop", title: "From chatbot to agent", file: "lesson1.html", ready: true, test: 7,
    summary: "Put the LLM in a loop: think, act, look at what happened, repeat.",
    leaves: "The agent wants to act. But what can it actually do?" },
  { n: 3, label: "2", step: "tools", title: "Tools", file: "lesson2.html", ready: true, test: 8,
    summary: "Give the agent a calculator, a search and more, and let it choose when to use them.",
    leaves: "You've watched an agent work. Can you build one yourself?" },
  { n: 4, label: "3", step: "build it", title: "Build the loop", file: "lesson3.html", ready: true, test: 9,
    summary: "Write your own agent in about 50 lines of Python. No framework.",
    leaves: "Your agent forgets everything when the task ends. How can it remember?" },
  { n: 5, label: "4", step: "memory", title: "Memory", file: "lesson4.html", ready: false,
    summary: "What the agent keeps in mind during a task, and what it saves for later.",
    leaves: "Big goals need many steps. How does an agent plan them?" },
  { n: 6, label: "5", step: "planning", title: "Planning", file: "lesson5.html", ready: false,
    summary: "Split a big goal into small steps, and fix the plan when a step fails.",
    leaves: "One agent does everything. Could a team do better?" },
  { n: 7, label: "6", step: "teams", title: "Teams of agents", file: "lesson6.html", ready: false,
    summary: "A planner, a worker and a checker, each with one job.",
    leaves: "Agents now act on their own. How do we keep them safe?" },
  { n: 8, label: "7", step: "safety", title: "Keeping agents safe", file: "lesson7.html", ready: false,
    summary: "Limits, mistakes, and asking a human before anything risky.",
    leaves: "You know every piece now. What will your agent do?" },
  { n: 9, label: "8", step: "your agent", title: "Your agent project", file: "lesson8.html", ready: false,
    summary: "Build an agent that does a real job, from start to finish.",
    leaves: null },
];

// ---------- Your agent: a sticky note with a little wrench, who learns to act ----------
// <p class="agent-say">Hello!</p>  becomes your agent, with a speech bubble.
const AGENT_SVG = `
<svg class="neo-face agent-face" viewBox="0 0 64 64" aria-hidden="true">
  <path d="M10 12 H48 L54 18 V56 H10 Z" class="neo-note" />
  <path d="M48 12 V18 H54" class="neo-fold" />
  <path d="M30 12 V5" /><circle cx="30" cy="4" r="2.4" class="agent-bulb" />
  <circle cx="23" cy="31" r="2.6" class="neo-eye" />
  <circle cx="39" cy="31" r="2.6" class="neo-eye" />
  <path d="M23 40 Q31 46 39 40" />
  <path d="M54 40 L61 33" class="agent-tool" /><path d="M58.5 30.5 A3.6 3.6 0 1 0 63.5 35.5" class="agent-tool" />
</svg>`;

function setupAgent() {
  document.querySelectorAll("p.agent-say").forEach(p => {
    const box = document.createElement("div");
    box.className = "neo";
    box.innerHTML = AGENT_SVG;
    const bubble = document.createElement("div");
    bubble.className = "neo-bubble";
    bubble.innerHTML = `<span class="neo-name">${p.dataset.name || "Your agent"}</span>${p.innerHTML}`;
    box.appendChild(bubble);
    if (p.id) box.id = p.id;
    p.replaceWith(box);
  });
}

// ---------- Chance bars: <div class="bars"></div> filled by drawBars(el, [[word, pct], …], pickedWord) ----------
function drawBars(el, rows, picked) {
  el.innerHTML = rows.map(([w, p]) => `
    <div class="bar${w === picked ? " picked" : ""}">
      <span>${w}</span><span class="track"><span class="fill" style="width:${p}%"></span></span><span class="pct">${p}%</span>
    </div>`).join("");
}

window.COURSE = {
  id: "agentic-ai",                // prefix for everything saved in this browser (progress, notes). Never change it.
  pathLabel: "Building the agent",
  lessons: COURSE_LESSONS,
  setup: [setupAgent],
};
