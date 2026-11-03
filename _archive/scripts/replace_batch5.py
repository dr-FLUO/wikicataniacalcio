import os
import requests
from io import BytesIO
from PIL import Image

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'}

batch5 = {
    "presidenti-dirigenti/antonino-pulvirenti-calcio-catania-presidente-serie-a-2004-2015.webp": "https://lasicilia.cdn.m33cloud.com/resizer/700/-1/true/2021/04/19/8c4cb9868f95a425b7a739c9d9a2649a_1618818081179.jpg--.jpg",
    "presidenti-dirigenti/pietro-lo-monaco-calcio-catania-amministratore-delegato-2004-2012.webp": "https://lasicilia.cdn.m33cloud.com/resizer/700/-1/true/2021/04/15/lo_monaco_1618525649646.jpg--pietro_lo_monaco.jpg",
    "maglie-e-simboli/sponsor/maglia-calcio-catania-sponsor-haribo-serie-a-1983-1984.webp": "https://upload.wikimedia.org/wikipedia/it/e/ed/Calcio_Catania_1982-83_%28Away%29.jpg",
    "stagioni/formazioni-storiche/formazione-calcio-catania-spareggi-roma-serie-b-1982-1983.webp": "https://upload.wikimedia.org/wikipedia/it/e/e7/Calcio_Catania_1982-1983.jpg",
    "tifoseria-e-curva/trasferta-roma-olimpico-calcio-catania-40000-tifosi-spareggi-1982-1983.webp": "https://upload.wikimedia.org/wikipedia/it/e/e7/Calcio_Catania_1982-1983.jpg",
}

for rel_target, url in batch5.items():
    target_path = os.path.join('content/assets/images', rel_target)
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content)).convert('RGB')
            img.save(target_path, 'WEBP', quality=88)
            print(f"Downloaded and saved: {rel_target} ({img.size})")
        else:
            print(f"Failed {url}: status {r.status_code}")
    except Exception as e:
        print(f"Error {rel_target}: {e}")
