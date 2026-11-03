import os
import re
from collections import defaultdict
import yaml

CONTENT_DIR = "content"

# 1. Collect all existing slugs and aliases
existing_entities = set()
for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith(".md"):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, CONTENT_DIR).replace(os.sep, "/")
            slug = os.path.splitext(rel)[0]
            existing_entities.add(slug)
            existing_entities.add(os.path.basename(slug))
            
            # read aliases and title
            try:
                with open(full, "r", encoding="utf-8") as fp:
                    first_kb = fp.read(2048)
                m = re.search(r"^---\n(.*?)\n---\n", first_kb, re.DOTALL)
                if m:
                    fm = yaml.safe_load(m.group(1))
                    if isinstance(fm, dict):
                        aliases = fm.get("aliases", [])
                        if isinstance(aliases, list):
                            for a in aliases:
                                existing_entities.add(str(a).strip().lstrip("/"))
                                existing_entities.add(os.path.basename(str(a)))
                        title = fm.get("title", "")
                        if title:
                            existing_entities.add(title.lower())
            except Exception:
                pass

print(f"Total existing entity identifiers/aliases: {len(existing_entities)}")

# 2. Candidate entities to track (curated historical list of frequent recurring Catania figures/events + dynamic regex)
CANDIDATE_PATTERNS = [
    # Presidenti & Dirigenti
    ("Vittorio Emanuele Brusca", "Presidente S.S. Catania (1936-1940)"),
    ("Angelo Attaguile", "Presidente Calcio Catania (1987-1991)"),
    ("Grazia Codiglione", "Presidente Calcio Catania (1996-2000, vedova Massimino)"),
    ("Agatino Pesce", "Presidente Calcio Catania (1955-1958)"),
    ("Davide Franco", "Presidente del Cda Calcio Catania (2016-2020)"),
    ("Santi Quasimodo", "Presidente S.S. Catania (1929-1930)"),
    ("Ottavio Teghini", "Presidente A.F.C. Catania (1940-1943)"),
    ("Santi Manganaro Passanisi", "Presidente C.C. Catania (1946-1948)"),
    ("Lorenzo Fazio", "Presidente Calcio Catania (1949-1951)"),
    ("Arturo Michisanti", "Presidente Calcio Catania (1951-1954 e 1958-1959)"),
    ("Salvatore Coco", "Presidente Calcio Catania (1973-1974)"),
    ("Nicola Le Mura", "Amministratore Unico Calcio Catania SIGI (2020-2021)"),
    ("Gianluca Astorina", "Presidente Cda Calcio Catania (2020)"),
    ("Sergio Santagati", "Amministratore Unico Calcio Catania (2021-2022)"),
    ("Daniele Faggiano", "Direttore Sportivo Catania FC (2024-2026)"),
    ("Maurizio Pellegrino", "Calciatore, Allenatore e Direttore dell'Area Tecnica"),
    ("Christian Argurio", "Direttore Sportivo Calcio Catania"),
    
    # Allenatori & Tecnici
    ("Lajos Czeizler", "Allenatore ungherese della S.S. Catania (1932-1933)"),
    ("Piero Andreoli", "Allenatore della prima promozione in Serie A (1953-1954)"),
    ("Lino De Petrillo", "Allenatore della promozione in Serie B (1979-1980)"),
    ("Bruno Pace", "Allenatore del Calcio Catania (1986-1987)"),
    ("Angelo Sormani", "Allenatore del Calcio Catania (1989-1991)"),
    ("Gennaro Rambone", "Allenatore e personaggio vulcanico rossazzurro"),
    ("Giovanni Degni", "Allenatore A.F.C. Catania e C.C. Catania"),
    ("Fioravante Baldi", "Allenatore del Calcio Catania negli anni Cinquanta"),
    ("Dino Ballacci", "Allenatore del Catania (1966-1968)"),
    ("Mario Magnozzi", "Allenatore del Calcio Catania (1949-1950)"),
    ("Stanislao Klein", "Allenatore del Catania (1950)"),
    ("Gipo Poggi", "Allenatore del Calcio Catania (1956-1958)"),
    ("Giovanni Mei", "Allenatore del Calcio Catania (1996-1998)"),
    ("Francesco Baldini", "Allenatore del Catania nell'anno del fallimento (2021-2022)"),
    ("Pietro Colombati", "Allenatore A.F.C. Catania (1936-1938)"),
    ("György Orth", "Allenatore ungherese A.F.C. Catania (1939-1940)"),
    ("Achille Piccini", "Campione Olimpico 1936 e tecnico del Catania (1947-1948)"),
    ("József Bánás", "Allenatore ungherese del Catania (1948-1949)"),
    ("Rodolfo Brondi", "Allenatore del Catania (1951)"),
    ("Giulio Cappelli", "Allenatore del Catania (1952-1953)"),
    ("Carmelo Russo", "Allenatore del Calcio Catania (1988-1990)"),
    ("Berardo Frisoni", "Tecnico e giocatore dell'A.F.C. Catania (1942-1943)"),
    
    # Avvenimenti, Tornei & Partite Storiche
    ("Coppa Italia Serie C", "Competizione nazionale vinta dal Catania nel 2023-2024"),
    ("Coppa delle Alpi 1964", "Storica finale internazionale disputata dal Catania a Berna"),
    ("Torneo di Viareggio", "Storica competizione giovanile disputata dal Catania"),
    ("Spareggi di Roma 1983", "Trionfali spareggi promozione all'Olimpico contro Como e Cremonese"),
    ("Derby di Sicilia", "Rivalità regionale e stracittadina contro il Palermo"),
    ("Derby dello Stretto", "Rivalità storica e sportiva contro il Messina"),
    ("Clamoroso al Cibali", "Celeberrima espressione di Sandro Ciotti per Catania-Inter 2-0 (1961)"),
    ("Caso Scaramella 1955", "Retrocessione a tavolino del Catania in Serie B"),
    ("Caso Catania 2003", "Contenzioso giuridico che portò al blocco dei campionati e alla Serie B a 24 squadre"),
    ("Radiazione 1993", "Esclusione federale del Catania di Massimino e ripartenza dall'Eccellenza"),
    ("Treni del Gol 2015", "Inchiesta giudiziaria e retrocessione d'ufficio in Lega Pro"),
    ("Fallimento 2021", "Dichiarazione di fallimento del Calcio Catania S.p.A. e revoca della matricola 11700"),
    ("Invasione campo Padova 2024", "Disordini nella finale d'andata di Coppa Italia all'Euganeo"),
    ("Asta Marchio Matricola 11700", "Acquisizione dei beni immateriali e del logo storico da parte di Pelligra"),

    # Personaggi & Giornalisti
    ("Sandro Ciotti", "Radiocronista RAI, autore del conio 'Clamoroso al Cibali'"),
    ("Enrico Ameri", "Storico radiocronista RAI di Tutto il Calcio Minuto per Minuto"),
    ("Luigi Necco", "Storico inviato Rai da Napoli e Cibali di 90° Minuto"),
    ("Franco Zuccalà", "Giornalista e storico inviato sportivo Rai catanese"),
    ("Turi Ferro", "Grande attore catanese e appassionato tifoso rossazzurro"),
    ("Pippo Baudo", "Presentatore televisivo e storico sostenitore del Calcio Catania")
]

# 3. Scan all markdown files for occurrences
entity_mentions = defaultdict(set) # entity_name -> set of file_paths

for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith(".md"):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, CONTENT_DIR).replace(os.sep, "/")
            try:
                with open(full, "r", encoding="utf-8") as fp:
                    content = fp.read()
                
                # Check each candidate
                for name, desc in CANDIDATE_PATTERNS:
                    # Search name as word or wikilink
                    pattern = re.compile(r"\b" + re.escape(name) + r"\b", re.IGNORECASE)
                    if pattern.search(content):
                        entity_mentions[name].add(rel)
            except Exception:
                pass

# Rank candidates by number of distinct pages mentioning them
results = []
for name, desc in CANDIDATE_PATTERNS:
    pages = entity_mentions[name]
    count = len(pages)
    results.append({
        "name": name,
        "description": desc,
        "page_count": count,
        "sample_pages": sorted(list(pages))[:5]
    })

results.sort(key=lambda x: x["page_count"], reverse=True)

print(f"\n--- TOP 50 ENTITIES WITHOUT A DEDICATED PAGE ---")
for i, r in enumerate(results[:50], 1):
    print(f"{i:2d}. {r['name']} ({r['page_count']} schede) — {r['description']}")
