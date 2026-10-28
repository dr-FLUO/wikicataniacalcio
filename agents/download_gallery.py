import json
import pathlib
import shutil
import time
import urllib.request

manifest = json.loads(
    pathlib.Path("quartz/static/images/commons_manifest.json").read_text(encoding="utf-8")
)

selection = {
    "File:Calcio Catania 1960-1961.jpg": "catania-1960-61.jpg",
    "File:Logo CATANIA FC.svg": "logo-catania-fc.svg",
    "File:Stadio Angelo Massimino 202302 CurvaNordPartita.jpg": "curva-nord-coreografia.jpg",
    "File:Curva Nord di Catania.jpg": "curva-nord-storica.jpg",
    "File:Spavaldiefieri.jpg": "spavaldi-e-fieri-cibali.jpg",
    "File:Stadio Massimino.jpg": "stadio-massimino-panoramica.jpg",
    "File:Stadio Angelo Massimino (295535050).jpg": "stadio-massimino-tribuna.jpg",
    "File:Catania FC v Giugliano Calcio 1928, 26 January 2025 - 08.jpg": "catania-fc-match-cibali.jpg",
    "File:Catania FC v Giugliano Calcio 1928, 26 January 2025 - 17.jpg": "catania-fc-curva-sud.jpg",
    "File:Mascara spinesi.jpg": "mascara-spinesi.jpg",
    "File:Mascara tifosi.jpg": "mascara-tifosi.jpg",
    "File:Falsini Mascara.jpg": "falsini-mascara.jpg",
    "File:Marco Biagianti a Massannunziata.JPG": "marco-biagianti.jpg",
    "File:Mariano Julio Izco.jpg": "mariano-izco.jpg",
    "File:Gonzalo Bergessio.jpg": "gonzalo-bergessio.jpg",
    "File:Francesco Lodi.jpg": "francesco-lodi.jpg",
    "File:CarmeloDiBella.jpg": "carmelo-di-bella.jpg",
    "File:Rolando Maran (cropped).JPG": "rolando-maran.jpg",
    "File:Diego Simeone - 01.jpg": "diego-simeone.jpg",
    "File:Liotru Fontana dellElefante (1221745427).jpg": "fontana-elefante-liotru.jpg",
    "File:N.° 1771. Catania. Fontana dell' Elefante - btv1b53262300f (1 of 2).jpg": "liotru-storico-1865.jpg",
}

static_dir = pathlib.Path("quartz/static/images/photos")
content_dir = pathlib.Path("content/assets/images")
static_dir.mkdir(parents=True, exist_ok=True)
content_dir.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "WikiCalcioCataniaBot/1.0 (https://localhost:8080; historical encyclopedia)"
}

for wiki_title, filename in selection.items():
    info = manifest.get(wiki_title)
    if not info:
        print(f"Skipping {wiki_title}, not in manifest")
        continue
    url = info["orig_url"] if filename.endswith(".svg") else info["url"]
    url = url.split("?")[0]
    dest = static_dir / filename
    if not dest.exists():
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                dest.write_bytes(data)
                shutil.copyfile(dest, content_dir / filename)
                print(f"Downloaded {filename} ({len(data)} bytes) [{info['license']} - {info['artist']}]")
            time.sleep(0.3)
        except Exception as e:
            print(f"Error downloading {filename} from {url}: {e}")
    else:
        shutil.copyfile(dest, content_dir / filename)
        print(f"Already exists: {filename}")
