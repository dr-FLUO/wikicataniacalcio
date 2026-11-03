import urllib.request
import json

url = 'https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Calcio_Catania&cmlimit=25&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (test@wikicalciocatania.org)'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

members = data.get('query', {}).get('categorymembers', [])
print(f"Total found in Category:Calcio_Catania: {len(members)}")
for m in members[:15]:
    print(f" - {m['title']}")
