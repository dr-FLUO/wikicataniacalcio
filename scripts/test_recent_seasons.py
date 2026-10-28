import urllib.request
import json
import urllib.parse

def get_summary(title):
    url = f"https://it.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(title)}&prop=wikitext&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read().decode('utf-8'))
    wt = d.get('parse', {}).get('wikitext', {}).get('*', '')
    return wt[:400]

for yr in ['2023-2024', '2024-2025', '2025-2026', '2026-2027']:
    t = f"Catania Football Club {yr}"
    try:
        res = get_summary(t)
        print(f"=== {t} ===\n{res}\n")
    except Exception as e:
        print(f"=== {t} === Error: {e}")
