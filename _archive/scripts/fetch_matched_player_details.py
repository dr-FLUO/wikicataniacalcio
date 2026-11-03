import json
import urllib.request
import ssl
import re
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}

with open('data/calciocatania_all_players.json', 'r', encoding='utf-8') as f:
    cc_players = json.load(f)

# Run match to find target players (existing 58 + top 50 by presenze)
import unicodedata
def norm(s):
    s = s.lower()
    s = unicodedata.normalize('NFD', s)
    s = re.sub(r'[\u0300-\u036f]', '', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

lookup = {norm(p['name']): p for p in cc_players}

target_players = {}

# 1. Existing monographs
import os
for f in os.listdir('content/tesserati/calciatori'):
    if not f.endswith('.md'):
        continue
    slug = f[:-3]
    with open(f'content/tesserati/calciatori/{f}', 'r', encoding='utf-8') as fp:
        txt = fp.read()
    m_name = re.search(r'full_name:\s*"([^"]+)"', txt)
    name = m_name.group(1).strip() if m_name else slug.replace('-', ' ')
    k = norm(name)
    if k in lookup:
        target_players[lookup[k]['id']] = (lookup[k], slug)
    else:
        for cck, ccp in lookup.items():
            if norm(slug.split('-')[-1]) in cck and norm(slug.split('-')[0]) in cck:
                target_players[ccp['id']] = (ccp, slug)
                break

# 2. Add top 50 by appearances
for p in sorted(cc_players, key=lambda x: x['appearances'], reverse=True)[:50]:
    if p['id'] not in target_players:
        target_players[p['id']] = (p, None)

print(f"Total target player detail pages to fetch: {len(target_players)}")

detailed_results = {}

for pid, (pinfo, slug) in target_players.items():
    url = pinfo['url']
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # Extract JSON-LD Person
        m = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        person_data = {}
        for b in m:
            try:
                d = json.loads(b)
                graph = d.get('@graph', [d]) if isinstance(d, dict) else d
                for item in graph:
                    if isinstance(item, dict) and item.get('@type') == 'Person':
                        person_data = item
                        break
            except Exception:
                pass
        
        # Extract season table
        # Table with Stagione, Pres, Tit, Sub, Gol, Amm, Esp
        seasons_stats = []
        table_m = re.search(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
        if table_m:
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_m.group(1), re.DOTALL)
            for r in rows[1:]: # skip header
                cols = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
                clean_cols = [re.sub(r'<[^>]+>', '', c).strip() for c in cols]
                if clean_cols and len(clean_cols) >= 5:
                    seasons_stats.append({
                        'season': clean_cols[0],
                        'appearances': clean_cols[1],
                        'starts': clean_cols[2] if len(clean_cols) > 2 else '',
                        'subs': clean_cols[3] if len(clean_cols) > 3 else '',
                        'goals': clean_cols[4] if len(clean_cols) > 4 else '0'
                    })
        
        detailed_results[pid] = {
            'id': pid,
            'name': pinfo['name'],
            'role': pinfo['role'],
            'total_appearances': pinfo['appearances'],
            'seasons_count': pinfo['seasons_count'],
            'thumb': pinfo['thumb'],
            'url': url,
            'slug': slug,
            'birth_date': person_data.get('birthDate'),
            'birth_place': person_data.get('birthPlace', {}).get('name') if isinstance(person_data.get('birthPlace'), dict) else str(person_data.get('birthPlace') or ''),
            'seasons_stats': seasons_stats
        }
        print(f"  Fetched {pinfo['name']} (DOB: {person_data.get('birthDate')}, Place: {detailed_results[pid]['birth_place']}, {len(seasons_stats)} seasons)", flush=True)
        time.sleep(0.15)
    except Exception as e:
        print(f"  ERROR {pinfo['name']}: {e}", flush=True)

with open('data/matched_players_detail.json', 'w', encoding='utf-8') as out:
    json.dump(detailed_results, out, indent=2, ensure_ascii=False)

print(f"\nSaved {len(detailed_results)} detailed players to data/matched_players_detail.json")
