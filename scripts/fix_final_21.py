import os
import re
import yaml
from pathlib import Path

content = Path("content")
invalid = []

for p in content.rglob("*.md"):
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
    if not m:
        continue
    fm, body = m.group(1), m.group(2)
    try:
        yaml.safe_load(fm)
    except Exception:
        invalid.append((p, fm, body))

print(f"Files to fix: {len(invalid)}")

for p, fm, body in invalid:
    lines = fm.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Se è una riga orfana tipo '    2011' o '    al Barbera'
        if re.match(r"^\s{2,}\S+", line) and not re.match(r"^\s*-\s*[a-zA-Z_]+:", line) and not re.match(r"^\s*[a-zA-Z_]+:", line):
            # unisci alla riga precedente
            if new_lines:
                orphan = line.strip()
                prev = new_lines[-1]
                if prev.endswith("'"):
                    new_lines[-1] = prev[:-1] + " " + orphan + "'"
                elif prev.endswith('"'):
                    new_lines[-1] = prev[:-1] + " " + orphan + '"'
                else:
                    new_lines[-1] = prev + " " + orphan
            i += 1
            continue
        new_lines.append(line)
        i += 1
        
    cleaned_fm = "\n".join(new_lines)
    
    # Rimuovi eventuali righe duplicate consecutive di author_or_archive o license_type
    # Verifica validità
    try:
        yaml.safe_load(cleaned_fm)
        p.write_text(f"---\n{cleaned_fm.strip()}\n---\n{body.lstrip()}", encoding="utf-8")
        print(f"Successfully fixed: {p.name}")
    except Exception as e:
        print(f"Still invalid {p.name}: {e}")
