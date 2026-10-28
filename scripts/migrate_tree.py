import os
import re
import shutil
import yaml

CONTENT_DIR = "content"

HISTORIC_LEGENDS = {
    "giuseppe-mascara", "gionatha-spinesi", "alejandro-gomez", "gonzalo-bergessio",
    "marco-biagianti", "mariano-izco", "davide-baiocco", "adrian-ricchiuti",
    "francesco-lodi", "nicolas-spolli", "marias-silvestre", "matias-silvestre",
    "pablo-alvarez", "cristian-llama", "mariano-andujar", "jorge-martinez",
    "adelmo-prenna", "giuseppe-vavassori", "claudio-ciceri", "loris-boni",
    "amedeo-biavati", "mario-miltone", "nicolo-nicolosi", "giorgio-mastropasqua",
    "roberto-sorrentino", "nicola-fusaro", "guido-biondi", "horst-szymaniak",
    "sidney-cunha-cinesinho", "alessandro-ambrosi", "gianvito-plasmati",
    "giuseppe-baronchelli", "loris-del-nevo", "carlo-borghi", "aldo-cantarutti",
    "angelo-pereni", "damiano-morra", "michele-fini", "gennaro-delvecchio",
    "orazio-russo", "lorenzo-stovini", "giuseppe-mascara"
}

DIRIGENTI = {
    "pietro-lo-monaco.md", "sergio-gasparin.md", "vincenzo-grella.md", "daniele-faggiano.md"
}

EPOCHE_FILES = {
    "1929-ss-catania.md", "1946-club-calcio-catania.md", "1967-calcio-catania-spa-massimino.md",
    "2000-era-gaucci.md", "2004-era-pulvirenti.md", "2020-sigi-e-fallimento.md",
    "2022-pelligra-catania-fc.md", "catania-degli-argentini.md"
}

STADIO_MASSIMINO_FILES = {
    "angelo-massimino.md", "cibalino.md", "tribuna-stampa-stefania-sberna.md"
}

CENTRI_SPORTIVI_FILES = {
    "torre-del-grifo-village.md", "campo-comunale-nesima.md"
}

CAMPI_STORICI_FILES = {
    "piazza-esposizione.md", "campo-due-obelischi.md"
}

ARALDICA_FILES = {
    "simbologia-colori-scudetti.md", "loghi-storici-liotru.md", "acquisizione-marchio-storico-2026.md"
}

SPONSOR_FILES = {
    "sponsor-commerciali.md", "sponsor-tecnici-e-commerciali.md"
}

def get_alpha_cluster(filename):
    # Determine cluster from first letter of basename
    base = filename.lower()
    ch = base[0] if base[0].isalpha() else 'a'
    if ch in 'abc':
        return 'a-c'
    elif ch in 'def':
        return 'd-f'
    elif ch in 'ghijkl':
        return 'g-l'
    elif ch in 'mno':
        return 'm-o'
    elif ch in 'pqr':
        return 'p-r'
    else:
        return 's-z'

