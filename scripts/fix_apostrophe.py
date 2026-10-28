import re
from pathlib import Path

files = [
    Path("content/01-societa/presidenti/santi-maimone.md"),
    Path("content/02-cronistoria/partite-storiche/1960-1961/catania-inter-2-0.md"),
    Path("content/03-tesserati/calciatori/rosa-attuale/emmanuele-pio-cicerelli.md"),
    Path("content/03-tesserati/calciatori/storici/mario-miltone.md"),
    Path("content/06-tifoseria-e-cultura/curve/curva-sud/falange-d-assalto.md")
]

for p in files:
    t = p.read_text(encoding="utf-8")
    t = t.replace('d"epoca', "d'epoca")
    t = t.replace('l"Inter', "l'Inter")
    t = t.replace('dell"attaccante', "dell'attaccante")
    t = t.replace('dell"Associazione', "dell'Associazione")
    t = t.replace('d"Assalto', "d'Assalto")
    # Make sure alt_text starts and ends with double quotes properly
    lines = t.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("alt_text:"):
            val = line.split("alt_text:", 1)[1].strip().strip("'\"")
            val = val.replace('"', '\\"')
            lines[i] = f'  alt_text: "{val}"'
    p.write_text("\n".join(lines), encoding="utf-8")
    print("Fixed:", p.name)
