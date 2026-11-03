import requests

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'}

files = [
    "File:Calcio Catania 1982-1983.jpg",
    "File:Calcio Catania 1982-83 (Away).jpg",
    "File:Calcio Catania 1983-1984.jpg",
    "File:Catania-Juventus 0-2, Serie A 1983-84, Tardelli e Sorrentino.jpg"
]

for fn in files:
    url = f"https://it.wikipedia.org/w/api.php?action=query&titles={fn}&prop=imageinfo&iiprop=url|size&format=json"
    r = requests.get(url, headers=headers).json()
    pdata = list(r.get('query', {}).get('pages', {}).values())[0]
    ii = pdata.get('imageinfo', [{}])[0]
    print(fn, "->", ii.get('url'), ii.get('width'), "x", ii.get('height'))