def determine_new_path(rel_path):
    parts = rel_path.split(os.sep)
    top = parts[0]
    
    # 0. Root files and assets
    if len(parts) == 1:
        return rel_path # stay at root
    if top == "assets":
        return rel_path # stay at assets
        
    # 1. 01-societa
    if top == "societa":
        sub = parts[1]
        if sub == "index.md":
            return os.path.join("01-societa", "index.md")
        elif sub == "matricola-11700.md":
            return os.path.join("01-societa", "matricola-11700.md")
        elif sub in EPOCHE_FILES:
            return os.path.join("01-societa", "epoche", sub)
        elif sub == "presidenti":
            filename = parts[2]
            if filename in DIRIGENTI:
                return os.path.join("01-societa", "dirigenti", filename)
            else:
                return os.path.join("01-societa", "presidenti", filename)
        elif sub == "dirigenti":
            return os.path.join("01-societa", "dirigenti", parts[2])
        else:
            return os.path.join("01-societa", *parts[1:])
            
    # vicende-legali -> 01-societa/vicende-legali
    if top == "vicende-legali":
        return os.path.join("01-societa", "vicende-legali", *parts[1:])
        
    # 2. 02-cronistoria
    if top == "stagioni":
        return os.path.join("02-cronistoria", "stagioni", *parts[1:])
    if top == "partite":
        return os.path.join("02-cronistoria", "partite-storiche", *parts[1:])
        
    # 3. 03-tesserati
    if top == "tesserati":
        sub = parts[1]
        if sub == "index.md":
            return os.path.join("03-tesserati", "index.md")
        elif sub == "allenatori":
            return os.path.join("03-tesserati", "allenatori", *parts[2:])
        elif sub == "calciatori":
            filename = parts[2]
            slug_base = os.path.splitext(filename)[0]
            # Check frontmatter if current_squad
            full_orig = os.path.join(CONTENT_DIR, rel_path)
            is_current = False
            try:
                with open(full_orig, "r", encoding="utf-8") as fp:
                    first_kb = fp.read(1500)
                if "current_squad: true" in first_kb:
                    is_current = True
            except Exception:
                pass
                
            if is_current:
                return os.path.join("03-tesserati", "calciatori", "rosa-attuale", filename)
            elif slug_base in HISTORIC_LEGENDS:
                return os.path.join("03-tesserati", "calciatori", "storici", filename)
            else:
                cluster = get_alpha_cluster(filename)
                return os.path.join("03-tesserati", "calciatori", "archivio", cluster, filename)
        else:
            return os.path.join("03-tesserati", *parts[1:])
            
    # 4. 04-strutture
    if top == "stadio":
        sub = parts[1]
        if sub == "index.md":
            return os.path.join("04-strutture", "index.md")
        elif sub in STADIO_MASSIMINO_FILES:
            return os.path.join("04-strutture", "stadio-massimino", sub)
        elif sub in CENTRI_SPORTIVI_FILES:
            return os.path.join("04-strutture", "centri-sportivi", sub)
        elif sub in CAMPI_STORICI_FILES:
            return os.path.join("04-strutture", "campi-storici", sub)
        else:
            return os.path.join("04-strutture", "stadio-massimino", sub)
            
    # 5. 05-identita-e-simboli
    if top == "maglie":
        sub = parts[1]
        if sub == "index.md":
            return os.path.join("05-identita-e-simboli", "index.md")
        elif sub in ARALDICA_FILES:
            return os.path.join("05-identita-e-simboli", "araldica-e-scudetti", sub)
        elif sub in SPONSOR_FILES:
            return os.path.join("05-identita-e-simboli", "sponsor", sub)
        else:
            return os.path.join("05-identita-e-simboli", "maglie", sub)
            
    # 6. 06-tifoseria-e-cultura
    if top == "tifoseria":
        sub = parts[1]
        if sub == "index.md":
            return os.path.join("06-tifoseria-e-cultura", "index.md")
        elif sub in ("curva-nord", "curva-sud"):
            return os.path.join("06-tifoseria-e-cultura", "curve", sub, *parts[2:])
        elif sub == "eventi":
            return os.path.join("06-tifoseria-e-cultura", "eventi-e-giustizia", *parts[2:])
        elif sub == "biografie":
            return os.path.join("06-tifoseria-e-cultura", "biografie", *parts[2:])
        elif sub in ("gemellaggi", "rivalita"):
            return os.path.join("06-tifoseria-e-cultura", "relazioni", sub, *parts[2:])
        else:
            return os.path.join("06-tifoseria-e-cultura", *parts[1:])
            
    # 7. 07-media-e-comunicazione
    if top == "media":
        sub = parts[1]
        if sub == "index.md":
            return os.path.join("07-media-e-comunicazione", "index.md")
        elif sub == "testate":
            return os.path.join("07-media-e-comunicazione", "testate", *parts[2:])
        elif sub == "giornalisti":
            return os.path.join("07-media-e-comunicazione", "firme-e-voci", *parts[2:])
        else:
            return os.path.join("07-media-e-comunicazione", *parts[1:])
            
    # 8. 08-settori-paralleli
    if top == "giovanili":
        return os.path.join("08-settori-paralleli", "giovanili", *parts[1:])
    if top == "women":
        return os.path.join("08-settori-paralleli", "women", *parts[1:])
        
    return rel_path

