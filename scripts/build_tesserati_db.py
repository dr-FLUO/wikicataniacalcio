import glob, os, re, yaml, json, unicodedata

PREFIXES = {'di', 'de', 'del', 'della', 'delle', 'delli', 'da', 'dal', 'dalla', 'dalle', 'lo', 'la', 'li', 'le', 'van', 'von', 'do', 'dos', 'das'}

SPECIAL_NAMES = {
    'diego pablo simeone': ('Simeone', 'Diego Pablo'),
    'sergio bernardo almiron': ('Almiron', 'Sergio Bernardo'),
    'cristian daniel ledesma': ('Ledesma', 'Cristian Daniel'),
    'pablo cesar barrientos': ('Barrientos', 'Pablo César'),
    'guilherme raymundo do prado': ('Do Prado', 'Guilherme (Guly)'),
    'guly do prado': ('Do Prado', 'Guly'),
    'babu': ('Babú', ''),
    'cate': ('Catê', ''),
    'jeda': ('Jeda', ''),
    'pia': ('Piá', ''),
}

def normalize_ascii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def split_name(full_name):
    # Remove quotation marks or nicknames in quotes
    full_name = re.sub(r'["«»“"][^"«»“”]+["«»“”]', '', full_name).strip()
    clean_lower = normalize_ascii(full_name).lower()
    if clean_lower in SPECIAL_NAMES:
        c, n = SPECIAL_NAMES[clean_lower]
        init = normalize_ascii(c).lstrip("'").lstrip('"')[0].upper()
        return c, n, init

    parts = full_name.split()
    if len(parts) <= 1:
        c_clean = normalize_ascii(full_name).lstrip("'").lstrip('"')
        initial = c_clean[0].upper() if c_clean else 'A'
        return full_name, '', initial if initial.isalpha() else 'A'
    
    if len(parts) >= 3 and parts[-2].lower() in PREFIXES:
        cognome = f"{parts[-2]} {parts[-1]}"
        nome = ' '.join(parts[:-2])
    elif len(parts) >= 4 and parts[-3].lower() in PREFIXES:
        cognome = f"{parts[-3]} {parts[-2]} {parts[-1]}"
        nome = ' '.join(parts[:-3])
    else:
        cognome = parts[-1]
        nome = ' '.join(parts[:-1])
    
    c_clean = normalize_ascii(cognome).lstrip("'").lstrip('"')
    initial = c_clean[0].upper() if c_clean else 'A'
    if not initial.isalpha():
        initial = 'A'
    return cognome, nome, initial

files = glob.glob('content/03-tesserati/**/*.md', recursive=True)
db = []

for f in files:
    if f.endswith('index.md'):
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    m = re.match(r'^---\n(.*?)\n---', c, re.DOTALL)
    if not m:
        continue
    try:
        data = yaml.safe_load(m.group(1))
    except Exception:
        continue
    if not isinstance(data, dict):
        continue
    
    slug = data.get('slug', '')
    if not slug:
        rel = os.path.relpath(f, 'content')
        slug = os.path.splitext(rel)[0].replace('\\', '/')
    
    title = data.get('title', '')
    name = title.split('—')[0].split('-')[0].split('(')[0].strip()
    if not name or len(name) < 2:
        name = os.path.splitext(os.path.basename(f))[0].replace('-', ' ').title()
    
    cognome, nome, initial = split_name(name)
    role = data.get('role', '') or data.get('ruolo', '')
    if not role:
        if 'allenatori' in slug:
            role = 'Allenatore'
        else:
            role = 'Calciatore'
    
    apps = int(data.get('total_appearances', 0) or 0)
    seasons = int(data.get('seasons_count', 0) or 1)
    img = data.get('image', '')
    entity = data.get('entity_type', 'calciatore')
    
    role_lower = role.lower()
    if 'allenatore' in role_lower:
        cat_role = 'Allenatore'
    elif 'portiere' in role_lower:
        cat_role = 'Portiere'
    elif 'difens' in role_lower or 'terzino' in role_lower or 'libero' in role_lower or 'stopper' in role_lower:
        cat_role = 'Difensore'
    elif 'centrocamp' in role_lower or 'mediano' in role_lower or 'regista' in role_lower or 'ala' in role_lower or 'mezzala' in role_lower:
        cat_role = 'Centrocampista'
    elif 'attaccant' in role_lower or 'centravanti' in role_lower or 'punta' in role_lower or 'fantasista' in role_lower:
        cat_role = 'Attaccante'
    else:
        cat_role = 'Calciatore'
    
    db.append({
        'c': cognome,
        'n': nome,
        'i': initial,
        'r': role,
        'cr': cat_role,
        'a': apps,
        's': seasons,
        'u': slug,
        'img': img if img else ''
    })

# Rigorous sorting: COGNOME (A-Z), then NOME (A-Z)
db.sort(key=lambda x: (normalize_ascii(x['c']).upper(), normalize_ascii(x['n']).upper()))

print(f"Total valid database entries: {len(db)}")

# Output files
os.makedirs('quartz/components', exist_ok=True)
with open('quartz/components/tesserati_db.json', 'w', encoding='utf-8') as out:
    json.dump(db, out, ensure_ascii=False, indent=None, separators=(',', ':'))

os.makedirs('quartz/static/data', exist_ok=True)
with open('quartz/static/data/tesserati_db.json', 'w', encoding='utf-8') as out:
    json.dump(db, out, ensure_ascii=False, indent=None, separators=(',', ':'))

print("Saved database to quartz/components/tesserati_db.json and quartz/static/data/tesserati_db.json successfully!")
