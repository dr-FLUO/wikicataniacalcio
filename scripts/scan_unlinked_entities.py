import os
import re
import json
from collections import defaultdict, Counter

CONTENT_DIR = "content"

# 1. Indicizzazione di tutte le entità già dotate di pagina o alias nel vault
existing_entities = set()
existing_titles = {}
all_md_files = []

for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if not f.endswith(".md"):
            continue
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, CONTENT_DIR).replace(os.sep, "/")
        slug = os.path.splitext(rel_path)[0]
        base_name = os.path.splitext(f)[0]
        
        all_md_files.append((slug, full_path))
        existing_entities.add(slug.lower())
        existing_entities.add(base_name.lower())
        existing_entities.add(base_name.replace("-", " ").lower())
        
        try:
            with open(full_path, "r", encoding="utf-8-sig") as fp:
                txt = fp.read()
            m = re.search(r"^---\r?\n(.*?)\r?\n---\r?\n", txt, re.DOTALL)
            if m:
                fm_raw = m.group(1)
                mt = re.search(r"^title:\s*(.*?)$", fm_raw, re.M)
                if mt:
                    clean_t = mt.group(1).strip("\"' ").lower()
                    existing_entities.add(clean_t)
                    existing_titles[slug] = clean_t
                ma = re.search(r"aliases:\s*\n((?:\s*-\s*.*?\r?\n)+)", fm_raw)
                if ma:
                    for line in ma.group(1).splitlines():
                        al = line.strip("- \"'").lower()
                        existing_entities.add(al)
                        existing_entities.add(al.split("/")[-1])
                        existing_entities.add(al.split("/")[-1].replace("-", " "))
        except Exception:
            pass

print(f"Indicizzate {len(existing_entities)} entità/alias/titoli già presenti nel vault.")
print(f"File totali nel vault: {len(all_md_files)}")

# 2. Stopwords ed esclusioni generiche del linguaggio calcistico/giornalistico
STOPWORDS = {
    "catania", "calcio catania", "rossazzurri", "rossazzurro", "rossazzurra", "etnei", "etnea",
    "serie a", "serie b", "serie c", "serie c1", "serie c2", "serie d", "prima divisione",
    "seconda divisione", "terza divisione", "campionato", "coppa italia", "coppa italia serie c",
    "girone", "girone a", "girone b", "girone c", "girone d", "girone e", "girone f", "girone g", "girone h", "girone i",
    "play-off", "play-out", "spareggio", "spareggi", "andata", "ritorno", "derby", "derby di sicilia",
    "figc", "lega calcio", "lega pro", "uefa", "fifa", "coni", "tar", "consiglio di stato",
    "italia", "roma", "milano", "torino", "palermo", "messina", "napoli",
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
    "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica",
    "primo tempo", "secondo tempo", "tempi supplementari", "calci di rigore", "rigore", "autogol",
    "ammonizione", "espulsione", "arbitro", "guardalinee", "stadio", "campo", "trasferta", "casa",
    "classifica", "tabellino", "formazione", "rosa", "allenatore", "presidente", "direttore", "dirigente",
    "curva nord", "curva sud", "tribuna a", "tribuna b", "gradinata", "settore ospiti",
    "stadio angelo massimino", "stadio cibali", "cibali", "torre del grifo", "torre del grifo village",
    "fonte", "fonti", "note", "riferimenti", "bibliografia", "collegamenti esterni",
    "almanacco illustrato del calcio", "la gazzetta dello sport", "corriere dello sport", "tuttosport", "la sicilia",
    "wiki calcio catania", "tutto il catania minuto per minuto", "geo edizioni",
    "società", "stagione", "archivio", "dossier", "dati", "statistiche", "cronistoria",
    "punti", "reti", "gol", "presenze", "vittorie", "pareggi", "sconfitte", "differenza reti",
    "minuto", "minuti", "marcatore", "marcatori", "titolari", "panchina", "sostituzioni",
    "squadra", "club", "matricola", "fallimento", "radiazione", "ripescaggio", "promozione", "retrocessione",
    "calciatori", "allenatori", "presidenti", "dirigenti", "capitano", "vice capitano"
}

# 3. Pattern specifici per estrarre entità non linkate
# a) Figure istituzionali nei metadati o nel testo (Presidente, Allenatore, Direttore)
pattern_pres = re.compile(r"(?:Presidente|Pres\.|Patron|Proprietario):\s*([A-ZÀ-Ú][a-zA-ZÀ-ÿ\s\.\-']{3,35})", re.I)
pattern_all = re.compile(r"(?:Allenatore|All\.|Tecnico|Mister):\s*([A-ZÀ-Ú][a-zA-ZÀ-ÿ\s\.\-']{3,35})", re.I)
pattern_dir = re.compile(r"(?:Direttore Sportivo|Direttore Generale|D\.S\.|D\.G\.|Amministratore Delegato|A\.D\.):\s*([A-ZÀ-Ú][a-zA-ZÀ-ÿ\s\.\-']{3,35})", re.I)
pattern_arb = re.compile(r"(?:Arbitro|Direttore di gara):\s*([A-ZÀ-Ú][a-zA-ZÀ-ÿ\s\.\-']{3,35})", re.I)

