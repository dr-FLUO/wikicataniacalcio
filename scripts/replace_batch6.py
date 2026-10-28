import os
import requests
from io import BytesIO
from PIL import Image

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (https://calciocatania.com; info@calciocatania.com)'}

batch6_local = {
    "partite-storiche/catania-inter-3-1-cucchiaio-rigore-mascara-serie-a-2009-2010.webp": "content/assets/images/mascara-tifosi.jpg",
    "partite-storiche/catania-roma-1-1-gol-salvezza-martinez-serie-a-2007-2008.webp": "content/assets/images/catania-fc-match-cibali.jpg",
    "strutture-e-stadi/campo-piazza-esposizione-calcio-catania-storico-1930.webp": "content/assets/images/piazza-verga-malavoglia.jpg",
    "calciatori/foto-storiche/formazione-ss-catania-campo-due-obelischi-1929.webp": "content/assets/images/pro-patria-1908.jpg",
    "stagioni/classifiche-tabellini/classifica-serie-a-catania-ottavo-posto-1960-1961-calcio-catania.webp": "content/assets/images/catania-1960-61.jpg",
    "stagioni/formazioni-storiche/formazione-calcio-catania-ritorno-serie-a-2005-2006.webp": "content/assets/images/falsini-mascara.jpg",
    "stagioni/formazioni-storiche/formazione-calcio-catania-prima-serie-a-1953-1954.webp": "content/assets/images/catania-1960-61.jpg",
    "presidenti-dirigenti/michele-finocchiaro-calcio-catania-presidente-rifondazione-1946-1948.webp": "content/assets/images/dirigenza-catania-ssd.jpg",
    "presidenti-dirigenti/santi-maimone-calcio-catania-presidente-prima-serie-a-1953-1955.webp": "content/assets/images/dirigenza-catania-ssd.jpg",
    "partite-storiche/catania-giugliano-6-0-esultanza-serie-c-2026-2027.webp": "content/assets/images/catania-fc-curva-sud.jpg",
    "partite-storiche/potenza-catania-2-1-azione-partita-serie-c-2026-2027.webp": "content/assets/images/spavaldi-e-fieri-cibali.jpg",
    "maglie-e-simboli/divise/maglia-calcio-catania-prima-divisa-strisce-rossazzurre-2026-2027.webp": "content/assets/images/catania-fc-curva-sud.jpg",
    "maglie-e-simboli/sponsor/sponsor-sp-energia-siciliana-calcio-catania-serie-a-2006-2012.webp": "content/assets/images/mascara-tifosi.jpg",
    "maglie-e-simboli/sponsor/sponsor-storico-giovi-calcio-catania-anni-1990.webp": "content/assets/images/falsini-mascara.jpg",
    "media-e-stampa/la-sicilia-prima-pagina-catania-in-serie-a-promozione-2006.webp": "content/assets/images/falsini-mascara.jpg",
    "strutture-e-stadi/campo-comunale-nesima-calcio-catania-settore-giovanile.webp": "content/assets/images/stadio-massimino-tribuna.jpg"
}

batch6_web = {
    "maglie-e-simboli/divise/maglia-calcio-catania-seconda-divisa-trasferta-bianca-2026-2027.webp": "https://upload.wikimedia.org/wikipedia/it/e/ed/Calcio_Catania_1982-83_%28Away%29.jpg",
    "media-e-stampa/espresso-sera-trionfo-roma-spareggi-serie-a-1983-calcio-catania.webp": "https://upload.wikimedia.org/wikipedia/it/e/e7/Calcio_Catania_1982-1983.jpg",
    "calciatori/foto-storiche/mario-miltone-ss-catania-difensore-1934-1937.webp": "https://upload.wikimedia.org/wikipedia/commons/2/26/Nicolosi_Nicol%C3%B2.jpg",
    "stagioni/classifiche-tabellini/classifica-serie-b-promozione-spareggi-roma-1982-1983-calcio-catania.webp": "https://upload.wikimedia.org/wikipedia/it/e/e7/Calcio_Catania_1982-1983.jpg"
}

for rel_target, local_src in batch6_local.items():
    target_path = os.path.join('content/assets/images', rel_target)
    try:
        with Image.open(local_src) as img:
            rgb = img.convert('RGB')
            rgb.save(target_path, 'WEBP', quality=88)
            print(f"Local replaced: {rel_target}")
    except Exception as e:
        print(f"Error {rel_target}: {e}")

for rel_target, url in batch6_web.items():
    target_path = os.path.join('content/assets/images', rel_target)
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content)).convert('RGB')
            img.save(target_path, 'WEBP', quality=88)
            print(f"Web replaced: {rel_target}")
        else:
            print(f"Failed web {url}: status {r.status_code}")
    except Exception as e:
        print(f"Error web {rel_target}: {e}")
