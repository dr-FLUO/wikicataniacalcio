import urllib.request
import json
import urllib.parse

def get_cat_members(cat_title):
    url = f"https://it.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={urllib.parse.quote(cat_title)}&cmlimit=500&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read().decode('utf-8'))
    return [x['title'] for x in d.get('query', {}).get('categorymembers', []) if x['ns'] == 0]

categories = [
    "Categoria:Catania F.C.",
    "Categoria:Presidenti del Catania F.C.",
    "Categoria:Allenatori del Catania F.C.",
    "Categoria:Dirigenti del Catania F.C.",
    "Categoria:Calcio a Catania",
]

all_cat_pages = {}
for c in categories:
    pages = get_cat_members(c)
    all_cat_pages[c] = pages
    print(f"{c}: {len(pages)} pagine trovate")

for c, pages in all_cat_pages.items():
    print(f"\n--- {c} ---")
    for p in pages:
        print(" *", p)
