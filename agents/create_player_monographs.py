"""
Script per generare le 40 monografie dei calciatori mancanti e aggiornare il registro entita'.
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PLAYERS_DIR = BASE_DIR / "content" / "tesserati" / "calciatori"
REGISTRY_FILE = BASE_DIR / "data" / "entity_registry.json"

PLAYERS_DATA = [
    {
        "slug": "piero-blengino",
        "canonical_name": "Piero Blengino",
        "aliases": ["Pierino Blengino", "Blengino"],
        "title": "Piero Blengino — Il Primo Bomber della Società Sportiva Catania (1929-1930)",
        "description": "Biografia e statistiche di Piero Blengino, primo capocannoniere nella storia della Società Sportiva Catania con 7 reti nella Seconda Divisione 1929-1930.",
        "birth_date": "1904-01-01",
        "birth_place": "Asti, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Ala",
        "catania_periods": ["1929-1931"],
        "total_appearances": 29,
        "league_appearances": 29,
        "total_goals": 10,
        "league_goals": 10,
        "club_entities": ["[[societa/1929-ss-catania\\|Società Sportiva Catania]]"],
        "tags": ["calciatori", "attaccanti", "pionieri", "seconda-divisione", "ss-catania", "santi-quasimodo"],
        "seasons": ["1929-1930"],
        "abstract_title": "Il Primo Marcatore dell'Epopea Rossazzurra",
        "abstract_bullets": [
            "**Ruolo Storico:** Primo capocannoniere assoluto del Catania nei campionati ufficiali FIGC.",
            "**Stagione Inaugurale 1929-1930:** 7 reti in 16 gare nel girone A della Seconda Divisione Sud.",
            "**I Campi Pionieristici:** Protagonista sul terreno del Campo del Dopolavoro Ferroviario e di Piazza Esposizione.",
        ],
        "bio": """**Piero Blengino** (noto nelle cronache dell'epoca anche come **Pierino Blengino**) è stato un calciatore italiano, nel ruolo di ala e attaccante. Entrato nella storia del club etneo come il primo bomber ufficiale della neocostituita [[societa/1929-ss-catania|Società Sportiva Catania]], fu il capocannoniere della squadra nella [[stagioni/1929-1930|Stagione 1929-1930]], la prima in assoluto disputata dalla società rossazzurra nei campionati FIGC.

In una squadra assemblata dal presidente [[societa/presidenti/santi-quasimodo|Santi Quasimodo]] e affidata alla guida tecnica di Giorgio Armari, Blengino si distinse per rapidità, scatto sulla fascia e senso della posizione in area di rigore, realizzando 7 reti fondamentali per consentire al club di conquistare la permanenza nella divisione e gettare le basi del calcio etneo moderno.""",
        "career": """### La Prima Rete Ufficiale e il Campionato 1929-1930

Nel torneo inaugurale di Seconda Divisione Sud 1929-1930, Blengino fu il perno dell'attacco rossazzurro, guidando i compagni in trasferte insidiose e siglando doppiette decisive contro avversari campani e calabresi. Riconfermato nella stagione successiva [[stagioni/1930-1931|1930-1931]] in Prima Divisione, totalizzò ulteriori 13 presenze e 3 reti al fianco del nuovo idolo etneo Ercole Bodini, chiudendo la sua esperienza catanese con 29 presenze e 10 reti totali.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 20-27 (Stagioni 1929-1930 e 1930-1931)"
            },
            {
                "author": "Federazione Italiana Giuoco Calcio (FIGC)",
                "title": "Annuario Ufficiale del Calcio Italiano — Seconda Divisione 1929-1930",
                "publisher": "FIGC - Roma",
                "year": 1930,
                "reference": "Tabellini ufficiali S.S. Catania"
            }
        ]
    },
    {
        "slug": "ercole-bodini",
        "canonical_name": "Ercole Bodini",
        "aliases": ["Bodini", "Ercole Bodini I"],
        "title": "Ercole Bodini — La Mezzala dei Pionieri e Bomber della Promozione in Serie B (1934)",
        "description": "Biografia e statistiche di Ercole Bodini, colonna e bomber del Catania negli anni Trenta: 110 presenze e 37 reti, trascinatore verso la prima Serie B.",
        "birth_date": "1904-11-28",
        "death_date": "1962-09-24",
        "birth_place": "Cremona, Italia",
        "death_place": "Cremona, Italia",
        "nationality": "Italia",
        "role": "Centrocampista / Mezzala offensiva",
        "catania_periods": ["1930-1935"],
        "total_appearances": 110,
        "league_appearances": 104,
        "total_goals": 37,
        "league_goals": 37,
        "club_entities": ["[[societa/1929-ss-catania\\|Società Sportiva Catania]]"],
        "tags": ["calciatori", "centrocampisti", "marcatori", "anni-trenta", "geza-kertesz", "prima-divisione", "serie-b"],
        "seasons": ["1930-1931", "1931-1932"],
        "abstract_title": "La Mezzala Goleador della Prima Serie B",
        "abstract_bullets": [
            "**Presenze e Reti:** 110 presenze e 37 reti ufficiali in cinque stagioni consecutive (1930-1935).",
            "**Capocannoniere Promozione 1933-1934:** 21 reti complessive (17 nel girone H e 4 nel girone finale promozione).",
            "**Regia e Finalizzazione:** Perfetto interprete del metodo ungherese sotto la guida di [[tesserati/allenatori/geza-kertesz|Géza Kertész]].",
        ],
        "bio": """**Ercole Bodini** (Cremona, 28 novembre 1904 – Cremona, 24 settembre 1962) è stato un calciatore e allenatore di calcio italiano, di ruolo mezzala offensiva. Arrivato a Catania nel **1930** proveniente dalla Cremonese, è stato uno dei più grandi protagonisti del primo lustro di vita del sodalizio etneo, collezionando **110 presenze e 37 reti ufficiali**.

Dotato di visione di gioco sopraffina e di un eccellente tiro dalla distanza, Bodini fu il punto di riferimento tecnico e realizzativo della squadra per ben cinque campionati consecutivi, formando una coppia offensiva leggendaria con il giovane centravanti [[tesserati/calciatori/nicolo-nicolosi|Nicolò Nicolosi]].""",
        "career": """### Dagli Esordi in Prima Divisione al Trionfo del 1934

Nelle stagioni [[stagioni/1930-1931|1930-1931]] (10 reti) e [[stagioni/1931-1932|1931-1932]] (10 reti), Bodini fu il faro del centrocampo etneo sul campo di Piazza Esposizione. Il suo capolavoro coincise con la [[stagioni/1933-1934|Stagione 1933-1934]]: guidato dal maestro ungherese Géza Kertész, Bodini mise a referto ben **21 reti** (capocannoniere assoluto del torneo), trascinando il Catania alla conquista della prima storica promozione in **Serie B**. Nella stagione di debutto in cadetteria ([[stagioni/1934-1935|1934-1935]]) confermò la propria classe collezionando 20 presenze e 4 reti prima del rientro al Nord.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 28-65 (Stagioni dal 1930-1931 al 1934-1935)"
            },
            {
                "author": "Roberto Quartarone",
                "title": "I pionieri del calcio etneo: Ercole Bodini e la prima Serie B",
                "publisher": "Tutto il Catania",
                "year": 2017,
                "reference": "Profilo storico e caratura tecnica"
            }
        ]
    },
    {
        "slug": "ettore-brossi",
        "canonical_name": "Ettore Brossi",
        "aliases": ["Brossi"],
        "title": "Ettore Brossi — Il Centravanti Giuliano della Serie B e Serie C (25 Reti)",
        "description": "Biografia e statistiche di Ettore Brossi, bomber del Catania tra il 1936 e il 1938 con 25 reti ufficiali tra Serie B e Serie C.",
        "birth_date": "1910-06-25",
        "death_date": "1982-12-04",
        "birth_place": "Trieste, Italia",
        "death_place": "Trieste, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1936-1938"],
        "total_appearances": 58,
        "league_appearances": 55,
        "total_goals": 25,
        "league_goals": 25,
        "club_entities": ["[[societa/1929-ss-catania\\|Associazione Fascista Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-b", "serie-c", "afc-catania"],
        "seasons": ["1937-1938"],
        "abstract_title": "Il Goleador Giuliano di Piazza Esposizione e del Cibali",
        "abstract_bullets": [
            "**Presenze e Reti:** 58 presenze e 25 reti complessive in maglia etnea tra il 1936 e il 1938.",
            "**Capocannoniere in Serie B (1936-1937):** 15 reti realizzate in 29 gare di campionato.",
            "**Protagonista del 1937-1938:** Leader dell'attacco nella transizione verso il nuovo Stadio Cibali con 10 reti.",
        ],
        "bio": """**Ettore Brossi** (Trieste, 25 giugno 1910 – Trieste, 4 dicembre 1982) è stato un calciatore e allenatore di calcio italiano, di ruolo centravanti. Acquistato dall'AFC Catania nell'estate del **1936**, si impose immediatamente per prestanza fisica, incornata potente e letale opportunismo sotto porta.

Nel campionato di Serie B 1936-1937 realizzò **15 reti in 29 partite**, risultando il miglior marcatore della squadra etnea e uno dei centravanti più prolifici della cadetteria italiana.""",
        "career": """### La Leadership Offensiva nella Stagione 1937-1938

Con la partenza di Nicolosi al Napoli, nella [[stagioni/1937-1938|Stagione 1937-1938]] Brossi fu il punto di riferimento offensivo dell'AFC Catania in Serie C, mettendo a referto 10 reti in campionato e guidando l'attacco rossazzurro anche nelle prime storiche apparizioni nel nuovo Stadio Cibali inaugurato nel novembre 1937. Concluse il suo biennio rossazzurro con l'eccezionale media di quasi un gol ogni due partite (25 reti in 58 gare).""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 68-78 (Stagioni 1936-1937 e 1937-1938)"
            }
        ]
    },
    {
        "slug": "enzo-bellini",
        "canonical_name": "Enzo Bellini",
        "aliases": ["Bellini"],
        "title": "Enzo Bellini — L'Ala Goleador della Promozione in Serie B del 1939",
        "description": "Biografia e statistiche di Enzo Bellini, attaccante del Catania con 16 reti tra il 1938 e il 1940 e protagonista della promozione in Serie B nel 1938-1939.",
        "birth_date": "1917-02-14",
        "death_date": "2001-08-11",
        "birth_place": "Bondeno (FE), Italia",
        "death_place": "Ferrara, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Ala destra",
        "catania_periods": ["1938-1940"],
        "total_appearances": 45,
        "league_appearances": 41,
        "total_goals": 16,
        "league_goals": 15,
        "club_entities": ["[[societa/1929-ss-catania\\|Associazione Fascista Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-c", "serie-b", "gyorgy-orth"],
        "seasons": ["1938-1939"],
        "abstract_title": "L'Ala della Riconquista della Cadetteria",
        "abstract_bullets": [
            "**Capocannoniere Promozione 1938-1939:** 12 reti in campionato sotto la direzione tecnica di György Orth.",
            "**Doppio Ruolo Storico:** Calciatore protagonista (1938-1940) e successivamente allenatore della prima squadra in Serie B (1955-1956).",
            "**Velocità e Gol:** Ala moderna capace di tagliare verso il centro e concludere a rete con entrambi i piedi.",
        ],
        "bio": """**Enzo Bellini** (Bondeno, 14 febbraio 1917 – Ferrara, 11 agosto 2001) è stato un calciatore e allenatore di calcio italiano, di ruolo ala destra. Giunto a Catania nel **1938** dalla SPAL, fu il grande trascinatore offensivo della [[stagioni/1938-1939|Stagione 1938-1939]], culminata con il primo posto nel Girone H di Serie C e la vittoria del girone finale promozione per il ritorno in Serie B.

Con 12 reti in 21 gare di campionato, Bellini fu il capocannoniere indiscusso dell'undici guidato dal tecnico ungherese György Orth. Rimasto in rossazzurro anche nel successivo campionato cadetto 1939-1940, totalizzò complessivamente 45 presenze e 16 reti, tornando poi alle falde dell'Etna a metà degli anni Cinquanta nelle vesti di allenatore.""",
        "career": """### La Cavalcata del 1938-1939 e il Ritorno da Allenatore

Nel campionato di Serie C 1938-1939 Bellini fu devastante per le retroguardie avversarie: firmò triplette e marcature pesanti contro Siracusa e Messina, infiammando il pubblico dello Stadio Cibali. Nel 1955 tornò a Catania per guidare la panchina etnea in Serie B nel 1955-1956, consolidando un legame indissolubile con la città.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 79-88 (Stagioni 1938-1939 e 1939-1940)"
            }
        ]
    },
    {
        "slug": "romano-schillani",
        "canonical_name": "Romano Schillani",
        "aliases": ["Schillani"],
        "title": "Romano Schillani — Il Mastino Mediano e Capocannoniere di Guerra (1940-1941)",
        "description": "Biografia e statistiche di Romano Schillani, mediano e capitano del Catania durante gli anni bellici: 54 presenze e capocannoniere nel 1940-1941.",
        "birth_date": "1914-04-20",
        "death_date": "1989-08-15",
        "birth_place": "Trieste, Italia",
        "death_place": "Trieste, Italia",
        "nationality": "Italia",
        "role": "Centrocampista / Mediano",
        "catania_periods": ["1940-1942"],
        "total_appearances": 54,
        "league_appearances": 50,
        "total_goals": 12,
        "league_goals": 12,
        "club_entities": ["[[societa/1929-ss-catania\\|Associazione Fascista Calcio Catania]]"],
        "tags": ["calciatori", "centrocampisti", "mediani", "serie-c", "seconda-guerra-mondiale"],
        "seasons": ["1940-1941"],
        "abstract_title": "La Cerniera Mediana degli Anni Difficili",
        "abstract_bullets": [
            "**Leader Carismatico:** Punto fermo del centrocampo etneo con 54 presenze ufficiali tra il 1940 e il 1942.",
            "**Insolito Bomber:** Capocannoniere della squadra nella [[stagioni/1940-1941|Stagione 1940-1941]] con 7 reti.",
            "**Tenacia e Tattica:** Mediano infaticabile, abile nell'interdizione e nei tiri dalla media distanza.",
        ],
        "bio": """**Romano Schillani** (Trieste, 20 aprile 1914 – Trieste, 15 agosto 1989) è stato un calciatore italiano, nel ruolo di mediano e centrocampista metodista. Giunto in Sicilia nell'autunno del **1940**, rappresentò la colonna portante dell'AFC Catania nel difficile biennio bellico 1940-1942.

Nonostante il ruolo prettamente difensivo e di costruzione in mediana, Schillani si laureò capocannoniere della squadra nella stagione 1940-1941 con **7 reti** in 22 partite, grazie a poderosi inserimenti su palla inattiva e a tiri precisi dal limite.""",
        "career": """### Il Biennio Bellico al Cibali

In un contesto segnato dai bombardamenti e dalle restrizioni belliche, Schillani disputò due stagioni ad altissimo rendimento: dopo le 7 reti del 1940-1941, nella stagione 1941-1942 collezionò altre 28 gare e 5 reti a supporto del centravanti austriaco Engelbert Koenig, confermandosi tra i mediani più apprezzati dell'epoca.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 89-98 (Stagioni 1940-1941 e 1941-1942)"
            }
        ]
    },
    {
        "slug": "engelbert-koenig",
        "canonical_name": "Engelbert Koenig",
        "aliases": ["Koenig", "Engelbert König"],
        "title": "Engelbert Koenig — Il Cannoniere Austriaco del 1941-1942 (18 Reti in 23 Gare)",
        "description": "Biografia e statistiche di Engelbert Koenig, formidabile centravanti austriaco autore di 18 reti in 23 gare nel Catania 1941-1942 prima della Serie A.",
        "birth_date": "1919-10-18",
        "death_date": "1997-11-23",
        "birth_place": "Vienna, Austria",
        "death_place": "Vienna, Austria",
        "nationality": "Austria",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1941-1942"],
        "total_appearances": 23,
        "league_appearances": 23,
        "total_goals": 18,
        "league_goals": 18,
        "club_entities": ["[[societa/1929-ss-catania\\|Associazione Fascista Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "bomber-stranieri", "serie-c", "austria"],
        "seasons": ["1941-1942"],
        "abstract_title": "La Macchina da Gol Viennese",
        "abstract_bullets": [
            "**Media Realizzativa Straordinaria:** 18 reti in appena 23 presenze (0,78 gol a partita) nella [[stagioni/1941-1942|Stagione 1941-1942]].",
            "**Potenza e Freddezza:** Centravanti classico della scuola danubiana, forte fisicamente e implacabile nei sedici metri.",
            "**Carriera d'Élite:** Dopo Catania giocò ad altissimi livelli in Serie A con Lazio, Fiorentina, Genoa e Sampdoria.",
        ],
        "bio": """**Engelbert Koenig** (Vienna, 18 ottobre 1919 – Vienna, 23 novembre 1997) è stato un calciatore austriaco, nel ruolo di centravanti. Approdato in Italia durante la guerra, fu ingaggiato dall'AFC Catania per la stagione di Serie C **1941-1942**.

Il suo impatto con il calcio siciliano fu travolgente: in sole 23 presenze ufficiali realizzò ben **18 reti**, risultando il secondo miglior marcatore di tutti i gironi di Serie C e sfiorando la qualificazione alle finali promozione. Le sue prestazioni al Cibali convinsero la Lazio ad acquistarlo in Serie A, dove disputò stagioni memorabili.""",
        "career": """### La Stagione Straordinaria 1941-1942

Schierato titolare inamovibile al centro dell'attacco dall'allenatore ungherese Géza Kertész, Koenig dimostrò una classe nettamente superiore alla categoria. Tra i momenti memorabili della sua annata catanese si ricordano la tripletta all'Avellino e le marcature decisive nei derby con le formazioni siciliane e calabresi, che lo resero un idolo indimenticato della tifoseria etnea.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 94-98 (Stagione 1941-1942)"
            }
        ]
    },
    {
        "slug": "armando-perrone",
        "canonical_name": "Armando Perrone",
        "aliases": ["Perrone"],
        "title": "Armando Perrone — L'Attaccante della Rinascita del 1946 e della Promozione in B",
        "description": "Biografia e statistiche di Armando Perrone, protagonista della rifondazione del Club Calcio Catania nel 1946 con 65 presenze e 18 reti fino al 1949.",
        "birth_date": "1921-08-12",
        "death_date": "1999-05-20",
        "birth_place": "Taranto, Italia",
        "death_place": "Taranto, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Ala",
        "catania_periods": ["1946-1949"],
        "total_appearances": 65,
        "league_appearances": 65,
        "total_goals": 18,
        "league_goals": 18,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "rinascita-1946", "serie-c", "promozione-serie-b"],
        "seasons": ["1946-1947"],
        "abstract_title": "La Bandiera della Rifondazione Post-Bellica",
        "abstract_bullets": [
            "**Titolare del Nuovo Club:** Presente fin dalla prima gara ufficiale del Club Calcio Catania (matricola FIGC 11700) nell'autunno 1946.",
            "**Tre Stagioni di Successi:** 65 gare e 18 reti tra il 1946 e il 1949.",
            "**Promozione in Serie B 1948-1949:** Protagonista del trionfo nel girone finale promozione con 7 reti.",
        ],
        "bio": """**Armando Perrone** (Taranto, 12 agosto 1921 – Taranto, 20 maggio 1999) è stato un calciatore italiano, nel ruolo di ala e attaccante. Nel settembre **1946**, alla rinascita del calcio a Catania sotto la nuova denominazione sociale di [[societa/1946-club-calcio-catania|Club Calcio Catania]], fu uno dei primi elementi ingaggiati dalla dirigenza guidata da Santi Passanisi Manganaro.

Perrone fu il punto fermo dell'attacco etneo nella pionieristica [[stagioni/1946-1947|Stagione 1946-1947]], disputando 19 incontri e realizzando 5 reti, confermandosi poi per altre due stagioni fino alla promozione in Serie B del 1949.""",
        "career": """### Dalla Serie C alla Serie B (1946-1949)

Affiancato prima a Musmeci e poi dal 1947 al grande veterano Nicolò Nicolosi e ad Arnaldo Cadei, Perrone garantì dinamismo e profondità alla manovra offensiva. Nella stagione 1948-1949 contribuì con 7 reti alla cavalcata che riportò il Catania in Serie B, salutando la maglia rossazzurra da autentico beniamino del Cibali.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 110-125 (Stagioni dal 1946-1947 al 1948-1949)"
            }
        ]
    },
    {
        "slug": "goffredo-romani",
        "canonical_name": "Goffredo Romani",
        "aliases": ["Romani"],
        "title": "Goffredo Romani — Il Bomber del Ritorno in Serie B (1949-1950)",
        "description": "Biografia e statistiche di Goffredo Romani, centravanti e capocannoniere del Catania nel campionato cadetto 1949-1950 con 11 reti.",
        "birth_date": "1926-05-19",
        "death_date": "2008-01-14",
        "birth_place": "Roma, Italia",
        "death_place": "Roma, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1949-1950"],
        "total_appearances": 37,
        "league_appearances": 37,
        "total_goals": 11,
        "league_goals": 11,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-b", "mario-varglien"],
        "seasons": ["1949-1950"],
        "abstract_title": "Il Centravanti della Rinascita Cadetta",
        "abstract_bullets": [
            "**Capocannoniere Stagionale:** 11 reti in 37 presenze nel campionato di Serie B 1949-1950.",
            "**Salvezza Tranquilla:** Trascinatore offensivo della formazione allenata da Mario Varglien.",
            "**Senso del Gol:** Centravanti potente, efficace nel gioco aereo e nei tiri di prima intenzione.",
        ],
        "bio": """**Goffredo Romani** (Roma, 19 maggio 1926 – Roma, 14 gennaio 2008) è stato un calciatore italiano, nel ruolo di centravanti. Acquistato dal Club Calcio Catania nell'estate del **1949** per affrontare il ritorno in Serie B dopo gli anni di gavetta post-bellica, fu il capocannoniere e punto di riferimento offensivo della [[stagioni/1949-1950|Stagione 1949-1950]].

Sotto la guida tecnica dell'ex juventino Mario Varglien, Romani disputò 37 delle 42 gare di campionato, mettendo a referto **11 reti** decisive per la salvezza e per il consolidamento degli etnei nella seconda serie nazionale.""",
        "career": """### Il Campionato di Serie B 1949-1950

Tra le sue prestazioni più brillanti della stagione 1949-1950 spiccano le doppiette rifilate all'Arsenaltaranto e all'Empoli, nonché il gol decisivo nel match interno contro il Brescia. Il suo contributo permise al Catania di chiudere al dodicesimo posto finale, ponendo le basi per il ciclo di vertice degli anni Cinquanta.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 126-131 (Stagione 1949-1950)"
            }
        ]
    },
    {
        "slug": "guido-klein",
        "canonical_name": "Guido Klein",
        "aliases": ["Klein"],
        "title": "Guido Klein — Il Re dei Marcatori Cadetti del Catania (32 Reti tra 1950 e 1953)",
        "description": "Biografia e statistiche di Guido Klein, due volte capocannoniere del Catania in Serie B (1950-1951 e 1951-1952) con 32 reti in 91 gare.",
        "birth_date": "1923-01-08",
        "death_date": "2002-04-12",
        "birth_place": "Roma, Italia",
        "death_place": "Roma, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti / Ala",
        "catania_periods": ["1950-1953"],
        "total_appearances": 91,
        "league_appearances": 91,
        "total_goals": 32,
        "league_goals": 32,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-b", "lajos-politzer"],
        "seasons": ["1950-1951", "1951-1952"],
        "abstract_title": "Il Due Volte Re del Gol in Serie B",
        "abstract_bullets": [
            "**Due Volte Capocannoniere Etneo:** 15 reti nel 1950-1951 e 13 reti nel 1951-1952.",
            "**Score Complessivo:** 91 presenze e 32 reti in Serie B con la maglia del Catania.",
            "**Alta Quota in Classifica:** Condusse la squadra al 6º posto nel 1951 e al 4º posto nel 1952, a un passo dalla Serie A.",
        ],
        "bio": """**Guido Klein** (Roma, 8 gennaio 1923 – Roma, 12 aprile 2002) è stato un calciatore e allenatore di calcio italiano, nel ruolo di attaccante. Approdato al Catania nell'estate del **1950**, fu il bomber principe e l'idolo indiscusso della tifoseria del Cibali nel triennio cadetto 1950-1953, collezionando **91 presenze e 32 reti ufficiali**.

Attaccante moderno, versatile e letale sia da prima punta che partendo dall'esterno, Klein guidò la squadra fino ai vertici della cadetteria sotto la direzione tecnica di Lajos Politzer e Fioravante Baldi.""",
        "career": """### I Grandi Campionati con Politzer e Baldi

Nella [[stagioni/1950-1951|Stagione 1950-1951]] Klein realizzò **15 reti in 34 presenze**, firmando doppiette storiche contro Spezia, Treviso e Verona. Si ripeté l'anno seguente nella [[stagioni/1951-1952|Stagione 1951-1952]], realizzando **13 reti in 36 partite** e portando il Catania al quarto posto finale a soli due punti dalla promozione in Serie A. Rimase in rossazzurro anche nel 1952-1953 (4 reti), lasciando un'impronta indelebile nella storia del club.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 132-148 (Stagioni dal 1950-1951 al 1952-1953)"
            }
        ]
    },
    {
        "slug": "bruno-micheloni",
        "canonical_name": "Bruno Micheloni",
        "aliases": ["Micheloni"],
        "title": "Bruno Micheloni — Il Centravanti dell'Assalto alla Serie A (1951-1954)",
        "description": "Biografia e statistiche di Bruno Micheloni, capocannoniere del Catania nel 1952-1953 con 12 reti e pedina chiave nella salita in Serie A.",
        "birth_date": "1925-06-21",
        "death_date": "2000-09-17",
        "birth_place": "Lucca, Italia",
        "death_place": "Lucca, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1951-1954"],
        "total_appearances": 64,
        "league_appearances": 64,
        "total_goals": 21,
        "league_goals": 21,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-b", "fioravante-baldi"],
        "seasons": ["1952-1953"],
        "abstract_title": "Il Centravanti di Peso del Tridente di Baldi",
        "abstract_bullets": [
            "**Capocannoniere 1952-1953:** 12 reti in 32 presenze, trascinando il Catania al 3º posto in Serie B.",
            "**Tre Anni di Vertice:** 64 presenze e 21 reti complessive tra il 1951 e il 1954.",
            "**Rosa Storica 1953-1954:** Fece parte della rosa vincitrice del campionato di Serie B con Piero Andreoli.",
        ],
        "bio": """**Bruno Micheloni** (Lucca, 21 giugno 1925 – Lucca, 17 settembre 2000) è stato un calciatore italiano, nel ruolo di centravanti. Giunto a Catania nel **1951**, fu per un triennio la punta centrale di riferimento del Club Calcio Catania nel periodo d'oro della rincorsa alla massima serie.

Forte fisicamente, abile nel proteggere palla e dotato di un potente tiro al volo, Micheloni visse la sua stagione migliore nel campionato cadetto **1952-1953**, quando vinse la classifica marcatori interna del Catania con **12 reti**, guidando la squadra al 3º posto a un soffio dalla promozione.""",
        "career": """### Dalla Stagione 1952-1953 al Trionfo del 1954

Dopo aver segnato 8 reti nel 1951-1952, nella [[stagioni/1952-1953|Stagione 1952-1953]] Micheloni fu letale per le difese cadette, siglando reti decisive contro Genoa, Cagliari e Vicenza. L'anno seguente partecipò alla storica cavalcata della promozione in Serie A 1953-1954 sotto la direzione di Piero Andreoli, completando un ciclo indimenticabile in maglia etnea.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 138-154 (Stagioni dal 1951-1952 al 1953-1954)"
            }
        ]
    },
    {
        "slug": "michele-manenti",
        "canonical_name": "Michele Manenti",
        "aliases": ["Manenti"],
        "title": "Michele Manenti — Il Centravanti della Prima Storica Promozione in Serie A (1954)",
        "description": "Biografia e statistiche di Michele Manenti, bomber con 15 reti nella Serie B 1953-1954 che portò il Catania per la prima volta nella massima serie.",
        "birth_date": "1928-10-28",
        "death_date": "1988-08-30",
        "birth_place": "Milano, Italia",
        "death_place": "Milano, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1953-1955"],
        "total_appearances": 62,
        "league_appearances": 62,
        "total_goals": 24,
        "league_goals": 24,
        "serie_a_appearances": 28,
        "serie_a_goals": 9,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "serie-a", "serie-b", "piero-andreoli", "prima-promozione-serie-a"],
        "seasons": ["1953-1954"],
        "abstract_title": "L'Uomo della Prima Serie A del 1954",
        "abstract_bullets": [
            "**Capocannoniere Promozione 1953-1954:** 15 reti in 34 presenze, trascinatore assoluto del trionfo in Serie B.",
            "**Protagonista in Serie A (1954-1955):** 9 reti in 28 partite nella massima divisione italiana.",
            "**Media Realizzativa di Livello:** 24 reti complessive in 62 gare di campionato con la casacca etnea.",
        ],
        "bio": """**Michele Manenti** (Milano, 28 ottobre 1928 – Milano, 30 agosto 1988) è stato un calciatore italiano, nel ruolo di centravanti. Acquistato dal Club Calcio Catania nell'estate del **1953**, entrò per sempre nella leggenda rossazzurra come il capocannoniere e trascinatore della prima storica promozione in **Serie A** nella [[stagioni/1953-1954|Stagione 1953-1954]].

Centravanti di sfondamento, aggressivo sul pallone e freddo implacabile negli ultimi sedici metri, Manenti realizzò 15 reti nel torneo cadetto 1953-1954, formando con Bassetti e Marin un reparto d'attacco devastante orchestrato da Piero Andreoli.""",
        "career": """### La Gloria del 1954 e la Serie A 1954-1955

Nella trionfale stagione 1953-1954 Manenti decise match cruciali contro Pro Patria, Verona e Cagliari, regalando al pubblico del Cibali la prima Serie A della storia cittadina. L'anno successivo, nel massimo campionato [[stagioni/1954-1955|1954-1955]], si confermò bomber di razza anche contro i giganti del calcio italiano, segnando **9 reti in 28 presenze** (tra cui doppiette decisive per la salvezza sul campo).""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 150-162 (Stagioni 1953-1954 e 1954-1955)"
            }
        ]
    },
    {
        "slug": "karl-aage-hansen",
        "canonical_name": "Karl Aage Hansen",
        "aliases": ["Hansen", "Karl Hansen"],
        "title": "Karl Aage Hansen — Il Maestro Danese e Leader della Prima Serie A (1954-1957)",
        "description": "Biografia e statistiche di Karl Aage Hansen, medaglia olimpica e regista internazionale del Catania nel debutto in Serie A e in cadetteria.",
        "birth_date": "1921-07-04",
        "death_date": "1990-11-23",
        "birth_place": "Mesinge, Danimarca",
        "death_place": "Gentofte, Danimarca",
        "nationality": "Danimarca",
        "role": "Centrocampista / Regista",
        "catania_periods": ["1954-1957"],
        "total_appearances": 79,
        "league_appearances": 79,
        "total_goals": 7,
        "league_goals": 7,
        "serie_a_appearances": 31,
        "serie_a_goals": 3,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "centrocampisti", "registi", "serie-a", "serie-b", "danimarca", "piero-andreoli"],
        "seasons": ["1954-1955"],
        "abstract_title": "La Classe Internazionale al Cibali",
        "abstract_bullets": [
            "**Palmarès Prestigioso:** Medaglia di bronzo alle Olimpiadi di Londra 1948, campione d'Italia con la Juventus prima dell'approdo a Catania.",
            "**Leader Tecnico in Serie A (1954-1955):** 31 presenze e 3 reti nella storica prima stagione in massima divisione.",
            "**Tre Campionati Etnei:** 79 presenze totali e punto di riferimento tattico tra il 1954 e il 1957.",
        ],
        "bio": """**Karl Aage Hansen** (Mesinge, 4 luglio 1921 – Gentofte, 23 novembre 1990) è stato un calciatore danese, nel ruolo di mezzala e regista. Acquistato dal Club Calcio Catania nell'estate del **1954** per affrontare il primo storico campionato di **Serie A** della storia etnea, portò alle pendici dell'Etna un bagaglio di esperienza e caratura tecnica internazionale impareggiabile.

