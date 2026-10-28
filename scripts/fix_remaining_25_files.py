import os
import re
import yaml
from pathlib import Path

CONTENT_DIR = Path("content")
fixed = 0

for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith(".md"):
            p = Path(root) / f
            raw = p.read_text(encoding="utf-8")
            m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
            if not m:
                continue
            fm, body = m.group(1), m.group(2)
            
            try:
                yaml.safe_load(fm)
                continue
            except Exception:
                pass
                
            # Identifica e ripulisci le righe orfane dentro image_credits
            lines = fm.splitlines()
            clean_lines = []
            skip = False
            for line in lines:
                # Se c'è una riga appesa dopo license_type (es. '    Herrera ...' o '    al Barbera')
                if re.match(r"^\s{4,}[a-zA-Z0-9(]", line) and ":" not in line:
                    continue
                # Se c'è un secondo author_or_archive o year consecutivo non preceduto da un nuovo - image_path
                clean_lines.append(line)
                
            new_fm = "\n".join(clean_lines)
            
            # Correggi quote rotte tipo d"autore)'
            new_fm = new_fm.replace('d"autore)\'', "d''autore)'").replace('d"autore)"', 'd\'\'autore)"')
            new_fm = new_fm.replace('d"autore)', "d''autore)")
            
            try:
                yaml.safe_load(new_fm)
                p.write_text(f"---\n{new_fm.strip()}\n---\n{body.lstrip()}", encoding="utf-8")
                fixed += 1
                print(f"Fixed: {p.name}")
                continue
            except Exception as e:
                # Se ancora fallisce, riscrivi programmaticamente image_credits estraendo solo i blocchi validi
                pass

print(f"Totale riparati: {fixed}")
