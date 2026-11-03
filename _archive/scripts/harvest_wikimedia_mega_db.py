"""
Script di estrazione massiva per il Mega Database Locale del Calcio Catania (1929-2027)
utilizzando Wikipedia REST/Action API, Wikidata SPARQL e Wikimedia Commons API.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "wikimedia_catania_db"
SEASONS_DIR = DB_DIR / "seasons"
USER_AGENT = "WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org; Educational Research)"


def http_get_json(url: str, retries: int = 3, delay: float = 0.5) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw)
        except Exception as e:
            if attempt == retries - 1:
                print(f"[ERROR] Failed request to {url}: {e}")
                return {}
            time.sleep(delay * (attempt + 1))
    return {}


def get_category_pages(cat_title: str) -> list[dict]:
    pages = []
    cmcontinue = None
    while True:
        url = (
            f"https://it.wikipedia.org/w/api.php?action=query&list=categorymembers"
            f"&cmtitle={urllib.parse.quote(cat_title)}&cmlimit=500&format=json"
        )
        if cmcontinue:
            url += f"&cmcontinue={urllib.parse.quote(cmcontinue)}"
        d = http_get_json(url)
        q = d.get("query", {})
        members = q.get("categorymembers", [])
        pages.extend(members)
        if "continue" in d and "cmcontinue" in d["continue"]:
            cmcontinue = d["continue"]["cmcontinue"]
        else:
            break
    return pages


def parse_season_wikitext(wt: str) -> dict:
    """Estrae campi chiave dall'infobox Stagione squadra e tabelle."""
    info = {}
    
    # Infobox extraction
    m_box = re.search(r"\{\{Stagione squadra(.*?)\n\}\}", wt, re.DOTALL)
    if m_box:
        box_text = m_box.group(1)
        for line in box_text.split("\n"):
            line = line.strip()
            if line.startswith("|") and "=" in line:
                k, v = line[1:].split("=", 1)
                info[k.strip()] = v.strip()
    
    # Presenze e marcatori (sezione statistiche)
    return info


def harvest_all_seasons():
    print("=== 1. Estrazione Stagioni da it.wikipedia.org ===")
    SEASONS_DIR.mkdir(parents=True, exist_ok=True)
    
    cat_members = get_category_pages("Categoria:Stagioni del Catania F.C.")
    print(f"Trovate {len(cat_members)} pagine di stagioni nella categoria ufficiale.")
    
    catalog = []
    
    for idx, member in enumerate(cat_members, 1):
        title = member["title"]
        page_id = member["pageid"]
        
        # Estrai etichetta stagione (es. 1960-1961 o 2024-2025)
        m_yr = re.search(r"(\d{4}-\d{4})", title)
        season_label = m_yr.group(1) if m_yr else title.replace(" ", "_")
        
        target_file = SEASONS_DIR / f"{season_label}.json"
        if target_file.exists():
            print(f"[{idx}/{len(cat_members)}] {season_label} già presente in cache locale.")
            with open(target_file, "r", encoding="utf-8") as f:
                catalog.append(json.load(f))
            continue
            
        print(f"[{idx}/{len(cat_members)}] Scarico {title} ({season_label})...")
        url = (
            f"https://it.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(title)}"
            f"&prop=wikitext|sections|images|externallinks&format=json"
        )
        data = http_get_json(url)
        parse_data = data.get("parse", {})
        wikitext = parse_data.get("wikitext", {}).get("*", "")
        sections = [s["line"] for s in parse_data.get("sections", [])]
        images = parse_data.get("images", [])
        extlinks = parse_data.get("externallinks", [])
        
        infobox = parse_season_wikitext(wikitext)
        
        season_record = {
            "wiki_title": title,
            "season_label": season_label,
            "page_id": page_id,
            "infobox": infobox,
            "sections": sections,
            "images": images,
            "external_links": extlinks,
            "wikitext_length": len(wikitext),
            "wikitext": wikitext,
        }
        
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(season_record, f, ensure_ascii=False, indent=2)
            
        catalog.append(season_record)
        time.sleep(0.15) # rispetta policy API di Wikimedia
        
    catalog_path = DB_DIR / "seasons_catalog.json"
    summary_catalog = [
        {
            "season_label": s["season_label"],
            "wiki_title": s["wiki_title"],
            "allenatore": s.get("infobox", {}).get("allenatore1", s.get("infobox", {}).get("allenatore", "")),
            "presidente": s.get("infobox", {}).get("presidente", ""),
            "campionato": s.get("infobox", {}).get("campionato", ""),
            "posizione": s.get("infobox", {}).get("campionato posizione", ""),
            "immagini": len(s.get("images", [])),
            "fonti_esterne": len(s.get("external_links", [])),
        }
        for s in catalog
    ]
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(summary_catalog, f, ensure_ascii=False, indent=2)
        
    print(f"[OK] Salvate {len(catalog)} stagioni in {SEASONS_DIR}")