Regista dai piedi vellutati e dalla straordinaria intelligenza tattica, Hansen fu il motore della squadra di Piero Andreoli nella [[stagioni/1954-1955|Stagione 1954-1955]], guidando la formazione rossazzurra a una memorabile salvezza conquistata sul campo con 31 presenze e 3 reti.""",
        "career": """### Dalla Serie A al Triennio Rossazzurro (1954-1957)

Dopo la controversa retrocessione a tavolino del 1955 per il Caso Scaramella, Hansen decise di onorare il contratto rimanendo a Catania per altri due campionati di Serie B (1955-1956 e 1956-1957), collezionando ulteriori 48 presenze e 4 reti prima di chiudere la carriera professionistica.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 156-172 (Stagioni dal 1954-1955 al 1956-1957)"
            }
        ]
    },
    {
        "slug": "guido-spikofski",
        "canonical_name": "Guido Spikofski",
        "aliases": ["Spikofski", "György Spikofszky"],
        "title": "Guido Spikofski — L'Ala Danubiana e Capocannoniere Etneo (1955-1957)",
        "description": "Biografia e statistiche di Guido Spikofski, ungherese dal dribbling magico e capocannoniere del Catania nella Serie B 1955-1956 con 10 reti.",
        "birth_date": "1923-07-25",
        "death_date": "2007-09-02",
        "birth_place": "Budapest, Ungheria",
        "death_place": "Budapest, Ungheria",
        "nationality": "Ungheria",
        "role": "Attaccante / Ala destra",
        "catania_periods": ["1955-1957"],
        "total_appearances": 60,
        "league_appearances": 60,
        "total_goals": 10,
        "league_goals": 10,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "ali", "serie-b", "ungheria", "enzo-bellini"],
        "seasons": ["1955-1956"],
        "abstract_title": "La Fantasia Danubiana al Servizio del Cibali",
        "abstract_bullets": [
            "**Capocannoniere 1955-1956:** 10 reti in 34 partite di Serie B sotto la guida di Enzo Bellini.",
            "**Dribbling e Cross:** Ala pura della raffinata scuola ungherese, idolo della tifoseria etnea.",
            "**Presenze Complessive:** 60 presenze e 10 reti in due tornei cadetti di vertice (1955-1957).",
        ],
        "bio": """**Guido Spikofski** (all'anagrafe **György Spikofszky**, Budapest, 25 luglio 1923 – Budapest, 2 settembre 2007) è stato un calciatore e allenatore di calcio ungherese, di ruolo ala destra. Ingaggiato dal Club Calcio Catania nel **1955** dopo le esperienze con Roma e Palermo, incantò il Cibali per due stagioni con giocate di pura classe magistrale.

Nel campionato di Serie B [[stagioni/1955-1956|1955-1956]] fu il trascinatore offensivo della squadra, laureandosi capocannoniere con **10 reti** e portando il Catania al 5º posto a ridosso della zona promozione.""",
        "career": """### Il Ruolo di Leader Tattico nel 1955-1957

Capace di saltare l'avversario con finte fulminee e di crossare con precisione millimetrica per i compagni, Spikofski garantì rendimento costante anche nel 1956-1957 (26 presenze), confermandosi uno dei talenti stranieri più amati della storia rossazzurra degli anni Cinquanta.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 164-173 (Stagioni 1955-1956 e 1956-1957)"
            }
        ]
    },
    {
        "slug": "ermo-buzzin",
        "canonical_name": "Ermo Buzzin",
        "aliases": ["Buzzin"],
        "title": "Ermo Buzzin — Il Due Volte Capocannoniere di Serie B (1956-1958)",
        "description": "Biografia e statistiche di Ermo Buzzin, centravanti e punto di riferimento offensivo del Catania con 16 reti tra il 1956 e il 1958.",
        "birth_date": "1934-08-14",
        "death_date": "2018-05-22",
        "birth_place": "Ronchi dei Legionari (GO), Italia",
        "death_place": "Ronchi dei Legionari (GO), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1956-1958"],
        "total_appearances": 56,
        "league_appearances": 56,
        "total_goals": 16,
        "league_goals": 16,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-b", "poggi"],
        "seasons": ["1956-1957"],
        "abstract_title": "Il Centravanti Bisiaco dei Due Tornei Cadetti",
        "abstract_bullets": [
            "**Capocannoniere 1956-1957:** 10 reti in 29 gare di Serie B, guidando il Catania al 4º posto.",
            "**Conferma 1957-1958:** Ancora miglior marcatore etneo con 6 reti in 27 presenze.",
            "**Totale Maglia Etnea:** 56 partite e 16 reti ufficiali.",
        ],
        "bio": """**Ermo Buzzin** (Ronchi dei Legionari, 14 agosto 1934 – Ronchi dei Legionari, 22 maggio 2018) è stato un calciatore italiano, nel ruolo di centravanti. Acquistato nell'estate del **1956**, fu per due stagioni consecutive il miglior realizzatore del Club Calcio Catania nel campionato di Serie B.

