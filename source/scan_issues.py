import os, re

docs_dir = "docs"
md_files = [os.path.join(docs_dir, f) for f in os.listdir(docs_dir) if f.endswith(".md")] + ["README.md"]

html_tag_pattern = re.compile(r'<[a-zA-Z0-9_\-\s%]+>')
math_pattern = re.compile(r'\$\$|\$')

for fpath in sorted(md_files):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    in_code_block = False
    issues = []

    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
        elif not in_code_block:
            # Check for unescaped < tag that isn't standard markdown or quote
            tags = html_tag_pattern.findall(line)
            if tags:
                issues.append((i+1, f"HTML-like tag: {tags}"))
            if "$$" in line or "$" in line:
                issues.append((i+1, f"Math syntax: {line.strip()[:60]}"))

    print(f"File: {os.path.basename(fpath):25s} | Potential Renderer Issues: {len(issues)}")
    for line_no, desc in issues:
        print(f"   Line {line_no:3d}: {desc}")
