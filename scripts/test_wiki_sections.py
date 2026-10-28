import urllib.request
import json

url = 'https://it.wikipedia.org/w/api.php?action=parse&page=Catania_Football_Club_2024-2025&prop=sections&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (test@wikicalciocatania.org)'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

sections = data.get('parse', {}).get('sections', [])
for s in sections:
    print(f"{s['number']} - {s['line']}")
