"""
Script per l'estrazione massiva di tutto il CONTESTO enciclopedico del Calcio Catania:
- Eventi storici e scandali giudiziari (Caso Catania, Scontri 2007, Scandalo Scaramella, Clamoroso al Cibali, Derby)
- Strutture e stadi (Massimino, Torre del Grifo, Due Obelischi)
- Settori paralleli (Catania Women / Jolly Componibili Campione d'Italia 1978, Settore Giovanile)
- Tifoseria, araldica e cultura (Gruppi ultras, gemellaggi, rivalità, simboli)
- Presidenti (12) e Dirigenti (17)
- Allenatori storici (120)
- Bibliografia e Letteratura completa
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# Force UTF-8 stdout to avoid cp1252 Windows crashes
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "wikimedia_catania_db"
USER_AGENT = "WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org; Context Harvester)"


def http_get_json(url: str, retries: int = 3, delay: float = 0.5) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw)
        except Exception as e:
            if attempt == retries - 1:
                return {}
            time.sleep(delay * (attempt + 1))
    return {}


def fetch_and_save_wiki_page(title: str, target_dir: Path, custom_filename: str | None = None) -> dict:
    target_dir.mkdir(parents=True, exist_ok=True)
    clean_name = custom_filename or re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")
    file_path = target_dir / f"{clean_name}.json"
    
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
            
    url = (
        f"https://it.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(title)}"
        f"&prop=wikitext|sections|images|externallinks&format=json"
    )
    data = http_get_json(url)
    parse = data.get("parse", {})
    if not parse:
        return {}
        
    wikitext = parse.get("wikitext", {}).get("*", "")
    sections = [s["line"] for s in parse.get("sections", [])]
    images = parse.get("images", [])
    extlinks = parse.get("externallinks", [])
    
    # Extract bibliography section if present
    biblio_items = []
    m_bib = re.search(r"==\s*Bibliografia\s*==\s*\n(.*?)(?=\n==|\Z)", wikitext, re.DOTALL | re.IGNORECASE)
    if m_bib:
        for line in m_bib.group(1).splitlines():
            line = line.strip()
            if line.startswith("*") or line.startswith("#"):
                clean = re.sub(r"[{}\[\]*#']", "", line).strip()
                if len(clean) > 5:
                    biblio_items.append(clean)
                    
    record = {
        "title": title,
        "page_id": parse.get("pageid"),
        "sections": sections,
        "images": images,
        "external_links": extlinks,
        "bibliography_extracted": biblio_items,
        "wikitext_length": len(wikitext),
        "wikitext": wikitext,
    }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    time.sleep(0.12)
    return record


def get_category_member_titles(cat_title: str) -> list[str]:
    titles = []
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
        for m in members:
            if m.get("ns") == 0:
                titles.append(m.get("title"))
        if "continue" in d and "cmcontinue" in d["continue"]:
            cmcontinue = d["continue"]["cmcontinue"]
        else:
            break
    return titles


def main():
    print("=== INIZIO ESTRAZIONE MASSIVA DEL CONTESTO (WIKIPEDIA / WIKIMEDIA) ===")
    all_biblio = []

    # 1. EVENTI STORICI, SCANDALI E DERBY
    print("\n--- 1. Eventi Storici, Giustizia Sportiva e Derby ---")
    eventi_dir = DB_DIR / "eventi_storici"
    eventi_pages = [
        ("Storia del Catania Football Club", "storia_del_catania"),
        ("Caso Catania", "caso_catania_2003_1993"),
        ("Scandalo Scaramella", "scandalo_scaramella"),
        ("Scontri di Catania", "scontri_di_catania_2007"),
        ("Filippo Raciti", "filippo_raciti"),
        ("Clamoroso al Cibali!", "clamoroso_al_cibali"),
        ("Cinquanta volti per il Cibali", "cinquanta_volti_per_il_cibali_hall_of_fame"),
        ("Derby calcistici in Sicilia", "derby_calcistici_in_sicilia"),
        ("Derby Palermo-Catania", "derby_palermo_catania"),
        ("Derby Catania-Siracusa", "derby_catania_siracusa"),
        ("Statistiche e record del Catania Football Club", "statistiche_e_record"),
        ("Catania Football Club", "monografia_istituzionale_catania_fc"),
    ]
    for title, fname in eventi_pages:
        rec = fetch_and_save_wiki_page(title, eventi_dir, fname)
        all_biblio.extend(rec.get("bibliography_extracted", []))

    # 2. STRUTTURE E STADI
    print("\n--- 2. Strutture e Impianti Sportivi ---")
    strutture_dir = DB_DIR / "strutture"
    strutture_pages = [
        ("Stadio Angelo Massimino", "stadio_angelo_massimino"),
        ("Torre del Grifo Village", "torre_del_grifo_village"),
    ]
    for title, fname in strutture_pages:
        rec = fetch_and_save_wiki_page(title, strutture_dir, fname)
        all_biblio.extend(rec.get("bibliography_extracted", []))

    # 3. SETTORI PARALLELI: CATANIA WOMEN E SETTORE GIOVANILE
    print("\n--- 3. Settori Paralleli (Catania Women e Giovanili) ---")
    settori_dir = DB_DIR / "settori_paralleli"
    settori_pages = [
        ("Calcio Femminile Jolly Catania", "catania_women_jolly_componibili_scudetto_1978"),
        ("Serie A 1978 (calcio femminile)", "campionato_femminile_scudetto_1978"),
    ]
    for title, fname in settori_pages:
        rec = fetch_and_save_wiki_page(title, settori_dir, fname)
        all_biblio.extend(rec.get("bibliography_extracted", []))

    # 4. TIFOSERIA, SIMBOLI E ARALDICA
    print("\n--- 4. Tifoseria, Identità e Araldica ---")
    tifoseria_dir = DB_DIR / "tifoseria_e_cultura"
    tifoseria_pages = [
        ("Tifoseria del Catania Football Club", "tifoseria_del_catania_ultras_curve"),
    ]
    for title, fname in tifoseria_pages:
        rec = fetch_and_save_wiki_page(title, tifoseria_dir, fname)
        all_biblio.extend(rec.get("bibliography_extracted", []))

    # 5. PRESIDENTI DEL CATANIA
    print("\n--- 5. Presidenti Storici del Catania ---")
    pres_dir = DB_DIR / "presidenti"
    pres_titles = get_category_member_titles("Categoria:Presidenti del Catania F.C.")
    for pt in pres_titles:
        rec = fetch_and_save_wiki_page(pt, pres_dir)
        all_biblio.extend(rec.get("bibliography_extracted", []))

    # 6. DIRIGENTI DEL CATANIA
    print("\n--- 6. Dirigenti del Catania ---")
    dir_dir = DB_DIR / "dirigenti"
    dir_titles = get_category_member_titles("Categoria:Dirigenti del Catania F.C.")
    for dt in dir_titles:
        rec = fetch_and_save_wiki_page(dt, dir_dir)
        all_biblio.extend(rec.get("bibliography_extracted", []))

    # 7. ALLENATORI DEL CATANIA (TUTTI I 120 TECNICI)
    print("\n--- 7. Allenatori Storici del Catania (120 Tecnici) ---")
    all_dir = DB_DIR / "allenatori"
    all_titles = get_category_member_titles("Categoria:Allenatori del Catania F.C.")
    print(f"Verifica/scaricamento {len(all_titles)} allenatori...")
    for idx, at in enumerate(all_titles, 1):
        rec = fetch_and_save_wiki_page(at, all_dir)
        all_biblio.extend(rec.get("bibliography_extracted", []))
        if idx % 20 == 0 or idx == len(all_titles):
            print(f"  Progresso allenatori: {idx}/{len(all_titles)}")

    # 8. BIBLIOGRAFIA E LETTERATURA COMPLETA
    print("\n--- 8. Consolidamento Bibliografia e Letteratura ---")
    biblio_dir = DB_DIR / "letteratura"
    biblio_dir.mkdir(parents=True, exist_ok=True)
    
    unique_biblio = []
    seen = set()
    for item in all_biblio:
        norm = re.sub(r"\s+", " ", item.strip().lower())
        if norm not in seen and len(norm) > 10:
            seen.add(norm)
            unique_biblio.append(item.strip())
            
    biblio_file = biblio_dir / "bibliografia_completa.json"
    with open(biblio_file, "w", encoding="utf-8") as f:
        json.dump(unique_biblio, f, ensure_ascii=False, indent=2)
        
    print(f"[OK] Salvate {len(unique_biblio)} opere bibliografiche e saggi storici unici in {biblio_file}")

    print("\n=======================================================")
    print("ESTRAZIONE DI TUTTO IL CONTESTO COMPLETATA CON SUCCESSO!")
    print(f"Tutti i dati sono disponibili in: {DB_DIR}")
    print("=======================================================")


if __name__ == "__main__":
    main()
