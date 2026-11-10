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
- Code lessons: code/lessonN.py is the source for the "The code" page, its terminal output, the Step through
  trace and the Colab notebook. After changing it: `python3 tools/fill_code.py N` (puts the code and its real output into the page), then
  `python3 tools/make_traces.py code/lessonN.py` and `python3 tools/make_notebooks.py`.
  code/lessonN_real.py (real LLM) only goes into the notebook. Line explanations live in tools/explanations.py.
- The real-model parts (code/lessonN_real.py, Qwen2.5 1.5B in Colab) have not been run by Claude: check them in Colab after changes.
- Lessons 4–8 use the shared helpers in assets/course.js (AG.line, AG.stepper, AG.modes, AG.chips).
