import os, re

files = [os.path.join("docs", f) for f in os.listdir("docs") if f.endswith(".md")] + ["README.md"]

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix math delimiters that break GitHub React viewer
    content = content.replace("$$\\text{SHORTEST ROUTE} \\neq \\text{SAFEST ROUTE}$$", "**SHORTEST ROUTE ≠ SAFEST ROUTE**")
    content = content.replace("$K$-shortest", "K-shortest")
    content = content.replace("slope $> 5\\%$", "slope > 5%")
    content = content.replace("Contrast ratio $> 7:1$", "Contrast ratio > 7:1")
    content = content.replace("$", "") # Remove orphan dollars
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("All markdown files sanitized for GitHub Web React renderer!")
