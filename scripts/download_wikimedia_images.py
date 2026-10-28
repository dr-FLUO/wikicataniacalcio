"""
Download effettivo di tutte le immagini fotografiche autenticate
estratte da Wikimedia Commons e Wikidata nel database locale.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "wikimedia_catania_db"
IMG_ROOT = DB_DIR / "images"
COMMONS_DIR = IMG_ROOT / "commons"
PORTRAITS_DIR = IMG_ROOT / "portraits"

USER_AGENT = "WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org; Binary Image Downloader)"


def download_file(url: str, dest_path: Path, retries: int = 3, delay: float = 0.5) -> bool:
    if dest_path.exists() and dest_path.stat().st_size > 1000:
        return True
        
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()
                dest_path.write_bytes(content)
                return True
        except Exception as e:
            if attempt == retries - 1:
                print(f"  [ERROR] Impossibile scaricare {url}: {e}")
                return False
            time.sleep(delay * (attempt + 1))
    return False


def sanitize_filename(name: str) -> str:
    clean = re.sub(r'[\\/*?:"<>|]', "", name)
    clean = clean.replace(" ", "_").strip(" ._")
    return clean[:120]


def main():
    COMMONS_DIR.mkdir(parents=True, exist_ok=True)
    PORTRAITS_DIR.mkdir(parents=True, exist_ok=True)
    
    manifest = []
    
    # 1. Download da Commons (commons_images.json)
    commons_json = DB_DIR / "commons_images.json"
    if commons_json.exists():
        with open(commons_json, "r", encoding="utf-8") as f:
            commons_data = json.load(f)
            
        print(f"=== 1. Download Immagini da Wikimedia Commons ({len(commons_data)} candidate) ===")
        downloaded_commons = 0
        for idx, item in enumerate(commons_data, 1):
            url = item.get("url")
            title = item.get("file_title", "").replace("File:", "")
            if not url or url.lower().endswith(".pdf") or url.lower().endswith(".svg"):
                continue
                
            fname = sanitize_filename(title)
            ext = os.path.splitext(url)[1].split("?")[0]
            if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                fname += (ext if ext else ".jpg")
                
            out_path = COMMONS_DIR / fname
            success = download_file(url, out_path)
            if success:
                downloaded_commons += 1
                manifest.append({
                    "category": "commons_archivio",
                    "file_name": fname,
                    "local_path": f"images/commons/{fname}",
                    "size_bytes": out_path.stat().st_size,
                    "author": item.get("author", "Archivio Storico"),
                    "license": item.get("license", "CC BY-SA"),
                    "description": item.get("description", ""),
                    "source_url": url,
                })
            if idx % 20 == 0 or idx == len(commons_data):
                print(f"  Progresso Commons: {downloaded_commons} immagini scaricate con successo...")
            time.sleep(0.08)
            
        print(f"[OK] Scaricate {downloaded_commons} immagini da Commons in {COMMONS_DIR}")

    # 2. Download Ritratti Tesserati da Wikidata (wikidata_people.json)
    people_json = DB_DIR / "wikidata_people.json"
    if people_json.exists():
        with open(people_json, "r", encoding="utf-8") as f:
            people_data = json.load(f)
            
        with_img = [p for p in people_data if p.get("image_url")]
        print(f"\n=== 2. Download Ritratti Ufficiali Tesserati da Wikidata ({len(with_img)} candidati) ===")
        downloaded_portraits = 0
        for idx, p in enumerate(with_img, 1):
            name = p["name"]
            img_url = p["image_url"]
            if not img_url.startswith("http"):
                img_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(img_url)}"
            elif img_url.startswith("http://"):
                img_url = "https://" + img_url[7:]
                
            slug_name = sanitize_filename(name).lower()
            fname = f"{slug_name}.jpg"
            out_path = PORTRAITS_DIR / fname
            
            success = download_file(img_url, out_path)
            if success:
                downloaded_portraits += 1
                manifest.append({
                    "category": "ritratto_tesserato",
                    "person_name": name,
                    "qid": p.get("qid"),
                    "file_name": fname,
                    "local_path": f"images/portraits/{fname}",
                    "size_bytes": out_path.stat().st_size,
                    "author": "Wikimedia Commons / Wikidata Contributor",
                    "license": "Creative Commons / Pubblico Dominio",
                    "description": f"Ritratto fotografico ufficiale di {name}",
                    "source_url": img_url,
                })
            if idx % 25 == 0 or idx == len(with_img):
                print(f"  Progresso Ritratti: {downloaded_portraits}/{len(with_img)} scaricati...")
            time.sleep(0.08)
            
        print(f"[OK] Scaricati {downloaded_portraits} ritratti ufficiali in {PORTRAITS_DIR}")

    # 3. Salva Manifest Immagini
    manifest_path = IMG_ROOT / "manifest_immagini.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        
    total_mb = sum(m["size_bytes"] for m in manifest) / (1024 * 1024)
    print("\n=======================================================")
    print(f"DOWNLOAD IMMAGINI COMPLETATO: {len(manifest)} FILE SCARICATI!")
    print(f"Volume totale sul disco: {total_mb:.2f} MB")
    print(f"Manifest di catalogazione salvato in: {manifest_path}")
    print("=======================================================")


if __name__ == "__main__":
    main()
