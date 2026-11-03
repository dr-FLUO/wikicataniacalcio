import urllib.request
import json
import urllib.parse

def get_cat_members(cat_title):
    url = f"https://it.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={urllib.parse.quote(cat_title)}&cmlimit=500&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d.get('query', {}).get('categorymembers', [])

root_cat = "Categoria:Calcio Catania"
members = get_cat_members(root_cat)
print(f"{root_cat}: {len(members)} total items")
subcats = [m for m in members if m['ns'] == 14]
pages = [m for m in members if m['ns'] == 0]

print(f"Subcategories ({len(subcats)}):")
for sc in subcats:
    print(" -", sc['title'])

print(f"\nDirect Pages ({len(pages)}):")
for p in pages:
    print(" -", p['title'])

for sc in subcats:
    sc_members = get_cat_members(sc['title'])
    print(f"\n{sc['title']} has {len(sc_members)} items:")
    for sm in sc_members[:5]:
        print("   *", sm['title'])
    if len(sc_members) > 5:
        print(f"   ... and {len(sc_members)-5} more")
