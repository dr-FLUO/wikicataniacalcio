import os
import json
from PIL import Image

placeholders = []
root_dir = 'content/assets/images'

for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.lower().endswith('.webp'):
            path = os.path.join(root, f)
            try:
                with Image.open(path) as img:
                    px = img.convert('RGB').load()
                    c1 = px[0, 0]
                    # Check for our placeholder gradient colors
                    if c1 in [(79, 17, 35), (77, 17, 35)]:
                        rel = os.path.relpath(path, root_dir).replace('\\', '/')
                        placeholders.append({
                            "rel_path": rel,
                            "filename": f,
                            "full_path": path.replace('\\', '/'),
                            "size": img.size,
                            "color": list(c1)
                        })
            except Exception as e:
                pass

placeholders.sort(key=lambda x: x["rel_path"])
print(f"Total placeholders found: {len(placeholders)}")

with open('data/placeholders_to_replace.json', 'w', encoding='utf-8') as f:
    json.dump(placeholders, f, indent=2, ensure_ascii=False)

for i, p in enumerate(placeholders, 1):
    print(f"{i:2d}. {p['rel_path']}")
