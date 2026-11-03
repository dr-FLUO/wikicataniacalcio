import os
import glob
import re

CONTENT_DIR = "content"

MAPPINGS = {
    "rosario-pelligra": "01-societa/presidenti/ross-pelligra",
    "01-societa/presidenti/rosario-pelligra": "01-societa/presidenti/ross-pelligra",
    "vespasiano-trigona-di-misterbianco": "01-societa/presidenti/vespasiano-trigona",
    "01-societa/presidenti/vespasiano-trigona-di-misterbianco": "01-societa/presidenti/vespasiano-trigona",
    "avv-andrea-gaudioso": "01-societa/presidenti/andrea-gaudioso",
    "01-societa/presidenti/avv-andrea-gaudioso": "01-societa/presidenti/andrea-gaudioso",
    "ruggero-albanese": "01-societa/presidenti/ruggero-albanese",
    "maxi-lpez": "03-tesserati/calciatori/storici/maxi-lopez",
    "tesserati/calciatori/maxi-lpez": "03-tesserati/calciatori/storici/maxi-lopez",
    "g-za-kert-sz": "03-tesserati/allenatori/geza-kertesz",
    "03-tesserati/allenatori/g-za-kert-sz": "03-tesserati/allenatori/geza-kertesz",
    "Andrea Salvadori (calciatore)": "03-tesserati/calciatori/archivio/s-z/andrea-salvadori",
    "Mario Corti (calciatore)": "03-tesserati/calciatori/archivio/a-c/mario-corti",
    "Claiton dos Santos Machado": "03-tesserati/calciatori/archivio/a-c/claiton",
    "Sergio Bernardo Almirón": "03-tesserati/calciatori/storici/sergio-almiron",
    "Marco Romano (calciatore)": "03-tesserati/calciatori/archivio/p-r/marco-romano",
    "Giovanni Marchese (calciatore)": "03-tesserati/calciatori/storici/giovanni-marchese",
    "tesserati/calciatori/cantarutti-crialesi": "03-tesserati/calciatori/storici/aldo-cantarutti",
    "tesserati/calciatori/buzzin-uzzecchini": "03-tesserati/calciatori/archivio/a-c/giorgio-buzzin",
    "tesserati/calciatori/buzzin-carapellese": "03-tesserati/calciatori/archivio/a-c/giorgio-buzzin",
    "03-tesserati/allenatori/gennaro-rambone-poi-bruno-pace": "03-tesserati/allenatori/gennaro-rambone",
}

def clean_file(fpath):
    with open(fpath, "r", encoding="utf-8") as fp:
        content = fp.read()

    changed = False
    for k, v in MAPPINGS.items():
        pattern = re.compile(rf'\[\[{re.escape(k)}(?:\|([^\]]+))?\]\]')
        if pattern.search(content):
            def repl(m):
                lbl = m.group(1) or k.split("/")[-1].replace("-", " ").title()
                return f"[[{v}|{lbl}]]"
            content = pattern.sub(repl, content)
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
    print(f"File corretti con mappature avanzate: {fixed}")

if __name__ == "__main__":
    main()