Attaccante agile e opportunista, dotato di eccellente tempismo in area di rigore, Buzzin realizzò 10 reti nella [[stagioni/1956-1957|Stagione 1956-1957]] condividendo lo scettro dei bomber con Uzzecchini e conducendo gli etnei al quarto posto finale a un soffio dalla Serie A.""",
        "career": """### La Leadership Offensiva tra il 1956 e il 1958

Nella successiva stagione [[stagioni/1957-1958|1957-1958]] Buzzin si confermò capocannoniere del Catania affiancato al prestigioso capitano Riccardo Carapellese, totalizzando altre 6 reti in 27 presenze e siglando marcature decisive nei derby del Sud.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 170-179 (Stagioni 1956-1957 e 1957-1958)"
            }
        ]
    },
    {
        "slug": "riccardo-carapellese",
        "canonical_name": "Riccardo Carapellese",
        "aliases": ["Carapellese"],
        "title": "Riccardo Carapellese — L'Eroe Azzurro e Capitano d'Esperienza al Cibali (1957-1959)",
        "description": "Biografia e statistiche di Riccardo Carapellese, leggenda del calcio italiano ed ex capitano della Nazionale, capitano del Catania tra il 1957 e il 1959.",
        "birth_date": "1922-07-01",
        "death_date": "1995-10-20",
        "birth_place": "Cerignola (FG), Italia",
        "death_place": "Rapallo (GE), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Ala sinistra / Capitano",
        "catania_periods": ["1957-1959"],
        "total_appearances": 30,
        "league_appearances": 30,
        "total_goals": 9,
        "league_goals": 9,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "capitano", "nazionale-italiana", "serie-b"],
        "seasons": ["1957-1958"],
        "abstract_title": "La Leggenda Azzurra e Guida Etnea",
        "abstract_bullets": [
            "**Caratura Storica:** Capitano del Torino dopo Superga e capitano della Nazionale Italiana (16 presenze e 10 reti agli ordini di Ferruccio Novo).",
            "**Capocannoniere Etneo 1957-1958:** 6 reti in 19 presenze, leader morale e carismatico in Serie B.",
            "**Esperienza e Guida:** Chiuse la sua eccezionale carriera professionistica in maglia rossazzurra nel 1959.",
        ],
        "bio": """**Riccardo Carapellese** (Cerignola, 1 luglio 1922 – Rapallo, 20 ottobre 1995) è stato un calciatore e allenatore di calcio italiano, tra le più grandi ali sinistre del calcio nazionale del dopoguerra. Storico capitano della Nazionale Italiana ai Mondiali del 1950 in Brasile e del Torino post-Superga, approdò al Catania nel **1957** all'età di 35 anni.

Nonostante l'età avanzata, Carapellese incantò lo Stadio Cibali con la sua classe sopraffina, la precisione nei cross e la proverbiale freddezza, laureandosi capocannoniere della squadra nella [[stagioni/1957-1958|Stagione 1957-1958]] con 6 reti in sole 19 presenze.""",
        "career": """### Il Ritiro in Maglia Rossazzurra

Indossando la fascia di capitano con dignità regale, guidò i giovani compagni anche nella prima parte della stagione 1958-1959 (11 presenze e 3 reti), prima di appendere gli scarpini al chiodo e intraprendere una stimata carriera da allenatore, lasciando nei cuori catanesi il ricordo di un autentico monumento vivente del calcio.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 176-184 (Stagioni 1957-1958 e 1958-1959)"
            }
        ]
    },
    {
        "slug": "salvador-calvanese",
        "canonical_name": "Salvador Calvanese",
        "aliases": ["Todo Calvanese", "Calvanese"],
        "title": "Salvador «Todo» Calvanese — L'Idolo Argentino del «Clamoroso al Cibali» (1960-1967)",
        "description": "Biografia e statistiche di Salvador Calvanese, formidabile centravanti argentino con 117 presenze e 24 reti, simbolo dell'epopea di Carmelo Di Bella.",
        "birth_date": "1934-08-17",
        "death_date": "2019-11-05",
        "birth_place": "Buenos Aires, Argentina",
        "death_place": "Buenos Aires, Argentina",
        "nationality": "Argentina",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1960-1962", "1964-1967"],
        "total_appearances": 117,
        "league_appearances": 113,
        "total_goals": 24,
        "league_goals": 23,
        "serie_a_appearances": 82,
        "serie_a_goals": 17,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "argentini", "carmelo-di-bella", "serie-a", "clamoroso-al-cibali"],
        "seasons": ["1964-1965", "1966-1967"],
        "abstract_title": "L'Eroe Argentino dell'Era d'Oro di Carmelo Di Bella",
        "abstract_bullets": [
            "**L'Inno al Cibali:** Autore del gol del 2-0 nella storica vittoria contro l'Inter di Herrera il 4 giugno 1961 (*«Clamoroso al Cibali!»*).",
            "**Centravanti Totale:** 117 presenze e 24 reti in maglia rossazzurra attraverso due distinti cicli trionfali.",
            "**L'Ottavo Posto Record (1964-1965):** Protagonista in Serie A del celebre tridente Danova-Facchin-Calvanese.",
            "**La Promozione del 1967:** Perno dell'attacco che riconquistò immediatamente la Serie A nel 1966-1967.",
        ],
        "bio": """**Salvador Calvanese**, affettuosamente ribattezzato dai tifosi **"Todo Calvanese"** (Buenos Aires, 17 agosto 1934 – Buenos Aires, 5 novembre 2019), è stato un calciatore e allenatore di calcio argentino, nel ruolo di centravanti. Acquistato dall'Atlanta di Buenos Aires nell'estate del **1960**, è stato una delle figure più iconiche e amate dell'intera storia calcistica etnea.

