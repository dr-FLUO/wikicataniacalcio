import os
import json
from PIL import Image

remaining = []
with open('data/placeholders_to_replace.json', encoding='utf-8') as f:
    placeholders = json.load(f)

for p in placeholders:
    path = os.path.join('content/assets/images', p['rel_path'])
    with Image.open(path) as img:
        px = img.convert('RGB').load()
        if px[0, 0] in [(79, 17, 35), (77, 17, 35)]:
            remaining.append(p['rel_path'])

print(f"Remaining placeholders: {len(remaining)}")
for i, r in enumerate(remaining, 1):
    print(f"{i:2d}. {r}")
