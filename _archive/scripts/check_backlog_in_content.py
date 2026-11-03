import json, os, glob, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open("data/wikimedia_catania_db/backlog_pagine_mancanti_wikipedia.json", encoding="utf-8") as f:
    backlog = json.load(f)

high = backlog["da_pubblicare_subito"]
all_files = glob.glob("content/**/*.md", recursive=True)
all_basenames = {os.path.basename(f).replace(".md", ""): f for f in all_files}

print("High priority items:")
for item in high:
    name = item["name"]
    cand = name.lower().replace(" ", "-").replace("'", "")
    match = None
    for bn, full in all_basenames.items():
        if cand in bn or bn in cand:
            match = full
            break
    print(f"  {name:40} -> {match}")