def harvest_wikidata():
    print("\n=== 2. Estrazione Tesserati e Figure Storiche da Wikidata SPARQL ===")
    # Query: tutti i soggetti legati a Calcio Catania (Q2018) o Catania FC (Q114881951)
    # sia come squadra attuale/precedente (P54) sia come allenatore (P286)
    sparql = """
    SELECT DISTINCT ?person ?personLabel ?birthDate ?birthPlaceLabel ?deathDate ?positionLabel ?countryLabel ?article ?image WHERE {
      { ?person wdt:P54 wd:Q2018 . }
      UNION
      { ?person wdt:P54 wd:Q114881951 . }
      UNION
      { ?person wdt:P286 wd:Q2018 . }
      UNION
      { ?person wdt:P286 wd:Q114881951 . }
      
      OPTIONAL { ?person wdt:P569 ?birthDate . }
      OPTIONAL { ?person wdt:P19 ?birthPlace . }
      OPTIONAL { ?person wdt:P570 ?deathDate . }
      OPTIONAL { ?person wdt:P413 ?position . }
      OPTIONAL { ?person wdt:P27 ?country . }
      OPTIONAL { ?person wdt:P18 ?image . }
      OPTIONAL {
        ?article schema:about ?person ;
                 schema:isPartOf <https://it.wikipedia.org/> .
      }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "it,en". }
    }
    """
    url = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(sparql)
    data = http_get_json(url, retries=5, delay=2.0)
    bindings = data.get("results", {}).get("bindings", [])
    print(f"Wikidata SPARQL ha restituito {len(bindings)} record!")
    
    people_map = {}
    for b in bindings:
        qid = b["person"]["value"].split("/")[-1]
        name = b.get("personLabel", {}).get("value", "")
        if not name or name.startswith("Q") and name[1:].isdigit():
            continue
            
        bdate = b.get("birthDate", {}).get("value", "")[:10] if "birthDate" in b else ""
        bplace = b.get("birthPlaceLabel", {}).get("value", "")
        ddate = b.get("deathDate", {}).get("value", "")[:10] if "deathDate" in b else ""
        pos = b.get("positionLabel", {}).get("value", "")
        country = b.get("countryLabel", {}).get("value", "")
        article = b.get("article", {}).get("value", "")
        img = b.get("image", {}).get("value", "")
        
        if qid not in people_map:
            people_map[qid] = {
                "qid": qid,
                "name": name,
                "birth_date": bdate,
                "birth_place": bplace,
                "death_date": ddate,
                "positions": [pos] if pos else [],
                "country": country,
                "it_wiki_article": article,
                "image_url": img,
            }
        else:
            if pos and pos not in people_map[qid]["positions"]:
                people_map[qid]["positions"].append(pos)
            if not people_map[qid]["image_url"] and img:
                people_map[qid]["image_url"] = img
                
    people_list = list(people_map.values())
    people_path = DB_DIR / "wikidata_people.json"
    with open(people_path, "w", encoding="utf-8") as f:
        json.dump(people_list, f, ensure_ascii=False, indent=2)
        
    print(f"[OK] Salvati {len(people_list)} tesserati e personaggi storici unici in {people_path}")


def harvest_wikimedia_commons():
    print("\n=== 3. Estrazione Immagini Ufficiali da Wikimedia Commons ===")
    # Ricerche mirate su Wikimedia Commons
    queries = [
        "Calcio Catania",
        "Catania Football Club",
        "Stadio Angelo Massimino",
        "Stadio Cibali",
        "Torre del Grifo Village",
        "Maglia Calcio Catania",
    ]
    
    all_images = {}
    
    for q in queries:
        print(f"Cercando su Commons per '{q}'...")
        url = (
            f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
            f"&gsrsearch={urllib.parse.quote(q)}&gsrnamespace=6&prop=imageinfo"
            f"&iiprop=url|extmetadata|size|mime&gsrlimit=100&format=json"
        )
        data = http_get_json(url)
        pages = data.get("query", {}).get("pages", {})
        print(f"  -> Trovate {len(pages)} immagini per '{q}'")
        for pid, p in pages.items():
            title = p.get("title", "")
            if title in all_images:
                continue
            info = p.get("imageinfo", [{}])[0]
            meta = info.get("extmetadata", {})
            lic = meta.get("LicenseShortName", {}).get("value", "N/A")
            desc = meta.get("ObjectName", {}).get("value") or meta.get("ImageDescription", {}).get("value", "")
            artist = meta.get("Artist", {}).get("value", "N/A")
            date_time = meta.get("DateTimeOriginal", {}).get("value") or meta.get("DateTime", {}).get("value", "")
            
            # Pulizia tag HTML da descrizione e autore
            desc_clean = re.sub(r"<[^>]+>", "", desc).strip()
            artist_clean = re.sub(r"<[^>]+>", "", artist).strip()
            
            all_images[title] = {
                "file_title": title,
                "url": info.get("url"),
                "description_url": info.get("descriptionurl"),
                "width": info.get("width"),
                "height": info.get("height"),
                "mime": info.get("mime"),
                "size_bytes": info.get("size"),
                "license": lic,
                "author": artist_clean[:120],
                "date": str(date_time)[:20],
                "description": desc_clean[:250],
            }
        time.sleep(0.3)
        
    commons_path = DB_DIR / "commons_images.json"
    with open(commons_path, "w", encoding="utf-8") as f:
        json.dump(list(all_images.values()), f, ensure_ascii=False, indent=2)
        
    print(f"[OK] Salvate {len(all_images)} immagini storiche uniche da Commons in {commons_path}")


def main():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    start = time.time()
    
    harvest_all_seasons()
    harvest_wikidata()
    harvest_wikimedia_commons()
    
    elapsed = time.time() - start
    print(f"\n=======================================================")
    print(f"ESTRAZIONE COMPLETATA CON SUCCESSO IN {elapsed:.1f} SECONDI!")
    print(f"Mega Database locale disponibile in: {DB_DIR}")
    print(f"=======================================================")


if __name__ == "__main__":
    main()
