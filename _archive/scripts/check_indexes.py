import os
import glob
import re

sections = [
    '01-societa',
    '02-cronistoria',
    '03-tesserati',
    '04-strutture',
    '05-identita-e-simboli',
    '06-tifoseria-e-cultura',
    '07-media-e-comunicazione',
    '08-settori-paralleli'
]

unindexed_pages = []

for sec in sections:
    sec_path = os.path.join('content', sec)
    for root, dirs, files in os.walk(sec_path):
        md_files = [f for f in files if f.endswith('.md') and f != 'index.md']
        if not md_files:
            continue
        index_file = os.path.join(root, 'index.md')
        if not os.path.exists(index_file):
            print(f"MISSING index.md in: {root}")
            continue
        
        with open(index_file, 'r', encoding='utf-8') as ifp:
            index_content = ifp.read()

        for md in md_files:
            slug = os.path.splitext(md)[0]
            # check if slug is linked in index.md
            if slug not in index_content and md not in index_content:
                unindexed_pages.append((root, md))

print(f"Total unindexed pages found: {len(unindexed_pages)}")
for root, md in unindexed_pages[:30]:
    print(f"  {root} -> {md}")
