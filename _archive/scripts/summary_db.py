import os
from pathlib import Path

db = Path("data/wikimedia_catania_db")
subdirs = [d for d in db.iterdir() if d.is_dir()]

print("=== RIEPILOGO DATABASE WIKIMEDIA LOCALE COMPLETO ===")
total_files = 0
total_size = 0

for d in sorted(subdirs):
    files = list(d.glob("*.json"))
    size = sum(f.stat().st_size for f in files)
    total_files += len(files)
    total_size += size
    print(f" - {d.name:25}: {len(files):3} file ({size / 1024:.1f} KB)")

root_files = list(db.glob("*.json"))
root_size = sum(f.stat().st_size for f in root_files)
print(f" - {'File Indice e Registry':25}: {len(root_files):3} file ({root_size / 1024:.1f} KB)")

print(f"\nTOTALE: {total_files + len(root_files)} file JSON strutturati nel database!")
print(f"PESO TOTALE WIKITEXT/METADATI: {(total_size + root_size) / (1024*1024):.2f} MB")
