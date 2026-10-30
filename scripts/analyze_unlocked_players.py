import csv, unicodedata, re, json
from pathlib import Path
import yaml

def normalize(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.lower().replace('', 'c').replace('', 'o').replace('', 'ss')
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

csv_path = Path("user-content/transfermarket-scraper/dati_catania/storico_giocatori_statistiche.csv")
tm_names = set()
with open(csv_path, encoding='utf-8', errors='replace') as f:
    for r in csv.DictReader(f):
        g = r.get('Giocatore', '').strip()
        if g:
            tm_names.add(g)

print(f"Giocatori unici nel CSV: {len(tm_names)}")

reg = json.loads(Path('locks/locked_entities.json').read_text(encoding='utf-8'))
all_calciatori = [p for p in Path('content/03-tesserati/calciatori').rglob('*.md') if p.name != 'index.md']
unlocked = [p for p in all_calciatori if str(p.as_posix()) not in reg]

found_fuzzy = []
not_in_tm = []

for p in unlocked:
    stem = p.stem
    norm_stem = normalize(stem)
    
    # Prova a leggere title o nome dal file
    title = ""
    try:
        txt = p.read_text(encoding="utf-8")
        if txt.startswith("---"):
            fm = yaml.safe_load(txt.split("---", 2)[1]) or {}
            title = fm.get("title", "")
    except:
        pass
        
    norm_title = normalize(title)
    
    # Cerca nel CSV per cognome o somiglianza
    match = None
    for tm_n in tm_names:
        norm_tm = normalize(tm_n)
        # Se uno contiene l'altro
        if norm_tm == norm_stem or norm_tm in norm_stem or norm_stem in norm_tm:
            match = tm_n
            break
        # O se il cognome principale combacia
        tm_parts = tm_n.split()
        stem_parts = stem.split("-")
        if len(tm_parts) >= 2 and len(stem_parts) >= 2:
            # confronta cognome
            if normalize(tm_parts[-1]) == normalize(stem_parts[-1]) and (normalize(tm_parts[0])[:3] == normalize(stem_parts[0])[:3] or len(tm_parts[0]) < 3):
                match = tm_n
                break
                
    if match:
        found_fuzzy.append((p.as_posix(), match))
    else:
        not_in_tm.append((p.as_posix(), stem, title[:40]))

print(f"\n[+] Possibili match trovati con logica flessibile: {len(found_fuzzy)}")
for p, m in found_fuzzy[:15]:
    print(f"  {p} <---> {m}")

print(f"\n[-] Non presenti nel dataset Transfermarkt: {len(not_in_tm)}")
for p, s, t in not_in_tm[:15]:
    print(f"  {s} | {t}")
