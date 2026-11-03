import requests

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'}

def get_all_images(title):
    imgs = []
    imcontinue = None
    while True:
        url = f"https://it.wikipedia.org/w/api.php?action=query&titles={title}&prop=images&format=json"
        if imcontinue:
            url += f"&imcontinue={imcontinue}"
        r = requests.get(url, headers=headers).json()
        pdata = list(r.get('query', {}).get('pages', {}).values())[0]
        for im in pdata.get('images', []):
            t = im['title']
            if not any(k in t.lower() for k in ['600px', 'leftarrow', 'rightarrow', 'pencil', 'blank', 'disambig']):
                imgs.append(t)
        if 'continue' in r:
            imcontinue = r['continue']['imcontinue']
        else:
            break
    return imgs

print("1982-1983:", get_all_images("Calcio_Catania_1982-1983"))
print("1983-1984:", get_all_images("Calcio_Catania_1983-1984"))
print("2005-2006:", get_all_images("Calcio_Catania_2005-2006"))
print("1953-1954:", get_all_images("Club_Calcio_Catania_1953-1954"))
