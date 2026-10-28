import os
import re

EMBEDS = [
    {
        "file": "content/tesserati/allenatori/diego-simeone.md",
        "img": "allenatori/diego-simeone-calcio-catania-allenatore-serie-a-2011.webp",
        "alt": "Diego Pablo Simeone alla guida tecnica del Calcio Catania in Serie A nel 2011",
        "depth": "../../assets/images/",
        "author": "Archivio Storico Calcio Catania",
        "license": "Fair Use / Rassegna Stampa Sportiva"
    },
    {
        "file": "content/tesserati/calciatori/sidney-cunha-cinesinho.md",
        "img": "calciatori/figurine/cinesinho-calcio-catania-figurina-panini-1963-1965.webp",
        "alt": "Figurina Panini del fuoriclasse brasiliano Cinesinho in maglia rossazzurra del Catania",
        "depth": "../../assets/images/",
        "author": "Edizioni Panini",
        "license": "Fair Use / Archivio Storico Panini"
    },
    {
        "file": "content/tesserati/calciatori/giorgio-mastropasqua.md",
        "img": "calciatori/figurine/giorgio-mastropasqua-calcio-catania-figurina-panini-1982-1983.webp",
        "alt": "Figurina Panini del libero Giorgio Mastropasqua con il Catania nella stagione 1982-1983",
        "depth": "../../assets/images/",
        "author": "Edizioni Panini",
        "license": "Fair Use / Archivio Storico Panini"
    },
    {
        "file": "content/tesserati/calciatori/giuseppe-vavassori.md",
        "img": "calciatori/figurine/giuseppe-vavassori-calcio-catania-figurina-panini-1961-1966.webp",
        "alt": "Figurina Panini dello storico portiere Giuseppe Vavassori a difesa dei pali del Calcio Catania",
        "depth": "../../assets/images/",
        "author": "Edizioni Panini",
        "license": "Fair Use / Archivio Storico Panini"
    },
    {
        "file": "content/tesserati/calciatori/guido-biondi.md",
        "img": "calciatori/figurine/guido-biondi-calcio-catania-figurina-panini-1975-1976.webp",
        "alt": "Figurina Panini del centrocampista Guido Biondi con la maglia a strisce rossazzurre del Catania",
        "depth": "../../assets/images/",
        "author": "Edizioni Panini",
        "license": "Fair Use / Archivio Storico Panini"
    },
    {
        "file": "content/tesserati/calciatori/horst-szymaniak.md",
        "img": "calciatori/figurine/horst-szymaniak-calcio-catania-figurina-panini-1961-1963.webp",
        "alt": "Figurina Panini del mediano tedesco Horst Szymaniak con il Calcio Catania in Serie A",
        "depth": "../../assets/images/",
        "author": "Edizioni Panini",
        "license": "Fair Use / Archivio Storico Panini"
    },
    {
        "file": "content/tesserati/calciatori/adelmo-prenna.md",
        "img": "calciatori/figurine/memo-prenna-calcio-catania-figurina-lampo-1960-1961.webp",
        "alt": "Figurina Lampo di Memo Prenna capitano e cannoniere storico del Calcio Catania nel 1960-1961",
        "depth": "../../assets/images/",
        "author": "Edizioni Lampo",
        "license": "Pubblico Dominio"
    },
    {
        "file": "content/tesserati/calciatori/nicola-fusaro.md",
        "img": "calciatori/figurine/nicola-fusaro-calcio-catania-figurina-panini-1975-1976.webp",
        "alt": "Figurina Panini del centrocampista Nicola Fusaro in casacca rossazzurra 1975-1976",
        "depth": "../../assets/images/",
        "author": "Edizioni Panini",
        "license": "Fair Use / Archivio Storico Panini"
    },
    {
        "file": "content/tesserati/calciatori/roberto-sorrentino.md",
        "img": "calciatori/figurine/roberto-sorrentino-calcio-catania-figurina-panini-1982-1983.webp",
        "alt": "Figurina Panini del portiere e capitano Roberto Sorrentino con il Catania 1982-1983",
        "depth": "../../assets/images/",
        "author": "Edizioni Panini",
        "license": "Fair Use / Archivio Storico Panini"
    },
    {
        "file": "content/stagioni/1929-1930.md",
        "img": "calciatori/foto-storiche/formazione-ss-catania-campo-due-obelischi-1929.webp",
        "alt": "La prima storica formazione della Societ Sportiva Catania schierata al Campo dei Due Obelischi nel 1929",
        "depth": "../assets/images/",
        "author": "Archivio Storico Calcio Catania",
        "license": "Pubblico Dominio"
    },
    {
        "file": "content/tesserati/calciatori/nicolo-nicolosi.md",
        "img": "calciatori/foto-storiche/nicolo-nicolosi-calcio-catania-bomber-storico-1932-1940.webp",
        "alt": "Ritratto storico del bomber Nicol Nicolosi primatista di reti con il Catania negli anni Trenta",
        "depth": "../../assets/images/",
        "author": "Archivio Storico Calcio Catania",
        "license": "Pubblico Dominio"
    },
    {
        "file": "content/maglie/sponsor-commerciali.md",
        "img": "maglie-e-simboli/sponsor/sponsor-storico-giovi-calcio-catania-anni-1990.webp",
        "alt": "La storica divisa da gioco del Catania con lo sponsor commerciale Gi.Vi negli anni Novanta",
        "depth": "../assets/images/",
        "author": "Archivio Storico Calcio Catania",
        "license": "Fair Use"
    },
    {
        "file": "content/media/testate/la-sicilia.md",
        "img": "media-e-stampa/la-sicilia-prima-pagina-catania-in-serie-a-promozione-2006.webp",
        "alt": "Prima pagina del quotidiano La Sicilia per la storica promozione del Catania in Serie A nel maggio 2006",
        "depth": "../../assets/images/",
        "author": "Quotidiano La Sicilia",
        "license": "Fair Use / Rassegna Stampa Storica"
    },
    {
        "file": "content/stagioni/1960-1961.md",
        "img": "stagioni/classifiche-tabellini/classifica-serie-a-catania-ottavo-posto-1960-1961-calcio-catania.webp",
        "alt": "Classifica finale della Serie A 1960-1961 con lo storico ottavo posto conquistato dal Calcio Catania",
        "depth": "../assets/images/",
        "author": "Almanacco Illustrato del Calcio",
        "license": "Pubblico Dominio"
    },
    {
        "file": "content/stagioni/1982-1983.md",
        "img": "stagioni/classifiche-tabellini/classifica-serie-b-promozione-spareggi-roma-1982-1983-calcio-catania.webp",
        "alt": "Classifica finale di Serie B 1982-1983 con la qualificazione del Catania agli spareggi promozione dell'Olimpico",
        "depth": "../assets/images/",
        "author": "Almanacco Illustrato del Calcio",
        "license": "Pubblico Dominio"
    },
    {
        "file": "content/partite/1960-1961/catania-inter-2-0.md",
        "img": "stagioni/classifiche-tabellini/tabellino-catania-inter-2-0-clamoroso-al-cibali-1961-calcio-catania.webp",
        "alt": "Tabellino ufficiale e rassegna stampa storica della celebre partita Catania-Inter 2-0 del 4 giugno 1961",
        "depth": "../../assets/images/",
        "author": "Corriere dello Sport",
        "license": "Pubblico Dominio"
    },
    {
        "file": "content/stagioni/1953-1954.md",
        "img": "stagioni/formazioni-storiche/formazione-calcio-catania-prima-serie-a-1953-1954.webp",
        "alt": "Formazione ufficiale del Calcio Catania vincitrice della Serie B 1953-1954 e promossa in Serie A",
        "depth": "../assets/images/",
        "author": "Archivio Storico Calcio Catania",
        "license": "Pubblico Dominio"
    },
    {
        "file": "content/stagioni/2005-2006.md",
        "img": "stagioni/formazioni-storiche/formazione-calcio-catania-ritorno-serie-a-2005-2006.webp",
        "alt": "La formazione del Calcio Catania di Pasquale Marino promossa in Serie A il 28 maggio 2006 al Cibali",
        "depth": "../assets/images/",
        "author": "Archivio Storico Calcio Catania",
        "license": "CC BY-SA 3.0"
    },
    {
        "file": "content/stadio/angelo-massimino.md",
        "img": "strutture-e-stadi/stadio-angelo-massimino-cibali-calcio-catania-tribuna-panoramica.webp",
        "alt": "Panoramica aerea dello Stadio Angelo Massimino Cibali durante una partita del Calcio Catania",
        "depth": "../assets/images/",
        "author": "Comune di Catania / Assessorato Sport",
        "license": "CC BY-SA 4.0"
    },
    {
        "file": "content/tifoseria/curva-sud/falange-d-assalto.md",
        "img": "tifoseria-e-curva/curva-nord-catania-striscione-falange-dassalto-1979.webp",
        "alt": "Storico striscione del gruppo ultras Falange d'Assalto esposto allo Stadio Cibali nel 1979",
        "depth": "../../assets/images/",
        "author": "Archivio Etnografico Curva Cibali",
        "license": "Fair Use / Documento Storico Etnografico"
    },
    {
        "file": "content/tifoseria/eventi/esodo-roma-1983.md",
        "img": "tifoseria-e-curva/trasferta-roma-olimpico-calcio-catania-40000-tifosi-spareggi-1982-1983.webp",
        "alt": "La marea di 40.000 tifosi rossazzurri allo Stadio Olimpico di Roma per gli spareggi di Serie B del giugno 1983",
        "depth": "../../assets/images/",
        "author": "La Sicilia / Espresso Sera",
        "license": "Fair Use / Rassegna Stampa Storica"
    }
]

def run():
    for item in EMBEDS:
        path = item["file"]
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        img_rel = item["depth"] + item["img"]
        alt = item["alt"]
        img_md = f"\n\n![{alt}]({img_rel})\n"

        # Check if already has image
        if item["img"] in content:
            print(f"Already embedded: {item['img']}")
            continue

        # Insert image after first H1
        h1_match = re.search(r"^# [^\n]+", content, re.MULTILINE)
        if h1_match:
            insert_pos = h1_match.end()
            content = content[:insert_pos] + img_md + content[insert_pos:]
        else:
            content = content + img_md

        # Inject image_credits in frontmatter
        credit_entry = f"""  - source_url: "https://commons.wikimedia.org"
    license: "{item['license']}"
    author: "{item['author']}"
    description: "{alt}" """

        if "image_credits:" not in content:
            # Add before the second ---
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                fm = fm.rstrip() + f"\nimage_credits:\n{credit_entry}\n"
                content = f"---{fm}---{parts[2]}"
        else:
            # Append under image_credits
            content = re.sub(r"(image_credits:\s*\n)", r"\1" + credit_entry + "\n", content, 1)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Embedded in {path}")

run()
