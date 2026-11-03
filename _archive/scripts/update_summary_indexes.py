# -*- coding: utf-8 -*-
import os
import re

def update_summary_indexes():
    # 1. content/03-tesserati/index.md
    p1 = 'content/03-tesserati/index.md'
    with open(p1, 'r', encoding='utf-8') as f:
        t1 = f.read()

    # Biagianti
    t1 = re.sub(
        r'\|\s*\*\*1º\*\*\s*\|\s*\[\[tesserati/calciatori/marco-biagianti\\\|Marco Biagianti\]\][^\n]+',
        r'| **1º** | [[tesserati/calciatori/marco-biagianti\\|Marco Biagianti]] | Centrocampista | 2007–2013, 2016–2020 | **284** (255 camp. + 11 PO / 148 Serie A) | 12 | **Primatista assoluto di presenze**; capitano in Serie A e in Serie C. |',
        t1
    )
    # Morra
    t1 = re.sub(
        r'\|\s*\*\*2º\*\*\s*\|\s*\[\[tesserati/calciatori/damiano-morra\\\|Damiano Morra\]\][^\n]+',
        r'| **2º** | [[tesserati/calciatori/damiano-morra\\|Damiano Morra]] | Mediano | 1975–1984 | **321** (281 camp. + 3 spar. / 25 Serie A) | 28 | Bandiera per 9 stagioni consecutive con 2 promozioni (1980 e 1983); 281 gare in campionato. |',
        t1
    )
    # Izco
    t1 = re.sub(
        r'\|\s*\*\*3º\*\*\s*\|\s*\[\[tesserati/calciatori/mariano-izco\\\|Mariano Izco\]\][^\n]+',
        r'| **3º** | [[tesserati/calciatori/mariano-izco\\|Mariano Izco]] | Centrocampista | 2006–2014, 2020–2022 | **258** (280 tot. / **218 Serie A**) | 7 | **Primatista assoluto di presenze con il Catania in Serie A (218)**; 280 gare giocate complessive. |',
        t1
    )
    # Lodi presenze
    t1 = re.sub(
        r'\|\s*\*\*5º\*\*\s*\|\s*\[\[tesserati/calciatori/francesco-lodi\\\|Francesco Lodi\]\][^\n]+',
        r'| **5º** | [[tesserati/calciatori/francesco-lodi\\|Francesco Lodi]] | Regista | 2011–13, 2014, 2017–20, 2022–23 | **239** (215 camp. + 10 post / 105 Serie A) | 54 | Protagonista in quattro cicli tra Serie A, B, C e il trionfo in [[stagioni/2022-2023\\|Serie D 2022-23]]. |',
        t1
    )
    # Mascara presenze
    t1 = re.sub(
        r'\|\s*\*\*6º\*\*\s*\|\s*\[\[tesserati/calciatori/giuseppe-mascara\\\|Giuseppe Mascara\]\][^\n]+',
        r'| **6º** | [[tesserati/calciatori/giuseppe-mascara\\|Giuseppe Mascara]] | Attaccante / Fantasista | 2003–2004, 2005–2011 | **238** (226 camp. / 149 Serie A) | 60 | Primo calciatore del Catania in Nazionale A (2009); simbolo dell\'era moderna con 60 reti ufficiali. |',
        t1
    )
    # Nicolosi marcatori
    t1 = re.sub(
        r'\|\s*\*\*1º\*\*\s*\|\s*\[\[tesserati/calciatori/nicolo-nicolosi\\\|Nicolò Nicolosi\]\][^\n]+',
        r'| **1º** | [[tesserati/calciatori/nicolo-nicolosi\\|Nicolò Nicolosi]] | *"Cocò"* | 1932–37, 1939–40, 1942–43, 1947–49 | **78** (71 camp.) | 156 | **Miglior marcatore assoluto della storia del Catania**; 1ª promozione in B ([[stagioni/1933-1934\\|1933-34]]). |',
        t1
    )
    # Mascara marcatori
    t1 = re.sub(
        r'\|\s*\*\*2º\*\*\s*\|\s*\[\[tesserati/calciatori/giuseppe-mascara\\\|Giuseppe Mascara\]\][^\n]+',
        r'| **2º** | [[tesserati/calciatori/giuseppe-mascara\\|Giuseppe Mascara]] | *Beppe* | 2003–2004, 2005–2011 | **60** (58 camp. / 31 Serie A) | 238 | Autore di gol iconici nel [[partite/precedenti/palermo\\|Derby di Palermo (0-4)]] e contro l\'[[partite/precedenti/inter\\|Inter (3-1)]]. |',
        t1
    )
    # Lodi marcatori
    t1 = re.sub(
        r'\|\s*\*\*3º\*\*\s*\|\s*\[\[tesserati/calciatori/francesco-lodi\\\|Francesco Lodi\]\][^\n]+',
        r'| **3º** | [[tesserati/calciatori/francesco-lodi\\|Francesco Lodi]] | *"Ciccio"* | 2011–2023 (4 cicli) | **54** (47 camp. / 20 Serie A) | 239 | Centrocampista più prolifico della storia rossazzurra; maestro delle punizioni. |',
        t1
    )

    with open(p1, 'w', encoding='utf-8') as f:
        f.write(t1)
    print('Updated content/03-tesserati/index.md')

    # 2. content/03-tesserati/calciatori/storici/index.md
    p2 = 'content/03-tesserati/calciatori/storici/index.md'
    with open(p2, 'r', encoding='utf-8') as f:
        t2 = f.read()

    t2 = re.sub(
        r'\|\s*\[\[03-tesserati/calciatori/storici/marco-biagianti\\\|Marco Biagianti\]\]\s*\|\s*Centrocampista\s*\|\s*\*\*284\*\*\s*/\s*6\s*\|[^\n]+',
        r'| [[03-tesserati/calciatori/storici/marco-biagianti\\|Marco Biagianti]] | Centrocampista | **284** / 12 | 2007–13, 2016–20 | **Record assoluto di presenze** in gare ufficiali col Catania |',
        t2
    )
    t2 = re.sub(
        r'\|\s*\[\[03-tesserati/calciatori/storici/damiano-morra\\\|Damiano Morra\]\]\s*\|\s*Mediano\s*\|\s*\*\*281\*\*\s*/\s*12\s*\|[^\n]+',
        r'| [[03-tesserati/calciatori/storici/damiano-morra\\|Damiano Morra]] | Mediano | **321** (281 camp.) / 28 | 1975–1984 | Bandiera per 9 stagioni consecutive (281 in camp., 321 tot.) e 2 promozioni |',
        t2
    )
    t2 = re.sub(
        r'\|\s*\[\[03-tesserati/calciatori/storici/mariano-izco\\\|Mariano Izco\]\]\s*\|\s*Centrocampista\s*\|\s*\*\*280\*\*\s*/\s*6\s*\|[^\n]+',
        r'| [[03-tesserati/calciatori/storici/mariano-izco\\|Mariano Izco]] | Centrocampista | **258** (280 tot.) / 7 | 2006–14, 2020–22 | **Record assoluto di presenze in Serie A col Catania (218)** (280 gare complessive) |',
        t2
    )
    t2 = re.sub(
        r'\|\s*\[\[03-tesserati/calciatori/storici/francesco-lodi\\\|Francesco Lodi\]\]\s*\|\s*Regista\s*\|\s*\*\*238\*\*\s*/\s*53\s*\|[^\n]+',
        r'| [[03-tesserati/calciatori/storici/francesco-lodi\\|Francesco Lodi]] | Regista | **239** / 54 | 2011–23 (4 cicli) | Centrocampista più prolifico e re dei calci piazzati |',
        t2
    )
    t2 = re.sub(
        r'\|\s*\[\[03-tesserati/calciatori/storici/giuseppe-mascara\\\|Giuseppe Mascara\]\]\s*\|\s*Attaccante\s*\|\s*\*\*235\*\*\s*/\s*60\s*\|[^\n]+',
        r'| [[03-tesserati/calciatori/storici/giuseppe-mascara\\|Giuseppe Mascara]] | Attaccante | **238** / 60 | 2003–04, 2005–11 | Simbolo dell\'era moderna (60 gol e 238 presenze), primo etneo in Nazionale A |',
        t2
    )
    t2 = re.sub(
        r'\|\s*\[\[03-tesserati/calciatori/storici/nicolo-nicolosi\\\|Nicolò Nicolosi\]\]\s*\|\s*Centravanti\s*\|\s*149\s*/\s*\*\*78\*\*\s*\|[^\n]+',
        r'| [[03-tesserati/calciatori/storici/nicolo-nicolosi\\|Nicolò Nicolosi]] | Centravanti | 156 / **78** | 1932–49 (4 cicli) | **Miglior marcatore assoluto di tutti i tempi** (78 gol in 156 gare) |',
        t2
    )

    with open(p2, 'w', encoding='utf-8') as f:
        f.write(t2)
    print('Updated content/03-tesserati/calciatori/storici/index.md')

if __name__ == '__main__':
    update_summary_indexes()
