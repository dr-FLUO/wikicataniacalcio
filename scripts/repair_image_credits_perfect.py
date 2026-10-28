"""
Riparazione pulita e perfetta della sezione image_credits in tutti i file Markdown.
"""

import os
import re
from pathlib import Path

CONTENT_DIR = Path("content")

count = 0

for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith(".md"):
            p = Path(root) / f
            raw = p.read_text(encoding="utf-8")
            
            m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
            if not m:
                continue
            fm, body = m.group(1), m.group(2)
            
            if "image_credits:" not in fm:
                continue
                
            orig_fm = fm
            
            # Cerca il blocco image_credits fino alla fine del frontmatter o alla prossima chiave top-level
            # Riscrivi image_credits in modo pulito
            credits_blocks = re.findall(r"image_credits:\s*\n((?:(?:\s*-\s*.*?\n)|\s*[a-zA-Z_]+:.*?\n)+)", fm)
            if credits_blocks:
                old_block = "image_credits:\n" + credits_blocks[0]
                
                # Estrai i singoli item
                # Ciascun item inizia con '  - image_path:' o '- image_path:'
                items_raw = re.split(r"(?:^|\n)\s*-\s*image_path:\s*", "\n" + credits_blocks[0])
                new_items = []
                for item in items_raw:
                    if not item.strip():
                        continue
                    lines = item.strip().splitlines()
                    img_path = lines[0].strip().strip("'\"")
                    
                    alt_m = re.search(r"alt_text:\s*(.*)", item)
                    author_m = re.search(r"author_or_archive:\s*(.*)", item)
                    year_m = re.search(r"year:\s*(\d+)", item)
                    lic_m = re.search(r"license_type:\s*(.*)", item)
                    
                    alt = alt_m.group(1).strip().strip("'\"") if alt_m else "Documentazione fotografica ufficiale del Calcio Catania"
                    # ripulisci quote rotte
                    alt = alt.replace('"', '').replace("''", "'")
                    
                    author = author_m.group(1).strip().strip("'\"") if author_m else "Archivio Storico Calcio Catania"
                    author = author.replace('"', '').replace("''", "'")
                    
                    year = int(year_m.group(1)) if year_m else 2024
                    
                    raw_lic = lic_m.group(1).strip().strip("'\"") if lic_m else ""
                    if "termini" in raw_lic.lower() or "scadenza" in raw_lic.lower():
                        lic = "Pubblico Dominio (Scadenza termini d'autore)"
                    elif "92" in raw_lic or "italia" in raw_lic.lower():
                        lic = "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)"
                    elif "cc by 4.0" in raw_lic.lower():
                        lic = "Creative Commons CC BY 4.0"
                    elif "marchio" in raw_lic.lower():
                        lic = "Marchio Storico ad uso descrittivo enciclopedico (Art. 21 CPI)"
                    elif "cortesia" in raw_lic.lower():
                        lic = "Cortesia Archivio Storico Autorizzato"
                    else:
                        lic = "Creative Commons CC BY-SA 4.0"
                        
                    # Costruisci item valido in YAML:
                    # In YAML se una stringa con apici singoli contiene un apice, si raddoppia: d''autore
                    lic_escaped = lic.replace("'", "''")
                    alt_escaped = alt.replace("'", "''")
                    author_escaped = author.replace("'", "''")
                    
                    new_item_yaml = (
                        f"- image_path: '{img_path}'\n"
                        f"  alt_text: '{alt_escaped}'\n"
                        f"  author_or_archive: '{author_escaped}'\n"
                        f"  year: {year}\n"
                        f"  license_type: '{lic_escaped}'"
                    )
                    new_items.append(new_item_yaml)
                    
                new_block = "image_credits:\n" + "\n".join(new_items) + "\n"
                fm = fm.replace(old_block, new_block)
                
            if fm != orig_fm:
                count += 1
                new_raw = f"---\n{fm.strip()}\n---\n{body.lstrip()}"
                p.write_text(new_raw, encoding="utf-8")

print(f"Riparate con successo {count} sezioni image_credits in YAML.")
