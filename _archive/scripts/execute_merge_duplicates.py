import os, glob, re, unicodedata, json, shutil
from collections import defaultdict
from pathlib import Path

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.lower().replace('-', ' ').replace('_', ' ')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return ' '.join(s.split())

files = glob.glob('content/03-tesserati/calciatori/**/*.md', recursive=True)
files = [f.replace('\\', '/') for f in files if not f.endswith('index.md') and not f.endswith('contributo-nazionali.md')]

players = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    title_m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', c, re.MULTILINE)
    title = title_m.group(1) if title_m else ''
    clean_name = title.split('—')[0].split('–')[0].split('-')[0].split('(')[0].strip()
    
    app_m = re.search(r'^total_appearances:\s*(\d+)', c, re.MULTILINE)
    apps = int(app_m.group(1)) if app_m else 0
    
    goal_m = re.search(r'^total_goals:\s*(\d+)', c, re.MULTILINE)
    goals = int(goal_m.group(1)) if goal_m else 0
    
    assist_m = re.search(r'^total_assists:\s*(\d+)', c, re.MULTILINE)
    assists = int(assist_m.group(1)) if assist_m else 0

    min_m = re.search(r'^minutes_played:\s*(\d+)', c, re.MULTILINE)
    minutes = int(min_m.group(1)) if min_m else 0

    img_m = re.search(r'^image:\s*["\']?(.*?)["\']?\s*$', c, re.MULTILINE)
    img = img_m.group(1).strip() if img_m else ''
    
    stem = os.path.splitext(os.path.basename(f))[0]
    folder = os.path.dirname(f)
    category = 'storici' if 'storici' in folder else ('rosa-attuale' if 'rosa-attuale' in folder else 'archivio')
    
    players.append({
        'path': f,
        'stem': stem,
        'title': clean_name,
        'norm_stem': norm(stem),
        'norm_name': norm(clean_name),
        'apps': apps,
        'goals': goals,
        'assists': assists,
        'minutes': minutes,
        'img': img,
        'category': category,
        'raw_content': c
    })

# Group candidates
groups = []
used = set()

for i, p1 in enumerate(players):
    if p1['path'] in used:
        continue
    group = [p1]
    t1 = set(p1['norm_name'].split())
    tokens_stem1 = set(p1['norm_stem'].split())
    
    for j in range(i + 1, len(players)):
        p2 = players[j]
        if p2['path'] in used:
            continue
        t2 = set(p2['norm_name'].split())
        tokens_stem2 = set(p2['norm_stem'].split())
        
        is_match = False
        if p1['norm_name'] == p2['norm_name'] or p1['norm_stem'] == p2['norm_stem']:
            is_match = True
        elif len(t1) >= 2 and len(t2) >= 2 and (t1.issubset(t2) or t2.issubset(t1)):
            is_match = True
        elif len(tokens_stem1) >= 2 and len(tokens_stem2) >= 2 and (tokens_stem1.issubset(tokens_stem2) or tokens_stem2.issubset(tokens_stem1)):
            is_match = True
        elif ('gomez' in t1 and 'gomez' in t2) or ('cinesinho' in p1['norm_stem'] and 'cinesinho' in p2['norm_stem']):
            is_match = True

        if is_match:
            group.append(p2)
            used.add(p2['path'])
            
    if len(group) > 1:
        used.add(p1['path'])
        groups.append(group)

print(f"Total Groups identified: {len(groups)}")

# Explicit overrides for canonical path selection to ensure 100% accuracy
CANONICAL_OVERRIDES = {
    'alejandro-gomez': 'content/03-tesserati/calciatori/storici/alejandro-gomez.md',
    'mariano-andujar': 'content/03-tesserati/calciatori/storici/mariano-andujar.md',
    'mariano-izco': 'content/03-tesserati/calciatori/storici/mariano-izco.md',
    'matias-silvestre': 'content/03-tesserati/calciatori/storici/matias-silvestre.md',
    'jorge-martinez': 'content/03-tesserati/calciatori/storici/jorge-martinez.md',
    'bruno-petkovic': 'content/03-tesserati/calciatori/archivio/a-c/bruno-petkovic.md',
    'filip-jankovic': 'content/03-tesserati/calciatori/archivio/d-f/filip-jankovic.md',
    'edgar-cani': 'content/03-tesserati/calciatori/archivio/d-f/edgar-çani.md',
    'franco-panizza': 'content/03-tesserati/calciatori/archivio/d-f/franco-panizza.md',
    'jaroslav-plasil': 'content/03-tesserati/calciatori/archivio/g-l/jaroslav-plasil.md',
    'jaroslav-sedivec': 'content/03-tesserati/calciatori/archivio/g-l/jaroslav-sedivec.md',
    'jean-francois-gillet': 'content/03-tesserati/calciatori/archivio/g-l/jean-françois-gillet.md',
    'maks-barisic': 'content/03-tesserati/calciatori/archivio/m-o/maks-barišič.md',
    'theofilos-karasavvidis': 'content/03-tesserati/calciatori/archivio/s-z/theofilos-karasavvidis.md',
    'tomas-kosicky': 'content/03-tesserati/calciatori/archivio/g-l/tomas-kosicky.md',
    'luvanor-donizete-borges': 'content/03-tesserati/calciatori/archivio/g-l/luvanor-donizete-borges.md',
    'wellington-teixeira-dos-montes': 'content/03-tesserati/calciatori/archivio/s-z/wellington-teixeira-dos-montes.md',
    'vinicio-cervo-de-luca-cesar': 'content/03-tesserati/calciatori/archivio/s-z/vinicio-cervo-de-luca-cesar.md',
}

