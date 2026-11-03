"""
Correzione della sintassi YAML nelle sezioni image_credits e sources di tutti i file in content/
"""

import os
import re
from pathlib import Path

CONTENT_DIR = Path("content")

count_fixed = 0

for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith(".md"):
            p = Path(root) / f
            raw = p.read_text(encoding="utf-8")
            
            # Match frontmatter
            m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
            if not m:
                continue
                
            fm, body = m.group(1), m.group(2)
            orig_fm = fm
            
            # 1. Correggi image_credits malformati
            # Cerca alt_text o license_type con apici singoli che contengono d'autore
            fm = re.sub(r"alt_text:\s*'(.*?)'", lambda mo: 'alt_text: "' + mo.group(1).replace('"', '\\"') + '"', fm)
            fm = re.sub(r"license_type:\s*'(.*?)'", lambda mo: 'license_type: "' + mo.group(1).replace('"', '\\"') + '"', fm)
            fm = re.sub(r"author_or_archive:\s*'(.*?)'", lambda mo: 'author_or_archive: "' + mo.group(1).replace('"', '\\"') + '"', fm)
            
            # Rimuovi eventuali righe duplicate di license_type
            fm = re.sub(r'(license_type:\s*"[^"]+"\r?\n)\s*license_type:\s*"[^"]+"', r'\1', fm)
            
            # 2. Correggi indentazione sources
            # Se ci sono righe con '    - author:' dopo un '- author:' senza indentazione, unifica
            lines = fm.splitlines()
            fixed_lines = []
            in_sources = False
            for line in lines:
                if line.strip() == "sources:":
                    in_sources = True
                    fixed_lines.append(line)
                    continue
                if in_sources and re.match(r"^[a-zA-Z_]+:", line):
                    in_sources = False
                if in_sources:
                    if line.strip().startswith("- author:"):
                        fixed_lines.append("- author:" + line.split("- author:", 1)[1])
                        continue
                    elif re.match(r"^\s+([a-zA-Z_]+:)", line):
                        # standardizza indentazione a 2 spazi
                        k_v = line.strip()
                        fixed_lines.append(f"  {k_v}")
                        continue
                fixed_lines.append(line)
                
            fm = "\n".join(fixed_lines)
            
            if fm != orig_fm:
                count_fixed += 1
                new_raw = f"---\n{fm.strip()}\n---\n{body.lstrip()}"
                p.write_text(new_raw, encoding="utf-8")

print(f"Corrette {count_fixed} pagine con problemi di sintassi YAML nei crediti o nelle fonti.")
