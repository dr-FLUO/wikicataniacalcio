from pathlib import Path

files = list(Path("content/03-tesserati/calciatori/archivio").glob("**/*.md"))
fixed = 0

for f in files:
    raw = f.read_text(encoding="utf-8")
    if "[[societa/matricola-11700|Calcio Catania]]" in raw:
        raw = raw.replace("[[societa/matricola-11700|Calcio Catania]]", r"[[societa/matricola-11700\|Calcio Catania]]")
        f.write_text(raw, encoding="utf-8")
        fixed += 1

print(f"[OK] Fixed table pipe escape in {fixed} player files.")
