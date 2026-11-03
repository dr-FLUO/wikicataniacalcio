import requests

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'}

pages = [
    "Calcio_Catania_2008-2009",
    "Calcio_Catania_2009-2010",
    "Calcio_Catania_2007-2008",
    "Giuseppe_Mascara",
    "Jorge_Andrés_Martínez",
    "Gianvito_Plasmati"
]

for p in pages:
    url = f"https://it.wikipedia.org/w/api.php?action=query&titles={p}&prop=images&format=json"
    r = requests.get(url, headers=headers).json()
    pdata = list(r.get('query', {}).get('pages', {}).values())[0]
    imgs = [i['title'] for i in pdata.get('images', []) if not any(k in i['title'].lower() for k in ['600px', 'leftarrow', 'rightarrow', 'pencil', 'blank', 'disambig', 'flag', 'icon'])]
    print(f"=== {p} ===")
    for im in imgs:
        print("  ", im)
