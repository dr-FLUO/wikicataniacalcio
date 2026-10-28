import os
import glob
import re
import json
import yaml
import unicodedata

TESSERATI_DIR = "content/03-tesserati"
WIKIDATA_FILE = "data/wikimedia_catania_db/wikidata_people.json"
PLAYERS_FILE = "data/calciocatania_all_players.json"
DETAILS_FILE = "data/matched_players_detail.json"

def normalize_ascii(s):
    if not s:
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(s)) if unicodedata.category(c) != 'Mn').lower().strip()

def run_cycle2():
    print("=== AVVIO CICLO 2: ARCHIVIO TESSERATI & MONOGRAFIE ===")
    
    # Load reference databases
    wikidata = []
    if os.path.exists(WIKIDATA_FILE):
        with open(WIKIDATA_FILE, "r", encoding="utf-8") as f:
            wikidata = json.load(f)
    print(f"Caricati {len(wikidata)} profili Wikidata.")

    players_db = []
    if os.path.exists(PLAYERS_FILE):
        with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
            players_db = json.load(f)
    print(f"Caricati {len(players_db)} profili CalcioCatania.")

    details_db = []
    if os.path.exists(DETAILS_FILE):
        with open(DETAILS_FILE, "r", encoding="utf-8") as f:
            details_db = json.load(f)
    print(f"Caricati {len(details_db)} profili dettagliati.")

    # Index reference DBs by normalized name
    wiki_by_name = {}
    for p in wikidata:
        norm = normalize_ascii(p.get("name", ""))
        if norm:
            wiki_by_name[norm] = p

    players_by_name = {}
    for p in players_db:
        norm = normalize_ascii(p.get("name", ""))
        if norm:
            players_by_name[norm] = p

    files = glob.glob(f"{TESSERATI_DIR}/**/*.md", recursive=True)
    report = {
        "total_files": 0,
        "index_files": 0,
        "tesserati_checked": 0,
        "enriched_wikidata": 0,
        "enriched_players_db": 0,
        "slugs_fixed": 0,
        "aliases_added": 0
    }

    for fpath in files:
        report["total_files"] += 1
        if fpath.endswith("index.md"):
            report["index_files"] += 1
            continue

        report["tesserati_checked"] += 1

        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()

        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        fm_text = parts[1]
        body = parts[2]

        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception as e:
            print(f"Error parsing YAML in {fpath}: {e}")
            continue

        changed = False

        # 1. Correct Slug to match file location
        rel_path = os.path.relpath(fpath, "content")
        expected_slug = os.path.splitext(rel_path)[0].replace("\\", "/")
        if fm.get("slug") != expected_slug:
            fm["slug"] = expected_slug
            changed = True
            report["slugs_fixed"] += 1

        # 2. Add Standard Aliases so links work from anywhere
        filename_base = os.path.splitext(os.path.basename(fpath))[0]
        aliases = fm.get("aliases", [])
        if not isinstance(aliases, list):
            aliases = [aliases] if aliases else []

        standard_aliases = [
            filename_base,
            f"tesserati/{filename_base}",
            f"calciatori/{filename_base}" if "calciatori" in expected_slug else f"allenatori/{filename_base}"
        ]

        # Add if not present
        existing_set = set(aliases)
        for sa in standard_aliases:
            if sa not in existing_set and sa != expected_slug:
                aliases.append(sa)
                existing_set.add(sa)
                changed = True
                report["aliases_added"] += 1

        fm["aliases"] = aliases

        # 3. Extract player name
        title = fm.get("title", "")
        # Clean title to get name
        raw_name = title.split("—")[0].split("-")[0].split("(")[0].strip()
        if not raw_name or len(raw_name) < 2:
            raw_name = filename_base.replace("-", " ").title()

        norm_name = normalize_ascii(raw_name)

        # 4. Cross-check with Wikidata
        w_match = wiki_by_name.get(norm_name)
        if w_match:
            if not fm.get("birth_date") and w_match.get("birth_date"):
                fm["birth_date"] = str(w_match["birth_date"])
                changed = True
                report["enriched_wikidata"] += 1
            if not fm.get("birth_place") and w_match.get("birth_place"):
                fm["birth_place"] = str(w_match["birth_place"])
                changed = True
            if not fm.get("citizenship") and w_match.get("country"):
                fm["citizenship"] = str(w_match["country"])
                changed = True

        # 5. Cross-check with CalcioCatania DB
        p_match = players_by_name.get(norm_name)
        if p_match:
            cur_apps = fm.get("total_appearances", 0) or 0
            db_apps = p_match.get("appearances", 0) or 0
            if (not cur_apps or cur_apps == 0) and db_apps > 0:
                fm["total_appearances"] = int(db_apps)
                changed = True
                report["enriched_players_db"] += 1

            cur_seasons = fm.get("seasons_count", 0) or 0
            db_seasons = p_match.get("seasons_count", 0) or 0
            if (not cur_seasons or cur_seasons == 0) and db_seasons > 0:
                fm["seasons_count"] = int(db_seasons)
                changed = True

            if not fm.get("role") and p_match.get("role"):
                fm["role"] = str(p_match["role"])
                changed = True

        # Save back if updated
        if changed:
            new_fm_str = yaml.dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
            new_content = f"---\n{new_fm_str}---\n{body}"
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(new_content)

    print("=== REPORT CICLO 2: TESSERATI ===")
    print(f"File totali analizzati: {report['total_files']}")
    print(f"Tesserati verificati: {report['tesserati_checked']}")
    print(f"Slug rettificati e riallineati: {report['slugs_fixed']}")
    print(f"Alias di compatibilità generati: {report['aliases_added']}")
    print(f"Profili arricchiti con dati Wikidata: {report['enriched_wikidata']}")
    print(f"Presenze/statistiche sincronizzate da CalcioCatania DB: {report['enriched_players_db']}")

if __name__ == "__main__":
    run_cycle2()
