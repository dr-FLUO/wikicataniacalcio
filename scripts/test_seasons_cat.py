import urllib.request
import json
import urllib.parse

def get_cat_members(cat_title):
    url = f"https://it.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={urllib.parse.quote(cat_title)}&cmlimit=500&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d.get('query', {}).get('categorymembers', [])

seasons = get_cat_members("Categoria:Stagioni del Catania F.C.")
print(f"Stagioni del Catania F.C. total pages: {len(seasons)}")
for s in sorted([s['title'] for s in seasons]):
    print(" -", s)
