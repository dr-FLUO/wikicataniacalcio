import re

# Update MagazineHome.tsx
with open('quartz/components/MagazineHome.tsx', 'r', encoding='utf-8') as f:
    mh = f.read()

pattern_mh = re.compile(r'\{\s*years:\s*"2022–OGGI",\s*name:\s*"Catania SSD ➔ Catania Football Club",\s*matricola:\s*"FIGC 955013",\s*figures:\s*"[^"]*",\s*event:\s*"[^"]*",\s*href:\s*"[^"]*",\s*\}', re.MULTILINE)

new_mh = '''{
    years: "2022–OGGI",
    name: "Catania SSD ➔ Catania Football Club",
    matricola: "FIGC 955013",
    figures: "Rosario Pelligra, V. Grella, D. Faggiano, D. Toscano",
    event: "Rinascita ex Art. 52 NOIF, record Serie D (88 pt), 1ª Coppa Italia Serie C (2024), riacquisto storico logo e acquisizione Torre del Grifo.",
    href: "./01-societa/epoche/2022-pelligra-catania-fc",
  }'''

if pattern_mh.search(mh):
    mh = pattern_mh.sub(new_mh, mh)
    with open('quartz/components/MagazineHome.tsx', 'w', encoding='utf-8') as f:
        f.write(mh)
    print("MagazineHome.tsx updated!")
else:
    print("Pattern in MagazineHome.tsx not found")

# Update content/index.md
with open('content/index.md', 'r', encoding='utf-8') as f:
    idx = f.read()

# Fix nested wikilinks in content/index.md
idx = idx.replace('[[vicende-legali/caso-scaramella-1955\\|[[01-societa/vicende-legali/caso-scaramella-1955\\|Caso Scaramella]] (1955)]]', '[[01-societa/vicende-legali/caso-scaramella-1955|Caso Scaramella (1955)]]')
idx = idx.replace('[[stagioni/1982-1983\\|[[02-cronistoria/partite-storiche/1982-1983/spareggi-roma-1983\\|spareggi di Roma]] 1983]]', '[[02-cronistoria/partite-storiche/1982-1983/spareggi-roma-1983|spareggi di Roma 1983]]')

# Update row 2022-Oggi
row_old = '| **2022–Oggi** | [[societa/2022-pelligra-catania-fc\\|Catania SSD ➔ Catania Football Club]] | **955013** | R. Pelligra, V. Grella, [[tesserati/allenatori/michele-zeoli\\|M. Zeoli]] | Vittoria Serie D 2022-23, [[stagioni/2023-2024\\|1ª Coppa Italia Serie C (2023-24)]] e [[maglie/loghi-storici-liotru\\|riacquisto logo storico]]. |'
row_new = '| **2022–Oggi** | [[societa/2022-pelligra-catania-fc\\|Catania SSD ➔ Catania Football Club]] | **955013** | R. Pelligra, V. Grella, D. Faggiano (DS), D. Toscano (All.) | Vittoria Serie D 2022-23 (record 88 pt), [[stagioni/2023-2024\\|1ª Coppa Italia Serie C (2023-24)]], [[maglie/loghi-storici-liotru\\|riacquisto logo storico]] e acquisizione Torre del Grifo (2025-2026). |'

if row_old in idx:
    idx = idx.replace(row_old, row_new)
    print("content/index.md 2022-Oggi row replaced")
else:
    print("row_old not directly matched, trying regex")
    idx = re.sub(r'\|\s*\*\*2022–Oggi\*\*.*?\n', row_new + '\n', idx)
    print("content/index.md regex substituted")

with open('content/index.md', 'w', encoding='utf-8') as f:
    f.write(idx)
print("content/index.md updated!")