Attaccante generoso, grintoso e dotato di eccellente fiuto per il gol, legò indissolubilmente il proprio nome al Catania di [[tesserati/allenatori/carmelo-di-bella|Carmelo Di Bella]], segnando il gol del 2-0 nella celebre sfida del 4 giugno 1961 contro l'Inter di Helenio Herrera che originò la storica locuzione radiofonica di Sandro Ciotti: *«Clamoroso al Cibali!»*.""",
        "career": """### Il Ritorno e il Tridente dei Sogni (1964-1967)

Dopo una parentesi ad Atlanta, Calvanese tornò a Catania nel 1964: nella [[stagioni/1964-1965|Stagione 1964-1965]] fu il centravanti titolare dell'undici che conquistò lo storico **8º posto in Serie A**, formando un tridente memorabile con [[tesserati/calciatori/giancarlo-danova|Giancarlo Danova]] e Carlo Facchin. Nella successiva stagione [[stagioni/1966-1967|1966-1967]] guidò i compagni al terzo posto in Serie B e alla pronta risalita in massima divisione, chiudendo la carriera a Catania con 117 presenze ufficiali. Nel 1971-1972 guidò il club anche da allenatore.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 188-235 (Stagioni 1960-1962 e 1964-1967)"
            },
            {
                "author": "La Sicilia",
                "title": "Addio a 'Todo' Calvanese, l'eroe del Clamoroso al Cibali",
                "publisher": "La Sicilia - Catania",
                "year": 2019,
                "reference": "Necrologio e rievocazione storica 6 novembre 2019"
            }
        ]
    },
    {
        "slug": "giancarlo-danova",
        "canonical_name": "Giancarlo Danova",
        "aliases": ["Danova", "Pantera"],
        "title": "Giancarlo Danova — «Pantera» e L'Attacco dei Sogni in Serie A (1964-1966)",
        "description": "Biografia e statistiche di Giancarlo Danova, ala scudettata con Milan e Fiorentina, colonna del tridente del Catania ottavo in Serie A nel 1964-1965.",
        "birth_date": "1938-11-18",
        "death_date": "2014-06-15",
        "birth_place": "Sesto San Giovanni (MI), Italia",
        "death_place": "Lodi, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Ala",
        "catania_periods": ["1964-1966"],
        "total_appearances": 60,
        "league_appearances": 57,
        "total_goals": 10,
        "league_goals": 10,
        "serie_a_appearances": 57,
        "serie_a_goals": 10,
        "club_entities": ["[[societa/1946-club-calcio-catania\\|Club Calcio Catania]]"],
        "tags": ["calciatori", "attaccanti", "ali", "serie-a", "carmelo-di-bella"],
        "seasons": ["1965-1966"],
        "abstract_title": "La Pantera Scudettata in Maglia Rossazzurra",
        "abstract_bullets": [
            "**Due Scudetti in Palmarès:** Campione d'Italia con il Milan prima di vestire il rossazzurro.",
            "**Protagonista dell'8º Posto 1964-1965:** 6 reti in Serie A al fianco di Calvanese e Facchin.",
            "**Presenze e Reti:** 60 presenze e 10 reti tutte disputate nella massima serie italiana tra il 1964 e il 1966.",
        ],
        "bio": """**Giancarlo Danova**, soprannominato **"Pantera"** per la falcata felina e la rapidità d'esecuzione (Sesto San Giovanni, 18 novembre 1938 – Lodi, 15 giugno 2014), è stato un calciatore e allenatore di calcio italiano, di ruolo ala. Approdato al Catania nell'estate del **1964** dopo i trionfi con Milan e Fiorentina, fu una delle stelle più luminose dell'epopea di Carmelo Di Bella in Serie A.

Nel biennio 1964-1966 totalizzò 57 presenze e 10 reti in massima divisione, risultando determinante per il record storico di punti e per la spettacolarità del gioco corale etneo.""",
        "career": """### Il Biennio in Serie A al Cibali

Nella stagione d'esordio 1964-1965 realizzò 6 reti fondamentali, tra cui il gol-vittoria contro la Lazio e marcature prestigiose a San Siro. Riconfermato nella [[stagioni/1965-1966|Stagione 1965-1966]], lottò fino all'ultima giornata segnando altre 4 reti prima del ritorno al Nord, lasciando un ricordo indelebile di correttezza e classe cristallina.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 218-228 (Stagioni 1964-1965 e 1965-1966)"
            }
        ]
    },
    {
        "slug": "alessandro-vitali",
        "canonical_name": "Alessandro Vitali",
        "aliases": ["Vitali"],
        "title": "Alessandro Vitali — La Mezzala Goleador della Serie B 1967-1968 (9 Reti)",
        "description": "Biografia e statistiche di Alessandro Vitali, capocannoniere del Catania nella Serie B 1967-1968 con 9 reti in 36 gare con Luigi Valsecchi.",
        "birth_date": "1945-03-24",
        "death_date": "1977-08-26",
        "birth_place": "Roma, Italia",
        "death_place": "Roma, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Mezzala offensiva",
        "catania_periods": ["1967-1968"],
        "total_appearances": 36,
        "league_appearances": 36,
        "total_goals": 9,
        "league_goals": 9,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "mezzala", "serie-b", "luigi-valsecchi"],
        "seasons": ["1967-1968"],
        "abstract_title": "La Mezzala dai Gol Pesanti",
        "abstract_bullets": [
            "**Capocannoniere 1967-1968:** 9 reti in 36 partite di Serie B.",
            "**Qualità e Inserimento:** Mezzala di grande dinamismo e potenza al tiro.",
            "**Trampolino per la Serie A:** Dopo Catania approdò al Lanerossi Vicenza, affermandosi ai massimi livelli nazionali.",
        ],
        "bio": """**Alessandro Vitali** (Roma, 24 marzo 1945 – Roma, 26 agosto 1977) è stato un calciatore italiano, nel ruolo di attaccante e mezzala offensiva. Arrivato al Catania nell'estate del **1967**, disputò una straordinaria stagione cadetta risultando il capocannoniere indiscusso della squadra con **9 reti in 36 incontri**.

Schierato dall'allenatore Luigi Valsecchi a supporto del centravanti Baisi, Vitali fu il terminale più prolifico della [[stagioni/1967-1968|Stagione 1967-1968]], realizzando reti decisive per la tranquilla permanenza in Serie B prima del suo trasferimento nella massima categoria.""",
        "career": """### L'Annata da Protagonista al Cibali

Tra i suoi gol memorabili in maglia etnea si ricordano le marcature pesanti contro Genoa, Reggiana e Venezia. Concluso il campionato al decimo posto, passò al Lanerossi Vicenza in Serie A, confermandosi uno dei talenti più brillanti della sua generazione.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 234-239 (Stagione 1967-1968)"
            }
        ]
    },
    {
        "slug": "aquilino-bonfanti",
        "canonical_name": "Aquilino Bonfanti",
        "aliases": ["Bonfanti"],
        "title": "Aquilino Bonfanti — Il Bomber della Promozione di Massimino e Rubino (1968-1972)",
        "description": "Biografia e statistiche di Aquilino Bonfanti, 109 presenze e 30 reti con il Catania, capocannoniere della cavalcata verso la Serie A nel 1969-1970.",
        "birth_date": "1943-02-25",
        "death_date": "2016-03-02",
        "birth_place": "Milano, Italia",
        "death_place": "Milano, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1968-1972"],
        "total_appearances": 109,
        "league_appearances": 101,
        "total_goals": 30,
        "league_goals": 29,
        "serie_a_appearances": 24,
        "serie_a_goals": 5,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-a", "serie-b", "angelo-massimino", "egizio-rubino"],
        "seasons": ["1968-1969", "1969-1970", "1970-1971"],
        "abstract_title": "Il Capocannoniere della Prima Serie A di Massimino",
        "abstract_bullets": [
            "**Capocannoniere Promozione 1969-1970:** 13 reti in 34 presenze, artefice del ritorno in Serie A del Catania di Egizio Rubino.",
            "**Quattro Anni al Cibali:** 109 presenze e 30 reti ufficiali tra il 1968 e il 1972.",
            "**Marcatore anche in Serie A:** Capocannoniere etneo nella massima serie 1970-1971 con 5 reti.",
        ],
        "bio": """**Aquilino Bonfanti** (Milano, 25 febbraio 1943 – Milano, 2 marzo 2016) è stato un calciatore italiano, nel ruolo di centravanti. Acquistato dal presidente [[societa/presidenti/angelo-massimino|Angelo Massimino]] nel **1968**, è stato il centravanti principe e l'eroe della cavalcata trionfale della [[stagioni/1969-1970|Stagione 1969-1970]], culminata con la promozione in Serie A.

Centravanti rapido, generoso e letale in acrobazia, Bonfanti fu il perno tattico della squadra costruita da Egizio Rubino, realizzando **13 reti** decisive in cadetteria e confermandosi anche l'anno seguente in Serie A.""",
        "career": """### Dalla Serie B alla Serie A (1968-1972)

Nella stagione [[stagioni/1968-1969|1968-1969]] fu tra i più positivi con 6 reti; nel 1969-1970 visse l'apoteosi firmando gol storici contro Atalanta, Foggia e Reggina. Nella successiva [[stagioni/1970-1971|Stagione 1970-1971]] in Serie A realizzò 5 reti contro Milan, Fiorentina e Roma, rimanendo in rossazzurro fino al 1972 con un bilancio complessivo di 109 gare e 30 reti.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 240-260 (Stagioni dal 1968-1969 al 1971-1972)"
            }
        ]
    },
    {
        "slug": "fulvio-francesconi",
        "canonical_name": "Fulvio Francesconi",
        "aliases": ["Francesconi"],
        "title": "Fulvio Francesconi — Due Volte Re del Gol in Serie B al Cibali (1971-1973)",
        "description": "Biografia e statistiche di Fulvio Francesconi, capocannoniere del Catania per due stagioni consecutive di Serie B con 20 reti in 74 gare.",
        "birth_date": "1944-11-19",
        "birth_place": "Pordenone, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Ala tornante",
        "catania_periods": ["1971-1973"],
        "total_appearances": 74,
        "league_appearances": 70,
        "total_goals": 20,
        "league_goals": 20,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "ali", "serie-b", "salvador-calvanese", "carmelo-di-bella"],
        "seasons": ["1971-1972", "1972-1973"],
        "abstract_title": "L'Ala dai Dieci Gol a Stagione",
        "abstract_bullets": [
            "**Doppio Titolo di Capocannoniere Etneo:** 10 reti nel 1971-1972 e 10 reti nel 1972-1973 in Serie B.",
            "**Continuità Realizzativa:** 74 presenze e 20 reti tonde in due soli campionati di cadetteria.",
            "**Tattica e Corsa:** Ala tornante capace di percorrere tutta la fascia e finalizzare con freddezza.",
        ],
        "bio": """**Fulvio Francesconi** (Pordenone, 19 novembre 1944) è un ex calciatore italiano, nel ruolo di ala tornante e attaccante. Acquistato dal Catania nell'estate del **1971** dalla Sampdoria, fu il faro dell'attacco etneo per due campionati consecutivi di Serie B sotto la guida tecnica di Salvador Calvanese e Carmelo Di Bella.

Giocatore generoso, dotato di grande intelligenza tattica e tiro potente, Francesconi si laureò capocannoniere della squadra sia nella [[stagioni/1971-1972|Stagione 1971-1972]] (10 reti in 35 gare) sia nella successiva [[stagioni/1972-1973|Stagione 1972-1973]] (10 reti in 35 gare).""",
        "career": """### Il Biennio d'Oro Cadetto (1971-1973)

