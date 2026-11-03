import re

files_needing_yaml_fix = [
    "content/partite/1960-1961/catania-inter-2-0.md",
    "content/stagioni/1982-1983.md",
    "content/tesserati/calciatori/giorgio-mastropasqua.md",
    "content/tesserati/calciatori/giuseppe-vavassori.md",
    "content/tesserati/calciatori/guido-biondi.md",
    "content/tesserati/calciatori/horst-szymaniak.md",
    "content/tesserati/calciatori/nicola-fusaro.md",
    "content/tesserati/calciatori/roberto-sorrentino.md",
    "content/tesserati/calciatori/sidney-cunha-cinesinho.md",
]

for p in files_needing_yaml_fix:
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()

    parts = text.split("---", 2)
    if len(parts) < 3:
        continue
    
    raw_fm = parts[1]
    body = parts[2]
    
    # We want to extract all image embeds in body and build clean image_credits
    img_matches = re.findall(r"!\[(.*?)\]\((.*?)\)", body)
    
    credits_list = []
    for alt, url in img_matches:
        clean_url = url.lstrip("/").replace("../../", "").replace("../", "")
        credits_list.append({
            "image_path": clean_url,
            "alt_text": alt.replace('"', "'"),
            "author_or_archive": "Archivio Storico Calcio Catania / Edizioni Panini",
            "year": 1983,
            "license_type": "Pubblico Dominio / Fair Use"
        })
    
    # Cut out old image_credits from raw_fm
    fm_lines = []
    skip = False
    for line in raw_fm.splitlines():
        if line.startswith("image_credits:"):
            skip = True
            continue
        if skip:
            if re.match(r"^[a-zA-Z0-9_-]+:", line) and not line.startswith(" "):
                skip = False
                fm_lines.append(line)
            else:
                continue
        else:
            fm_lines.append(line)
            
    # Add clean image_credits
    clean_credits_yaml = "image_credits:\n"
    for c in credits_list:
        clean_credits_yaml += f"""  - image_path: "{c['image_path']}"
    alt_text: "{c['alt_text']}"
    author_or_archive: "{c['author_or_archive']}"
    year: {c['year']}
    license_type: "{c['license_type']}"\n"""
        
    new_raw_fm = "\n".join(fm_lines) + "\n" + clean_credits_yaml
    new_text = f"---{new_raw_fm}---{body}"
    with open(p, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"Cleaned image_credits in: {p}")
