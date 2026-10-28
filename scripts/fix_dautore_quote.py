from pathlib import Path

content = Path("content")
for p in content.rglob("*.md"):
    t = p.read_text(encoding="utf-8")
    if 'd"autore)' in t:
        t = t.replace('license_type: \'Pubblico Dominio (Scadenza termini d"autore)\'', 'license_type: "Pubblico Dominio (Scadenza termini d\'autore)"')
        t = t.replace('license_type: "Pubblico Dominio (Scadenza termini d"autore)"', 'license_type: "Pubblico Dominio (Scadenza termini d\'autore)"')
        t = t.replace('d"autore)', "d'autore)")
        p.write_text(t, encoding="utf-8")
        print(f"Fixed quote in {p.name}")