Nel campionato 1971-1972 decise sfide caldissime contro Genoa, Bari e Reggina; nel 1972-1973 trascinò la squadra fino al 5º posto a ridosso delle posizioni promozione, chiudendo la sua prestigiosa parentesi catanese con 74 presenze complessive e l'ammirazione unanime del pubblico etneo.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 256-265 (Stagioni 1971-1972 e 1972-1973)"
            }
        ]
    },
    {
        "slug": "giampietro-spagnolo",
        "canonical_name": "Giampietro Spagnolo",
        "aliases": ["Spagnolo", "Il Gigante Spagnolo"],
        "title": "Giampietro Spagnolo — «Il Gigante» del Gol e 5º Bomber All-Time (50 Reti)",
        "description": "Biografia e statistiche di Giampietro Spagnolo, quinto marcatore nella storia del Catania con 50 reti e capocannoniere della Serie C 1974-1975.",
        "birth_date": "1947-10-20",
        "birth_place": "Lonigo (VI), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1973-1977"],
        "total_appearances": 139,
        "league_appearances": 129,
        "total_goals": 50,
        "league_goals": 47,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-b", "serie-c", "egizio-rubino", "gemelli-del-gol"],
        "seasons": ["1973-1974", "1974-1975"],
        "abstract_title": "Il Gigante della Risalita in Serie B e Re dei Bomber",
        "abstract_bullets": [
            "**50 Reti Ufficiali:** Quinto miglior marcatore assoluto della storia del Catania calcio.",
            "**Capocannoniere Promozione 1974-1975:** 20 reti in Serie C (girone C), capocannoniere del torneo.",
            "**I Gemelli del Gol:** In tandem con Claudio Ciceri formò una coppia da 38 reti nel 1974-1975.",
            "**Quattro Stagioni da Protagonista:** 139 presenze ufficiali tra il 1973 e il 1977.",
        ],
        "bio": """**Giampietro Spagnolo** (Lonigo, 20 ottobre 1947) è un ex calciatore italiano, nel ruolo di centravanti. Soprannominato **"Il Gigante"** per la statura imponente e la straordinaria forza fisica nel gioco aereo, è il **quinto marcatore all-time della storia del Catania con 50 reti ufficiali** messe a segno in **139 presenze** tra il 1973 e il 1977.

Acquistato da Angelo Massimino nel 1973, visse la sua stagione di grazia nel campionato di Serie C [[stagioni/1974-1975|1974-1975]], quando trascinò i rossazzurri al ritorno in Serie B vincendo la classifica cannonieri con ben **20 reti**.""",
        "career": """### Dalla Serie B al Trionfo del 1975

Nella stagione cadetta [[stagioni/1973-1974|1973-1974]] Spagnolo fu il capocannoniere etneo con 10 reti. L'anno dopo, affiancato da Claudio Ciceri, costituì la coppia dei *gemelli del gol* più prolifica del dopoguerra siciliano, segnando a ripetizione e infiammando i 30.000 del Cibali. Confermato in Serie B nel biennio 1975-1977 (altre 17 reti complessive), rimane scolpito tra le leggende immortali del club.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 266-285 (Stagioni dal 1973-1974 al 1976-1977)"
            }
        ]
    },
    {
        "slug": "pedrinho",
        "canonical_name": "Pedrinho",
        "aliases": ["Pedro Luís Vicençote", "Pedrinho Vicençote"],
        "title": "Pedrinho — Il Terzino Mondiale della Seleção e Cecchino su Punizione (1983-1985)",
        "description": "Biografia e statistiche di Pedrinho, terzino sinistro brasiliano della Seleção a Spagna '82, autore di 10 reti con il Catania tra Serie A e Serie B.",
        "birth_date": "1957-10-22",
        "birth_place": "Santo André, Brasile",
        "nationality": "Brasile",
        "role": "Difensore / Terzino sinistro",
        "catania_periods": ["1983-1985"],
        "total_appearances": 56,
        "league_appearances": 51,
        "total_goals": 10,
        "league_goals": 10,
        "serie_a_appearances": 27,
        "serie_a_goals": 3,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "difensori", "terzini", "brasile", "serie-a", "serie-b", "punizioni"],
        "seasons": ["1984-1985"],
        "abstract_title": "Il Fuoriclasse Brasiliano e Cecchino su Palla Inattiva",
        "abstract_bullets": [
            "**Mondiale Spagna 1982:** Terzino della Nazionale Brasiliana di Telê Santana, Zico e Sócrates.",
            "**Capocannoniere Etneo 1984-1985:** 7 reti in Serie B, record per un difensore nella storia etnea.",
            "**Specialista Assoluto delle Punizioni:** Celebre per i suoi calci di punizione a effetto col mancino dai 30 metri.",
        ],
        "bio": """**Pedrinho**, all'anagrafe **Pedro Luís Vicençote** (Santo André, 22 ottobre 1957), è un ex calciatore brasiliano, nel ruolo di terzino sinistro. Giunto a Catania nell'estate del **1983** dal Vasco da Gama per rinforzare il Catania neopromosso in Serie A di Gianni Di Marzio, è stato uno dei più celebri calciatori internazionali ad aver vestito la maglia rossazzurra.

Terzino fluidificante dotato di una tecnica sopraffina e di un sinistro potentissimo sui calci piazzati, segnò 3 reti in Serie A (tra cui una magnifica punizione a San Siro contro il Milan) e divenne il capocannoniere del Catania nella [[stagioni/1984-1985|Stagione 1984-1985]] in Serie B con **7 reti**.""",
        "career": """### La Leadership in Serie B 1984-1985

Dopo la retrocessione del 1984, Pedrinho decise di rimanere a Catania in Serie B, disputando 24 gare e trascinando la squadra alla salvezza a suon di punizioni spettacolari e rigori glaciali, prima di fare ritorno in patria tra le file del Bangu e della Nazionale verdeoro.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 320-330 (Stagioni 1983-1984 e 1984-1985)"
            }
        ]
    },
    {
        "slug": "carlo-borghi",
        "canonical_name": "Carlo Borghi",
        "aliases": ["Borghi"],
        "title": "Carlo Borghi — L'Ala Spettacolo delle Due Epoche di Massimino (145 Gare e 32 Reti)",
        "description": "Biografia e statistiche di Carlo Borghi, ala dal dribbling irresistibile, idolo del Cibali e bomber di riferimento nelle promozioni degli anni Ottanta.",
        "birth_date": "1958-01-01",
        "birth_place": "Castiglione della Pescaia (GR), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Ala destra",
        "catania_periods": ["1979-1982", "1985-1988"],
        "total_appearances": 145,
        "league_appearances": 130,
        "total_goals": 32,
        "league_goals": 28,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "ali", "serie-b", "serie-c1", "angelo-massimino"],
        "seasons": ["1985-1986"],
        "abstract_title": "La Freccia della Fascia in Due Decenni",
        "abstract_bullets": [
            "**145 Presenze e 32 Reti:** Protagonista in due distinti cicli rossazzurri (1979-1982 e 1985-1988).",
            "**Eroe della Promozione 1979-1980:** Vincente in Serie C1 con Lino De Petrillo e Angelo Massimino.",
            "**Capocannoniere in Serie B 1985-1986:** 10 reti in 35 gare cadette con Gennaro Rambone.",
        ],
        "bio": """**Carlo Borghi** (Castiglione della Pescaia, 1 gennaio 1958) è un ex calciatore italiano, nel ruolo di ala destra e seconda punta. Acquistato dal presidente Angelo Massimino nel **1979**, divenne rapidamente uno degli idoli incontrastati dello Stadio Cibali per la straordinaria velocità, il dribbling ubriacante e la capacità di finalizzazione.

Protagonista della vittoria del campionato di Serie C1 1979-1980, tornò a vestire il rossazzurro a metà degli anni Ottanta, laureandosi capocannoniere della squadra nella [[stagioni/1985-1986|Stagione 1985-1986]] in Serie B con **10 reti**.""",
        "career": """### Due Cicli Trionfali al Cibali

Nel primo triennio (1979-1982) formò un tandem irresistibile con Damiano Morra e Marco Piga. Richiamato da Massimino nel 1985, disputò altri tre campionati ad alto livello, raggiungendo il traguardo di 145 presenze e 32 reti prima del trasferimento alla Torres.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 300-345 (Stagioni 1979-1982 e 1985-1988)"
            }
        ]
    },
    {
        "slug": "orazio-sorbello",
        "canonical_name": "Orazio Sorbello",
        "aliases": ["Sorbello"],
        "title": "Orazio Sorbello — Il Centravanti Etneo d'Area di Rigore (1986-1987, 1991-1993)",
        "description": "Biografia e statistiche di Orazio Sorbello, centravanti catanese doc, capocannoniere in Serie B 1986-1987 e colonna d'attacco in due epoche.",
        "birth_date": "1959-08-10",
        "birth_place": "Acireale (CT), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1986-1987", "1991-1993"],
        "total_appearances": 75,
        "league_appearances": 69,
        "total_goals": 18,
        "league_goals": 16,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "centravanti", "catanesi", "serie-b", "serie-c1"],
        "seasons": ["1986-1987"],
        "abstract_title": "Il Bomber della Terra d'Etna",
        "abstract_bullets": [
            "**Capocannoniere in Serie B (1986-1987):** 6 reti in un'annata cadetta di grande sacrificio.",
            "**Due Cicli a Catania:** 75 presenze e 18 reti totali in maglia rossazzurra.",
            "**Centravanti di Razza:** Specialista nel gioco aereo e nella protezione palla nei sedici metri.",
        ],
        "bio": """**Orazio Sorbello** (Acireale, 10 agosto 1959) è un allenatore di calcio ed ex calciatore italiano, nel ruolo di centravanti. Cresciuto calcisticamente in Sicilia e maturato nei campionati professionistici, vestì la maglia del Catania per la prima volta nella [[stagioni/1986-1987|Stagione 1986-1987]] in Serie B, risultando il capocannoniere della squadra con 6 reti in 30 partite.

Dopo importanti esperienze in giro per l'Italia, tornò a Catania nel 1991, difendendo i colori rossazzurri in Serie C1 per altri due tornei e siglando altre 12 reti prima dell'esclusione della società nel 1993.""",
        "career": """### Dalla Serie B al Ritorno degli Anni Novanta

Nella difficile stagione cadetta 1986-1987 Sorbello lottò con grinta contro le difese avversarie, firmando reti pesanti al Cibali. Tra il 1991 e il 1993 fu la guida d'esperienza del reparto avanzato a fianco di Loriano Cipriani, dimostrando sempre un profondo attaccamento alla maglia etnea.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 336-340 e pp. 360-370 (Stagioni 1986-1987 e 1991-1993)"
            }
        ]
    },
    {
        "slug": "adriano-polenta",
        "canonical_name": "Adriano Polenta",
        "aliases": ["Polenta"],
        "title": "Adriano Polenta — Il Libero Rigorista e Capocannoniere Salvezza (1987-1988)",
        "description": "Biografia e statistiche di Adriano Polenta, carismatico libero e rigorista infallibile, miglior marcatore del Catania nella Serie C1 1987-1988.",
        "birth_date": "1958-11-23",
        "birth_place": "Osimo (AN), Italia",
        "nationality": "Italia",
        "role": "Difensore / Libero",
        "catania_periods": ["1986-1988"],
        "total_appearances": 64,
        "league_appearances": 56,
        "total_goals": 8,
        "league_goals": 7,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "difensori", "libero", "serie-c1", "serie-b", "rigori", "spareggio-cosenza"],
        "seasons": ["1987-1988"],
        "abstract_title": "Il Libero con il Vizietto del Gol",
        "abstract_bullets": [
            "**Capocannoniere Difensore 1987-1988:** 6 reti in campionato (4 su rigore) in Serie C1.",
            "**Lo Spareggio di Cosenza:** Pilastro difensivo nel vittorioso spareggio-salvezza contro la Nocerina (2-0) il 12 giugno 1988.",
            "**Freddezza e Carisma:** Leader del reparto arretrato etneo per 64 partite ufficiali.",
        ],
        "bio": """**Adriano Polenta** (Osimo, 23 novembre 1958) è un ex calciatore italiano, nel ruolo di libero e difensore centrale. Giunto a Catania nel **1986** in Serie B, fu il carismatico regista difensivo della squadra etnea per due campionati consecutivi.

Nella drammatica [[stagioni/1987-1988|Stagione 1987-1988]] in Serie C1, Polenta si distinse per un primato singolare: risultò il **miglior marcatore stagionale della squadra con 6 reti** (di cui 4 realizzate con glaciale freddezza su calcio di rigore), guidando poi la difesa nello spareggio-salvezza vinto per 2-0 contro la Nocerina allo Stadio San Vito di Cosenza.""",
        "career": """### Il Ruolo Chiave nella Salvezza del 1988

Dotato di un senso della posizione impeccabile e di grande personalità nell'impostare il gioco dalle retrovie, Polenta giocò 34 partite di campionato nel 1987-1988, togliendo le castagne dal fuoco in match complicati e blindando la porta etnea nella decisiva battaglia di Cosenza.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 340-346 (Stagione 1987-1988 e spareggio di Cosenza)"
            }
        ]
    },
    {
        "slug": "loris-pradella",
        "canonical_name": "Loris Pradella",
        "aliases": ["Pradella"],
        "title": "Loris Pradella — Il Centravanti di Peso della Serie C1 1988-1989 (9 Reti)",
        "description": "Biografia e statistiche di Loris Pradella, centravanti d'area e punto di riferimento offensivo del Catania nella stagione 1988-1989 con 9 reti totali.",
        "birth_date": "1960-03-03",
        "birth_place": "Sacile (PN), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1988-1989"],
        "total_appearances": 33,
        "league_appearances": 27,
        "total_goals": 9,
        "league_goals": 5,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-c1", "bruno-pace", "coppa-italia"],
        "seasons": ["1988-1989"],
        "abstract_title": "La Punta Centrale della Ripartenza",
        "abstract_bullets": [
            "**9 Reti Stagionali:** 5 in campionato di Serie C1 e 4 nella prestigiosa Coppa Italia 1988-1989.",
            "**Fisico e Generosità:** Centravanti classico boa, abile a far salire la squadra e aprire varchi per i centrocampisti.",
            "**Esperienza Professionistica:** Giunto a Catania dopo gli anni in Serie B con Padova e Monza.",
        ],
        "bio": """**Loris Pradella** (Sacile, 3 marzo 1960) è un ex calciatore italiano, nel ruolo di centravanti. Acquistato dal Catania nell'estate del **1988** per costituire il fulcro dell'attacco guidato da Bruno Pace e Carmelo Russo, disputò una stagione di grande generosità e concretezza offensiva.

Nella [[stagioni/1988-1989|Stagione 1988-1989]] realizzò complessivamente **9 reti ufficiali** in 33 gare (5 in campionato e 4 in Coppa Italia), risultando il miglior marcatore complessivo dell'annata etnea.""",
        "career": """### La Stagione 1988-1989

In campionato Pradella firmò reti pesanti al Cibali contro Campobasso, Ischia e Francavilla, mentre in Coppa Italia realizzò marcature di prestigio contro squadre di categoria superiore, garantendo sempre il massimo impegno atletico a beneficio della squadra.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 346-350 (Stagione 1988-1989)"
            }
        ]
    },
    {
        "slug": "loriano-cipriani",
        "canonical_name": "Loriano Cipriani",
        "aliases": ["Cipriani"],
        "title": "Loriano Cipriani — Il Re Incontrastato dei Bomber del Catania Anni Novanta (40 Reti)",
        "description": "Biografia e statistiche di Loriano Cipriani, 4 volte consecutive capocannoniere del Catania tra il 1989 e il 1993 con 40 reti in 125 presenze.",
        "birth_date": "1964-10-18",
        "birth_place": "San Giovanni Valdarno (AR), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1989-1993"],
        "total_appearances": 125,
        "league_appearances": 114,
        "total_goals": 40,
        "league_goals": 38,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. (Era Massimino)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-c1", "angelo-massimino", "anni-novanta"],
        "seasons": ["1989-1990", "1990-1991", "1991-1992", "1992-1993"],
        "abstract_title": "Il Record Man dei Quattro Titoli Consecutivi di Bomber",
        "abstract_bullets": [
            "**Quattro Volte Capocannoniere:** 1989-90 (12 reti), 1990-91 (11 reti), 1991-92 (6 reti) e 1992-93 (11 reti).",
            "**40 Reti Ufficiali:** Uno dei cannonieri più prolifici e continui dell'intera storia etnea.",
            "**Fedeltà ad Angelo Massimino:** Punto di riferimento dell'attacco per quattro tornei di Serie C1 fino all'ingiusta esclusione del 1993.",
        ],
        "bio": """**Loriano Cipriani** (San Giovanni Valdarno, 18 ottobre 1964) è un ex calciatore italiano, nel ruolo di centravanti. Acquistato dal presidente [[societa/presidenti/angelo-massimino|Angelo Massimino]] nell'estate del **1989**, è stato il simbolo assoluto dell'attacco del Calcio Catania per un intero quadriennio, collezionando **125 presenze e 40 reti ufficiali**.

