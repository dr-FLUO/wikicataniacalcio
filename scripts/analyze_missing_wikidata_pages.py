import json
import os
import re

# Load wikidata people
with open("data/wikimedia_catania_db/wikidata_people.json", "r", encoding="utf-8") as f:
    people = json.load(f)

# Collect all slugs/filenames in content
existing_slugs = set()
for root, _, files in os.walk("content"):
    for f in files:
        if f.endswith(".md"):
            existing_slugs.add(f.replace(".md", "").lower())
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as fp:
                t = fp.read()
            m = re.search(r"^slug:\s*(.*?)$", t, re.M)
            if m:
                existing_slugs.add(m.group(1).split("/")[-1].lower())
            # aliases
            m_al = re.search(r"aliases:\s*\n((?:\s*-\s*.*?\n)+)", t)
            if m_al:
                for line in m_al.group(1).splitlines():
                    al = line.strip("- ").strip("'\"").split("/")[-1].lower()
                    existing_slugs.add(al)

print(f"Total people in Wikidata DB: {len(people)}")
print(f"Total existing entity slugs in vault: {len(existing_slugs)}")

missing_with_wiki = []
missing_with_image = []
missing_others = []

def slugify(name):
    s = name.lower().replace("à", "a").replace("è", "e").replace("é", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

for p in people:
    name = p["name"]
    s = slugify(name)
    has_page = (s in existing_slugs)
    if not has_page:
        # Check by lastname
        parts = s.split("-")
        if any(len(pt) > 3 and pt in existing_slugs for pt in parts):
            has_page = True
            
    if not has_page:
        if p.get("it_wiki_article"):
            missing_with_wiki.append(p)
        elif p.get("image_url"):
            missing_with_image.append(p)
        else:
            missing_others.append(p)

print(f"\nMissing from vault WITH an Italian Wikipedia article: {len(missing_with_wiki)}")
print(f"Missing from vault WITH an image on Commons: {len(missing_with_image)}")
print(f"Missing from vault without wiki article: {len(missing_others)}")

print("\n--- TOP 25 MISSING NOTABLE FIGURES (con voce Wikipedia e dati anagrafici) ---")
for p in missing_with_wiki[:25]:
    roles = ", ".join(p.get("positions", [])) or "Ruolo N/D"
    bdate = p.get("birth_date", "Data N/D")
    bplace = p.get("birth_place", "Luogo N/D")
    art = p.get("it_wiki_article", "")
    print(f" - {p['name']} ({roles} | Nato: {bdate} a {bplace}) -> {art}")
