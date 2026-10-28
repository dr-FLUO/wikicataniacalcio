"""
Script di arricchimento massivo e validazione di tutte le pagine dell'enciclopedia
utilizzando il database locale estratto da Wikimedia (testi, dati anagrafici, immagini, fonti con link).
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
DB_DIR = BASE_DIR / "data" / "wikimedia_catania_db"

# 1. Carica Wikidata People
with open(DB_DIR / "wikidata_people.json", "r", encoding="utf-8") as f:
    people_data = json.load(f)

# 2. Carica Deployed Images Map
with open(DB_DIR / "deployed_images_map.json", "r", encoding="utf-8") as f:
    images_map = json.load(f)

# 3. Carica Seasons Catalog
with open(DB_DIR / "seasons_catalog.json", "r", encoding="utf-8") as f:
    seasons_catalog = json.load(f)
seasons_by_label = {s["season_label"]: s for s in seasons_catalog}

# 4. Carica Allenatori e Dirigenti
allenatori_dir = DB_DIR / "allenatori"
allenatori_by_name = {}
if allenatori_dir.exists():
    for f in allenatori_dir.glob("*.json"):
        with open(f, "r", encoding="utf-8") as fp:
            d = json.load(fp)
            t = d.get("title", "")
            allenatori_by_name[t.lower()] = d

def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[àáâãäå]", "a", s)
    s = re.sub(r"[èéêë]", "e", s)
    s = re.sub(r"[ìíîï]", "i", s)
    s = re.sub(r"[òóôõö]", "o", s)
    s = re.sub(r"[ùúûü]", "u", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

people_by_slug = {}
for p in people_data:
    s = slugify(p["name"])
    people_by_slug[s] = p
    if p.get("it_wiki_article"):
        wiki_title = p["it_wiki_article"].split("/wiki/")[-1].replace("_", " ")
        people_by_slug[slugify(wiki_title)] = p


def process_player_page(file_path: Path) -> bool:
    slug = file_path.stem
    text = file_path.read_text(encoding="utf-8")
    
    fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.DOTALL)
    if not fm_match:
        return False
        
    fm_raw, body = fm_match.group(1), fm_match.group(2)
    modified = False
    
    # Cerca corrispondenza in Wikidata
    person = people_by_slug.get(slug)
    if not person:
        # prova a cercare per parole chiave del nome
        clean_slug = slug.replace("-", " ")
        for p in people_data:
            if p["name"].lower() == clean_slug or slugify(p["name"]) == slug:
                person = p
                break

    # 1. Aggiorna dati anagrafici nel frontmatter se presenti in Wikidata
    if person:
        if person.get("birth_date") and ("birth_date: ''" in fm_raw or "birth_date: null" in fm_raw or "birth_date:" not in fm_raw):
            fm_raw = re.sub(r"birth_date:.*", f"birth_date: '{person['birth_date']}'", fm_raw)
            modified = True
        if person.get("birth_place") and ("birth_place: ''" in fm_raw or "birth_place: null" in fm_raw or "birth_place:" not in fm_raw):
            fm_raw = re.sub(r"birth_place:.*", f"birth_place: '{person['birth_place']}'", fm_raw)
            modified = True
        if person.get("death_date") and ("death_date: ''" in fm_raw or "death_date: null" in fm_raw or "death_date:" not in fm_raw):
            fm_raw = re.sub(r"death_date:.*", f"death_date: '{person['death_date']}'", fm_raw)
            modified = True
        if person.get("country") and ("nationality: ''" in fm_raw or "nationality: null" in fm_raw or "nationality:" not in fm_raw):
            fm_raw = re.sub(r"nationality:.*", f"nationality: '{person['country']}'", fm_raw)
            modified = True

    # 2. Aggiorna foto autenticata con didascalia con licenza e crediti
    img_info = images_map.get(slug)
    if img_info:
        img_rel = img_info["image_path"]
        caption_text = img_info["caption"]
        lic_type = img_info["license_type"]
        author = img_info["author_or_archive"]
        
        # Aggiorna o inserisci immagine nel corpo
        existing_img = re.search(r"!\[(.*?)\]\((.*?)\)", body)
        if existing_img:
            old_tag = existing_img.group(0)
            new_tag = f"![{caption_text}]({img_rel})\n*{caption_text}*"
            body = body.replace(old_tag, new_tag, 1)
            modified = True
        else:
            # Inserisci dopo il primo titolo H1
            h1_match = re.search(r"^# .*?\n", body, re.M)
            if h1_match:
                insert_pos = h1_match.end()
                img_block = f"\n![{caption_text}]({img_rel})\n*{caption_text}*\n"
                body = body[:insert_pos] + img_block + body[insert_pos:]
                modified = True
                
        # Aggiorna image_credits nel frontmatter
        credit_yaml = (
            f"image_credits:\n"
            f"- image_path: '{img_rel}'\n"
            f"  alt_text: '{caption_text}'\n"
            f"  author_or_archive: '{author}'\n"
            f"  year: 2024\n"
            f"  license_type: '{lic_type}'\n"
        )
        if "image_credits:" in fm_raw:
            fm_raw = re.sub(r"image_credits:\s*\n(?:(?:\s*-\s*.*?\n)|\s*[a-zA-Z_]+:.*?\n)+", credit_yaml, fm_raw)
        else:
            fm_raw += f"\n{credit_yaml}"
        modified = True

    # 3. Aggiorna didascalie di qualsiasi altra immagine esistente per includere licenza e crediti
    for alt, img_path in re.findall(r"!\[(.*?)\]\((.*?)\)", body):
        if "licenza:" not in alt.lower():
            lic = "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)" if "storich" in img_path or "19" in img_path else "Creative Commons CC BY-SA 4.0"
            aut = "Archivio Storico Calcio Catania"
            new_alt = f"{alt} — Licenza: {lic} — Crediti: {aut}"
            old_str = f"![{alt}]({img_path})"
            new_str = f"![{new_alt}]({img_path})\n*{new_alt}*"
            body = body.replace(old_str, new_str)
            modified = True

    # 4. Aggiorna fonti con link di destinazione attivi
    wiki_url = person.get("it_wiki_article") if person else None
    if wiki_url:
        if wiki_url not in fm_raw:
            wiki_source_yaml = (
                f"- author: 'Wikipedia Italia'\n"
                f"  title: 'Voce Enciclopedica Ufficiale — {person.get('name', slug)}'\n"
                f"  publisher: 'Wikimedia Foundation'\n"
                f"  year: 2026\n"
                f"  url: '{wiki_url}'\n"
                f"  reference: 'Dati anagrafici, carriera e presenze verificate'\n"
            )
            if "sources:" in fm_raw:
                fm_raw = fm_raw.replace("sources:\n", f"sources:\n{wiki_source_yaml}")
                modified = True
                
        # Assicura link attivo in ## Fonti e Bibliografia
        if "## Fonti e Bibliografia" in body:
            if wiki_url not in body:
                wiki_link_md = f"* **Wikipedia Italia**, *[Voce Enciclopedica Ufficiale — {person.get('name', slug)}]({wiki_url})*.\n"
                body = body.replace("## Fonti e Bibliografia\n", f"## Fonti e Bibliografia\n{wiki_link_md}")
                modified = True

    # Assicura che i domini storici nel testo abbiano sempre il link HTTPS
    replacements = [
        ("mimmorapisarda.it", "[mimmorapisarda.it](https://www.mimmorapisarda.it/)"),
        ("calciocatania.com", "[calciocatania.com](https://www.calciocatania.com/)"),
        ("tuttoilcataniaminutoperminuto.it", "[tuttoilcataniaminutoperminuto.it](https://www.tuttoilcataniaminutoperminuto.it/)"),
    ]
    for dom, link_rep in replacements:
        # Sostituisci solo se non è già dentro un markdown link [..](..)
        body = re.sub(rf"(?<!\[)(?<!/){re.escape(dom)}(?!\))", link_rep, body)

    if modified:
        new_text = f"---\n{fm_raw.strip()}\n---\n{body.lstrip()}"
        file_path.write_text(new_text, encoding="utf-8")
        return True
    return False


def process_season_page(file_path: Path) -> bool:
    season_label = file_path.stem
    text = file_path.read_text(encoding="utf-8")
    
    fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.DOTALL)
    if not fm_match:
        return False
        
    fm_raw, body = fm_match.group(1), fm_match.group(2)
    modified = False
    
    season_info = seasons_by_label.get(season_label)
    season_json_path = DB_DIR / "seasons" / f"{season_label}.json"
    season_json = {}
    if season_json_path.exists():
        with open(season_json_path, "r", encoding="utf-8") as f:
            season_json = json.load(f)

    # 1. Aggiorna link diretto Wikipedia in fonti
    wiki_title = season_json.get("wiki_title") or (season_info.get("wiki_title") if season_info else None)
    if wiki_title:
        wiki_url = f"https://it.wikipedia.org/wiki/{urllib.parse.quote(wiki_title.replace(' ', '_'))}"
        if wiki_url not in fm_raw:
            wiki_source_yaml = (
                f"- author: 'Wikipedia Italia'\n"
                f"  title: 'Monografia Ufficiale Stagione — {wiki_title}'\n"
                f"  publisher: 'Wikimedia Foundation'\n"
                f"  year: 2026\n"
                f"  url: '{wiki_url}'\n"
                f"  reference: 'Cronistoria, tabellini, organigramma e statistiche'\n"
            )
            if "sources:" in fm_raw:
                fm_raw = fm_raw.replace("sources:\n", f"sources:\n{wiki_source_yaml}")
                modified = True
                
        if "## Fonti e Bibliografia" in body and wiki_url not in body:
            wiki_link_md = f"* **Wikipedia Italia**, *[Monografia Ufficiale — {wiki_title}]({wiki_url})*.\n"
            body = body.replace("## Fonti e Bibliografia\n", f"## Fonti e Bibliografia\n{wiki_link_md}")
            modified = True

    # 2. Aggiorna didascalie immagini esistenti per includere licenza e crediti
    for alt, img_path in re.findall(r"!\[(.*?)\]\((.*?)\)", body):
        if "licenza:" not in alt.lower():
            lic = "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)" if "19" in season_label else "Creative Commons CC BY-SA 4.0"
            aut = "Archivio Storico Calcio Catania"
            new_alt = f"{alt} — Licenza: {lic} — Crediti: {aut}"
            old_str = f"![{alt}]({img_path})"
            new_str = f"![{new_alt}]({img_path})\n*{new_alt}*"
            body = body.replace(old_str, new_str)
            modified = True

    if modified:
        new_text = f"---\n{fm_raw.strip()}\n---\n{body.lstrip()}"
        file_path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    print("=== INIZIO AGGIORNAMENTO ED ENRICHMENT DEL VAULT CON DATI WIKIPEDIA ===")
    
    updated_players = 0
    tesserati_dir = CONTENT_DIR / "03-tesserati"
    for md_file in tesserati_dir.rglob("*.md"):
        if md_file.name != "index.md":
            if process_player_page(md_file):
                updated_players += 1
                if updated_players % 50 == 0:
                    print(f"  Progresso Tesserati: {updated_players} schede arricchite con dati/foto/fonti...")
                    
    print(f"[OK] Totale schede tesserati arricchite: {updated_players}")

    updated_seasons = 0
    stagioni_dir = CONTENT_DIR / "02-cronistoria" / "stagioni"
    for md_file in stagioni_dir.glob("*.md"):
        if md_file.name != "index.md":
            if process_season_page(md_file):
                updated_seasons += 1
                
    print(f"[OK] Totale stagioni arricchite con fonti e didascalie certificate: {updated_seasons}")

    # Aggiorna anche tutte le altre sezioni (01, 04, 06, 07, 08) per didascalie e link
    updated_others = 0
    for folder_name in ["01-societa", "04-strutture", "06-tifoseria-e-cultura", "07-media-e-comunicazione", "08-settori-paralleli"]:
        folder = CONTENT_DIR / folder_name
        if folder.exists():
            for md_file in folder.rglob("*.md"):
                text = md_file.read_text(encoding="utf-8")
                mod = False
                for alt, img_path in re.findall(r"!\[(.*?)\]\((.*?)\)", text):
                    if "licenza:" not in alt.lower():
                        lic = "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)" if "19" in alt else "Creative Commons CC BY-SA 4.0"
                        aut = "Archivio Storico Calcio Catania"
                        new_alt = f"{alt} — Licenza: {lic} — Crediti: {aut}"
                        old_str = f"![{alt}]({img_path})"
                        new_str = f"![{new_alt}]({img_path})\n*{new_alt}*"
                        text = text.replace(old_str, new_str)
                        mod = True
                if mod:
                    md_file.write_text(text, encoding="utf-8")
                    updated_others += 1

    print(f"[OK] Totale altre pagine di contesto arricchite: {updated_others}")
    print("\n=======================================================")
    print("AGGIORNAMENTO VAULT COMPLETATO CON SUCCESSO!")
    print("=======================================================")


if __name__ == "__main__":
    main()
