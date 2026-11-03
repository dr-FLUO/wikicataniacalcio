import os
import re
import json
from collections import defaultdict, Counter

CONTENT_DIR = "content"

# Raccogli tutti i file esistenti
existing_slugs = set()
for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if f.endswith('.md'):
            existing_slugs.add(f[:-3].lower())

def slugify(s):
    s = s.lower().strip()
    s = s.replace('à','a').replace('è','e').replace('é','e').replace('ì','i').replace('ò','o').replace('ù','u')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

# 1. Scansione stagioni (tutte le 90+ annate)
seasons_dir = os.path.join(CONTENT_DIR, '02-cronistoria', 'stagioni')
missing_presidents = Counter()
missing_coaches = Counter()
missing_directors = Counter()
pres_seasons = defaultdict(list)
coach_seasons = defaultdict(list)
dir_seasons = defaultdict(list)

for f in os.listdir(seasons_dir):
    if not f.endswith('.md'): continue
    season_name = f[:-3]
    with open(os.path.join(seasons_dir, f), 'r', encoding='utf-8-sig') as fp:
        txt = fp.read()
    
    # Cerca Presidente
    m_p = re.findall(r'(?:Presidente|Pres\.|Presidenti):\s*([^\n\r\|]+)', txt, re.I)
    for p_line in m_p:
        # Pulisci nomi separati da virgole, 'poi', 'e', o date
        names = re.split(r'[,;/]|(?:\s+poi\s+)|\be\b', p_line)
        for n in names:
            n_clean = re.sub(r'\(.*?\)|\[\[.*?\]\]|[0-9\-\*]', '', n).strip()
            if len(n_clean) > 4 and len(n_clean.split()) >= 2:
                s = slugify(n_clean)
                if s not in existing_slugs and not any(part in existing_slugs for part in s.split('-') if len(part) > 4):
                    missing_presidents[n_clean] += 1
                    pres_seasons[n_clean].append(season_name)

    # Cerca Allenatore
    m_c = re.findall(r'(?:Allenatore|All\.|Allenatori|Tecnico):\s*([^\n\r\|]+)', txt, re.I)
    for c_line in m_c:
        names = re.split(r'[,;/]|(?:\s+poi\s+)|\be\b', c_line)
        for n in names:
            n_clean = re.sub(r'\(.*?\)|\[\[.*?\]\]|[0-9\-\*]', '', n).strip()
            if len(n_clean) > 4 and len(n_clean.split()) >= 2:
                s = slugify(n_clean)
                if s not in existing_slugs and not any(part in existing_slugs for part in s.split('-') if len(part) > 4):
                    missing_coaches[n_clean] += 1
                    coach_seasons[n_clean].append(season_name)

    # Cerca Dirigente
    m_d = re.findall(r'(?:Direttore|D\.S\.|D\.G\.|General Manager|Segretario):\s*([^\n\r\|]+)', txt, re.I)
    for d_line in m_d:
        names = re.split(r'[,;/]|(?:\s+poi\s+)|\be\b', d_line)
        for n in names:
            n_clean = re.sub(r'\(.*?\)|\[\[.*?\]\]|[0-9\-\*]', '', n).strip()
            if len(n_clean) > 4 and len(n_clean.split()) >= 2:
                s = slugify(n_clean)
                if s not in existing_slugs and not any(part in existing_slugs for part in s.split('-') if len(part) > 4):
                    missing_directors[n_clean] += 1
                    dir_seasons[n_clean].append(season_name)

print("=== PRESIDENTI CITATI NELLE STAGIONI MA SENZA SCHEDA ===")
for p, cnt in missing_presidents.most_common(15):
    print(f"  - {p} ({cnt} stagioni): {', '.join(pres_seasons[p][:4])}")

print("\n=== ALLENATORI CITATI NELLE STAGIONI MA SENZA SCHEDA ===")
for c, cnt in missing_coaches.most_common(15):
    print(f"  - {c} ({cnt} stagioni): {', '.join(coach_seasons[c][:4])}")

print("\n=== DIRIGENTI CITATI NELLE STAGIONI MA SENZA SCHEDA ===")
for d, cnt in missing_directors.most_common(15):
    print(f"  - {d} ({cnt} stagioni): {', '.join(dir_seasons[d][:4])}")
