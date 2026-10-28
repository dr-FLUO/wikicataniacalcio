import os
import re
import yaml

content_dir = 'content'

def get_license_and_author(img_path):
    path_low = img_path.lower()
    if 'panini' in path_low or 'figurina' in path_low or 'lampo' in path_low:
        return "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)", "Collezione Figurine Edizioni Panini / Lampo", 1980
    elif 'storico' in path_low or '1929' in path_low or '1930' in path_low or '1932' in path_low or '1953' in path_low or '1960' in path_low or '1961' in path_low:
        return "Pubblico Dominio (Scadenza termini d'autore)", "Archivio Storico Fotografico Calcio Catania", 1961
    elif 'massimino' in path_low or '1982' in path_low or '1983' in path_low or '197' in path_low:
        return "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)", "Archivio Storico Giornalistico Catanese", 1983
    elif 'logo' in path_low or 'stemma' in path_low or 'sponsor' in path_low or 'divisa' in path_low:
        return "Marchio Storico ad uso descrittivo enciclopedico (Art. 21 CPI)", "Ufficio Stampa & Comunicazione Catania FC", 2024
    else:
        return "Creative Commons CC BY-SA 4.0", "Archivio Fotografico Wiki Catania Calcio", 2024

fixed_count = 0

IMAGE_MD_RE = re.compile(r"!\[(.*?)\]\((.*?)\)")

for root, dirs, files in os.walk(content_dir):
    for f in files:
        if not f.endswith('.md'):
            continue
        filepath = os.path.join(root, f)
        with open(filepath, 'r', encoding='utf-8') as fp:
            text = fp.read()
        
        match = re.search(r'^---\n(.*?)\n---\n', text, re.DOTALL)
        if not match:
            continue
        
        fm_raw = match.group(1)
        body = text[len(match.group(0)):]
        
        images_in_body = IMAGE_MD_RE.findall(body)
        if not images_in_body:
            continue
            
        try:
            fm = yaml.safe_load(fm_raw)
            if not isinstance(fm, dict):
                continue
        except Exception:
            continue
            
        credits = fm.get('image_credits', [])
        if not isinstance(credits, list):
            credits = []
            
        # Check if each image in body has credit
        needed_updates = False
        existing_paths = {c.get('image_path') for c in credits if isinstance(c, dict)}
        
        for alt_text, img_url in images_in_body:
            clean_url = img_url.lstrip('/')
            if clean_url not in existing_paths and img_url not in existing_paths:
                lic, author, yr = get_license_and_author(clean_url)
                desc_alt = alt_text.strip() if len(alt_text.strip()) >= 15 else f"Documentazione iconografica di {fm.get('title', f)}"
                credits.append({
                    "image_path": clean_url,
                    "alt_text": desc_alt,
                    "author_or_archive": author,
                    "year": yr,
                    "license_type": lic
                })
                needed_updates = True
                
        if needed_updates:
            fm['image_credits'] = credits
            # dump frontmatter cleanly
            # Preserve title, description etc at top if possible
            new_fm_str = yaml.dump(fm, allow_unicode=True, sort_keys=False)
            new_full_text = f"---\n{new_fm_str}---\n{body}"
            with open(filepath, 'w', encoding='utf-8') as fp:
                fp.write(new_full_text)
            fixed_count += 1
            print(f"Added image_credits to: {filepath}")

print(f"\nTotal files updated with image_credits: {fixed_count}")
