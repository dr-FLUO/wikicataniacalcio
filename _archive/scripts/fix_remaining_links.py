import os
import glob
import re
import json

CONTENT_DIR = "content"

# Load tesserati db for surname lookup
with open("quartz/components/tesserati_db.json", "r", encoding="utf-8") as f:
    tesserati = json.load(f)

surname_map = {}
for p in tesserati:
    c = p.get("c", "").lower().strip()
    if c and c not in surname_map:
        surname_map[c] = p.get("u")

SPECIAL_FIXES = {
    "gza-kertsz": "03-tesserati/allenatori/geza-kertesz",
    "geza-kertesz": "03-tesserati/allenatori/geza-kertesz",
    "03-tesserati/allenatori/gza-kertsz": "03-tesserati/allenatori/geza-kertesz",
    "tesserati/calciatori/marcatore-totale": "02-cronistoria/stagioni/index",
    "02-cronistoria/stagioni/1928-1929": "01-societa/epoche/1929-ss-catania",
    "stagioni/1928-1929": "01-societa/epoche/1929-ss-catania",
}

def clean_file(fpath):
    with open(fpath, "r", encoding="utf-8") as fp:
        content = fp.read()

    changed = False

    # 1. Fix asterisks inside wikilinks: [[Target**|Label]] or [[Target**]]
    def clean_asterisks(m):
        target = m.group(1).replace("**", "").replace("*", "").strip()
        label = m.group(2)
        if label:
            label = label.replace("**", "").replace("*", "").strip()
            return f"[[{target}|{label}]]"
        return f"[[{target}]]"

    new_content = re.sub(r'\[\[([^\]|]+\*+[^\]|]*)(?:\|([^\]]+))?\]\]', clean_asterisks, content)
    if new_content != content:
        content = new_content
        changed = True

    # 2. Fix specific known broken links
    for old_k, new_v in SPECIAL_FIXES.items():
        pattern = re.compile(rf'\[\[{re.escape(old_k)}(?:\|([^\]]+))?\]\]')
        if pattern.search(content):
            def repl_known(m):
                lbl = m.group(1) or old_k.split("/")[-1].replace("-", " ").title()
                return f"[[{new_v}|{lbl}]]"
            content = pattern.sub(repl_known, content)
            changed = True

    # 3. Fix concatenated coaches in coach_refs
    # e.g., aldo-ammazzalorso-poi-pietro-vierchowod-poi-francesco-graziani
    if "aldo-ammazzalorso-poi-pietro-vierchowod-poi-francesco-graziani" in content:
        content = content.replace(
            "[[03-tesserati/allenatori/aldo-ammazzalorso-poi-pietro-vierchowod-poi-francesco-graziani|Aldo Ammazzalorso, poi Pietro Vierchowod, poi Francesco Graziani]]",
            "[[03-tesserati/allenatori/aldo-ammazzalorso|Aldo Ammazzalorso]], [[03-tesserati/allenatori/pietro-vierchowod|Pietro Vierchowod]], [[03-tesserati/allenatori/francesco-graziani|Francesco Graziani]]"
        )
        changed = True

    if "osvaldo-jaconi-poi-pietro-santin-poi-bruno-pace" in content:
        content = content.replace(
            "[[03-tesserati/allenatori/osvaldo-jaconi-poi-pietro-santin-poi-bruno-pace|Osvaldo Jaconi, poi Pietro Santin, poi Bruno Pace]]",
            "[[03-tesserati/allenatori/osvaldo-jaconi|Osvaldo Jaconi]], [[03-tesserati/allenatori/pietro-santin|Pietro Santin]], [[03-tesserati/allenatori/bruno-pace|Bruno Pace]]"
        )
        changed = True

    if "francesco-graziani-maurizio-pellegrino" in content:
        content = content.replace(
            "[[03-tesserati/allenatori/francesco-graziani-maurizio-pellegrino|Francesco Graziani e Maurizio Pellegrino]]",
            "[[03-tesserati/allenatori/francesco-graziani|Francesco Graziani]], [[03-tesserati/allenatori/maurizio-pellegrino|Maurizio Pellegrino]]"
        )
        changed = True

    # 4. Fix concatenated presidents
    if "carmelo-antonio-milazzo" in content and "davide-franco" in content:
        content = re.sub(
            r'\[\[01-societa/presidenti/carmelo-antonio-milazzo[^\]]*\]\]',
            "[[01-societa/presidenti/davide-franco|Davide Franco]]",
            content
        )
        changed = True

    if "nicola-le-murafino-al-16-novembre-2021-poi-sergio-santagati" in content:
        content = re.sub(
            r'\[\[01-societa/presidenti/nicola-le-murafino[^\]]*\]\]',
            "[[01-societa/presidenti/nicola-le-mura|Nicola Le Mura]]",
            content
        )
        changed = True

    if "ruggero-albanese-reggente-poibr-cav-filippo-cusmano" in content:
        content = re.sub(
            r'\[\[01-societa/presidenti/ruggero-albanese[^\]]*\]\]',
            "[[01-societa/presidenti/ruggero-albanese|Ruggero Albanese]]",
            content
        )
        changed = True

    # 5. Fix single-surname links like [[tesserati/calciatori/passiatore]] -> lookup
    def fix_surname(m):
        raw_slug = m.group(1).strip()
        label = m.group(2)
        if raw_slug.startswith("tesserati/calciatori/") or raw_slug.startswith("calciatori/"):
            surname = raw_slug.split("/")[-1].lower()
            if surname in surname_map:
                real_slug = surname_map[surname]
                disp = label if label else surname.title()
                return f"[[{real_slug}|{disp}]]"
        return m.group(0)

    new_content = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', fix_surname, content)
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(content)
        return True
    return False

def main():
    files = glob.glob(f"{CONTENT_DIR}/**/*.md", recursive=True)
    fixed = 0
    for f in files:
        if clean_file(f):
            fixed += 1
    print(f"File corretti con fix mirati: {fixed}")

if __name__ == "__main__":
    main()
