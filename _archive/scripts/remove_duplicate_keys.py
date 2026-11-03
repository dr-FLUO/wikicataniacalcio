import os
import re
from pathlib import Path

content = Path("content")
count = 0

for p in content.rglob("*.md"):
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
    if not m:
        continue
    fm, body = m.group(1), m.group(2)
    orig_fm = fm
    
    lines = fm.splitlines()
    new_lines = []
    in_credits = False
    current_keys = set()
    
    for line in lines:
        sline = line.strip()
        if sline == "image_credits:":
            in_credits = True
            current_keys = set()
            new_lines.append(line)
            continue
            
        # Esci da image_credits solo se la riga NON è indentata e non inizia con trattino
        if in_credits and line and not line.startswith(" ") and not line.startswith("-"):
            in_credits = False
            new_lines.append(line)
            continue
            
        if in_credits:
            if sline.startswith("- image_path:") or sline.startswith("- image_path :"):
                current_keys = set(["image_path"])
                new_lines.append(line)
                continue
            key_m = re.match(r"^([a-zA-Z_]+)\s*:", sline)
            if key_m:
                k = key_m.group(1)
                if k in current_keys:
                    # Rimuovi chiave duplicata
                    continue
                current_keys.add(k)
                new_lines.append(line)
                continue
                
        new_lines.append(line)
        
    new_fm = "\n".join(new_lines)
    if new_fm != orig_fm:
        count += 1
        p.write_text(f"---\n{new_fm.strip()}\n---\n{body.lstrip()}", encoding="utf-8")

print(f"Rimosse chiavi duplicate in {count} file.")
