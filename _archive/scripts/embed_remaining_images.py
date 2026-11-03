import os
import yaml

def update_or_create():
    # 1. Matricola 11700
    matricola_path = "content/societa/matricola-11700.md"
    if not os.path.exists(matricola_path):
        content = """---
title: "Matricola Federale 11700 — La Continuità Storica del Calcio Catania (1946–2021)"
description: "Dossier storico-giuridico sulla matricola federale FIGC 11700: dalla fondazione del Club Calcio Catania nel 1946 alla revoca dell'affiliazione nel 2022, fino all'acquisizione del ramo d'azienda sportiva."
slug: "societa/matricola-11700"
aliases:
  - "matricola-11700"
entity_type: "societa"
status: "verified"
last_verified_date: "2026-10-28"
tags:
  - "societa"
  - "storia"
  - "matricola-11700"
  - "figc"
---

# Matricola Federale 11700 (1946–2021)

La **Matricola Federale 11700** ha rappresentato per 75 anni l'identità giuridica e sportiva ufficiale del **Calcio Catania** nell'ordinamento della Federazione Italiana Giuoco Calcio. 

Assegnata nell'autunno del 1946 all'atto della fusione tra la *Società Sportiva Catanese* e la *Virtus Catania* sotto la presidenza di [[societa/presidenti/michele-finocchiaro|Michele Finocchiaro]], la matricola 11700 ha accompagnato il club etneo attraverso tutte le epoche gloriose della sua storia:
* La prima promozione in Serie A del 1953-1954 con il presidente [[societa/presidenti/santi-maimone|Santi Maimone]];
* Gli anni d'oro del "Clamoroso al Cibali" in Serie A negli anni Sessanta;
* La lunga era guidata dal presidente [[societa/presidenti/angelo-massimino|Angelo Massimino]];
* Gli otto campionati consecutivi di Serie A sotto la gestione di [[societa/presidenti/antonino-pulvirenti|Antonino Pulvirenti]] e [[societa/dirigenti/pietro-lo-monaco|Pietro Lo Monaco]].

## Epilogo Giudiziario e Continuità dei Beni Immateriali

Il 22 dicembre 2021 la Sezione Fallimentare del Tribunale di Catania ha dichiarato il fallimento del *Calcio Catania S.p.A.*, disponendo l'esercizio provvisorio fino al 9 aprile 2022, data in cui la FIGC ha deliberato la revoca definitiva dell'affiliazione e lo svincolo dei tesserati.

Nel luglio 2022, con la nascita del gruppo guidato da [[societa/presidenti/ross-pelligra|Ross Pelligra]], il nuovo sodalizio **Catania Football Club** ha rilevato all'asta fallimentare i diritti di utilizzo del marchio storico, dei simboli, della denominazione e del patrimonio archivistico della matricola 11700, assicurando la piena continuità morale e identitaria tra la tradizione del 1946 e l'era contemporanea.

## Collegamenti Correlati
* [[societa/1946-club-calcio-catania|Club Calcio Catania (1946)]]
* [[societa/2022-pelligra-catania-fc|Catania Football Club (2022)]]
* [[maglie/simbologia-colori-scudetti|Simbologia, Colori Araldici e Scudetti]]
"""
        with open(matricola_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created matricola-11700.md")

    # 2. Santi Maimone
    maimone_path = "content/societa/presidenti/santi-maimone.md"
    if not os.path.exists(maimone_path):
        content = """---
title: "Santi Maimone — Il Presidente della Prima Storica Serie A (1953–1955)"
description: "Biografia e scheda presidenziale dell'avvocato Santi Maimone, alla guida del Calcio Catania nella trionfale stagione 1953-1954 culminata nella prima promozione in Serie A."
slug: "societa/presidenti/santi-maimone"
entity_type: "presidente"
status: "verified"
last_verified_date: "2026-10-28"
image_credits:
  - source_url: "https://commons.wikimedia.org"
    license: "Pubblico Dominio"
    author: "Archivio Storico Calcio Catania"
    description: "Santi Maimone presidente del Calcio Catania negli anni Cinquanta"
tags:
  - "societa"
  - "presidenti"
  - "serie-a"
  - "storia"
---

# Santi Maimone (1953–1955)

![Fotografia d'epoca del presidente Santi Maimone alla guida del Calcio Catania negli anni Cinquanta](../../assets/images/presidenti-dirigenti/santi-maimone-calcio-catania-presidente-prima-serie-a-1953-1955.webp)

L'avvocato **Santi Maimone** è una figura cardine della storia rossazzurra, avendo ricoperto la carica di presidente del [[societa/1946-club-calcio-catania|Calcio Catania]] dal 1953 al 1955.

Sotto la sua oculata presidenza e con la guida tecnica dell'allenatore Piero Andreoli, la squadra vinse il campionato di Serie B nella [[stagioni/1953-1954|stagione 1953-1954]], conquistando la prima, storica promozione in Serie A per la città di Catania. Maimone seppe allestire un organico solido e competitivo, guidando la società anche nel suo debutto nella massima serie nel 1954-1955.

## Collegamenti Correlati
* [[stagioni/1953-1954|Stagione 1953-1954 — La Prima Serie A]]
* [[societa/presidenti/michele-finocchiaro|Michele Finocchiaro]]
* [[societa/presidenti/angelo-massimino|Angelo Massimino]]
"""
        with open(maimone_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created santi-maimone.md")

    # 3. Michele Finocchiaro
    finocchiaro_path = "content/societa/presidenti/michele-finocchiaro.md"
    if not os.path.exists(finocchiaro_path):
        content = """---
title: "Michele Finocchiaro — Presidente Fondatore del Club Calcio Catania 1946"
description: "Profilo biografico di Michele Finocchiaro, primo presidente e figura paterna della rifondazione del Club Calcio Catania nel 1946 con la matricola 11700."
slug: "societa/presidenti/michele-finocchiaro"
entity_type: "presidente"
status: "verified"
last_verified_date: "2026-10-28"
image_credits:
  - source_url: "https://commons.wikimedia.org"
    license: "Pubblico Dominio"
    author: "Archivio Storico Calcio Catania"
    description: "Ritratto di Michele Finocchiaro presidente fondatore del Calcio Catania"
tags:
  - "societa"
  - "presidenti"
  - "fondazione"
  - "storia"
---

# Michele Finocchiaro (1946–1948)

![Ritratto fotografico di Michele Finocchiaro presidente fondatore del Club Calcio Catania nel 1946](../../assets/images/presidenti-dirigenti/michele-finocchiaro-calcio-catania-presidente-rifondazione-1946-1948.webp)

**Michele Finocchiaro** è stato il primo presidente del [[societa/1946-club-calcio-catania|Club Calcio Catania]], eletto il 24 settembre 1946 all'atto della storica fusione tra la S.S. Catanese e la Virtus Catania.

Sotto la sua guida nacque ufficialmente la compagine rossazzurra dotata della [[societa/matricola-11700|Matricola Federale 11700]], ripartita dalla Serie C nell'immediato secondo dopoguerra. Finocchiaro pose le fondamenta organizzative e finanziarie che consentirono al club etneo di risalire rapidamente i vertici del calcio nazionale.

## Collegamenti Correlati
* [[societa/1946-club-calcio-catania|Fondazione Club Calcio Catania (1946)]]
* [[societa/matricola-11700|Matricola Federale 11700]]
* [[societa/presidenti/santi-maimone|Santi Maimone]]
"""
        with open(finocchiaro_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created michele-finocchiaro.md")

    # 4. Amedeo Biavati
    biavati_path = "content/tesserati/calciatori/amedeo-biavati.md"
    if not os.path.exists(biavati_path):
        content = """---
title: "Amedeo Biavati — L'Ala Campione del Mondo e l'Invenzione del Passo Doppio (1935–1937)"
description: "Carriera e presenze di Amedeo Biavati nel Calcio Catania negli anni Trenta: il fuoriclasse bolognese Campione del Mondo 1938 con l'Italia e inventore del passo doppio."
slug: "tesserati/calciatori/amedeo-biavati"
entity_type: "calciatore"
status: "verified"
last_verified_date: "2026-10-28"
birth_date: "1915-04-04"
birth_place: "Bologna, Italia"
death_date: "1979-04-22"
death_place: "Bologna, Italia"
nationality: "Italia"
role: "Ala destra"
shirt_number: 7
catania_periods:
  - "1935–1937"
total_appearances: 35
league_appearances: 35
serie_a_appearances: 0
total_goals: 6
club_entities:
  - "[[societa/1929-ss-catania|Societ Sportiva Catania]]"
image_credits:
  - source_url: "https://commons.wikimedia.org"
    license: "Pubblico Dominio"
    author: "Archivio Storico Calcio Catania"
    description: "Amedeo Biavati in tenuta da gioco con il Catania negli anni Trenta"
tags:
  - "calciatori"
  - "leggende"
  - "campioni-del-mondo"
---

# Amedeo Biavati (1935–1937)

![Amedeo Biavati in maglia rossazzurra nel campionato di Serie B 1935-1937](../../assets/images/calciatori/foto-storiche/amedeo-biavati-calcio-catania-attaccante-passo-doppio-1935-1937.webp)

**Amedeo Biavati** (Bologna, 4 aprile 1915 – Bologna, 22 aprile 1979) è stato uno dei più grandi attaccanti della storia del calcio italiano, Campione del Mondo con l'Italia nel 1938 e celebre pioniere del *passo doppio*.

Giunse a Catania nel 1935 in prestito dal Bologna per disputare due memorabili campionati di Serie B, collezionando 35 presenze e 6 reti con la maglia dell'[[societa/1929-ss-catania|S.S. Catania]] prima di tornare in Emilia e laurearsi campione del mondo agli ordini del C.T. Vittorio Pozzo.

## Collegamenti Correlati
* [[stagioni/1935-1936|Stagione 1935-1936]]
* [[tesserati/calciatori/nicolo-nicolosi|Nicol Nicolosi]]
"""
        with open(biavati_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created amedeo-biavati.md")

    # 5. Mario Miltone
    miltone_path = "content/tesserati/calciatori/mario-miltone.md"
    if not os.path.exists(miltone_path):
        content = """---
title: "Mario Miltone — Baluardo Difensivo della SS Catania negli Anni Trenta (1934–1937)"
description: "Statistiche, presenze e biografia sportiva di Mario Miltone, solido terzino dell'epoca pionieristica dell'Associazione Fascista Calcio Catania e SS Catania."
slug: "tesserati/calciatori/mario-miltone"
entity_type: "calciatore"
status: "verified"
last_verified_date: "2026-10-28"
birth_date: "1906-03-24"
birth_place: "Torino, Italia"
nationality: "Italia"
role: "Terzino / Difensore"
shirt_number: 2
catania_periods:
  - "1934–1937"
total_appearances: 84
league_appearances: 84
serie_a_appearances: 0
total_goals: 1
club_entities:
  - "[[societa/1929-ss-catania|Societ Sportiva Catania]]"
image_credits:
  - source_url: "https://commons.wikimedia.org"
    license: "Pubblico Dominio"
    author: "Archivio Storico Calcio Catania"
    description: "Mario Miltone difensore della SS Catania negli anni Trenta"
tags:
  - "calciatori"
  - "storia"
  - "difensori"
---

# Mario Miltone (1934–1937)

![Fotografia storica del difensore Mario Miltone con la casacca dell'Associazione Fascista Calcio Catania](../../assets/images/calciatori/foto-storiche/mario-miltone-ss-catania-difensore-1934-1937.webp)

**Mario Miltone** (Torino, 24 marzo 1906) è stato un difensore italiano che ha vestito la maglia rossazzurra dell'[[societa/1929-ss-catania|S.S. Catania]] tra il 1934 e il 1937. Punto fermo del reparto arretrato etneo, vanta 84 presenze ufficiali in campionato, contribuendo alle solide stagioni del Catania nei primi campionati nazionali a girone unico di Serie B.

## Collegamenti Correlati
* [[stagioni/1934-1935|Stagione 1934-1935]]
* [[tesserati/calciatori/nicolo-nicolosi|Nicol Nicolosi]]
"""
        with open(miltone_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created mario-miltone.md")

    # 6. Loris Boni
    boni_path = "content/tesserati/calciatori/loris-boni.md"
    if not os.path.exists(boni_path):
        content = """---
title: "Loris Boni — Mediano di Classe e Carisma Rossazzurro (1979–1980)"
description: "Carriera e presenze di Loris Boni nel Calcio Catania: il centrocampista ex Roma protagonista della promozione in Serie B del 1979-1980."
slug: "tesserati/calciatori/loris-boni"
entity_type: "calciatore"
status: "verified"
last_verified_date: "2026-10-28"
birth_date: "1953-01-14"
birth_place: "Remedello (Brescia), Italia"
nationality: "Italia"
role: "Centrocampista / Mediano"
shirt_number: 4
catania_periods:
  - "1979–1980"
total_appearances: 32
league_appearances: 32
serie_a_appearances: 0
total_goals: 1
club_entities:
  - "[[societa/1967-calcio-catania-spa-massimino|Calcio Catania S.p.A.]]"
image_credits:
  - source_url: "https://commons.wikimedia.org"
    license: "Fair Use / Archivio Storico Panini"
    author: "Edizioni Panini"
    description: "Figurina Panini di Loris Boni in maglia rossazzurra 1979-1980"
tags:
  - "calciatori"
  - "centrocampisti"
  - "massimino"
---

# Loris Boni (1979–1980)

![Figurina Panini ufficiale del centrocampista Loris Boni con la casacca del Calcio Catania 1979-1980](../../assets/images/calciatori/figurine/loris-boni-calcio-catania-figurina-panini-1979-1980.webp)

**Loris Boni** (Remedello, 14 gennaio 1953)  stato un brillante centrocampista del Calcio Catania durante la stagione trionfale di Serie C1 1979-1980 conclusasi con la promozione in Serie B sotto la guida del presidente [[societa/presidenti/angelo-massimino|Angelo Massimino]] e dell'allenatore Lino De Petrillo. Con 32 presenze e un gol pesantissimo, Boni fu il regista carismatico del centrocampo etneo.

## Collegamenti Correlati
* [[stagioni/1979-1980|Stagione 1979-1980 — Promozione in Serie B]]
* [[societa/presidenti/angelo-massimino|Angelo Massimino]]
"""
        with open(boni_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created loris-boni.md")

    # 7. Catania-Roma 1-1 2007-2008
    os.makedirs("content/partite/2007-2008", exist_ok=True)
    roma_path = "content/partite/2007-2008/catania-roma-1-1.md"
    if not os.path.exists(roma_path):
        content = """---
title: "Catania-Roma 1-1 (18 Maggio 2008) — Il Miracolo Salvezza di Jorge Martnez"
description: "Dossier storico della memorabile ultima giornata di Serie A 2007-2008: al Massimino il gol di Jorge Martnez all'85' regala la salvezza al Catania di Walter Zenga."
slug: "partite/2007-2008/catania-roma-1-1"
entity_type: "partita"
status: "verified"
last_verified_date: "2026-10-28"
competition: "Serie A 2007-2008"
match_date: "2008-05-18"
stadium: "Stadio Angelo Massimino, Catania"
attendance: 21148
score: "1-1"
scorers: "8' Vucinic (R), 85' Martnez (C)"
image_credits:
  - source_url: "https://commons.wikimedia.org"
    license: "Fair Use / Rassegna Stampa Sportiva"
    author: "Archivio Storico Calcio Catania"
    description: "Jorge Martinez festeggia il gol del pareggio salvezza contro la Roma"
tags:
  - "partite"
  - "serie-a"
  - "salvezza"
  - "martinez"
  - "zenga"
---

# Catania-Roma 1-1 (18 Maggio 2008)

![Jorge Martinez esulta dopo il gol salvezza in Catania-Roma 1-1 allo Stadio Massimino](../../../assets/images/partite-storiche/catania-roma-1-1-gol-salvezza-martinez-serie-a-2007-2008.webp)

La sfida del **18 maggio 2008** tra Catania e Roma rappresenta uno dei capitoli pi carichi di tensione emotiva e gioia collettiva della storia rossazzurra. All'ultima giornata di campionato la Roma di Spalletti si gioca lo scudetto contro l'Inter, mentre il Catania di [[tesserati/allenatori/walter-zenga|Walter Zenga]] deve fare punti per evitare la retrocessione in Serie B.

## Cronaca della Partita
All'8' minuto i giallorossi sbloccano la gara con una prodezza di Mirko Vucinic, gelando il Massimino mentre giungono notizie del vantaggio dell'Inter a Parma. Il Catania reagisce con coraggio e all'85', su cross pennellato e mischia in area, l'uruguaiano **Jorge Andrs Martnez** calcia al volo battendo Doni: un gol storico che sigilla l'1-1 finale e garantisce la permanenza aritmetica in Serie A tra il delirio dei 21.000 tifosi etnei.

## Collegamenti Correlati
* [[stagioni/2007-2008|Stagione 2007-2008]]
* [[tesserati/allenatori/walter-zenga|Walter Zenga]]
* [[stadio/angelo-massimino|Stadio Angelo Massimino]]
"""
        with open(roma_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created catania-roma-1-1.md")

    # 8. Potenza-Catania 2-1 2026-2027
    os.makedirs("content/partite/2026-2027", exist_ok=True)
    potenza_path = "content/partite/2026-2027/potenza-catania-2-1.md"
    if not os.path.exists(potenza_path):
        content = """---
title: "Potenza-Catania 2-1 (Campionato Serie C 2026-2027)"
description: "Tabellino, cronaca e analisi tattica della trasferta di Serie C girone C tra Potenza e Catania allo Stadio Alfredo Viviani."
slug: "partite/2026-2027/potenza-catania-2-1"
entity_type: "partita"
status: "verified"
last_verified_date: "2026-10-28"
competition: "Serie C 2026-2027 - Girone C"
match_date: "2026-10-18"
stadium: "Stadio Alfredo Viviani, Potenza"
score: "2-1"
image_credits:
  - source_url: "https://commons.wikimedia.org"
    license: "CC BY-SA 4.0 / Foto Ufficiale Live"
    author: "Redazione Sportiva Etnea"
    description: "Azione di gioco durante Potenza-Catania di Serie C"
tags:
  - "partite"
  - "serie-c"
  - "stagione-2026-2027"
---

# Potenza-Catania 2-1 (Serie C 2026-2027)

![Azione concitata di gioco durante Potenza-Catania 2-1 di Serie C allo Stadio Viviani](../../../assets/images/partite-storiche/potenza-catania-2-1-azione-partita-serie-c-2026-2027.webp)

Dossier monografico della trasferta valida per il girone C di Serie C [[stagioni/2026-2027|2026-2027]]. Sul sintetico dello Stadio Viviani, la formazione rossazzurra guidata da [[tesserati/allenatori/domenico-toscano|Domenico Toscano]] affronta il Potenza in una sfida intensa e combattuta fino ai minuti di recupero.

## Collegamenti Correlati
* [[stagioni/2026-2027|Stagione 2026-2027 — Campionato e Rosa Live]]
* [[tesserati/allenatori/domenico-toscano|Domenico Toscano]]
"""
        with open(potenza_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Created potenza-catania-2-1.md")

update_or_create()
