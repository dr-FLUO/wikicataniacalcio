import os, glob, re, unicodedata

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower()

letters_meta = {
    'a-c': ('Calciatori — Lettere A – C', 'A-C', 'A – C'),
    'd-f': ('Calciatori — Lettere D – F', 'D-F', 'D – F'),
    'g-l': ('Calciatori — Lettere G – L', 'G-L', 'G – L'),
    'm-o': ('Calciatori — Lettere M – O', 'M-O', 'M – O'),
    'p-r': ('Calciatori — Lettere P – R', 'P-R', 'P – R'),
    's-z': ('Calciatori — Lettere S – Z', 'S-Z', 'S – Z'),
}

for l_code, (title_str, group_str, label_str) in letters_meta.items():
    folder = f"content/03-tesserati/calciatori/archivio/{l_code}"
    index_file = f"{folder}/index.md"
    
    files = [f.replace('\\', '/') for f in glob.glob(f"{folder}/*.md") if not f.endswith('index.md')]
    
    entries = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
            
        stem = os.path.splitext(os.path.basename(f))[0]
        
        # Name
        m_t = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', c, re.MULTILINE)
        t_raw = m_t.group(1) if m_t else stem
        name = t_raw.split('—')[0].split('–')[0].split('-')[0].split('(')[0].strip()
        
        # Period
        m_p = re.search(r'<th>Al Catania</th>\s*<td colspan="3">([^<]*)</td>', c)
        period = m_p.group(1).strip() if m_p else "ND"
        
        # Apps
        m_a = re.search(r'^total_appearances:\s*(\d+)', c, re.MULTILINE)
        apps = m_a.group(1) if m_a else "0"
        
        # Goals
        m_g = re.search(r'^total_goals:\s*(\d+)', c, re.MULTILINE)
        goals = m_g.group(1) if m_g else "0"
        
        slug = f"03-tesserati/calciatori/archivio/{l_code}/{stem}"
        link = f"[[{slug}|Visualizza scheda →]]"
        
        entries.append({
            'name': name,
            'norm_name': norm(name),
            'period': period,
            'apps': apps,
            'goals': goals,
            'link': link
        })
        
    entries.sort(key=lambda x: x['norm_name'])
    
    rows = []
    for e in entries:
        rows.append(f"| **{e['name']}** | {e['period']} | {e['apps']} | {e['goals']} | {e['link']} |")
        
    new_index_content = f"""---
title: "{title_str}"
description: "Indice alfabetico e schede biografiche dei calciatori del Catania con cognome compreso nel gruppo Lettere {label_str}."
slug: 03-tesserati/calciatori/archivio/{l_code}
entity_type: section_index
status: verified
last_verified_date: '2026-11-02'
tags:
- calciatori
- archivio
- {l_code}
sources:
- author: Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino
  title: Tutto il Catania minuto per minuto (1929-2010)
  publisher: GEO Edizioni, Empoli
  year: 2010
  reference: Registro alfabetico calciatori
aliases:
- tesserati/calciatori/archivio/{l_code}
- calciatori/archivio/{l_code}
---

# {title_str}

Questo dossier raccoglie le schede biografiche e statistiche di tutti i calciatori rossazzurri con cognome appartenente al gruppo alfabetico **{group_str}**.

Totale calciatori censiti in questa sezione: **{len(entries)}**.

---

## Elenco Calciatori

| Calciatore | Periodo al Catania | Presenze | Reti | Scheda Monografica |
| :--- | :---: | :---: | :---: | :--- |
""" + "\n".join(rows) + "\n"

    with open(index_file, 'w', encoding='utf-8') as fp:
        fp.write(new_index_content)
        
    print(f"Rebuilt {index_file}: {len(entries)} players listed.")

print("All letter indexes successfully rebuilt!")
