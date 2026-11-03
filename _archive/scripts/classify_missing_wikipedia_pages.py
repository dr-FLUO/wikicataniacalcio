"""
Classificazione e ranking di tutte le pagine presenti su Wikipedia ma non ancora sul nostro Wiki Catania Calcio.
Suddivisione nelle 4 categorie richieste:
1. Da pubblicare subito (Alta Priorità)
2. Media priorità
3. Bassa priorità
4. Non rilevanti
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
DB_DIR = BASE_DIR / "data" / "wikimedia_catania_db"

# 1. Raccogli tutti gli slug e alias esistenti nel nostro Vault
existing_slugs = set()
for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith(".md"):
            existing_slugs.add(f.replace(".md", "").lower())
            p = Path(root) / f
            raw = p.read_text(encoding="utf-8")
            m_slug = re.search(r"^slug:\s*(.*?)$", raw, re.M)
            if m_slug:
                existing_slugs.add(m_slug.group(1).split("/")[-1].lower())
            m_al = re.search(r"aliases:\s*\n((?:\s*-\s*.*?\n)+)", raw)
            if m_al:
                for line in m_al.group(1).splitlines():
                    al = line.strip("- ").strip("'\"").split("/")[-1].lower()
                    existing_slugs.add(al)

def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[àáâãäå]", "a", s)
    s = re.sub(r"[èéêë]", "e", s)
    s = re.sub(r"[ìíîï]", "i", s)
    s = re.sub(r"[òóôõö]", "o", s)
    s = re.sub(r"[ùúûü]", "u", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def has_sheet(name: str, wiki_url: str = "") -> bool:
    s = slugify(name)
    if s in existing_slugs:
        return True
    parts = s.split("-")
    # se cognome distintivo >= 4 lettere presente
    if len(parts) >= 2 and any(len(pt) >= 5 and pt in existing_slugs for pt in parts):
        return True
    if wiki_url:
        wiki_title = wiki_url.split("/wiki/")[-1].replace("_", "-").lower()
        if wiki_title in existing_slugs:
            return True
    return False

# 2. Carica Wikidata People
with open(DB_DIR / "wikidata_people.json", "r", encoding="utf-8") as f:
    people = json.load(f)

# 3. Carica Allenatori e Dirigenti estratti
allenatori = []
all_dir = DB_DIR / "allenatori"
if all_dir.exists():
    for f in all_dir.glob("*.json"):
        with open(f, "r", encoding="utf-8") as fp:
            allenatori.append(json.load(fp))

# 4. Raccogli eventi storici e incontri
eventi_incontri = [
    {"name": "Scandalo Scaramella (1955)", "type": "evento_giudiziario", "url": "https://it.wikipedia.org/wiki/Scandalo_Scaramella", "desc": "Caso di illecito sportivo che revocò la prima salvezza in Serie A retrocedendo il Catania in Serie B a tavolino"},
    {"name": "Spareggi Serie B 1982-1983 (Roma)", "type": "partita_storica", "url": "https://it.wikipedia.org/wiki/Serie_B_1982-1983#Spareggi_promozione", "desc": "Triangolare storico all'Olimpico di Roma con Como e Cremonese davanti a 40.000 catanesi"},
    {"name": "Derby Catania-Messina", "type": "derby", "url": "https://it.wikipedia.org/wiki/Derby_calcistici_in_Sicilia#Catania-Messina", "desc": "La storica rivalità dello Stretto e della Sicilia Orientale"},
    {"name": "Cinquanta volti per il Cibali (Murales Stadio)", "type": "monumento_cultura", "url": "https://it.wikipedia.org/wiki/Cinquanta_volti_per_il_Cibali", "desc": "Opera artistica monumentale con i 50 murales celebrativi della storia rossazzurra"},
    {"name": "Coppa delle Alpi 1964", "type": "torneo_internazionale", "url": "https://it.wikipedia.org/wiki/Coppa_delle_Alpi_1964", "desc": "La prima e unica finale europea/internazionale disputata dal Calcio Catania a Berna contro il Genoa"},
]

missing_high = []
missing_medium = []
missing_low = []
missing_not_relevant = []

# Analisi Eventi
for ev in eventi_incontri:
    s = slugify(ev["name"])
    if not has_sheet(ev["name"]):
        missing_high.append({
            "name": ev["name"],
            "category": "Eventi Storici & Tornei Internazionali",
            "reason": ev["desc"],
            "url": ev["url"]
        })

# Analisi Tesserati Wikidata
for p in people:
    name = p["name"]
    url = p.get("it_wiki_article", "")
    if has_sheet(name, url):
        continue
        
    pos = ", ".join(p.get("positions", [])) or "Calciatore"
    bdate = p.get("birth_date", "")[:4]
    country = p.get("country", "")
    
    # Classificazione in base al rilievo storico enciclopedico
    # Rilevanza Alta: presenze in Serie A, Campioni o figure con voce Wikipedia corposa
    high_priority_names = [
        "Bruno Pizzul", "Alexis Rolín", "Nicola D'Ottavio", "Babú", "Generoso Rossi",
        "Dante Mircoli", "Tomáš Košický", "Norbert Gyömbér", "Marco Romano", "Gilberto Pogliano",
        "Benedetto Stella", "Guilherme Raymundo do Prado", "Paolo Dall'Oro", "Renato Miglioli",
        "Pietro Podestà", "Carlo Ravizzoli", "Gyula Mikossy", "Giulio Rossi", "Aboubacar Sankharé",
        "Pier Luigi Nicoli", "Christian Kanyengele", "Nello Tedeschini"
    ]
    
    if any(hp.lower() in name.lower() for hp in high_priority_names):
        missing_high.append({
            "name": name,
            "category": f"Tesserati — {pos} ({bdate}, {country})",
            "reason": "Protagonista in Serie A o pioniere storico con oltre 30 presenze o record societari",
            "url": url or f"https://www.wikidata.org/wiki/{p.get('qid')}"
        })
    elif url:
        # Se ha una pagina su Wikipedia in italiano, è di Media Priorità
        missing_medium.append({
            "name": name,
            "category": f"Tesserati — {pos} ({bdate}, {country})",
            "reason": "Calciatore/Tecnico professionista con voce autonoma su Wikipedia Italia",
            "url": url
        })
    elif p.get("image_url"):
        # Ha immagine su Commons ma non pagina it.wiki autonoma
        missing_low.append({
            "name": name,
            "category": f"Tesserati — {pos} ({bdate})",
            "reason": "Presenze documentate e ritratto presente su Commons/Wikidata",
            "url": f"https://www.wikidata.org/wiki/{p.get('qid')}"
        })
    else:
        # Pochi dati, passaggi brevissimi o omonimie
        missing_not_relevant.append({
            "name": name,
            "category": "Figure Minori / Omonimie",
            "reason": "Singole apparizioni giovanili o dati anagrafici non verificabili da fonti primarie",
            "url": f"https://www.wikidata.org/wiki/{p.get('qid')}"
        })

report = {
    "da_pubblicare_subito": missing_high,
    "media_priorita": missing_medium[:50],  # top 50
    "bassa_priorita": missing_low[:40],
    "non_rilevanti": missing_not_relevant[:20],
    "counts": {
        "alta": len(missing_high),
        "media": len(missing_medium),
        "bassa": len(missing_low),
        "non_rilevante": len(missing_not_relevant)
    }
}

out_file = DB_DIR / "backlog_pagine_mancanti_wikipedia.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"=== CLASSIFICAZIONE COMPLETATA ===")
print(f" - Da pubblicare subito (Alta priorità) : {report['counts']['alta']}")
print(f" - Media priorità                       : {report['counts']['media']}")
print(f" - Bassa priorità                       : {report['counts']['bassa']}")
print(f" - Non rilevanti                        : {report['counts']['non_rilevante']}")
