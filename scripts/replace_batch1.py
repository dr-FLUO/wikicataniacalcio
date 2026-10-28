import os
from PIL import Image

replacements = {
    "allenatori/carmelo-di-bella-calcio-catania-allenatore-record-panchine-1958-1977.webp": "content/assets/images/carmelo-di-bella.jpg",
    "allenatori/diego-simeone-calcio-catania-allenatore-serie-a-2011.webp": "content/assets/images/diego-simeone.jpg",
    "allenatori/pasquale-marino-calcio-catania-allenatore-promozione-serie-a-2005-2007.webp": "content/assets/images/pasquale-marino.jpg",
    "allenatori/vincenzo-montella-calcio-catania-allenatore-serie-a-2011-2012.webp": "content/assets/images/vincenzo-montella.jpg",
    "allenatori/walter-zenga-calcio-catania-allenatore-serie-a-2008-2009.webp": "content/assets/images/walter-zenga.jpg",
    "presidenti-dirigenti/angelo-massimino-calcio-catania-presidente-storico-1969-1996.webp": "content/assets/images/angelo-massimino.jpg",
    "presidenti-dirigenti/ross-pelligra-calcio-catania-presidente-catania-fc-2022-oggi.webp": "content/assets/images/ross-pelligra.jpg",
    "strutture-e-stadi/stadio-angelo-massimino-cibali-calcio-catania-tribuna-panoramica.webp": "content/assets/images/stadio-massimino-panoramica.jpg",
    "strutture-e-stadi/centro-sportivo-torre-del-grifo-village-calcio-catania.webp": "content/assets/images/torre-del-grifo-village.jpg",
    "tifoseria-e-curva/curva-nord-catania-striscione-falange-dassalto-1979.webp": "content/assets/images/curva-nord-storica.jpg",
    "calciatori/figurine/aldo-cantarutti-calcio-catania-figurina-panini-1982-1983.webp": "content/assets/images/players/467_aldo-cantarutti.jpg",
    "calciatori/figurine/aquilino-bonfanti-calcio-catania-figurina-panini-1970-1971.webp": "content/assets/images/players/578_aquilino-bonfanti.jpg",
    "calciatori/figurine/cinesinho-calcio-catania-figurina-panini-1963-1965.webp": "content/assets/images/players/639_sidney-cunha-cinesinho.jpg",
    "calciatori/figurine/damiano-morra-calcio-catania-figurina-panini-1975-1984.webp": "content/assets/images/players/477_damiano-morra.jpg",
    "calciatori/figurine/giorgio-mastropasqua-calcio-catania-figurina-panini-1982-1983.webp": "content/assets/images/players/476_giorgio-mastropasqua.jpg",
    "calciatori/figurine/guido-biondi-calcio-catania-figurina-panini-1975-1976.webp": "content/assets/images/players/545_guido-biondi.jpg",
    "calciatori/figurine/horst-szymaniak-calcio-catania-figurina-panini-1961-1963.webp": "content/assets/images/players/664_horst-szymaniak.jpg",
    "calciatori/figurine/memo-prenna-calcio-catania-figurina-lampo-1960-1961.webp": "content/assets/images/players/648_adelmo-prenna.jpg",
    "calciatori/rosa-attuale/roberto-inglese-calcio-catania-attaccante-bomber-2026-2027.webp": "content/assets/images/players/1087_roberto-inglese.jpg",
    "partite-storiche/palermo-catania-0-4-gol-centrocampo-mascara-serie-a-2008-2009.webp": "content/assets/images/mascara-spinesi.jpg",
}

done = 0
for rel_target, src in replacements.items():
    target_path = os.path.join('content/assets/images', rel_target)
    if os.path.exists(src):
        try:
            with Image.open(src) as img:
                # convert to RGB and save as webp
                rgb = img.convert('RGB')
                rgb.save(target_path, 'WEBP', quality=88)
                done += 1
                print(f"Replaced {rel_target} with {src} ({rgb.size})")
        except Exception as e:
            print(f"Error converting {src}: {e}")
    else:
        print(f"Source not found: {src}")

print(f"\nBatch 1 completed: {done}/{len(replacements)} replaced.")
