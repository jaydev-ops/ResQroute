import os

docs_dir = "docs"
md_files = [f for f in os.listdir(docs_dir) if f.endswith(".md")] + ["README.md"]

for fname in sorted(md_files):
    fpath = os.path.join(docs_dir, fname) if fname in os.listdir(docs_dir) else fname
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    unfenced_boxes = []
    unfenced_html = []
    in_code_block = False
    for i, l in enumerate(lines):
        if l.strip().startswith("```"):
            in_code_block = not in_code_block
        elif not in_code_block:
            if "+---" in l or "+===" in l:
                unfenced_boxes.append((i+1, l))

    print(f"File: {fname:25s} | Lines: {len(lines):4d} | Unfenced ASCII boxes: {len(unfenced_boxes)}")
    if unfenced_boxes:
        for line_no, line in unfenced_boxes:
            print(f"   Line {line_no}: {line[:70]}")