# b) Entità messe in risalto con grassetto: **Nome Cognome** o **Entità**
pattern_bold = re.compile(r"\*\*([A-ZÀ-Ú][a-zA-ZÀ-ÿ0-9\s\.\-']{3,45})\*\*")

# c) Nomi propri di due o tre parole con iniziale maiuscola
pattern_capitalized = re.compile(r"\b([A-ZÀ-Ú][a-zà-ÿ]+(?:\s+[A-ZÀ-Ú][a-zà-ÿ]+){1,2})\b")

# Mappa per contare le citazioni
entity_counts = Counter()
entity_files = defaultdict(set)
entity_categories = defaultdict(set)

def clean_name(n):
    n = re.sub(r"[,\(\)\[\]\|\"'\*]", "", n).strip()
    # Rimuovi eventuali prefissi/suffissi
    n = re.sub(r"^(dott\.|avv\.|ing\.|cav\.|sig\.)\s+", "", n, flags=re.I).strip()
    return n

def is_valid_candidate(candidate):
    low = candidate.lower()
    if len(candidate) < 4:
        return False
    if low in STOPWORDS:
        return False
    if any(low == stop or low.startswith(stop + " ") or low.endswith(" " + stop) for stop in ["serie", "girone", "coppa", "almanacco"]):
        return False
    # Escludi se già registrato nel vault
    slug_cand = candidate.lower().replace(" ", "-")
    if low in existing_entities or slug_cand in existing_entities:
        return False
    # Escludi se corrisponde a parti banali
    words = candidate.split()
    if len(words) < 2 and candidate not in ["Giarre", "Acireale", "Siracusa", "Trapani", "Licata", "Paternò", "Enna", "Ragusa", "Marsala", "Nissa", "Vittoria", "Leonanzio", "Massese"]:
        return False
    return True

print("Scansione in corso su tutti i file del vault...")

for slug, full_path in all_md_files:
    try:
        with open(full_path, "r", encoding="utf-8-sig") as fp:
            text = fp.read()
            
        # Rimuovi frontmatter
        text = re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", text, flags=re.DOTALL)
        # Rimuovi link markdown e wikilink per non contare cose già linkate
        clean_text = re.sub(r"\[\[.*?\]\]", "", text)
        clean_text = re.sub(r"\[.*?\]\(.*?\)", "", clean_text)
        clean_text = re.sub(r"`.*?`", "", clean_text)
        
        # 1. Cerca Presidenti
        for match in pattern_pres.finditer(clean_text):
            name = clean_name(match.group(1))
            if is_valid_candidate(name):
                entity_counts[name] += 1
                entity_files[name].add(slug)
                entity_categories[name].add("Presidenti / Proprietà")

        # 2. Cerca Dirigenti
        for match in pattern_dir.finditer(clean_text):
            name = clean_name(match.group(1))
            if is_valid_candidate(name):
                entity_counts[name] += 1
                entity_files[name].add(slug)
                entity_categories[name].add("Dirigenti / Area Tecnica")

        # 3. Cerca Allenatori citati
        for match in pattern_all.finditer(clean_text):
            name = clean_name(match.group(1))
            if is_valid_candidate(name):
                entity_counts[name] += 1
                entity_files[name].add(slug)
                entity_categories[name].add("Allenatori")

        # 4. Cerca Arbitri
        for match in pattern_arb.finditer(clean_text):
            name = clean_name(match.group(1))
            if is_valid_candidate(name):
                entity_counts[name] += 1
                entity_files[name].add(slug)
                entity_categories[name].add("Arbitri storici")

        # 5. Cerca entità marcate in grassetto
        for match in pattern_bold.finditer(clean_text):
            name = clean_name(match.group(1))
            if is_valid_candidate(name):
                entity_counts[name] += 1
                entity_files[name].add(slug)
                if not entity_categories[name]:
                    entity_categories[name].add("Entità in rilievo / Eventi")

        # 6. Cerca nomi propri ricorrenti con almeno 2 parole maiuscole
        for match in pattern_capitalized.finditer(clean_text):
            name = clean_name(match.group(1))
            if is_valid_candidate(name):
                entity_counts[name] += 1
                entity_files[name].add(slug)

    except Exception as e:
        pass

# Salva e raggruppa i risultati
results = []
for entity, count in entity_counts.items():
    file_count = len(entity_files[entity])
    if file_count >= 2 or count >= 3: # Minimo 2 file o 3 citazioni
        cat = list(entity_categories[entity]) if entity in entity_categories else ["Personaggio / Entità"]
        results.append({
            "name": entity,
            "total_mentions": count,
            "distinct_pages": file_count,
            "categories": cat,
            "sample_pages": list(entity_files[entity])[:5]
        })

results.sort(key=lambda x: (x["distinct_pages"], x["total_mentions"]), reverse=True)

with open("data_unlinked_entities.json", "w", encoding="utf-8") as fp:
    json.dump(results, fp, indent=2, ensure_ascii=False)

print(f"Scansione completata. Trovate {len(results)} entità ricorrenti non ancora dotate di pagina.")
print("\nTop 30 entità più citate senza pagina:")
for r in results[:30]:
    cats = ", ".join(r["categories"])
    print(f"  - {r['name']} ({r['distinct_pages']} pagine, {r['total_mentions']} citazioni) [{cats}]")