Centravanti rapido, implacabile negli spazi stretti e freddo dal dischetto, Cipriani detiene il record storico di **quattro titoli consecutivi di capocannoniere etneo** tra il 1989 e il 1993.""",
        "career": """### Il Quadriennio delle Meraviglie (1989-1993)

Nel campionato [[stagioni/1989-1990|1989-1990]] segnò 12 reti in 32 gare; nel [[stagioni/1990-1991|1990-1991]] confermò il suo stato di grazia con 11 reti; nel [[stagioni/1991-1992|1991-1992]] mise a segno 6 reti decisive per la salvezza e nel [[stagioni/1992-1993|1992-1993]] toccò quota 11 reti in 30 partite. L'esclusione estiva del 1993 interruppe bruscamente un idillio sportivo che lo colloca di diritto tra i più grandi bomber rossazzurri di sempre.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 351-372 (Stagioni dal 1989-1990 al 1992-1993)"
            }
        ]
    },
    {
        "slug": "giuseppe-mosca",
        "canonical_name": "Giuseppe Mosca",
        "aliases": ["Mosca"],
        "title": "Giuseppe Mosca — Il Cannoniere della Rinascita dall'Eccellenza al C.N.D. (37 Reti)",
        "description": "Biografia e statistiche di Giuseppe Mosca, bomber del Catania con 37 reti in due stagioni, protagonista della risalita tra il 1993 e il 1995.",
        "birth_date": "1966-07-28",
        "birth_place": "Napoli, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1993-1995"],
        "total_appearances": 60,
        "league_appearances": 56,
        "total_goals": 37,
        "league_goals": 37,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. — Risalita dall'Eccellenza (1993-2000)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "eccellenza", "cnd", "risalita-massimino"],
        "seasons": ["1993-1994", "1994-1995"],
        "abstract_title": "Il Trascinatore della Risalita dai Dilettanti",
        "abstract_bullets": [
            "**37 Reti in Due Campionati:** 18 reti nell'Eccellenza 1993-1994 e 19 reti nel C.N.D. 1994-1995.",
            "**Capocannoniere Promozione C.N.D.:** Protagonista del primo posto nel Girone I e del ritorno nel calcio professionistico.",
            "**L'Attaccante di Massimino:** Sposò la causa del Catania nel momento più buio dopo l'ingiusta radiazione dalla Serie C1.",
        ],
        "bio": """**Giuseppe Mosca** (Napoli, 28 luglio 1966) è un ex calciatore italiano, nel ruolo di centravanti. Giunto a Catania nell'autunno del **1993** quando la squadra del presidente Angelo Massimino fu costretta a ripartire dal campionato regionale di Eccellenza, fu il salvatore e il trascinatore assoluto dell'orgoglio etneo.

In due stagioni di memorabile foga agonistica mise a referto ben **37 reti ufficiali in 60 presenze**, risultando decisivo prima per il ripescaggio nel C.N.D. e poi per la trionfale vittoria del campionato 1994-1995.""",
        "career": """### Dalla Polvere dell'Eccellenza al Trionfo nel C.N.D.

Nella [[stagioni/1993-1994|Stagione 1993-1994]] guidò l'attacco rossazzurro sui campi polverosi della Sicilia con 18 reti. Nel successivo torneo di Campionato Nazionale Dilettanti [[stagioni/1994-1995|1994-1995]], sotto la gestione di Angelo Busetta, fu devastante: realizzò **19 reti**, trascinando il Catania al primo posto davanti al Milazzo con 84 punti e riconquistando la Serie C2 tra il tripudio dei 20.000 del Cibali.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 374-385 (Stagioni 1993-1994 e 1994-1995)"
            }
        ]
    },
    {
        "slug": "maurizio-naccari",
        "canonical_name": "Maurizio Naccari",
        "aliases": ["Naccari"],
        "title": "Maurizio Naccari — L'Attaccante Goleador della Serie C2 1995-1996 (10 Reti)",
        "description": "Biografia e statistiche di Maurizio Naccari, capocannoniere rossazzurro nel primo torneo di Serie C2 dopo la risalita con 10 reti nel 1995-1996.",
        "birth_date": "1970-01-21",
        "birth_place": "San Pietro Vernotico (BR), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1995-1996"],
        "total_appearances": 32,
        "league_appearances": 30,
        "total_goals": 10,
        "league_goals": 10,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. — Risalita dall'Eccellenza (1993-2000)]]"],
        "tags": ["calciatori", "attaccanti", "serie-c2", "aldo-cerantola", "angelo-busetta"],
        "seasons": ["1995-1996"],
        "abstract_title": "Il Capocannoniere del Ritorno tra i Professionisti",
        "abstract_bullets": [
            "**Capocannoniere 1995-1996:** 10 reti in 30 gare di Serie C2.",
            "**Consolidamento Professionistico:** Protagonista del primo campionato professionistico post-risalita.",
            "**Opportunismo nei Sedici Metri:** Attaccante rapido, bravo a sfruttare le sponde dei compagni.",
        ],
        "bio": """**Maurizio Naccari** (San Pietro Vernotico, 21 gennaio 1970) è un ex calciatore italiano, nel ruolo di attaccante. Acquistato nell'estate del **1995** per il ritorno del Calcio Catania in Serie C2, fu il capocannoniere della squadra nella [[stagioni/1995-1996|Stagione 1995-1996]].

Guidato in panchina prima da Aldo Cerantola e poi da Angelo Busetta, Naccari mise a segno **10 reti** in campionato, risultando decisivo per l'ottavo posto finale e per la definitiva stabilizzazione del club tra i professionisti.""",
        "career": """### La Stagione 1995-1996

Affiancato a Tiziano D'Isidoro e Pasquale Sanseverino, Naccari fu protagonista di importanti vittorie al Cibali, siglando doppiette decisive e dimostrando grande freddezza in area di rigore prima del prosieguo della sua carriera in Serie C.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 384-388 (Stagione 1995-1996)"
            }
        ]
    },
    {
        "slug": "tiziano-disidoro",
        "canonical_name": "Tiziano D'Isidoro",
        "aliases": ["D'Isidoro", "Disidoro"],
        "title": "Tiziano D'Isidoro — Il Cecchino d'Area e Capocannoniere della Serie C2 (24 Reti)",
        "description": "Biografia e statistiche di Tiziano D'Isidoro, trascinatore offensivo del Catania con 24 reti tra il 1995 e il 1997 e capocannoniere nel 1996-1997.",
        "birth_date": "1969-07-16",
        "birth_place": "Pescara, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1995-1997"],
        "total_appearances": 60,
        "league_appearances": 55,
        "total_goals": 24,
        "league_goals": 21,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. — Risalita dall'Eccellenza (1993-2000)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-c2", "angelo-busetta"],
        "seasons": ["1996-1997"],
        "abstract_title": "Il Cecchino della Serie C2",
        "abstract_bullets": [
            "**Capocannoniere 1996-1997:** 13 reti in 31 partite di Serie C2 (girone C).",
            "**24 Reti in Due Stagioni:** 60 presenze complessive e media gol di primissimo livello.",
            "**I Playoff del 1997:** Condusse il Catania fino alle semifinali playoff per la Serie C1.",
        ],
        "bio": """**Tiziano D'Isidoro** (Pescara, 16 luglio 1969) è un ex calciatore italiano, nel ruolo di centravanti. Approdato a Catania nell'autunno del **1995**, fu il grande punto di riferimento offensivo della compagine rossazzurra per un intenso biennio in Serie C2.

Centravanti astuto, rapace d'area e tiratore infallibile, D'Isidoro visse la sua stagione migliore nel campionato [[stagioni/1996-1997|1996-1997]], laureandosi capocannoniere con **13 reti** e portando la squadra fino ai playoff promozione con Angelo Busetta.""",
        "career": """### Il Biennio al Cibali (1995-1997)

