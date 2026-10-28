import urllib.request
import os
import shutil

images_to_download = [
    {
        "filename": "ross-pelligra.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Rosspelligra_tribunab.jpg"
    },
    {
        "filename": "dirigenza-catania-ssd.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Dirigenza_Catania_SSD.jpg"
    },
    {
        "filename": "angelo-massimino.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/it/5/58/Angelo_Massimino%2C_Catania%2C_1980.jpg"
    },
    {
        "filename": "luciano-gaucci.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/it/f/f1/Luciano_Gaucci_-_1993_circa.jpg"
    },
    {
        "filename": "szymaniak-marcoccio.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/43/Szymaniak_e_Marcoccio.jpg"
    },
    {
        "filename": "torre-del-grifo-village.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Vista_aerea_del_centro_sportivo_Torre_del_Grifo_Village.jpg"
    },
    {
        "filename": "palazzo-giustizia-catania.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Palazzo_di_Giustizia_%28Catania%29.jpg"
    },
    {
        "filename": "piazza-verga-malavoglia.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Catania_Fontana_dei_Malavoglia.jpg"
    },
    {
        "filename": "pala-spedini-raciti-2007.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/64/PalaSpedini_9_febbraio_2007.jpg"
    },
    {
        "filename": "maxi-lopez.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Maxi_Lopez_Catania.jpg"
    },
    {
        "filename": "pablo-barrientos.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/7/76/Pablo_Barrientos.jpg"
    },
    {
        "filename": "papu-gomez.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Papu_G%C3%B3mez_2022.jpg"
    },
    {
        "filename": "sinisa-mihajlovic.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Sini%C5%A1a_Mihajlovi%C4%87.JPG"
    },
    {
        "filename": "pasquale-marino.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Pasquale_marino.JPG"
    },
    {
        "filename": "vincenzo-montella.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/49/Vincenzo_Montella_2.jpg"
    },
    {
        "filename": "walter-zenga.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Walter_zenga.jpg"
    },
    {
        "filename": "gianni-di-marzio.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Gianni_Di_Marzio.jpg"
    },
    {
        "filename": "pro-patria-1908.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/db/ProPatria1908.jpg"
    }
]

dest_dir1 = os.path.abspath("quartz/static/images/photos")
dest_dir2 = os.path.abspath("content/assets/images")
os.makedirs(dest_dir1, exist_ok=True)
os.makedirs(dest_dir2, exist_ok=True)

headers = {'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.it)'}

for item in images_to_download:
    fname = item["filename"]
    url = item["url"]
    p1 = os.path.join(dest_dir1, fname)
    p2 = os.path.join(dest_dir2, fname)
    print(f"Downloading {fname} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(p1, "wb") as f:
                f.write(data)
            shutil.copyfile(p1, p2)
            print(f"  OK: {len(data)} bytes -> {p1}")
    except Exception as e:
        print(f"  ERROR {fname}: {e}")
