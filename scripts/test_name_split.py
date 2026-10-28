import glob, os, re, yaml

PREFIXES = {'di', 'de', 'del', 'della', 'delle', 'delli', 'da', 'dal', 'dalla', 'dalle', 'lo', 'la', 'li', 'le', 'van', 'von', 'do', 'dos', 'das'}

def split_name(full_name):
    # Remove quotes, nicknames in quotes
    full_name = re.sub(r'["«»“"][^"«»“”]+["«»“”]', '', full_name).strip()
    parts = full_name.split()
    if len(parts) <= 1:
        initial = full_name[0].upper() if full_name else 'A'
        return full_name, '', initial
    
    if len(parts) >= 3 and parts[-2].lower() in PREFIXES:
        cognome = f"{parts[-2]} {parts[-1]}"
        nome = ' '.join(parts[:-2])
    elif len(parts) >= 4 and parts[-3].lower() in PREFIXES:
        cognome = f"{parts[-3]} {parts[-2]} {parts[-1]}"
        nome = ' '.join(parts[:-3])
    else:
        cognome = parts[-1]
        nome = ' '.join(parts[:-1])
    
    c_clean = cognome.lstrip("'").lstrip('"')
    initial = c_clean[0].upper() if c_clean else 'A'
    if not initial.isalpha():
        initial = 'A'
    return cognome, nome, initial

files = glob.glob('content/03-tesserati/**/*.md', recursive=True)
by_letter = {}
parsed = []

for f in files:
    if f.endswith('index.md'): continue
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    m = re.match(r'^---\n(.*?)\n---', c, re.DOTALL)
    if not m: continue
    try:
        data = yaml.safe_load(m.group(1))
    except Exception:
        continue
    title = data.get('title', '')
    name = title.split('—')[0].split('-')[0].split('(')[0].strip()
    if not name or len(name) < 2:
        name = os.path.splitext(os.path.basename(f))[0].replace('-', ' ').title()
    
    cognome, nome, initial = split_name(name)
    by_letter.setdefault(initial, []).append((cognome, nome))
    parsed.append((cognome, nome, initial, f, data))

print(f"Total parsed: {len(parsed)}")
print("Letter distribution by COGNOME:")
for k in sorted(by_letter.keys()):
    sample = by_letter[k][0]
    print(f"  {k}: {len(by_letter[k])} tesserati (sample: {sample[0]}, {sample[1]})")
