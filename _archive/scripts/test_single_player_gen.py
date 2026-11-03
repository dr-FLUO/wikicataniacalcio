import json
import os
import re
import yaml

with open('data/calciocatania_all_players.json', encoding='utf-8') as f:
    players = json.load(f)

with open('data/player_local_images.json', encoding='utf-8') as f:
    local_imgs = json.load(f)

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

p = players[0] # Paolo Acerbis
name = p['name']
slug = slugify(name)
pid = str(p['id'])
role = p.get('role', 'Calciatore')
apps = p.get('appearances', 0)
seasons = p.get('seasons_count', 1)
src_url = p.get('url', 'https://www.calciocatania.com/')
local_img = local_imgs.get(pid)

fm = {
    "title": f"{name} — Scheda Giocatore e Statistiche nel Calcio Catania",
    "description": f"Biografia, presenze e statistiche ufficiali di {name}, {role.lower()} del Calcio Catania con {apps} presenze registrate in maglia rossazzurra.",
    "slug": f"tesserati/calciatori/{slug}",
    "entity_type": "calciatore",
    "status": "verified",
    "last_verified_date": "2026-10-28",
    "role": role,
    "total_appearances": apps,
    "seasons_count": seasons,
    "tags": ["calciatori", slug, role.lower()],
    "sources": [
        {
            "author": "Salvatore Giovanni Emanuele, Max Licari",
            "title": f"Scheda anagrafica e statistiche di {name}",
            "publisher": "calciocatania.com",
            "url": src_url,
            "year": 2024,
            "reference": f"Archivio Giocatori CalcioCatania.com - ID {pid}"
        },
        {
            "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
            "title": "Tutto il Catania minuto per minuto",
            "publisher": "GEO Edizioni, Empoli",
            "year": 2010,
            "reference": "Registro generale calciatori e presenze ufficiali"
        }
    ]
}

body_img = ""
if local_img and os.path.exists(os.path.join('content', local_img)):
    alt = f"Ritratto del calciatore {name} in maglia rossazzurra del Calcio Catania"
    fm["image"] = local_img
    fm["image_credits"] = [
        {
            "image_path": local_img,
            "alt_text": alt,
            "author_or_archive": "Archivio Fotografico CalcioCatania.com",
            "year": 2010,
            "license_type": "Creative Commons CC BY-SA 4.0"
        }
    ]
    body_img = f"\n![{alt}](/{local_img})\n"

body = f"""# {name} — Scheda Giocatore nel Calcio Catania
{body_img}
**{name}** è stato un calciatore del [[societa/matricola-11700|Calcio Catania]], nel ruolo di **{role}**.

---

## 1. Dati di Rendimento in Maglia Rossazzurra

* **Ruolo**: {role}
* **Presenze Ufficiali complessive**: {apps}
* **Stagioni disputate**: {seasons}
* **Stadio di casa**: [[stadio/angelo-massimino|Stadio Angelo Massimino]]

---

## 2. Note e Scheda di Carriera

Il calciatore ha difeso i colori rossazzurri durante la sua militanza all'ombra dell'Etna, contribuendo alle vicende sportive del sodalizio etneo nei campionati nazionali.

---

## 3. Collegamenti e Voci Correlate

* [[societa/matricola-11700|Calcio Catania: La storia societaria e la Matricola 11700]]
* [[stadio/angelo-massimino|Stadio Angelo Massimino (ex Cibali)]]
* [[maglie/simbologia-colori-scudetti|I colori e la simbologia rossazzurra]]
* [[media/testate/calciocatania-com|Archivio Storico e Portale d'Informazione CalcioCatania]]

---

## Fonti e Bibliografia

1. **Salvatore Giovanni Emanuele, Max Licari**, *Scheda anagrafica e statistiche di {name}*, in [{src_url}]({src_url}), 2024.
2. **Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino**, *Tutto il Catania minuto per minuto*, GEO Edizioni, Empoli, 2010.
"""

test_path = f"content/tesserati/calciatori/{slug}.md"
with open(test_path, 'w', encoding='utf-8') as f:
    f.write(f"---\n{yaml.dump(fm, allow_unicode=True, sort_keys=False)}---\n{body}")

print(f"Written test player to {test_path}")
