import urllib.request
import json
import urllib.parse

query = "Calcio Catania"
url = f'https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata|size&gsrlimit=10&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (test@wikicalciocatania.org)'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

pages = data.get('query', {}).get('pages', {})
print(f"Total search results on Commons: {len(pages)}")
for pid, p in pages.items():
    title = p.get('title')
    info = p.get('imageinfo', [{}])[0]
    meta = info.get('extmetadata', {})
    license_name = meta.get('LicenseShortName', {}).get('value', 'N/A')
    desc = meta.get('ObjectName', {}).get('value') or meta.get('ImageDescription', {}).get('value', '')[:60]
    print(f"File: {title} | Lic: {license_name} | Desc: {desc[:50]}")
