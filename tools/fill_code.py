"""Put code/lessonN.py and its real output into lessons/lessonN.html ("The code" page).

Run from the repo root:  python3 tools/fill_code.py 4
It replaces the first <pre><code>…</code></pre> after data-title="The code", and the
terminal output after "$ python lessonN.py", so the page always matches the file.
"""
import html, re, subprocess, sys

n = sys.argv[1]
code = open(f"code/lesson{n}.py", encoding="utf-8").read().rstrip("\n")
out = subprocess.run([sys.executable, "-I", f"code/lesson{n}.py"], capture_output=True, text=True, check=True).stdout.rstrip("\n")
fmt = lambda l: f'<span class="c">{html.escape(l, quote=False)}</span>' if l.strip().startswith("#") else html.escape(l, quote=False)
block = "<pre><code>" + "\n".join(fmt(l) for l in code.split("\n")) + "</code></pre>"
p = f"lessons/lesson{n}.html"
s = open(p, encoding="utf-8").read()
start = s.index('data-title="The code"')
if "<!--CODE-->" in s:
    s = s.replace("<!--CODE-->", block, 1)
else:
    i = s.index("<pre><code>", start); j = s.index("</code></pre>", i) + len("</code></pre>")
    s = s[:i] + block + s[j:]
prompt = f'<span class="prompt">$ python lesson{n}.py</span>\n'
i = s.index(prompt) + len(prompt); j = s.index("</pre>", i)
s = s[:i] + html.escape(out, quote=False) + s[j:]
open(p, "w", encoding="utf-8").write(s)
print(f"{p}: code ({len(code.splitlines())} lines) and output ({len(out.splitlines())} lines) filled in")
