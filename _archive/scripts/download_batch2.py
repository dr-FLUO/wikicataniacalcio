import requests
from PIL import Image
from io import BytesIO
import os
import time

headers = {
    'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://github.com/wikicalciocatania; bot@calciocatania.com)'
}

downloads = {
    "allenatori/cristiano-lucarelli-calcio-catania-allenatore-coppa-italia-serie-c-2017-2024.webp": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Cristiano_Lucarelli_2026_%28headshot%29.jpg/640px-Cristiano_Lucarelli_2026_%28headshot%29.jpg",
    "allenatori/domenico-toscano-calcio-catania-allenatore-serie-c-2024-2027.webp": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Domenico_Toscano.jpg/640px-Domenico_Toscano.jpg",
    "allenatori/egizio-rubino-calcio-catania-allenatore-serie-a-1968-1974.webp": "https://upload.wikimedia.org/wikipedia/it/thumb/8/8c/Egizio_Rubino.jpg/640px-Egizio_Rubino.jpg",
    "allenatori/guido-mazzetti-calcio-catania-allenatore-anni-1970.webp": "https://upload.wikimedia.org/wikipedia/it/5/50/Guido_Mazzetti_-_Associazione_Calcio_Perugia.jpeg",
    "calciatori/figurine/claudio-ranieri-calcio-catania-figurina-panini-1982-1983.webp": "https://upload.wikimedia.org/wikipedia/commons/2/24/Claudio_Ranieri_Inter_%28cropped%29.jpg",
    "calciatori/figurine/giancarlo-danova-calcio-catania-figurina-panini-1965-1966.webp": "https://upload.wikimedia.org/wikipedia/it/6/61/Giancarlo_Danova.jpg",
    "calciatori/figurine/loris-boni-calcio-catania-figurina-panini-1979-1980.webp": "https://upload.wikimedia.org/wikipedia/commons/c/c2/1974%E2%80%9375_UC_Sampdoria_-_Loris_Boni.jpg",
    "calciatori/foto-storiche/amedeo-biavati-calcio-catania-attaccante-passo-doppio-1935-1937.webp": "https://upload.wikimedia.org/wikipedia/it/0/0a/Amedeo_Biavati.jpg"
}

for rel_target, url in downloads.items():
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
    time.sleep(1)
