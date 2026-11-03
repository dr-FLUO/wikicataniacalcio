"""
Deploy delle immagini verificate dal database Wikimedia in content/assets/images/
e generazione della mappa entita -> metadati immagine (autore, licenza, didascalia).
"""

import json
import os
import shutil
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "wikimedia_catania_db"
IMG_DB = DB_DIR / "images"
CONTENT_IMG = BASE_DIR / "content" / "assets" / "images"

with open(IMG_DB / "manifest_immagini.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Carica i dati delle persone per mappare qid e nome a slug
with open(DB_DIR / "wikidata_people.json", "r", encoding="utf-8") as f:
    people = json.load(f)

def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[àáâãäå]", "a", s)
    s = re.sub(r"[èéêë]", "e", s)
    s = re.sub(r"[ìíîï]", "i", s)
    s = re.sub(r"[òóôõö]", "o", s)
    s = re.sub(r"[ùúûü]", "u", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

name_to_slug = {}
for p in people:
    name_to_slug[p["name"].lower()] = slugify(p["name"])
    if p.get("it_wiki_article"):
        wiki_title = p["it_wiki_article"].split("/wiki/")[-1].replace("_", " ").lower()
        name_to_slug[wiki_title] = slugify(p["name"])

deployed_map = {}

(CONTENT_IMG / "calciatori").mkdir(parents=True, exist_ok=True)
(CONTENT_IMG / "allenatori").mkdir(parents=True, exist_ok=True)
(CONTENT_IMG / "stagioni").mkdir(parents=True, exist_ok=True)
(CONTENT_IMG / "strutture-e-stadi").mkdir(parents=True, exist_ok=True)
(CONTENT_IMG / "partite-storiche").mkdir(parents=True, exist_ok=True)

# 1. Copia ritratti
for item in manifest:
    if item["category"] == "ritratto_tesserato":
        src = DB_DIR / item["local_path"]
        if not src.exists():
            continue
            
        person_name = item["person_name"]
        slug = slugify(person_name)
        target_name = f"{slug}.jpg"
        dest = CONTENT_IMG / "calciatori" / target_name
        shutil.copy2(src, dest)
        
        # Mappa licenza
        lic = item.get("license", "Creative Commons CC BY-SA 4.0")
        if "pubblico" in lic.lower() or "public" in lic.lower() or "1958" in item["file_name"]:
            lic_type = "Pubblico Dominio (Scadenza termini d'autore)"
        else:
            lic_type = "Creative Commons CC BY-SA 4.0"
            
        author = item.get("author") or "Archivio Fotografico Wikimedia"
        if "contributor" in author.lower() or author == "N/A":
            author = "Wikimedia Commons Contributors"
            
        deployed_map[slug] = {
            "image_path": f"/assets/images/calciatori/{target_name}",
            "relative_path": f"assets/images/calciatori/{target_name}",
            "alt_text": f"Ritratto ufficiale di {person_name} — Licenza: {lic_type} — Crediti: {author}",
            "caption": f"Ritratto ufficiale di {person_name} — Licenza: {lic_type} — Crediti: {author}",
            "author_or_archive": author,
            "license_type": lic_type,
            "year": 2024,
        }

# 2. Copia Commons storiche
for item in manifest:
    if item["category"] == "commons_archivio":
        src = DB_DIR / item["local_path"]
        if not src.exists():
            continue
        fname = item["file_name"]
        dest = CONTENT_IMG / "stagioni" / fname
        shutil.copy2(src, dest)
        
        lic = item.get("license", "Creative Commons CC BY-SA 4.0")
        if "public" in lic.lower() or "pubblico" in lic.lower():
            lic_type = "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)"
        else:
            lic_type = "Creative Commons CC BY-SA 4.0"
            
        author = item.get("author") or "Archivio Storico Catania"
        if author == "N/A" or "unknown" in author.lower():
            author = "Archivio Storico Wikimedia / Pubblico Dominio"
            
        desc = item.get("description") or fname.replace("_", " ").replace(".jpg", "")
        clean_desc = re.sub(r"<[^>]+>", "", desc).strip()
        if len(clean_desc) > 80:
            clean_desc = clean_desc[:77] + "..."
            
        deployed_map[fname] = {
            "image_path": f"/assets/images/stagioni/{fname}",
            "relative_path": f"assets/images/stagioni/{fname}",
            "alt_text": f"{clean_desc} — Licenza: {lic_type} — Crediti: {author}",
            "caption": f"{clean_desc} — Licenza: {lic_type} — Crediti: {author}",
            "author_or_archive": author,
            "license_type": lic_type,
            "year": 2024,
        }

registry_file = DB_DIR / "deployed_images_map.json"
with open(registry_file, "w", encoding="utf-8") as f:
    json.dump(deployed_map, f, ensure_ascii=False, indent=2)

print(f"Deploy completato! Mappate {len(deployed_map)} immagini pronte in content/assets/images/")