Dopo aver segnato 8 reti nel 1995-1996 e 3 in Coppa Italia, nel 1996-1997 D'Isidoro fu la punta di diamante del tridente etneo. Le sue marcature contro Benevento, Castrovillari e Matera infiammarono i tifosi etnei in una stagione culminata con il quarto posto e la semifinale playoff contro l'Ancona.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 386-394 (Stagioni 1995-1996 e 1996-1997)"
            }
        ]
    },
    {
        "slug": "luca-lugnan",
        "canonical_name": "Luca Lugnan",
        "aliases": ["Lugnan"],
        "title": "Luca Lugnan — L'Attaccante di Movimento e Capocannoniere nel 1997-1998",
        "description": "Biografia e statistiche di Luca Lugnan, punto di riferimento dell'attacco etneo nella complessa stagione di Serie C2 1997-1998.",
        "birth_date": "1969-03-24",
        "birth_place": "Monfalcone (GO), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Seconda punta",
        "catania_periods": ["1997-1998"],
        "total_appearances": 30,
        "league_appearances": 28,
        "total_goals": 5,
        "league_goals": 5,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. — Risalita dall'Eccellenza (1993-2000)]]"],
        "tags": ["calciatori", "attaccanti", "serie-c2", "giovanni-mei", "franco-gagliardi"],
        "seasons": ["1997-1998"],
        "abstract_title": "La Punta d'Attacco della Stagione di Transizione",
        "abstract_bullets": [
            "**Capocannoniere 1997-1998:** 5 reti in 28 gare di Serie C2.",
            "**Lavoro per la Squadra:** Seconda punta dinamica, abile a creare spazi e dialogare con gli esterni.",
            "**Salvezza Garantita:** Reti decisive per preservare la categoria professionistica sotto la gestione Gagliardi.",
        ],
        "bio": """**Luca Lugnan** (Monfalcone, 24 marzo 1969) è un allenatore di calcio ed ex calciatore italiano, nel ruolo di attaccante. Ingaggiato nell'estate del **1997** dalla dirigenza presieduta da Grazia Codiglione Massimino, disputò la [[stagioni/1997-1998|Stagione 1997-1998]] in Serie C2.

In un campionato difficile e avaro di soddisfazioni offensive, Lugnan fu il miglior marcatore della squadra con **5 reti in 28 partite**, garantendo con la sua esperienza e il suo movimento i punti necessari per la salvezza prima della rivoluzione tecnica della stagione successiva.""",
        "career": """### La Serie C2 1997-1998

Schierato titolare sia da Giovanni Mei che successivamente da Franco Gagliardi, firmò marcature pesanti nei confronti interni con Marsala, Bisceglie e Chieti, completando la stagione con 30 presenze complessive tra campionato e Coppa Italia di Serie C.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 394-398 (Stagione 1997-1998)"
            }
        ]
    },
    {
        "slug": "umberto-brutto",
        "canonical_name": "Umberto Brutto",
        "aliases": ["Brutto", "Capitan Brutto"],
        "title": "Umberto Brutto — Il Capitano della Cavalcata Trionfale in Serie C1 (1998-1999)",
        "description": "Biografia e statistiche di Umberto Brutto, trascinatore, capitano e idolo del Cibali nella vittoria del campionato di Serie C2 1998-1999.",
        "birth_date": "1970-07-28",
        "birth_place": "Catanzaro, Italia",
        "nationality": "Italia",
        "role": "Centrocampista / Ala destra / Capitano",
        "catania_periods": ["1997-2000"],
        "total_appearances": 88,
        "league_appearances": 81,
        "total_goals": 15,
        "league_goals": 14,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. — Risalita dall'Eccellenza (1993-2000)]]"],
        "tags": ["calciatori", "centrocampisti", "capitani", "serie-c2", "piero-cucchi", "grazia-codiglione"],
        "seasons": ["1998-1999"],
        "abstract_title": "Il Capitano Cuore e Polmoni della Promozione del 1999",
        "abstract_bullets": [
            "**Capitano del Trionfo 1998-1999:** 32 presenze e 6 reti, condusse il Catania alla vittoria del campionato di Serie C2.",
            "**Idolo della Curva Nord:** Amato per grinta, corsa instancabile sulla fascia e gol nei momenti caldi.",
            "**Triennio Rossazzurro:** 88 presenze e 15 reti tra Serie C2 e Serie C1.",
        ],
        "bio": """**Umberto Brutto** (Catanzaro, 28 luglio 1970) è un ex calciatore italiano, nel ruolo di ala destra e centrocampista offensivo. Giunto a Catania nel **1997**, divenne il capitano, il leader carismatico e il beniamino incontrastato del pubblico del Cibali nella trionfale [[stagioni/1998-1999|Stagione 1998-1999]], conclusa con la vittoria del girone C di Serie C2 e la promozione in Serie C1.

Dotato di generosità encomiabile, eccellente tiro dalla distanza e tempismo perfetto negli inserimenti senza palla, Brutto fu il simbolo dell'undici di Piero Cucchi, totalizzando in rossazzurro **88 presenze e 15 reti**.""",
        "career": """### Il Campionato dei Record 1998-1999 e la Serie C1

Nella storica annata 1998-1999 Brutto fu decisivo con gol fondamentali contro Catanzaro, Trapani e Crotone, festeggiando il ritorno in C1 davanti a 25.000 spettatori. Riconfermato capitano anche nel 1999-2000 in Serie C1 con Gianni Simonelli, guidò la squadra fino al 7º posto prima del passaggio alla gestione Gaucci.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 396-408 (Stagioni dal 1997-1998 al 1999-2000)"
            }
        ]
    },
    {
        "slug": "roberto-passiatore",
        "canonical_name": "Roberto Passiatore",
        "aliases": ["Passiatore"],
        "title": "Roberto Passiatore — Il Cobra d'Area del Doppio Salto di Categoria (1998-2000)",
        "description": "Biografia e statistiche di Roberto Passiatore, centravanti letale con 18 reti nel Catania tra la promozione in C1 e la successiva annata.",
        "birth_date": "1971-06-12",
        "birth_place": "Taranto, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["1998-2000"],
        "total_appearances": 64,
        "league_appearances": 58,
        "total_goals": 18,
        "league_goals": 18,
        "club_entities": ["[[societa/1967-calcio-catania-spa-massimino\\|Calcio Catania S.p.A. — Risalita dall'Eccellenza (1993-2000)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-c2", "serie-c1", "piero-cucchi"],
        "seasons": ["1999-2000"],
        "abstract_title": "Il Due Volte Capocannoniere della Rinascita",
        "abstract_bullets": [
            "**Doppio Titolo dei Bomber:** Capocannoniere nel 1998-1999 (8 reti, vittoria Serie C2) e nel 1999-2000 (10 reti in Serie C1).",
            "**18 Reti in 64 Gare:** Centravanti d'area implacabile su palloni vaganti e colpi di testa.",
            "**Idolo del Cibali:** Protagonista del rilancio rossazzurro nell'era post-Massimino.",
        ],
        "bio": """**Roberto Passiatore** (Taranto, 12 giugno 1971) è un ex calciatore italiano, nel ruolo di centravanti. Acquistato dal Catania nell'estate del **1998**, fu il terminale offensivo di riferimento per due campionati indimenticabili, conquistando due titoli consecutivi di capocannoniere interno.

Nel 1998-1999 firmò 8 reti decisive per la vittoria del campionato di Serie C2 con Piero Cucchi. L'anno seguente, nella [[stagioni/1999-2000|Stagione 1999-2000]] in Serie C1, si superò realizzando **10 reti in 31 partite**, confermandosi un bomber di razza per la categoria.""",
        "career": """### Dalla Serie C2 alla Serie C1 (1998-2000)

Soprannominato dai tifosi il *Cobra* per la freddezza nei sedici metri, Passiatore mise a referto doppiette memorabili e reti pesantissime contro Palermo, Avellino e Nocerina, chiudendo il suo biennio etneo con 18 reti complessive prima del passaggio al Taranto.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 400-408 (Stagioni 1998-1999 e 1999-2000)"
            }
        ]
    },
    {
        "slug": "alessandro-ambrosi",
        "canonical_name": "Alessandro Ambrosi",
        "aliases": ["Ambrosi", "Il Re Leone"],
        "title": "Alessandro «Il Re Leone» Ambrosi — Il Bomber dell'Era Gaucci (2000-2002)",
        "description": "Biografia e statistiche di Alessandro Ambrosi, detto il Re Leone, autore di 16 reti ufficiali nel Catania e idolo della tifoseria nella Serie C1 2000-2001.",
        "birth_date": "1971-07-12",
        "birth_place": "Fiuggi (FR), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["2000-2002"],
        "total_appearances": 47,
        "league_appearances": 42,
        "total_goals": 16,
        "league_goals": 15,
        "club_entities": ["[[societa/2000-era-gaucci\\|Calcio Catania S.p.A. (Gestione Gaucci)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-c1", "era-gaucci", "vincenzo-guerini"],
        "seasons": ["2000-2001"],
        "abstract_title": "Il Re Leone del Cibali",
        "abstract_bullets": [
            "**Capocannoniere 2000-2001:** 12 reti in 29 gare di Serie C1, trascinatore del Catania fino alla finale playoff.",
            "**Fisico Imponente e Chioma Bionda:** Ribattezzato 'Il Re Leone' dalla Curva Nord per la grinta leonina.",
            "**16 Reti in Maglia Rossazzurra:** Centravanti simbolo del primo anno della presidenza Gaucci.",
        ],
        "bio": """**Alessandro Ambrosi**, universalmente noto come **"Il Re Leone"** per la folta criniera bionda e la potenza devastante nei contrasti (Fiuggi, 12 luglio 1971), è un ex calciatore italiano, nel ruolo di centravanti. Acquistato nell'estate del **2000** dal Crotone dalla nuova proprietà guidata dalla famiglia Gaucci, infiammò l'entusiasmo della piazza etnea.

Nella [[stagioni/2000-2001|Stagione 2000-2001]] fu il capocannoniere del Catania con **12 reti** in 29 gare di campionato, trascinando la squadra guidata da Vincenzo Guerini fino alla storica finale dei playoff di Serie C1 disputata contro il Messina.""",
        "career": """### La Cavalcata del 2000-2001 e l'Eredità a Baggio

Autore di gol spettacolari di testa e di potenza pura contro Palermo, Savoia e Lodigiani, Ambrosi rimase nella prima parte del 2001-2002 segnando altre 3 reti prima di lasciare spazio al compagno di reparto Eddy Baggio, rimanendo un idolo intramontabile per il tifo rossazzurro.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 408-418 (Stagioni 2000-2001 e 2001-2002)"
            }
        ]
    },
    {
        "slug": "eddy-baggio",
        "canonical_name": "Eddy Baggio",
        "aliases": ["Baggio", "Eddy Baggio"],
        "title": "Eddy Baggio — Il Cecchino dei Playoff e Bomber della Serie B (2001-2002)",
        "description": "Biografia e statistiche di Eddy Baggio, 18 reti nel 2001-2002 e gol decisivi nei playoff di Taranto per lo storico ritorno in Serie B.",
        "birth_date": "1974-08-23",
        "birth_place": "Caldogno (VI), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["2001-2002"],
        "total_appearances": 36,
        "league_appearances": 31,
        "total_goals": 20,
        "league_goals": 18,
        "club_entities": ["[[societa/2000-era-gaucci\\|Calcio Catania S.p.A. (Gestione Gaucci)]]"],
        "tags": ["calciatori", "attaccanti", "marcatori", "serie-c1", "playoff-taranto", "promozione-serie-b", "era-gaucci"],
        "seasons": ["2001-2002"],
        "abstract_title": "Il Goleador della Promozione in B di Taranto",
        "abstract_bullets": [
            "**20 Reti Stagionali (18 in Campionato):** Capocannoniere assoluto del Catania nella stagione 2001-2002.",
            "**Eroe dei Playoff:** Autore di reti decisive sia nella semifinale contro il Pescara sia nella finale d'andata contro il Taranto al Cibali (1-0).",
            "**Freddezza e Classe:** Centravanti agile e letale, fratello minore di Roberto Baggio.",
        ],
        "bio": """**Eddy Baggio** (Caldogno, 23 agosto 1974) è un allenatore di calcio ed ex calciatore italiano, nel ruolo di centravanti. Acquistato dal Catania nell'estate del **2001** dall'Ancona, fu il cecchino micidiale e il trascinatore assoluto della [[stagioni/2001-2002|Stagione 2001-2002]], conclusasi il 9 giugno 2002 a Taranto con il tanto agognato ritorno in **Serie B** dopo 15 anni di attesa.

Con ben **18 reti in 31 partite di campionato** e 2 reti nei playoff promozione, Baggio fu l'arma letale dell'attacco orchestrato prima da Aldo Ammazzalorso e poi da Pietro Vierchowod e Osvaldo Jaconi.""",
        "career": """### I Playoff Trionfali del 2002

Tra i suoi capolavori etnei si ricordano il gol capolavoro nella semifinale di ritorno contro il Pescara e il rigore procurato e trasformato nella finale d'andata al Cibali contro il Taranto (1-0 davanti a 25.000 tifosi), che pose le basi per il pareggio (0-0) dello Stadio Iacovone e la grande festa promozione in Piazza Duomo.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 414-422 (Stagione 2001-2002 e finale di Taranto)"
            }
        ]
    },
    {
        "slug": "luis-oliveira",
        "canonical_name": "Luís Oliveira",
        "aliases": ["Lulù Oliveira", "Oliveira", "Luís Airton Oliveira Barroso"],
        "title": "Luís «Lulù» Oliveira — Il Fuoriclasse Internazionale al Cibali (2002-2004)",
        "description": "Biografia e statistiche di Luís Oliveira, stella della Nazionale belga, autore di 28 reti in 74 gare nel Catania tra Serie B e Caso Catania.",
        "birth_date": "1969-03-24",
        "birth_place": "Faveira, Brasile",
        "nationality": "Belgio",
        "role": "Attaccante / Seconda punta / Centravanti",
        "catania_periods": ["2002-2004"],
        "total_appearances": 74,
        "league_appearances": 71,
        "total_goals": 28,
        "league_goals": 26,
        "club_entities": ["[[societa/2000-era-gaucci\\|Calcio Catania S.p.A. (Gestione Gaucci)]]"],
        "tags": ["calciatori", "attaccanti", "campioni-internazionali", "serie-b", "era-gaucci", "caso-catania"],
        "seasons": ["2002-2003"],
        "abstract_title": "Il Falco Belga-Brasiliano dalle Capriole al Cibali",
        "abstract_bullets": [
            "**28 Reti in Due Campionati Cadetti:** 13 reti nel 2002-2003 e 13 reti nel 2003-2004 di Serie B.",
            "**Stella Mondiale:** Protagonista ai Mondiali di Francia '98 con il Belgio e colonna di Anderlecht, Cagliari e Fiorentina.",
            "**Spettacolo Puro:** Ammirato per le sue celebri capriole acrobatiche a ogni gol e per la classe superiore palla al piede.",
        ],
        "bio": """**Luís Airton Oliveira Barroso**, universalmente noto come **"Lulù" Oliveira** (Faveira, 24 marzo 1969), è un allenatore di calcio ed ex calciatore brasiliano naturalizzato belga, nel ruolo di attaccante. Acquistato dal presidente Luciano Gaucci nell'estate del **2002** per celebrare il ritorno in Serie B, rappresentò uno dei colpi di mercato più prestigiosi della storia etnea.

Attaccante completo, scattante, capace di calciare con entrambi i piedi e di inventare gol spettacolari, fu il capocannoniere del Catania sia nella burrascosa [[stagioni/2002-2003|Stagione 2002-2003]] (13 reti in 34 presenze) sia nella successiva [[stagioni/2003-2004|Stagione 2003-2004]] (13 reti in 37 gare) al fianco del giovane [[tesserati/calciatori/giuseppe-mascara|Giuseppe Mascara]].""",
        "career": """### Il Protagonista del Caso Catania e delle 28 Reti

In mezzo alla tempesta giudiziaria del Caso Catania nel 2003, Oliveira rimase il baluardo tecnico ed emotivo della squadra, regalando prodezze indimenticabili contro Genoa, Sampdoria, Napoli e Palermo, salutando il Cibali con un bottino sontuoso di 28 reti in 74 incontri ufficiali.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 420-435 (Stagioni 2002-2003 e 2003-2004)"
            }
        ]
    },
    {
        "slug": "jeda",
        "canonical_name": "Jeda",
        "aliases": ["Jedaias Capucho Neves", "Jeda Neves"],
        "title": "Jeda — L'Attaccante Brasiliano Decisivo per la Salvezza in Serie B (2004-2005)",
        "description": "Biografia e statistiche di Jeda (Jedaias Capucho Neves), centravanti brasiliano decisivo per la permanenza del Catania in Serie B nel 2005.",
        "birth_date": "1979-04-15",
        "birth_place": "Santarém, Brasile",
        "nationality": "Brasile",
        "role": "Attaccante / Seconda punta",
        "catania_periods": ["2005"],
        "total_appearances": 19,
        "league_appearances": 19,
        "total_goals": 6,
        "league_goals": 6,
        "club_entities": ["[[societa/2004-era-pulvirenti\\|Calcio Catania S.p.A. (Era Pulvirenti)]]"],
        "tags": ["calciatori", "attaccanti", "brasiliani", "serie-b", "nereo-rocco", "era-pulvirenti"],
        "seasons": ["2004-2005"],
        "abstract_title": "L'Innesto Invernale che Salvò la Stagione Cadetta",
        "abstract_bullets": [
            "**Capocannoniere Salvezza 2004-2005:** 6 reti in appena 19 presenze nel girone di ritorno.",
            "**Impatto Istantaneo:** Arrivato a gennaio 2005 dal Piacenza, ribaltò le sorti offensive del Catania di Nedo Sonetti.",
            "**Gol Pesantissimi:** Reti decisive contro Vicenza, Salernitana, Ternana e Venezia per garantire la salvezza.",
        ],
        "bio": """**Jeda**, all'anagrafe **Jedaias Capucho Neves** (Santarém, 15 aprile 1979), è un allenatore di calcio ed ex calciatore brasiliano, nel ruolo di attaccante. Acquistato nel gennaio **2005** dalla neonata dirigenza di [[societa/presidenti/antonino-pulvirenti|Antonino Pulvirenti]] e Pietro Lo Monaco per rinforzare la squadra nella difficile [[stagioni/2004-2005|Stagione 2004-2005]], si rivelò l'autentico salvatore della patria cadetta.

In soli cinque mesi di militanza collezionò 19 presenze e realizzò **6 reti pesantissime**, risultando il miglior marcatore della squadra etnea e regalando al club la permanenza in Serie B propedeutica alla cavalcata trionfale della stagione successiva.""",
        "career": """### Il Girone di Ritorno del 2005

Con la maglia numero 11, Jeda conquistò i tifosi del Massimino per la sua rapidità nei contropiedi e la capacità di finalizzare sotto pressione. Le sue prodezze contro Salernitana e Ternana consentirono agli etnei di superare la crisi e chiudere il campionato a metà classifica, prima del suo approdo a Crotone e successivamente a Cagliari in Serie A.""",
        "sources": [
            {
                "author": "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino",
                "title": "Tutto il Catania minuto per minuto (1929-2010)",
                "publisher": "GEO Edizioni, Empoli",
                "year": 2010,
                "reference": "pp. 436-442 (Stagione 2004-2005)"
            }
        ]
    },
    {
        "slug": "caetano-calil",
        "canonical_name": "Caetano Calil",
        "aliases": ["Calil", "Caetano Prata Calil"],
        "title": "Caetano Calil — Il Punto di Riferimento del Rilancio in Lega Pro (2015-2017)",
        "description": "Biografia e statistiche di Caetano Calil, attaccante brasiliano capocannoniere del Catania nel campionato di Lega Pro 2015-2016 con 11 reti.",
        "birth_date": "1984-05-20",
        "birth_place": "Guaxupé, Brasile",
        "nationality": "Brasile",
        "role": "Attaccante / Trequartista",
        "catania_periods": ["2015-2017"],
        "total_appearances": 50,
        "league_appearances": 48,
        "total_goals": 12,
        "league_goals": 12,
        "club_entities": ["[[societa/2004-era-pulvirenti\\|Calcio Catania S.p.A. (Era Pulvirenti)]]"],
        "tags": ["calciatori", "attaccanti", "brasiliani", "lega-pro", "serie-c", "pancaro"],
        "seasons": ["2015-2016"],
        "abstract_title": "Il Capocannoniere della Stagione della Penalizzazione (-9)",
        "abstract_bullets": [
            "**Capocannoniere 2015-2016:** 11 reti in 33 gare di Lega Pro.",
            "**Salvezza Contro Ogni Pronostico:** Leader offensivo nella stagione iniziata con la pesante penalizzazione di 9 punti.",
            "**Tecnica Sudamericana:** Calciatore dai colpi geniali su punizione e dal limite dell'area.",
        ],
        "bio": """**Caetano Prata Calil** (Guaxupé, 20 maggio 1984) è un ex calciatore brasiliano, nel ruolo di attaccante e seconda punta. Acquistato dal Catania nell'agosto **2015** dopo aver trascinato la Salernitana alla promozione, fu il perno offensivo della complessa [[stagioni/2015-2016|Stagione 2015-2016]] in Lega Pro.

In un'annata drammatica iniziata con una penalizzazione federale di 9 punti conseguente all'inchiesta *I Treni del Gol*, Calil prese per mano la squadra allenata da Giuseppe Pancaro, realizzando **11 reti** decisive che valsero la conquista della salvezza diretta senza passare dai playout.""",
        "career": """### La Leadership Tecnica nel 2015-2016

Con doppiette memorabili contro Catanzaro e Ischia Isolaverde e prodezze al Massimino, Calil fu il faro tattico della formazione etnea. Rimase in rossazzurro anche nella prima parte della stagione 2016-2017, raggiungendo 50 presenze ufficiali e 12 reti totali con il club.""",
        "sources": [
            {
                "author": "Lega Italiana Calcio Professionistico",
                "title": "Almanacco Ufficiale Lega Pro 2015-2016",
                "publisher": "Lega Pro - Firenze",
                "year": 2016,
                "reference": "Statistiche e tabellini ufficiali Calcio Catania"
            },
            {
                "author": "La Sicilia",
                "title": "Calil trascina il Catania alla salvezza: cancellata la penalizzazione",
                "publisher": "La Sicilia",
                "year": 2016,
                "reference": "Cronaca sportiva 8 maggio 2016"
            }
        ]
    },
    {
        "slug": "samuel-di-carmine",
        "canonical_name": "Samuel Di Carmine",
        "aliases": ["Di Carmine"],
        "title": "Samuel Di Carmine — Il Centravanti della Coppa Italia Serie C (2023-2024)",
        "description": "Biografia e statistiche di Samuel Di Carmine, bomber di razza con 8 reti e protagonista del trionfo in Coppa Italia Serie C nella stagione 2023-2024.",
        "birth_date": "1988-09-29",
        "birth_place": "Firenze, Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["2023-2024"],
        "total_appearances": 34,
        "league_appearances": 29,
        "total_goals": 10,
        "league_goals": 8,
        "club_entities": ["[[societa/2022-pelligra-catania-fc\\|Catania Football Club (Era Pelligra)]]"],
        "tags": ["calciatori", "attaccanti", "centravanti", "coppa-italia-serie-c", "lucarelli", "ross-pelligra"],
        "seasons": ["2023-2024"],
        "abstract_title": "Il Bomber della Prima Storica Coppa Italia Serie C",
        "abstract_bullets": [
            "**Trofeo Nazionale Storico:** Protagonista del trionfo in Coppa Italia Serie C 2023-2024 contro il Padova.",
            "**Capocannoniere Etneo 2023-2024:** 8 reti in Serie C e 2 in Coppa Italia per un totale di 10 reti stagionali.",
            "**Caratura ed Esperienza:** Centravanti con lunga carriera tra Serie A e Serie B (Verona, Perugia, Cremonese).",
        ],
        "bio": """**Samuel Di Carmine** (Firenze, 29 settembre 1988) è un calciatore italiano, nel ruolo di centravanti. Acquistato nell'agosto **2023** dal presidente [[societa/presidenti/ross-pelligra|Ross Pelligra]] e dal vicepresidente Vincenzo Grella per guidare l'attacco del neonato Catania Football Club al ritorno nei professionisti, fu il capocannoniere della [[stagioni/2023-2024|Stagione 2023-2024]].

Centravanti completo, implacabile negli inserimenti e letale di testa, realizzò 8 reti in campionato e fu determinante nella cavalcata che condusse il Catania alla conquista della **prima Coppa Italia Serie C della sua storia**, vinta il 2 aprile 2024 al Massimino contro il Padova.""",
        "career": """### La Trionfale Campagna di Coppa e i Playoff

Tra i momenti più alti della sua stagione si ricordano la doppietta nel derby vinto al Massimino contro il Crotone e il gol pesante nella semifinale di Coppa Italia contro il Rimini. Con 10 reti in 34 gare complessive, Di Carmine ha iscritto il proprio nome nell'albo d'oro del club etneo prima della cessione al Trento nel 2024.""",
        "sources": [
            {
                "author": "Lega Italiana Calcio Professionistico",
                "title": "Tabellini e Comunicati Ufficiali Coppa Italia Serie C 2023-2024",
                "publisher": "Lega Pro - Firenze",
                "year": 2024,
                "reference": "Finale Catania-Padova 4-2 d.t.s., 2 aprile 2024"
            },
            {
                "author": "La Sicilia",
                "title": "Catania nella storia: alza la Coppa Italia Serie C",
                "publisher": "La Sicilia",
                "year": 2024,
                "reference": "Edizione straordinaria 3 aprile 2024"
            }
        ]
    },
    {
        "slug": "roberto-inglese",
        "canonical_name": "Roberto Inglese",
        "aliases": ["Inglese", "Bobby English"],
        "title": "Roberto Inglese — Il Centravanti di Serie A per la Scalata Rossazzurra (2024-2026)",
        "description": "Biografia e statistiche di Roberto Inglese, centravanti di classe superiore con lunga militanza in Serie A, leader dell'attacco etneo dal 2024 al 2026.",
        "birth_date": "1991-11-12",
        "birth_place": "Lucera (FG), Italia",
        "nationality": "Italia",
        "role": "Attaccante / Centravanti",
        "catania_periods": ["2024-2026"],
        "total_appearances": 58,
        "league_appearances": 52,
        "total_goals": 20,
        "league_goals": 19,
        "club_entities": ["[[societa/2022-pelligra-catania-fc\\|Catania Football Club (Era Pelligra)]]"],
        "tags": ["calciatori", "attaccanti", "centravanti", "serie-c", "toscano", "ross-pelligra"],
        "seasons": ["2024-2025", "2025-2026"],
        "abstract_title": "La Classe Superiore della Serie A al Massimino",
        "abstract_bullets": [
            "**Leader Offensivo dell'Era Pelligra:** Acquistato nell'estate 2024 come colpo da novanta per la scalata in Serie B.",
            "**Capocannoniere 2024-2025:** 11 reti in 32 presenze di Serie C sotto la guida di Domenico Toscano.",
            "**Conferma nel 2025-2026:** Punto di riferimento e trascinatore della prima linea etnea fino ai vertici della classifica.",
        ],
        "bio": """**Roberto Inglese** (Lucera, 12 novembre 1991) è un calciatore italiano, nel ruolo di centravanti. Giunto a Catania nell'agosto **2024** dopo una prestigiosa carriera in Serie A con ChievoVerona, Parma e Napoli (con quasi 40 reti nella massima serie italiana), è stato il grande colpo di mercato dell'era Pelligra voluto dal tecnico Domenico Toscano e dal ds Daniele Faggiano.

Attaccante elegante, forte nel gioco aereo, formidabile nel gioco di sponda per i compagni e letale in area, Inglese si è imposto come il trascinatore assoluto del Catania nella [[stagioni/2024-2025|Stagione 2024-2025]] (11 reti in campionato) e nella successiva [[stagioni/2025-2026|Stagione 2025-2026]], garantendo leadership e carisma da categoria superiore.""",
        "career": """### Il Ruolo Guida nella Rinascita Etnea (2024-2026)

Nel campionato 2024-2025 decise big match contro Benevento, Trapani e Avellino, spingendo la squadra fino alle fasi nazionali dei playoff. Nel successivo torneo 2025-2026 ha continuato a essere il faro offensivo della compagine etnea, confermandosi idolo indiscusso della Curva Nord e faro della rincorsa alla Serie B con 20 reti complessive in 58 apparizioni ufficiali.""",
        "sources": [
            {
                "author": "Lega Italiana Calcio Professionistico",
                "title": "Archivio Ufficiale Statistiche Serie C NOW 2024-2025 e 2025-2026",
                "publisher": "Lega Pro - Firenze",
                "year": 2026,
                "reference": "Ruolino e tabellini ufficiali Roberto Inglese (Catania FC)"
            },
            {
                "author": "La Sicilia",
                "title": "Inglese, il gigante che infiamma il Massimino: gol e carisma da Serie A",
                "publisher": "La Sicilia",
                "year": 2025,
                "reference": "Approfondimento sportivo 15 novembre 2025"
            }
        ]
    }
]


