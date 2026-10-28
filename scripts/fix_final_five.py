import re
from pathlib import Path

content = Path("content")

targets = [
    "01-societa/presidenti/santi-maimone.md",
    "02-cronistoria/partite-storiche/1960-1961/catania-inter-2-0.md",
    "03-tesserati/calciatori/rosa-attuale/emmanuele-pio-cicerelli.md",
    "03-tesserati/calciatori/storici/mario-miltone.md",
    "06-tifoseria-e-cultura/curve/curva-sud/falange-d-assalto.md",
]

for rel in targets:
    p = content / rel
    lines = p.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        if 'alt_text: "' in line and line.count('"') > 2:
            # Fix broken inner quotes
            parts = line.split('alt_text: "', 1)
            clean = parts[1].rstrip('"\'').replace('"', "'")
            new_lines.append(f'{parts[0]}alt_text: "{clean}"')
        elif "alt_text: '" in line and line.count("'") > 2:
            parts = line.split("alt_text: '", 1)
            clean = parts[1].rstrip('"\'').replace('"', "'")
            new_lines.append(f'{parts[0]}alt_text: "{clean}"')
        else:
            new_lines.append(line)
            
    p.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"Fixed quotes in {rel}")

# Now fix duplicate keys in santi-maimone, catania-inter, mario-miltone, falange
from scripts.sanitize_image_credits import *
