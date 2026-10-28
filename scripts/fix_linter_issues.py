import os
import re
import yaml

# Standard bibliographic sources compliant with EU copyright guardrail
STD_SOURCES = [
    {
        "title": "Tutto il Catania minuto per minuto",
        "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
        "publisher": "GEO Edizioni, Empoli",
        "year": 2010,
        "reference": "Registro generale calciatori, cronache e tabellini ufficiali"
    },
    {
        "title": "Almanacco Illustrato del Calcio",
        "author": "Panini",
        "publisher": "Panini Edizioni, Modena",
        "year": 2024,
        "reference": "Archivio federale e storico campionati italiani"
    },
    {
        "title": "Archivio Storico Calcio Catania",
        "author": "Redazione Storica CalcioCatania.com",
        "publisher": "calciocatania.com",
        "year": 2024,
        "url": "https://www.calciocatania.com/",
        "reference": "Documentazione anagrafica e statistiche certificate"
    }
]

STD_FONTI_MD = """

## Fonti e Bibliografia
* Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino, *Tutto il Catania minuto per minuto*, GEO Edizioni, Empoli, 2010.
* *Almanacco Illustrato del Calcio*, Panini Edizioni, Modena.
* [CalcioCatania.com](https://www.calciocatania.com/) — Archivio storico e statistiche ufficiali.
"""

files_needing_sources = [
    "content/partite/2007-2008/catania-roma-1-1.md",
    "content/partite/2026-2027/potenza-catania-2-1.md",
    "content/societa/matricola-11700.md",
    "content/societa/presidenti/michele-finocchiaro.md",
    "content/societa/presidenti/santi-maimone.md",
    "content/tesserati/calciatori/amedeo-biavati.md",
    "content/tesserati/calciatori/loris-boni.md",
    "content/tesserati/calciatori/mario-miltone.md",
]

for p in files_needing_sources:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            fm["sources"] = STD_SOURCES
            body = parts[2]
            if "## Fonti e Bibliografia" not in body:
                body = body.rstrip() + STD_FONTI_MD
            new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False)
            new_text = f"---\n{new_fm}---\n{body}"
            with open(p, "w", encoding="utf-8") as f:
                f.write(new_text)
            print(f"Added sources and bibliography to: {p}")

files_needing_yaml_fix = [
    "content/partite/1960-1961/catania-inter-2-0.md",
    "content/stagioni/1982-1983.md",
    "content/tesserati/calciatori/giorgio-mastropasqua.md",
    "content/tesserati/calciatori/giuseppe-vavassori.md",
    "content/tesserati/calciatori/guido-biondi.md",
    "content/tesserati/calciatori/horst-szymaniak.md",
    "content/tesserati/calciatori/nicola-fusaro.md",
    "content/tesserati/calciatori/roberto-sorrentino.md",
    "content/tesserati/calciatori/sidney-cunha-cinesinho.md",
]

for p in files_needing_yaml_fix:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1]
            body = parts[2]
            # Replace unindented "- image_path" or "- source_url" under image_credits
            lines = raw_fm.splitlines()
            fixed_lines = []
            under_credits = False
            for line in lines:
                if line.startswith("image_credits:"):
                    under_credits = True
                    fixed_lines.append(line)
                elif under_credits:
                    if line.startswith("- "):
                        fixed_lines.append("  " + line)
                    elif line.startswith("  ") and not line.startswith("    ") and not line.strip().startswith("-"):
                        fixed_lines.append("  " + line)
                    elif re.match(r"^[a-zA-Z0-9_-]+:", line):
                        under_credits = False
                        fixed_lines.append(line)
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            
            try:
                fm = yaml.safe_load("\n".join(fixed_lines))
                new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False)
                new_text = f"---\n{new_fm}---\n{body}"
                with open(p, "w", encoding="utf-8") as f:
                    f.write(new_text)
                print(f"Fixed YAML indentation in: {p}")
            except Exception as e:
                print(f"Still failed {p}: {e}")
