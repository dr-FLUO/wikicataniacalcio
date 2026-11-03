import os
import json

with open('data/placeholders_to_replace.json', encoding='utf-8') as f:
    placeholders = json.load(f)

root_files = os.listdir('content/assets/images')
player_files = os.listdir('content/assets/images/players') if os.path.exists('content/assets/images/players') else []

print(f"Total placeholders: {len(placeholders)}")
matches = []

for p in placeholders:
    fname = p['filename']
    stem = os.path.splitext(fname)[0]
    # extract main keyword: first 2 words
    parts = stem.split('-')
    keywords = parts[:2]
    key_str = "-".join(keywords)
    
    # Check root files
    root_match = [rf for rf in root_files if any(k in rf for k in keywords) and not os.path.isdir(os.path.join('content/assets/images', rf))]
    # Check player files
    player_match = [pf for pf in player_files if any(k in pf.lower() for k in keywords)]
    
    print(f"\nPlaceholder: {p['rel_path']}")
    if root_match:
        print(f"  Root matches: {root_match}")
    if player_match:
        print(f"  Player matches: {player_match[:3]}")
