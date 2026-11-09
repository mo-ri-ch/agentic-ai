# Build an AI Agent — notes for Claude

- Read the design guidelines first: https://github.com/mo-ri-ch/study-notebook-design/blob/main/GUIDELINES.md
  (also at ../study-notebook-design/GUIDELINES.md when that repo is checked out next to this one).
- The shared look comes from study-notebook-design/v1; this repo has the lessons, assets/course.js
  (lesson list, "Your agent" sticky note, chance bars), assets/course.css and assets/practice.js.
- **Standalone course.** Every topic is taught here, from scratch. Never require Build a Tiny LLM or
  Transformers & LLMs; links to them are optional "want to go deeper?" extras only.
- Lessons are numbered 0–8 for readers (`label`), but saved progress uses `n` (1–9). Never change `n`
  or the id "agentic-ai", or students lose their notes.
- Lessons 0–2: browser activities only. Code (Colab) starts in Lesson 3 ("Build the loop").
- Activities that show an agent before Lesson 3 are illustrations; say so where it matters.
- Check pages with `python3 ../build-an-llm-from-scratch/tools/check_pages.py` (run from this repo) before pushing.
