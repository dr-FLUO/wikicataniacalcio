import os
import json

with open('data/placeholders_to_replace.json', encoding='utf-8') as f:
    images = json.load(f)

# Find matching markdown files for each image
all_mds = []
for root, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            all_mds.append((os.path.join(root, f).replace('\\', '/'), f.replace('.md', '')))

print(f"Total markdown files: {len(all_mds)}")

mappings = []
for img in images:
    rel = img['rel_path']
    fname = img['filename']
    stem = os.path.splitext(fname)[0]
    
    # Try finding an md matching the slug or entities
    parts = stem.split('-calcio-catania-')[0].split('-catania-')[0]
    # search among mds
    matched_md = None
    for full_path, md_stem in all_mds:
        if md_stem in parts or parts in md_stem or md_stem == parts:
            matched_md = full_path
            break
    
    mappings.append({
        "image_rel": f"assets/images/{rel}",
        "stem": stem,
        "matched_md": matched_md
    })

found = sum(1 for m in mappings if m['matched_md'])
print(f"Direct matched MD files: {found}/{len(mappings)}")
for m in mappings:
    print(f"{m['image_rel']} -> {m['matched_md']}")