def pick_canonical(group):
    # 1. Check if any override matches
    for p in group:
        for k, target_path in CANONICAL_OVERRIDES.items():
            if p['path'] == target_path:
                return p
    # 2. Check if in storici
    for p in group:
        if p['category'] == 'storici':
            return p
    # 3. Check for truncated diacritics
    clean = [p for p in group if not any(c in p['stem'] for c in ['-ani', 'pla-il', 'edivec', 'fran-ois', 'bari-i', 'karasavvid-s', 'ko-ick', 'petkovi', 'jankovi', 'dic'])]
    if len(clean) == 1:
        return clean[0]
    # 4. Check for '-calciatore'
    non_suff = [p for p in group if not p['stem'].endswith('-calciatore')]
    if len(non_suff) == 1:
        return non_suff[0]
    # 5. Default to shorter stem or higher apps
    sorted_g = sorted(group, key=lambda p: (len(p['stem'].split('-')), -p['apps']))
    return sorted_g[0]

def extract_aliases(content):
    m = re.search(r'^aliases:\s*\n((?:\s*-[^\n]+\n)+)', content, re.MULTILINE)
    if not m:
        return []
    lines = m.group(1).split('\n')
    aliases = []
    for line in lines:
        line = line.strip()
        if line.startswith('-'):
            aliases.append(line.lstrip('-').strip().strip('\'"'))
    return [a for a in aliases if a]

merged_count = 0
deleted_count = 0

for g in groups:
    canon = pick_canonical(g)
    to_delete = [p for p in g if p['path'] != canon['path']]
    if not to_delete:
        continue
        
    print(f"\nMerging group into canonical: {canon['stem']} ({canon['path']})")
    
    canon_content = canon['raw_content']
    
    # 1. Consolidate aliases
    existing_aliases = extract_aliases(canon_content)
    new_aliases = set(existing_aliases)
    
    # Add slugs and paths of deleted files
    for d in to_delete:
        d_slug = d['path'].replace('content/', '').replace('.md', '')
        d_stem = d['stem']
        new_aliases.add(d_slug)
        new_aliases.add(d_stem)
        new_aliases.add(f"tesserati/calciatori/{d_stem}")
        new_aliases.add(f"calciatori/{d_stem}")
        new_aliases.add(f"03-tesserati/calciatori/{d_stem}")
        # Add any aliases the deleted file had
        del_aliases = extract_aliases(d['raw_content'])
        for da in del_aliases:
            new_aliases.add(da)
            
    # Remove self from aliases
    canon_slug = canon['path'].replace('content/', '').replace('.md', '')
    if canon_slug in new_aliases: new_aliases.remove(canon_slug)
    if canon['stem'] in new_aliases: new_aliases.remove(canon['stem'])
    
    # Format aliases list
    aliases_yaml = "aliases:\n" + "\n".join(f"- {a}" for a in sorted(new_aliases))
    
    if re.search(r'^aliases:\s*\n((?:\s*-[^\n]+\n)+)', canon_content, re.MULTILINE):
        canon_content = re.sub(r'^aliases:\s*\n((?:\s*-[^\n]+\n)+)', aliases_yaml + "\n", canon_content, flags=re.MULTILINE)
    else:
        # inject before closing frontmatter
        canon_content = canon_content.replace('\n---', f"\n{aliases_yaml}\n---", 1)

    # 2. Check and consolidate stats (take max apps, goals, assists, minutes)
    max_apps = max(canon['apps'], max(d['apps'] for d in to_delete))
    max_goals = max(canon['goals'], max(d['goals'] for d in to_delete))
    max_assists = max(canon['assists'], max(d['assists'] for d in to_delete))
    max_min = max(canon['minutes'], max(d['minutes'] for d in to_delete))
    
    if max_apps > canon['apps']:
        canon_content = re.sub(r'^total_appearances:\s*\d+', f"total_appearances: {max_apps}", canon_content, flags=re.MULTILINE)
    if max_goals > canon['goals']:
        canon_content = re.sub(r'^total_goals:\s*\d+', f"total_goals: {max_goals}", canon_content, flags=re.MULTILINE)
    if max_assists > canon['assists']:
        canon_content = re.sub(r'^total_assists:\s*\d+', f"total_assists: {max_assists}", canon_content, flags=re.MULTILINE)
    if max_min > canon['minutes']:
        canon_content = re.sub(r'^minutes_played:\s*\d+', f"minutes_played: {max_min}", canon_content, flags=re.MULTILINE)

    # 3. Check image
    if not canon['img']:
        for d in to_delete:
            if d['img']:
                print(f"  Transferring image from {d['stem']} to {canon['stem']}: {d['img']}")
                canon_content = re.sub(r'^image:\s*.*$', f"image: {d['img']}", canon_content, flags=re.MULTILINE)
                canon['img'] = d['img']
                break

    # Save canonical file
    with open(canon['path'], 'w', encoding='utf-8') as fp:
        fp.write(canon_content)
    merged_count += 1
    
    # 4. Physically delete redundant duplicate files
    for d in to_delete:
        print(f"  Deleting redundant file: {d['path']}")
        try:
            os.remove(d['path'])
            deleted_count += 1
        except Exception as e:
            print(f"  Error deleting {d['path']}: {e}")

print(f"\n[+] Operazione completata: {merged_count} gruppi consolidati, {deleted_count} file duplicati eliminati con successo.")
