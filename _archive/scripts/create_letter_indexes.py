import os
import glob
import re

letter_groups = {
    'a-c': 'Calciatori — Lettere A – C',
    'd-f': 'Calciatori — Lettere D – F',
    'g-l': 'Calciatori — Lettere G – L',
    'm-o': 'Calciatori — Lettere M – O',
    'p-r': 'Calciatori — Lettere P – R',
    's-z': 'Calciatori — Lettere S – Z'
}

for group, title in letter_groups.items():
    dir_path = os.path.join('content/03-tesserati/calciatori/archivio', group)
    if not os.path.isdir(dir_path):
        continue
    
    index_file = os.path.join(dir_path, 'index.md')
    files = sorted(glob.glob(os.path.join(dir_path, '*.md')))
    
    players = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        if slug == 'index':
            continue
        with open(f, 'r', encoding='utf-8') as pfp:
            txt = pfp.read()
        
        # get name from H1 or title
        m_name = re.search(r'^#\s+([^\n]+)', txt, re.MULTILINE)
        name_raw = m_name.group(1) if m_name else slug.replace('-', ' ').title()
        name = re.split(r'\s+[—–\-:]\s+', re.sub(r'^#\s*', '', name_raw))[0].strip()
        
        # get period
        m_per = re.search(r'<th>Al Catania</th>\s*<td>([^<]+)</td>', txt)
        period = m_per.group(1).strip() if m_per else 'ND'
        
        # get apps and goals
        m_app = re.search(r'<th>Presenze totali</th>\s*<td>([^<]+)</td>', txt)
        apps = m_app.group(1).strip() if m_app else '0'
        
        m_gol = re.search(r'<th>Goal totali</th>\s*<td>([^<]+)</td>', txt)
        goals = m_gol.group(1).strip() if m_gol else '0'

        players.append({
            'slug': slug,
            'name': name,
            'period': period,
            'apps': apps,
            'goals': goals
        })

    content = f"""---
title: "{title}"
description: "Indice alfabetico e schede biografiche dei calciatori del Catania con cognome compreso nel gruppo {title.split('—')[1].strip()}."
slug: 03-tesserati/calciatori/archivio/{group}
entity_type: section_index
status: verified
last_verified_date: '2026-10-30'
tags:
- calciatori
- archivio
- {group}
sources:
- author: Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino
  title: Tutto il Catania minuto per minuto (1929-2010)
  publisher: GEO Edizioni, Empoli
  year: 2010
  reference: Registro alfabetico calciatori
aliases:
- tesserati/calciatori/archivio/{group}
- calciatori/archivio/{group}
---

# {title}

Questo dossier raccoglie le schede biografiche e statistiche di tutti i calciatori rossazzurri con cognome appartenente al gruppo alfabetico **{group.upper()}**.

Totale calciatori censiti in questa sezione: **{len(players)}**.

---

## Elenco Calciatori

| Calciatore | Periodo al Catania | Presenze | Reti | Scheda Monografica |
| :--- | :---: | :---: | :---: | :--- |
"""

    for p in players:
        content += f"| **{p['name']}** | {p['period']} | {p['apps']} | {p['goals']} | [[03-tesserati/calciatori/archivio/{group}/{p['slug']}|Visualizza scheda →]] |\n"

    content += f"""
---

## Collegamenti Correlati

- [[03-tesserati/calciatori/archivio/index|Archivio Generale Calciatori (Indice Alfabetico)]]
- [[03-tesserati/calciatori/storici/index|Campioni Storici]]
- [[03-tesserati/calciatori/rosa-attuale/index|Rosa Attuale]]
- [[03-tesserati/calciatori/index|Indice Generale Sezione Calciatori]]
"""

    with open(index_file, 'w', encoding='utf-8') as ifp:
        ifp.write(content)
    print(f"Generated index for {group} with {len(players)} players.")

print("All letter group indexes generated successfully.")
