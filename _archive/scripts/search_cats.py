import urllib.request
import json
import urllib.parse

def search_cats(query):
    url = f"https://it.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&srnamespace=14&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d.get('query', {}).get('search', [])

for q in ["Catania", "Calcio Catania", "Catania FC"]:
    results = search_cats(q)
    print(f"Search categories for '{q}':")
    for r in results[:8]:
        print(" -", r['title'])
