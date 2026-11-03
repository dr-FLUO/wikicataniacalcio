import requests

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'}

pages = [
    "Roberto_Sorrentino_(calciatore)",
    "Giuseppe_Vavassori",
    "Nicola_Fusaro",
    "Mario_Miltone",
    "Calcio_Catania_1953-1954",
    "Calcio_Catania_1960-1961",
    "Calcio_Catania_1982-1983",
    "Calcio_Catania_2005-2006",
    "Stadio_Angelo_Massimino",
    "Antonino_Pulvirenti",
    "Pietro_Lo_Monaco",
    "Clamoroso_al_Cibali!"
]

for p in pages:
    url = f"https://it.wikipedia.org/w/api.php?action=query&titles={p}&prop=images&format=json"
    r = requests.get(url, headers=headers).json()
    pdata = list(r.get('query', {}).get('pages', {}).values())[0]
    imgs = [i['title'] for i in pdata.get('images', []) if not any(x in i['title'].lower() for x in ['icon', 'stub', 'flag', 'disambig', 'logo', 'badge', 'crystal', 'ball'])]
    print(f"=== {p} ===")
    for im in imgs:
        print("  ", im)
