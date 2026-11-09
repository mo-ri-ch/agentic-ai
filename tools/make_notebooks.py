"""Build the Google Colab notebook for each lesson with code, from code/lessonN.py
(the same code as the lesson's "The code" page), plus code/lessonN_real.py if it exists
(the part that needs a real LLM, which only runs in Colab).

Run from the repo root:  python3 tools/make_notebooks.py
Writes notebooks/lessonN.ipynb, one cell per commented block.
"""
import glob
import json
import os
import re

TITLES = {3: "Build the loop"}


def cells_from(code):
    cells = []
    for part in re.split(r"\n\n(?=#)", code.strip("\n")):
        lines = part.strip("\n").split("\n")
        if any("print(" in l for l in lines):
            cells.append({"cell_type": "markdown", "metadata": {}, "source": ["🤔 *Guess what this prints, then press ▶.*"]})
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                      "source": [l + "\n" for l in lines[:-1]] + [lines[-1]]})
    return cells


for path in sorted(glob.glob("code/lesson[0-9].py")):
    n = int(re.search(r"lesson(\d+)", path).group(1))
    title = TITLES.get(n, f"Lesson {n}")
    cells = [{"cell_type": "markdown", "metadata": {}, "source": [
        f"# Lesson {n}: {title}\n", "\n",
        "For each cell: **guess what it will print first**, then press ▶ and check.\n", "\n",
        f"From [Build an AI Agent](https://gradlabs.in/learn/agents/lessons/lesson{n}.html).",
    ]}]
    cells += cells_from(open(path, encoding="utf-8").read())
    real = f"code/lesson{n}_real.py"
    if os.path.exists(real):
        cells.append({"cell_type": "markdown", "metadata": {}, "source": [
            "## Now a real LLM\n", "\n",
            "The same loop, with a small free model (Qwen2.5 1.5B) instead of the fake LLM.\n",
            "The first run downloads it (about 3 GB), so give it a few minutes.\n", "\n",
            "Small models make mistakes. Watch the `LOOK:` lines: errors go back to the LLM, so it can often fix them.",
        ]})
        cells += cells_from(open(real, encoding="utf-8").read())
    notebook = {"cells": cells,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                             "language_info": {"name": "python"}},
                "nbformat": 4, "nbformat_minor": 5}
    with open(f"notebooks/lesson{n}.ipynb", "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    print(f"notebooks/lesson{n}.ipynb: {sum(c['cell_type'] == 'code' for c in cells)} code cells")
