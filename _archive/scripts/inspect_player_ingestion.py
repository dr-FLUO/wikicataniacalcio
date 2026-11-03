import json
import os
import re

with open('data/calciocatania_all_players.json', encoding='utf-8') as f:
    players = json.load(f)

with open('data/player_local_images.json', encoding='utf-8') as f:
    local_imgs = json.load(f)

existing = set()
for f in os.listdir('content/tesserati/calciatori'):
    if f.endswith('.md'):
        existing.add(f.replace('.md', ''))

print(f"Total players in JSON: {len(players)}")
print(f"Existing player markdown files: {len(existing)}")

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

already_exist = 0
to_generate = []

for p in players:
    name = p.get('name', '')
    slug = slugify(name)
    pid = str(p.get('id', ''))
    img_path = local_imgs.get(pid)
    
    # check if already exists
    if slug in existing:
        already_exist += 1
    else:
        to_generate.append((slug, p, img_path))

print(f"Already existing: {already_exist}")
print(f"To generate: {len(to_generate)}")
print("Sample first 5 to generate:", [x[0] for x in to_generate[:5]])