def migrate():
    # 1. Collect all files to move
    all_files = []
    for root, _, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith(".md"):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, CONTENT_DIR)
                all_files.append((full, rel))
                
    moves = []
    for full, rel in all_files:
        new_rel = determine_new_path(rel)
        if new_rel != rel:
            moves.append((full, rel, new_rel))
            
    print(f"Total markdown files to migrate: {len(moves)}")
    
    # 2. Execute migration with alias injection & relative depth update
    for full, rel, new_rel in moves:
        old_slug = os.path.splitext(rel.replace(os.sep, "/"))[0]
        new_slug = os.path.splitext(new_rel.replace(os.sep, "/"))[0]
        new_full = os.path.join(CONTENT_DIR, new_rel)
        
        with open(full, "r", encoding="utf-8") as fp:
            text = fp.read()
            
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1]
            body = parts[2]
            try:
                fm = yaml.safe_load(raw_fm) or {}
            except Exception:
                fm = {}
                
            # Update slug
            fm["slug"] = new_slug
            
            # Ensure aliases list contains old_slug
            aliases = fm.get("aliases", [])
            if not isinstance(aliases, list):
                aliases = [aliases] if aliases else []
            if old_slug not in aliases and old_slug != new_slug:
                aliases.append(old_slug)
            fm["aliases"] = aliases
            
            # Adjust relative image URLs to match new nesting depth
            # Depth from new_rel directory to CONTENT_DIR
            new_dir = os.path.dirname(new_rel)
            depth = len(new_dir.split(os.sep)) if new_dir else 0
            rel_prefix = "../" * depth if depth > 0 else "./"
            
            # Replace any ../*assets/images/ with new exact relative prefix
            new_body = re.sub(r"(\!\[.*?\]\()(?:\.\./)*assets/images/", r"\g<1>" + rel_prefix + "assets/images/", body)
            
            new_fm_str = yaml.dump(fm, allow_unicode=True, sort_keys=False)
            new_text = f"---\n{new_fm_str}---\n{new_body}"
        else:
            new_text = text
            
        # Create target dir
        os.makedirs(os.path.dirname(new_full), exist_ok=True)
        with open(new_full, "w", encoding="utf-8") as fp:
            fp.write(new_text)
            
        # Remove old file
        os.remove(full)
        
    # 3. Clean up empty old directories
    old_top_dirs = ["societa", "vicende-legali", "stagioni", "partite", "tesserati", "stadio", "maglie", "tifoseria", "media", "giovanili", "women"]
    for d in old_top_dirs:
        p = os.path.join(CONTENT_DIR, d)
        if os.path.exists(p):
            shutil.rmtree(p, ignore_errors=True)
            print(f"Removed old directory tree: {p}")
            
    # 4. Create missing macro hubs if not present
    # Hub 02: Cronistoria
    hub_02 = os.path.join(CONTENT_DIR, "02-cronistoria", "index.md")
    if not os.path.exists(hub_02):
        with open(hub_02, "w", encoding="utf-8") as fp:
            fp.write("""---
title: "02 · Cronistoria — Stagioni Ufficiali e Partite Storiche (1929–2027)"
description: "Archivio cronologico completo del Calcio Catania: tutte le stagioni agonistiche con quadratura algebrica federale e i dossier monografici dei match leggendari."
slug: "02-cronistoria/index"
aliases:
  - "cronistoria"
  - "cronistoria/index"
entity_type: "section_index"
status: "verified"
last_verified_date: "2026-10-28"
tags:
  - "cronistoria"
  - "stagioni"
  - "partite"
---

# Cronistoria Rossazzurra (1929–2027)

Benvenuti nella sezione **Cronistoria** di Wiki Catania Calcio. In questa sezione sono archiviati in ordine cronologico tutti i campionati disputati dal club etneo dalla fondazione a oggi, oltre ai dossier approfonditi delle partite leggendarie.

## Sezioni dell'Archivio
* [[02-cronistoria/stagioni/index|Stagioni Ufficiali (1929–2027)]] — Tabelle algebriche, tabellini, capocannonieri e cronache per ogni annata.
* [[02-cronistoria/partite-storiche/index|Partite Storiche]] — Dalle vittorie sul Grande Torino e sull'Inter ("Clamoroso al Cibali") agli spareggi dell'Olimpico e al derby di Palermo 0-4.
""")
        print("Created 02-cronistoria/index.md")

    # Hub 08: Settori Paralleli
    hub_08 = os.path.join(CONTENT_DIR, "08-settori-paralleli", "index.md")
    if not os.path.exists(hub_08):
        with open(hub_08, "w", encoding="utf-8") as fp:
            fp.write("""---
title: "08 · Settori Paralleli — Giovanili, Primavera e Catania Women"
description: "Dossier e archivi dedicati al Settore Giovanile rossazzurro, al Torneo di Viareggio e alla squadra femminile Catania Women (Scudetto 1978 Jolly Componibili)."
slug: "08-settori-paralleli/index"
aliases:
  - "settori-paralleli"
  - "settori-paralleli/index"
entity_type: "section_index"
status: "verified"
last_verified_date: "2026-10-28"
tags:
  - "giovanili"
  - "women"
  - "primavera"
---

# Settori Paralleli: Giovanili & Catania Women

Questa sezione documenta la continuità sportiva del Calcio Catania al di fuori della prima squadra maschile:
* [[08-settori-paralleli/giovanili/index|Settore Giovanile & Primavera]] — Storia del vivaio etneo, dai talenti storici alle partecipazioni al Torneo di Viareggio e alle strutture di Nesima e Torre del Grifo.
* [[08-settori-paralleli/women/index|Catania Women & Calcio Femminile]] — La storica conquista dello Scudetto 1978 da parte della Jolly Componibili Catania e l'attività del dipartimento femminile contemporaneo.
""")
        print("Created 08-settori-paralleli/index.md")

    print("\n[SUCCESS] Alberatura vault migrata con successo in 8 macro-sezioni!")

if __name__ == "__main__":
    migrate()
