import os
import requests
from io import BytesIO
from PIL import Image

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'}

local_mappings = {
    "calciatori/figurine/giuseppe-vavassori-calcio-catania-figurina-panini-1961-1966.webp": "content/assets/images/players/621_giuseppe-vavassori.jpg",
    "calciatori/figurine/nicola-fusaro-calcio-catania-figurina-panini-1975-1976.webp": "content/assets/images/players/525_nicola-fusaro.jpg",
    "calciatori/figurine/roberto-sorrentino-calcio-catania-figurina-panini-1982-1983.webp": "content/assets/images/players/480_roberto-sorrentino.jpg",
    "calciatori/rosa-attuale/adriano-montalto-calcio-catania-attaccante-2026-2027.webp": "content/assets/images/players/1091_adriano-montalto.jpg",
    "calciatori/rosa-attuale/alessandro-quaini-calcio-catania-centrocampista-2026-2027.webp": "content/assets/images/players/1056_alessandro-quaini.png",
    "calciatori/rosa-attuale/alessio-castellini-calcio-catania-difensore-capitano-2026-2027.webp": "content/assets/images/players/944_alessio-castellini.jpg",
    "calciatori/rosa-attuale/emmanuele-pio-cicerelli-calcio-catania-attaccante-2026-2027.webp": "content/assets/images/players/1066_emmanuele-pio-cicerelli.png",
    "calciatori/rosa-attuale/gabriel-lunetta-calcio-catania-centrocampista-2026-2027.webp": "content/assets/images/players/1070_gabriel-lunetta.png",
    "calciatori/rosa-attuale/marius-adamonis-calcio-catania-portiere-2026-2027.webp": "content/assets/images/players/1107_marius-adamonis.png",
}

web_mappings = {
    "calciatori/foto-storiche/nicolo-nicolosi-calcio-catania-bomber-storico-1932-1940.webp": "https://upload.wikimedia.org/wikipedia/commons/2/26/Nicolosi_Nicol%C3%B2.jpg",
    "partite-storiche/catania-inter-2-0-clamoroso-al-cibali-serie-a-1960-1961.webp": "https://upload.wikimedia.org/wikipedia/it/e/e2/CataniaInter1961.JPG",
    "media-e-stampa/la-sicilia-prima-pagina-clamoroso-al-cibali-catania-inter-1961.webp": "https://upload.wikimedia.org/wikipedia/it/f/fb/Clamorosoalcibali.jpg",
    "stagioni/classifiche-tabellini/tabellino-catania-inter-2-0-clamoroso-al-cibali-1961-calcio-catania.webp": "https://upload.wikimedia.org/wikipedia/it/e/e2/CataniaInter1961.JPG"
}

for rel_target, local_src in local_mappings.items():
    target_path = os.path.join('content/assets/images', rel_target)
    try:
        with Image.open(local_src) as img:
            rgb = img.convert('RGB')
            rgb.save(target_path, 'WEBP', quality=90)
            print(f"Local replaced: {rel_target} from {local_src}")
    except Exception as e:
        print(f"Error {rel_target}: {e}")

for rel_target, url in web_mappings.items():
    target_path = os.path.join('content/assets/images', rel_target)
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content)).convert('RGB')
            img.save(target_path, 'WEBP', quality=90)
            print(f"Web replaced: {rel_target} from {url}")
        else:
            print(f"Failed web {url}: status {r.status_code}")
    except Exception as e:
        print(f"Error web {rel_target}: {e}")
