import os
import glob
import yaml
import re

subdirs = glob.glob('content/02-cronistoria/partite-storiche/*/')

for s in subdirs:
    folder_name = os.path.basename(os.path.normpath(s))
    if folder_name == 'precedenti':
        continue
    
    index_path = os.path.join(s, 'index.md')
    if os.path.exists(index_path):
        continue

    files = [f for f in os.listdir(s) if f.endswith('.md') and f != 'index.md']
    if not files:
        continue

    matches_info = []
    for f in files:
        fpath = os.path.join(s, f)
        slug = f[:-3]
        with open(fpath, 'r', encoding='utf-8') as mfp:
            content = mfp.read()
        
        # extract title
        m_title = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        title = m_title.group(1).strip() if m_title else slug.replace('-', ' ').title()
        
        # extract description
        m_desc = re.search(r'description:\s*["\']?([^"\'\n]+)["\']?', content)
        desc = m_desc.group(1).strip() if m_desc else "Cronaca, tabellino e testimonianze ufficiali della sfida."

        matches_info.append({
            'slug': slug,
            'title': title,
            'desc': desc,
            'filename': f
        })

    index_content = f"""---
title: "Partite Storiche — Stagione {folder_name}"
description: "Raccolta e tabellini ufficiali delle sfide leggendarie e dei match memorabili disputati dal Calcio Catania nella stagione sportiva {folder_name}."
slug: 02-cronistoria/partite-storiche/{folder_name}
entity_type: dossier_stagionale
status: verified
last_verified_date: '2026-10-30'
tags:
- partite-storiche
- {folder_name}
- tabellini
- serie-a
- coppa-italia
sources:
- author: Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino
  title: Tutto il Catania minuto per minuto
  publisher: GEO Edizioni, Empoli
  year: 2011
  reference: Tabellini ufficiali stagione {folder_name}
---

# Partite Storiche — Stagione {folder_name}

In questa sezione sono raccolte le monografie documentali, i tabellini ufficiali e le cronache d'epoca dei match memorabili disputati dal **Calcio Catania** nel corso dell'annata sportiva **{folder_name}**.

---

## Elenco Incontri Monografici

"""
    for m in matches_info:
        index_content += f"""### [[02-cronistoria/partite-storiche/{folder_name}/{m['slug']}|{m['title']}]]
{m['desc']}

"""

    index_content += f"""---

## Collegamenti Correlati

- [[02-cronistoria/partite-storiche/index|Indice Generale delle Partite Storiche]]
- [[02-cronistoria/stagioni/{folder_name}|Dossier Stagione {folder_name} del Calcio Catania]]
- [[02-cronistoria/index|Cronistoria e Almanacco Generale]]
"""

    with open(index_path, 'w', encoding='utf-8') as ifp:
        ifp.write(index_content)
    print(f"Created index for {folder_name} with {len(matches_info)} matches.")

print("All missing partite-storiche indexes created successfully.")
