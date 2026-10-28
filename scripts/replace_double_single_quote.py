from pathlib import Path

content = Path("content")
count = 0
for p in content.rglob("*.md"):
    t = p.read_text(encoding="utf-8")
    if "d''autore" in t:
        t = t.replace("d''autore", "d'autore")
        p.write_text(t, encoding="utf-8")
        count += 1
print(f"Replaced in {count} files.")
