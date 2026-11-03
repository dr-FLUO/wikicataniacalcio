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
    t = t.replace('\"\'', "'")
    t = t.replace('\'\"', "'")
    t = re.sub(r'alt_text:\s*"(.*?)\'', r'alt_text: "\1"', t)
    t = re.sub(r'alt_text:\s*\'(.*?)"', r'alt_text: "\1"', t)
    p.write_text(t, encoding="utf-8")
    print("Fixed:", p.name)
