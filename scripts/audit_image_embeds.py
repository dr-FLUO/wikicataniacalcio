import os
import json

with open('data/placeholders_to_replace.json', encoding='utf-8') as f:
    placeholders = json.load(f)

# Collect all markdown text
all_text = {}
for root, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                all_text[p] = fp.read()

embedded = []
not_embedded = []

for p in placeholders:
    rel = p['rel_path']
    fname = p['filename']
    # Check if fname or rel is in any markdown file
    found_in = []
    for md_path, text in all_text.items():
        if fname in text or rel in text:
            found_in.append(md_path)
    
    if found_in:
        embedded.append((rel, found_in))
    else:
        not_embedded.append(rel)

print(f"Total target images: {len(placeholders)}")
print(f"Embedded in markdown: {len(embedded)}")
print(f"NOT yet embedded in markdown: {len(not_embedded)}")

print("\n--- NOT EMBEDDED ---")
for i, n in enumerate(not_embedded, 1):
    print(f"{i:2d}. {n}")
