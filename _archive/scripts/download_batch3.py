import requests
from PIL import Image
from io import BytesIO
import os

headers = {
    'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'
}

batch3 = {
    "allenatori/cristiano-lucarelli-calcio-catania-allenatore-coppa-italia-serie-c-2017-2024.webp": "https://upload.wikimedia.org/wikipedia/commons/2/25/Cristiano_Lucarelli_2026_%28headshot%29.jpg",
    "allenatori/domenico-toscano-calcio-catania-allenatore-serie-c-2024-2027.webp": "https://upload.wikimedia.org/wikipedia/commons/5/57/Domenico_Toscano.jpg",
    "allenatori/egizio-rubino-calcio-catania-allenatore-serie-a-1968-1974.webp": "https://upload.wikimedia.org/wikipedia/it/8/8c/Egizio_Rubino.jpg",
    "calciatori/rosa-attuale/stefano-sturaro-calcio-catania-centrocampista-leader-2026-2027.webp": "https://upload.wikimedia.org/wikipedia/commons/7/76/Frosinone_Calcio_-_Stadio_Matusa_-_vs_Juventus_7_2_2016_0-2_-_DSC_8609_-_Stefano_Sturaro_%28cropped%29.jpg"
}

for rel_target, url in batch3.items():
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