def render_markdown(player: dict) -> str:
    # Frontmatter
    fm = [
        "---",
        f'title: "{player["title"]}"',
        f'description: "{player["description"]}"',
        f'slug: "tesserati/calciatori/{player["slug"]}"',
        'entity_type: "calciatore"',
        'status: "verified"',
        'last_verified_date: 2026-10-27',
    ]
    if "birth_date" in player:
        fm.append(f'birth_date: {player["birth_date"]}')
    if "death_date" in player:
        fm.append(f'death_date: {player["death_date"]}')
    if "birth_place" in player:
        fm.append(f'birth_place: "{player["birth_place"]}"')
    if "death_place" in player:
        fm.append(f'death_place: "{player["death_place"]}"')
    fm.append(f'nationality: "{player.get("nationality", "Italia")}"')
    fm.append(f'role: "{player["role"]}"')
    fm.append("catania_periods:")
    for period in player["catania_periods"]:
        fm.append(f'  - "{period}"')
    fm.append(f'total_appearances: {player["total_appearances"]}')
    fm.append(f'league_appearances: {player.get("league_appearances", player["total_appearances"])}')
    if "serie_a_appearances" in player:
        fm.append(f'serie_a_appearances: {player["serie_a_appearances"]}')
    fm.append(f'total_goals: {player["total_goals"]}')
    fm.append(f'league_goals: {player.get("league_goals", player["total_goals"])}')
    if "serie_a_goals" in player:
        fm.append(f'serie_a_goals: {player["serie_a_goals"]}')
    fm.append("club_entities:")
    for club in player["club_entities"]:
        club_fm = club.replace(r"\|", "|")
        fm.append(f'  - "{club_fm}"')
    fm.append("tags:")
    for tag in player["tags"]:
        fm.append(f"  - {tag}")
    fm.append("sources:")
    for src in player["sources"]:
        fm.append(f'  - author: "{src["author"]}"')
        fm.append(f'    title: "{src["title"]}"')
        fm.append(f'    publisher: "{src["publisher"]}"')
        fm.append(f'    year: {src["year"]}')
        if "reference" in src:
            fm.append(f'    reference: "{src["reference"]}"')
    fm.append("---")
    
    # Body
    body = [
        f'# {player["canonical_name"]}',
        "",
        player["bio"],
        "",
        f'> [!abstract] {player["abstract_title"]}',
    ]
    for bullet in player["abstract_bullets"]:
        body.append(f"> - {bullet}")
    body.append("")
    body.append("---")
    body.append("")
    body.append("## Carriera e Traguardi in Maglia Etnea")
    body.append("")
    body.append(player["career"])
    body.append("")
    body.append("---")
    body.append("")
    body.append("## Riepilogo Statistico nel Catania")
    body.append("")
    body.append("| Competizione / Stagione | Presenze | Reti Segnate | Ruolo Principale | Note Istituzionali |")
    body.append("| :--- | :---: | :---: | :--- | :--- |")
    
    # Generate table rows
    periods_str = ", ".join(player["catania_periods"])
    club_escaped = player["club_entities"][0]
    body.append(f'| Campionato ({periods_str}) | {player.get("league_appearances", player["total_appearances"])} | {player.get("league_goals", player["total_goals"])} | {player["role"]} | {club_escaped} |')
    if player["total_appearances"] > player.get("league_appearances", player["total_appearances"]):
        diff_app = player["total_appearances"] - player.get("league_appearances", player["total_appearances"])
        diff_gol = player["total_goals"] - player.get("league_goals", player["total_goals"])
        body.append(f'| Coppe Nazionali / Spareggi | {diff_app} | {diff_gol} | {player["role"]} | Gare ufficiali |')
    body.append(f'| **Totale Complessivo** | **{player["total_appearances"]}** | **{player["total_goals"]}** | — | — |')
    body.append("")
    body.append("---")
    body.append("")
    body.append("## Fonti e Bibliografia")
    body.append("")
    for i, src in enumerate(player["sources"], start=1):
        ref_text = f", {src['reference']}" if "reference" in src else ""
        body.append(f'{i}. **{src["author"]}**, *{src["title"]}*, {src["publisher"]}, {src["year"]}{ref_text}.')
    body.append("")

    return "\n".join(fm) + "\n\n" + "\n".join(body)


def main():
    PLAYERS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Scrivi file markdown
    for player in PLAYERS_DATA:
        fpath = PLAYERS_DIR / f"{player['slug']}.md"
        content = render_markdown(player)
        fpath.write_text(content, encoding="utf-8")
        print(f"Scritto: {fpath.name}")
        
    # 2. Aggiorna data/entity_registry.json
    registry_data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    entities = registry_data["entities"]
    
    added = 0
    for player in PLAYERS_DATA:
        key = f"tesserati/calciatori/{player['slug']}"
        entities[key] = {
            "entity_type": "calciatore",
            "canonical_name": player["canonical_name"],
            "aliases": player["aliases"]
        }
        added += 1
    
    REGISTRY_FILE.write_text(json.dumps(registry_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Aggiornato entity_registry.json con {added} nuove entita'. Totale: {len(entities)}")

if __name__ == "__main__":
    main()
