import urllib.request
import json
import urllib.parse

def search_wiki(q, limit=10):
    url = f"https://it.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(q)}&srlimit={limit}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d.get('query', {}).get('search', [])

queries = [
    "Catania Football Club",
    "Stadio Angelo Massimino",
    "Torre del Grifo Village",
    "Catania Calcio Femminile",
    "Caso Catania",
    "Scontri di Catania",
    "Derby di Sicilia",
    "Clamoroso al Cibali!",
    "Cinquanta volti per il Cibali",
    "Statistiche e record del Catania Football Club",
    "Storia del Catania Football Club",
    "Colori e simboli del Catania Football Club",
    "Tifoseria del Catania Football Club",
]

for q in queries:
    res = search_wiki(q, limit=4)
    print(f"=== {q} ===")
    for r in res:
        print(f"  * {r['title']} (size: {r['size']} bytes)")
