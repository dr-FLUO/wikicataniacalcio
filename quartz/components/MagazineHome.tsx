import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

interface CoverStory {
  id: string
  issue: string
  category: string
  title: string
  excerpt: string
  href: string
  image: string
  credit: string
}

const COVER_STORIES_POOL: CoverStory[] = [
  // Batch 1 (Epica, Record, Diritto, Esodo, Ritorno in A, Trofeo)
  {
    id: "catania-inter-1961",
    issue: "EPICA · 04.06.1961",
    category: "SERIE A",
    title: "«Clamoroso al Cibali!»: Catania–Inter 2-0 e il mito di Sandro Ciotti",
    excerpt:
      "Il 4 giugno 1961 le reti di Castellazzi e Calvanese abbattono l'Inter di Herrera, consegnando alla storia il più celebre neologismo radiocronistico del dopoguerra.",
    href: "./02-cronistoria/stagioni/1960-1961",
    image: "./static/images/photos/catania-1960-61.jpg",
    credit: "Archivio Storico · Pubblico Dominio",
  },
  {
    id: "maran-56-punti",
    issue: "RECORD · 2012-2013",
    category: "SERIE A",
    title: "56 Punti all'ombra dell'Etna: la Serie A dei record di Rolando Maran",
    excerpt:
      "Dalle 15 vittorie in massima serie al tridente Gómez–Bergessio–Barrientos: anatomia statistica e tattica del punto più alto mai toccato dal club.",
    href: "./02-cronistoria/stagioni/2012-2013",
    image: "./static/images/photos/rolando-maran.jpg",
    credit: "Foto: Pottercomuneo (CC BY-SA 4.0)",
  },
  {
    id: "caso-catania-2003",
    issue: "DIRITTO · ESTATE 2003",
    category: "DIRITTO SPORTIVO",
    title: "Il Caso Catania (Caso Martinelli) e la nascita della Legge 280/2003",
    excerpt:
      "Il contenzioso per la posizione di Luigi Martinelli in Catania–Siena travolse l'autodichia della FIGC, portando al Decreto Salva-Calcio e alla Serie B a 24 squadre.",
    href: "./01-societa/vicende-legali/caso-catania-2003",
    image: "./static/images/photos/luciano-gaucci.jpg",
    credit: "Archivio Storico · Pubblico Dominio",
  },
  {
    id: "esodo-olimpico-1983",
    issue: "ESODO · GIUGNO 1983",
    category: "CULTURA ULTRAS",
    title: "Quarantamila all'Olimpico: la grande migrazione rossazzurra a Roma",
    excerpt:
      "Treni speciali, navi traghetto e carovane sull'Autostrada del Sole per gli spareggi promozione contro Como e Cremonese del giugno 1983.",
    href: "./02-cronistoria/stagioni/1982-1983",
    image: "./static/images/photos/curva-nord-storica.jpg",
    credit: "Foto: Roberto Quartarone (CC BY-SA 2.5)",
  },
  {
    id: "promozione-marino-2006",
    issue: "PROMOZIONE · 2005-2006",
    category: "SERIE B",
    title: "La cavalcata di Pasquale Marino: 78 punti e il duo Mascara–Spinesi",
    excerpt:
      "Il ritorno in Serie A dopo ventidue anni d'attesa grazie al 4-3-3 offensivo e ai 36 gol combinati della coppia d'attacco più amata del nuovo millennio.",
    href: "./02-cronistoria/stagioni/2005-2006",
    image: "./static/images/photos/mascara-spinesi.jpg",
    credit: "Foto: Roberto Quartarone (CC BY-SA 2.5)",
  },
  {
    id: "coppa-italia-c-2024",
    issue: "TROFEO · 02.04.2024",
    category: "FINALE COPPA",
    title: "Catania–Padova 4-2 d.t.s.: il primo trofeo nazionale nella bacheca etnea",
    excerpt:
      "Dal gol di Marsura al 120' alla bolgia del Massimino: cronaca e tabellino della prima Coppa Italia Serie C conquistata dal club.",
    href: "./02-cronistoria/coppa-italia-serie-c",
    image: "./static/images/photos/coccarda-coppa-italia-c.png",
    credit: "Lega Pro · Foto Ufficiale",
  },

  // Batch 2 (Treni del Gol, Simeone, Massimino TAR, Derby Barbera 0-4, Inter 3-1, Rinascita Serie D)
  {
    id: "treni-del-gol-2015",
    issue: "GIUSTIZIA · 23.06.2015",
    category: "VICENDA GIUDIZIARIA",
    title: "Inchiesta I Treni del Gol: il blitz a Torre del Grifo e la retrocessione",
    excerpt:
      "L'operazione giudiziaria della Polizia, le confessioni presidenziali e le sentenze del TFN che declassarono d'ufficio il Catania in Lega Pro.",
    href: "./01-societa/vicende-legali/treni-del-gol-2015",
    image: "./static/images/photos/torre-del-grifo-village.jpg",
    credit: "Foto: Salvosmav (CC BY-SA 4.0)",
  },
  {
    id: "salvezza-simeone-2011",
    issue: "IMPRESA · 2010-2011",
    category: "SERIE A",
    title: "Il Cholo all'ombra del vulcano: la salvezza record a 46 punti del 2011",
    excerpt:
      "Il carisma di Diego Pablo Simeone, il trionfo nel derby per 4-0 e la storica vittoria sulla Roma (2-1) che suggellarono la permanenza record in massima serie.",
    href: "./02-cronistoria/stagioni/2010-2011",
    image: "./static/images/photos/diego-simeone.jpg",
    credit: "Foto: Carlos Delgado (CC BY-SA 3.0)",
  },
  {
    id: "massimino-tar-1993",
    issue: "BATTAGLIA · ESTATE 1993",
    category: "DIRITTO SPORTIVO",
    title: "La battaglia di Angelo Massimino: il salvataggio della matricola 11700",
    excerpt:
      "La revoca dell'affiliazione da parte della FIGC di Matarrese e la clamorosa vittoria al TAR e al CGA che mantenne in vita la storia societaria rossazzurra.",
    href: "./01-societa/vicende-legali/caso-catania-1993-eccellenza",
    image: "./static/images/photos/angelo-massimino.jpg",
    credit: "Archivio Storico Calcio Catania",
  },
  {
    id: "derby-barbera-2009",
    issue: "MAGIA · 01.03.2009",
    category: "SERIE A",
    title: "Palermo–Catania 0-4: il capolavoro da centrocampo di Peppe Mascara",
    excerpt:
      "La prodezza balistica al volo da cinquanta metri che ammutolì il Barbera e la più travolgente affermazione esterna nella storia del derby di Sicilia.",
    href: "./02-cronistoria/stagioni/2008-2009",
    image: "./static/images/photos/mascara-tifosi.jpg",
    credit: "Foto: Roberto Quartarone (CC BY-SA 2.5)",
  },
  {
    id: "catania-inter-2010",
    issue: "TRIONFO · 12.03.2010",
    category: "SERIE A",
    title: "Catania–Inter 3-1: la notte in cui Mihajlović batté l'Inter del Triplete",
    excerpt:
      "Maxi López, Mascara su rigore a cucchiaio e Martínez firmano la memorabile rimonta sui futuri campioni d'Europa di José Mourinho.",
    href: "./02-cronistoria/stagioni/2009-2010",
    image: "./static/images/photos/sinisa-mihajlovic.jpg",
    credit: "Foto: Wikimedia Commons (CC BY-SA 3.0)",
  },
  {
    id: "rinascita-pelligra-2023",
    issue: "RINASCITA · 2022-2023",
    category: "SERIE D",
    title: "Dalle ceneri del fallimento: gli 88 punti del Catania SSD di Ross Pelligra",
    excerpt:
      "La ripartenza ex Art. 52 NOIF con 31 vittorie su 34 giornate e la promozione trionfale in Serie C con sei turni d'anticipo.",
    href: "./01-societa/epoche/2022-pelligra-catania-fc",
    image: "./static/images/photos/ross-pelligra.jpg",
    credit: "Foto: Supergaefs (CC BY-SA 4.0)",
  },

  // Batch 3 (Fatti 2 Febbraio, Fallimento 2021, Piazza Esposizione, Marcoccio-Szymaniak, Biagianti, Papu Gomez)
  {
    id: "fatti-2-febbraio-2007",
    issue: "MEMORIA · 02.02.2007",
    category: "SICUREZZA & LEGGE",
    title: "I fatti del 2 febbraio 2007: la Legge 41/2007 e la svolta negli stadi",
    excerpt:
      "I tragici scontri del derby, la scomparsa dell'ispettore Raciti e la legislazione governativa che rivoluzionò i canoni dell'ordine pubblico negli impianti sportivi.",
    href: "./01-societa/vicende-legali/decreto-2-febbraio-2007",
    image: "./static/images/photos/pala-spedini-raciti-2007.jpg",
    credit: "Foto: Wikimedia Commons (CC BY-SA 2.5)",
  },
  {
    id: "fallimento-2021",
    issue: "TRIBUNALE · 2021-2022",
    category: "DIRITTO FALLIMENTARE",
    title: "La sentenza di fallimento n. 158/2021 e la fine della Matricola 11700",
    excerpt:
      "La drammatica estinzione della matricola storica del 1946 decretata dal Tribunale di Catania e la revoca dell'esercizio provvisorio.",
    href: "./01-societa/vicende-legali/fallimento-2021-art52-noif",
    image: "./static/images/photos/palazzo-giustizia-catania.jpg",
    credit: "Foto: DMarx22 (CC BY-SA 4.0)",
  },
  {
    id: "piazza-esposizione-1910",
    issue: "ORIGINI · 1910-1930",
    category: "ARCHITETTURA",
    title: "Piazza Esposizione: il primo rettangolo di gioco del calcio a Catania",
    excerpt:
      "La culla pionieristica della Pro Patria e della SS Catania nella piazza dei Malavoglia, prima dell'inaugurazione del Cibali nel 1937.",
    href: "./04-strutture/campi-storici/piazza-esposizione",
    image: "./static/images/photos/piazza-verga-malavoglia.jpg",
    credit: "Foto: Drunkpiper (Pubblico Dominio)",
  },
  {
    id: "marcoccio-szymaniak-1961",
    issue: "ANNI D'ORO · 1961",
    category: "PRESIDENTI",
    title: "L'era Marcoccio e Horst Szymaniak: il primo fuoriclasse mondiale al Cibali",
    excerpt:
      "La gestione illuminata del Commissario Straordinario Ignazio Marcoccio e l'acquisto del leggendario centrocampista della Nazionale tedesca.",
    href: "./01-societa/presidenti/ignazio-marcoccio",
    image: "./static/images/photos/szymaniak-marcoccio.jpg",
    credit: "Archivio Storico · Pubblico Dominio",
  },
  {
    id: "biagianti-capitano",
    issue: "BANDIERA · 2007–2020",
    category: "HALL OF FAME",
    title: "Marco Biagianti: 284 battaglie e il record assoluto di presenze in Serie A",
    excerpt:
      "Dalla chiamata in Nazionale maggiore di Marcello Lippi al ritorno in Serie C: fedeltà incrollabile di una bandiera rossazzurra.",
    href: "./03-tesserati/calciatori/storici/marco-biagianti",
    image: "./static/images/photos/marco-biagianti.jpg",
    credit: "Foto: Manku 7 (Pubblico Dominio)",
  },
  {
    id: "papu-gomez-fantasia",
    issue: "FANTASIA · 2010–2013",
    category: "HALL OF FAME",
    title: "Il «Papu» Gómez e la favola argentina: 111 gare di pura poesia calcistica",
    excerpt:
      "Dribbling ubriacanti, assist al bacio e 18 reti: l'icona del gioco spettacolare del Catania dei miracoli nell'Olimpo della Serie A.",
    href: "./03-tesserati/calciatori/storici/alejandro-gomez",
    image: "./static/images/photos/papu-gomez.jpg",
    credit: "Foto: Wikimedia Commons (CC BY-SA 4.0)",
  },

  // Batch 4 (Cinema, Nazionali, Prima Serie A 1954, Promozione B 1934, Mascotte & Inni, Araldica)
  {
    id: "catania-cinema-tv",
    issue: "CINEMA · 1973–2010",
    category: "CULTURA POPOLARE",
    title: "Il Catania nel cinema italiano: da Oronzo Canà ad Al bar dello sport e Malizia",
    excerpt:
      "Da Lino Banfi all'Hotel Executive per Luvanor e Pedrinho alle scene di culto con Turi Ferro e Giancarlo Giannini nella commedia all'italiana.",
    href: "./07-media-e-comunicazione/cinema-e-tv/cultura-di-massa",
    image: "./static/images/photos/clamoroso-inter-1961.jpg",
    credit: "Archivio Storico · Pubblico Dominio",
  },
  {
    id: "contributo-nazionali",
    issue: "MONDIALI · 1962–2024",
    category: "AZZURRI & ESTERO",
    title: "I rossazzurri nel mondo: dai Mondiali del 1962 al titolo iridato di Janković",
    excerpt:
      "Dalla storica spedizione di Horst Szymaniak a Cile '62 e la notte di Mascara a Pisa, fino ad Andújar vicecampione del mondo e Janković campione U-20.",
    href: "./03-tesserati/calciatori/contributo-nazionali",
    image: "./static/images/photos/szymaniak-marcoccio.jpg",
    credit: "Archivio Storico · Pubblico Dominio",
  },
  {
    id: "prima-serie-a-1954-1955",
    issue: "SERIE A · 1954-1955",
    category: "PRIMATI STORICI",
    title: "La prima volta in Paradiso: la favola del Catania di Piero Andreoli",
    excerpt:
      "Dall'apoteosi della promozione del 1954 alla clamorosa vittoria al Comunale di Bologna: cronaca della storica prima stagione in massima serie.",
    href: "./02-cronistoria/stagioni/1954-1955",
    image: "./static/images/photos/catania-1954-55.jpg",
    credit: "Archivio Storico Calcio Catania",
  },
  {
    id: "ss-catania-1933-1934",
    issue: "PIONIERI · 1933-1934",
    category: "PRIMA DIVISIONE",
    title: "La cavalcata della SS Catania: Géza Kertész e la prima storica Serie B",
    excerpt:
      "Il trionfo nelle finali promozione del 1934 che spalancò le porte del professionismo nazionale alla società dell'Elefante.",
    href: "./02-cronistoria/stagioni/1933-1934",
    image: "./static/images/photos/catania-1933-34.jpg",
    credit: "Archivio Storico Calcio Catania",
  },
  {
    id: "mascotte-e-inni",
    issue: "IDENTITÀ · SIMBOLI",
    category: "ARALDICA & FOLKLORE",
    title: "Agatino il Liotru e gli inni del Cibali: storie di devozione e canti popolari",
    excerpt:
      "Dal sondaggio del 2014 in onore di Sant'Agata alle hit di Giuseppe Castiglia e la carica orchestrale di Pirati dei Caraibi sul prato del Massimino.",
    href: "./05-identita-e-simboli/mascotte-e-inni",
    image: "./static/images/photos/liotru-storico-1865.jpg",
    credit: "Archivio Civico Catanese",
  },
  {
    id: "araldica-marchio-2026",
    issue: "ARALDICA · 1946–2026",
    category: "IDENTITÀ CIVICA",
    title: "Dallo scudetto del 1946 a Bob Liuzzo: l'evoluzione araldica del Liotru",
    excerpt:
      "Lo scudo palato con il pallone in cuoio, la rinascita grafica post-fallimento e la storica procedura di riacquisto del marchio tradizionale.",
    href: "./05-identita-e-simboli/araldica-e-scudetti/acquisizione-marchio-storico-2026",
    image: "./static/images/photos/stemma-catania-spa-2002-2022.png",
    credit: "Archivio Storico Calcio Catania",
  },

  // Batch 5 (US Catanese 1910, Massimino Restyling, Maglie & Sponsor, Curva Nord Ciccio Famoso, Argentini, Torre del Grifo)
  {
    id: "us-catanese-1910",
    issue: "ORIGINI · 1910",
    category: "ARCHEOLOGIA CALCISTICA",
    title: "1910: l'Unione Sportiva Catanese e le prime sfide a Piazza Esposizione",
    excerpt:
      "Dai pionieri contro i marinai inglesi all'eredità della Pro Patria: la scintilla che accese la passione calcistica nella città etnea.",
    href: "./01-societa/epoche/1929-ss-catania",
    image: "./static/images/photos/unione-sportiva-catanese-1910.jpg",
    credit: "Archivio Storico Digitale Catanese",
  },
  {
    id: "stadio-massimino-restyling",
    issue: "ARCHITETTURA · 1937–2024",
    category: "IMPIANTI SPORTIVI",
    title: "Stadio Angelo Massimino: dal Cibali di Raffaele Leone al restyling 2023",
    excerpt:
      "Oltre ottant'anni di battaglie sportive, dalle universiadi del 1997 alla posa dei nuovi seggiolini rossazzurri e del manto moderno.",
    href: "./04-strutture/stadio-massimino/angelo-massimino",
    image: "./static/images/photos/stadio-massimino-restyling-2023.jpg",
    credit: "Comune di Catania / Catania FC",
  },
  {
    id: "maglie-e-sponsor",
    issue: "MATERIALI · 1979–OGGI",
    category: "CULTURA TESSILE",
    title: "Quarant'anni di divise e sponsor: dall'acrilico Ennerre alla lava di Erreà",
    excerpt:
      "La trasformazione della maglia palata tra cotone, lanetta, colletti vintage e sponsor leggendari come Haribo, Poiatti ed SP.",
    href: "./05-identita-e-simboli/sponsor/sponsor-tecnici-e-commerciali",
    image: "./static/images/photos/stemma-catania-ssd-2022-2023.png",
    credit: "Archivio Storico Maglie Catania",
  },
  {
    id: "ciccio-famoso-ultras",
    issue: "CURVA NORD · 1979",
    category: "MOVIMENTO ULTRAS",
    title: "Ciccio Famoso e la Falange d'Assalto: la nascita della passione ultras",
    excerpt:
      "Nel 1979 nasce la prima falange organizzata del Cibali: quarant'anni di cortei, trasferte epiche e coreografie monumentali della Curva Nord.",
    href: "./06-tifoseria-e-cultura/biografie/ciccio-famoso",
    image: "./static/images/photos/coreografia-ciccio-famoso.jpg",
    credit: "Curva Nord Catania",
  },
  {
    id: "catania-degli-argentini",
    issue: "SERIE A · 2008–2013",
    category: "LABORATORIO TATTICO",
    title: "Il Catania degli Argentini: l'epopea sudamericana che incantò l'Italia",
    excerpt:
      "Da Papu Gómez a Maxi López, Bergessio, Izco, Barrientos e Andújar: quando il Massimino divenne una filiale della Bombonera.",
    href: "./01-societa/epoche/catania-degli-argentini",
    image: "./static/images/photos/gonzalo-bergessio.jpg",
    credit: "Archivio Storico Calcio Catania",
  },
  {
    id: "torre-del-grifo-village",
    issue: "CENTRO SPORTIVO · 2011–2026",
    category: "PATRIMONIO IMMOBILIARE",
    title: "Torre del Grifo Village: il sogno d'eccellenza, il baratro e la rinascita",
    excerpt:
      "Centocinquantamila metri quadri di campi e strutture d'avanguardia a Mascalucia: la culla dei successi in A e il piano di riscatto.",
    href: "./04-strutture/stadio-massimino/acquisizione-torre-del-grifo-2025-2026",
    image: "./static/images/photos/torre-del-grifo-village.jpg",
    credit: "Foto: Salvosmav (CC BY-SA 4.0)",
  },
]

interface PortraitItem {
  id: string
  name: string
  role: string
  stat: string
  href: string
  image: string
}

const PORTRAITS_POOL: PortraitItem[] = [
  // Batch 1 (Capitani e Condottieri storici)
  {
    id: "giuseppe-mascara",
    name: "Giuseppe Mascara",
    role: "ATTACCANTE · 2003–2011",
    stat: "236 PRES · 61 GOL",
    href: "./03-tesserati/calciatori/storici/giuseppe-mascara",
    image: "./static/images/photos/mascara-tifosi.jpg",
  },
  {
    id: "marco-biagianti",
    name: "Marco Biagianti",
    role: "CAPITANO · 2007–2020",
    stat: "284 PRES · RECORD A",
    href: "./03-tesserati/calciatori/storici/marco-biagianti",
    image: "./static/images/photos/marco-biagianti.jpg",
  },
  {
    id: "carmelo-di-bella",
    name: "Carmelo Di Bella",
    role: "ALLENATORE · 1958–1966",
    stat: "297 PANCHINE",
    href: "./03-tesserati/allenatori/carmelo-di-bella",
    image: "./static/images/photos/carmelo-di-bella.jpg",
  },
  {
    id: "angelo-massimino",
    name: "Angelo Massimino",
    role: "PRESIDENTISSIMO · 1969–1996",
    stat: "27 STAGIONI",
    href: "./01-societa/presidenti/angelo-massimino",
    image: "./static/images/photos/angelo-massimino.jpg",
  },

  // Batch 2 (Tecnici e Bomber dell'Era A)
  {
    id: "diego-pablo-simeone",
    name: "Diego Pablo Simeone",
    role: "ALLENATORE · 2011",
    stat: "RECORD 46 PT (2011)",
    href: "./03-tesserati/allenatori/diego-pablo-simeone",
    image: "./static/images/photos/diego-simeone.jpg",
  },
  {
    id: "gonzalo-bergessio",
    name: "Gonzalo Bergessio",
    role: "CENTRAVANTI · 2011–2014",
    stat: "113 PRES · 37 GOL",
    href: "./03-tesserati/calciatori/storici/gonzalo-bergessio",
    image: "./static/images/photos/gonzalo-bergessio.jpg",
  },
  {
    id: "alejandro-gomez",
    name: "Alejandro «Papu» Gómez",
    role: "FANTASISTA · 2010–2013",
    stat: "111 PRES · 18 GOL",
    href: "./03-tesserati/calciatori/storici/alejandro-gomez",
    image: "./static/images/photos/papu-gomez.jpg",
  },
  {
    id: "sinisa-mihajlovic",
    name: "Siniša Mihajlović",
    role: "ALLENATORE · 2009–2010",
    stat: "RIMONTA STORICA",
    href: "./03-tesserati/allenatori/sinisa-mihajlovic",
    image: "./static/images/photos/sinisa-mihajlovic.jpg",
  },

  // Batch 3 (Rinascita, Risalita e Registi)
  {
    id: "ross-pelligra",
    name: "Ross Pelligra",
    role: "PRESIDENTE · 2022–OGGI",
    stat: "88 PT · RINASCITA D",
    href: "./01-societa/presidenti/ross-pelligra",
    image: "./static/images/photos/ross-pelligra.jpg",
  },
  {
    id: "pasquale-marino",
    name: "Pasquale Marino",
    role: "ALLENATORE · 2005–2007",
    stat: "PROMOZIONE IN A",
    href: "./03-tesserati/allenatori/pasquale-marino",
    image: "./static/images/photos/pasquale-marino.jpg",
  },
  {
    id: "francesco-lodi",
    name: "Francesco Lodi",
    role: "REGISTA · 3 CICLI STORICI",
    stat: "238 PRES · 52 GOL",
    href: "./03-tesserati/calciatori/storici/francesco-lodi",
    image: "./static/images/photos/francesco-lodi.jpg",
  },
  {
    id: "gionatha-spinesi",
    name: "Gionatha Spinesi",
    role: "BOMBER · 2005–2009",
    stat: "127 PRES · 49 RETI",
    href: "./03-tesserati/calciatori/storici/gionatha-spinesi",
    image: "./static/images/photos/mascara-spinesi.jpg",
  },

  // Batch 4 (Protagonisti del ciclo A)
  {
    id: "maxi-lopez",
    name: "Maxi López",
    role: "ATTACCANTE · 2010–2014",
    stat: "70 PRES · 27 GOL",
    href: "./03-tesserati/calciatori/archivio/m-o/maxi-lopez",
    image: "./static/images/photos/maxi-lopez.jpg",
  },
  {
    id: "mariano-izco",
    name: "Mariano Julio Izco",
    role: "CENTROCAMPISTA · 2006–2014",
    stat: "280 PRES · 8 ANNI A",
    href: "./03-tesserati/calciatori/storici/mariano-izco",
    image: "./static/images/photos/mariano-izco.jpg",
  },
  {
    id: "pablo-barrientos",
    name: "Pablo Barrientos",
    role: "TREQUARTISTA · 2011–2014",
    stat: "86 PRES · 14 GOL",
    href: "./03-tesserati/calciatori/archivio/p-r/pablo-barrientos",
    image: "./static/images/photos/pablo-barrientos.jpg",
  },
  {
    id: "rolando-maran",
    name: "Rolando Maran",
    role: "ALLENATORE · 2012–2014",
    stat: "56 PT · 8° IN SERIE A",
    href: "./03-tesserati/allenatori/rolando-maran",
    image: "./static/images/photos/rolando-maran.jpg",
  },

  // Batch 5 (Condottieri storici e Tecnici d'Autore)
  {
    id: "gianni-di-marzio",
    name: "Gianni Di Marzio",
    role: "ALLENATORE · 1982–1984",
    stat: "SPAREGGI ROMA 1983",
    href: "./03-tesserati/allenatori/gianni-di-marzio",
    image: "./static/images/photos/gianni-di-marzio.jpg",
  },
  {
    id: "ignazio-marcoccio",
    name: "Ignazio Marcoccio",
    role: "PRESIDENTE · 1959–1969",
    stat: "SERIE A D'ORO",
    href: "./01-societa/presidenti/ignazio-marcoccio",
    image: "./static/images/photos/szymaniak-marcoccio.jpg",
  },
  {
    id: "walter-zenga",
    name: "Walter Zenga",
    role: "ALLENATORE · 2008–2009",
    stat: "SALVEZZA A · DERBY 0-4",
    href: "./03-tesserati/allenatori/walter-zenga",
    image: "./static/images/photos/walter-zenga.jpg",
  },
  {
    id: "vincenzo-montella",
    name: "Vincenzo Montella",
    role: "ALLENATORE · 2011–2012",
    stat: "48 PT · BEL GIOCO A",
    href: "./03-tesserati/allenatori/vincenzo-montella",
    image: "./static/images/photos/vincenzo-montella.jpg",
  },

  // Batch 6 (Recordmen e Bandiere Eterne)
  {
    id: "nicolo-nicolosi",
    name: "Nicolò Nicolosi",
    role: "CENTRAVANTI · 1932–1949",
    stat: "78 GOL · RECORD ASSOLUTO",
    href: "./03-tesserati/calciatori/storici/nicolo-nicolosi",
    image: "./static/images/photos/nicolo-nicolosi.jpg",
  },
  {
    id: "damiano-morra",
    name: "Damiano Morra",
    role: "CAPITANO · 1975–1984",
    stat: "320 PRES · RECORD ASSOLUTO",
    href: "./03-tesserati/calciatori/storici/damiano-morra",
    image: "./static/images/photos/damiano-morra.webp",
  },
  {
    id: "adelmo-prenna",
    name: "Adelmo Prenna",
    role: "MEZZALA · 1958–1964",
    stat: "247 PRES · 48 GOL IN A",
    href: "./03-tesserati/calciatori/storici/adelmo-prenna",
    image: "./static/images/photos/adelmo-prenna.jpg",
  },
  {
    id: "aldo-cantarutti",
    name: "Aldo Cantarutti",
    role: "CENTRAVANTI · 1981–1984",
    stat: "SPAREGGI ROMA 1983",
    href: "./03-tesserati/calciatori/storici/aldo-cantarutti",
    image: "./static/images/photos/mastalli-cantarutti.jpg",
  },

  // Batch 7 (Eroi Internazionali e Maestri Tattici)
  {
    id: "horst-szymaniak",
    name: "Horst Szymaniak",
    role: "MEDIANO · 1961–1963",
    stat: "MONDIALI CILE 1962",
    href: "./03-tesserati/calciatori/storici/horst-szymaniak",
    image: "./static/images/photos/horst-szymaniak.jpg",
  },
  {
    id: "piero-andreoli",
    name: "Piero Andreoli",
    role: "ALLENATORE · 1953–1956",
    stat: "1ª SERIE A (1954)",
    href: "./03-tesserati/allenatori/piero-andreoli",
    image: "./static/images/photos/piero-andreoli.jpg",
  },
  {
    id: "geza-kertesz",
    name: "Géza Kertész",
    role: "ALLENATORE · 1933–1936",
    stat: "1ª SERIE B · EROE CIVICO",
    href: "./03-tesserati/allenatori/geza-kertesz",
    image: "./static/images/photos/geza-kertesz.jpg",
  },
  {
    id: "egizio-rubino",
    name: "Egizio Rubino",
    role: "ALLENATORE · 1968–1974",
    stat: "SERIE A 1970 · SERIE B '75",
    href: "./03-tesserati/allenatori/egizio-rubino",
    image: "./static/images/photos/egizio-rubino.webp",
  },

  // Batch 8 (Presidenti e Dirigenti di Peso)
  {
    id: "luciano-gaucci",
    name: "Luciano Gaucci",
    role: "PRESIDENTE · 2000–2004",
    stat: "RISALITA IN SERIE B",
    href: "./01-societa/presidenti/luciano-gaucci",
    image: "./static/images/photos/luciano-gaucci.jpg",
  },
  {
    id: "angelo-attaguile",
    name: "Angelo Attaguile",
    role: "PRESIDENTE · 1987–1991",
    stat: "CORDATA ANNI '80",
    href: "./01-societa/presidenti/angelo-attaguile",
    image: "./static/images/photos/angelo-attaguile.jpg",
  },
  {
    id: "pietro-lo-monaco",
    name: "Pietro Lo Monaco",
    role: "AMM. DELEGATO · 2004–2012",
    stat: "ARCHITETTO SERIE A",
    href: "./01-societa/dirigenti/pietro-lo-monaco",
    image: "./static/images/photos/pietro-lo-monaco.webp",
  },
  {
    id: "mariano-andujar",
    name: "Mariano Andújar",
    role: "PORTIERE · 2009–2014",
    stat: "164 PRES · VICE-CAMPIONE MONDO",
    href: "./03-tesserati/calciatori/storici/mariano-andujar",
    image: "./static/images/photos/mariano-andujar.jpg",
  },

  // Batch 9 (Idoli dei Tifosi e Icone di Cuore)
  {
    id: "juan-manuel-vargas",
    name: "Juan Manuel Vargas",
    role: "TERZINO · 2006–2008",
    stat: "69 PRES · «EL LOCO»",
    href: "./03-tesserati/calciatori/archivio/g-l/juan-manuel-vargas",
    image: "./static/images/photos/juan-manuel-vargas.jpg",
  },
  {
    id: "takayuki-morimoto",
    name: "Takayuki Morimoto",
    role: "ATTACCANTE · 2006–2013",
    stat: "117 PRES · 24 GOL",
    href: "./03-tesserati/calciatori/archivio/s-z/takayuki-morimoto",
    image: "./static/images/photos/takayuki-morimoto.jpg",
  },
  {
    id: "ciccio-famoso",
    name: "Ciccio Famoso",
    role: "CAPO ULTRAS · 1979–2017",
    stat: "FALANGE D'ASSALTO",
    href: "./06-tifoseria-e-cultura/biografie/ciccio-famoso",
    image: "./static/images/photos/ciccio-famoso.jpg",
  },
  {
    id: "aquilino-bonfanti",
    name: "Aquilino Bonfanti",
    role: "ATTACCANTE · 1969–1972",
    stat: "DOPPIETTA SERIE A 1970",
    href: "./03-tesserati/calciatori/archivio/a-c/aquilino-bonfanti",
    image: "./static/images/photos/aquilino-bonfanti.webp",
  },
]

const ERAS = [
  {
    years: "1929–1943",
    name: "SS Catania / AFC Catania",
    matricola: "PRE-1946",
    figures: "V. Trigona, V. Santi, Géza Kertész",
    event: "1ª storica promozione in Serie B (1933-34) e inaugurazione Stadio Cibali (1937).",
    href: "./societa/1929-ss-catania",
  },
  {
    years: "1946–1967",
    name: "Club Calcio Catania",
    matricola: "FIGC 11700",
    figures: "L. Santi, A. Pesce, I. Marcoccio, C. Di Bella",
    event: "Nascita della Matricola 11700, 1ª Serie A (1953-54) ed epopea anni '60 (Catania–Inter 2-0).",
    href: "./societa/1946-club-calcio-catania",
  },
  {
    years: "1967–1993",
    name: "Calcio Catania S.p.A. (Era Massimino)",
    matricola: "FIGC 11700",
    figures: "Angelo Massimino, E. Rubino, G. Di Marzio",
    event: "Promozioni in Serie A 1969-70 e spareggi di Roma 1983 davanti a 40.000 catanesi.",
    href: "./societa/1967-calcio-catania-spa-massimino",
  },
  {
    years: "1993–2004",
    name: "La Risalita dall'Eccellenza & Era Gaucci",
    matricola: "FIGC 11700",
    figures: "Angelo Massimino, L. Gaucci, R. Gaucci",
    event: "Vittoria al TAR (1993), scalata dall'Eccellenza, play-off Taranto 2002 e Caso Catania (2003).",
    href: "./societa/2000-era-gaucci",
  },
  {
    years: "2004–2020",
    name: "Calcio Catania S.p.A. (Era Pulvirenti)",
    matricola: "FIGC 11700",
    figures: "A. Pulvirenti, P. Lo Monaco, P. Marino, R. Maran",
    event: "Inaugurazione Torre del Grifo, 8 stagioni consecutive in Serie A e record di 56 punti (2012-13).",
    href: "./societa/2004-era-pulvirenti",
  },
  {
    years: "2020–2022",
    name: "Gestione SIGI & Estinzione Matricola 11700",
    matricola: "FIGC 11700",
    figures: "SIGI S.p.A., F. Baldini, L. Moro",
    event: "Sentenza di fallimento n. 158/2021 del Tribunale di Catania e revoca esercizio provvisorio (09/04/2022).",
    href: "./societa/2020-sigi-e-fallimento",
  },
  {
    years: "2022–OGGI",
    name: "Catania SSD ➔ Catania Football Club",
    matricola: "FIGC 955013",
    figures: "Rosario Pelligra, V. Grella, D. Faggiano, D. Toscano",
    event: "Rinascita ex Art. 52 NOIF, record Serie D (88 pt), 1ª Coppa Italia Serie C (2024), riacquisto storico logo e acquisizione Torre del Grifo.",
    href: "./01-societa/epoche/2022-pelligra-catania-fc",
  },
]

interface NumberStat {
  id: string
  kicker: string
  digits: string
  desc: string
  href: string
}

const NUMBERS_POOL: NumberStat[] = [
  {
    id: "fondazione-1929",
    kicker: "FONDAZIONE",
    digits: "1929",
    desc: "Dalla Società Sportiva Catania di Piazza Esposizione all'attuale Catania Football Club.",
    href: "./01-societa/epoche/1929-ss-catania",
  },
  {
    id: "serie-a-17",
    kicker: "MASSIMA SERIE",
    digits: "17",
    desc: "Campionati di Serie A disputati tra il debutto del 1954-55 e gli otto tornei consecutivi 2006–2014.",
    href: "./02-cronistoria/stagioni/",
  },
  {
    id: "record-a-56pt",
    kicker: "RECORD SERIE A",
    digits: "56 PT",
    desc: "L'ottavo posto storico della stagione 2012-2013 con 15 vittorie sotto la guida di Rolando Maran.",
    href: "./02-cronistoria/stagioni/2012-2013",
  },
  {
    id: "esodo-olimpico-40000",
    kicker: "OLIMPICO 1983",
    digits: "40.000",
    desc: "Catanesi in trasferta a Roma il 25 giugno 1983: il più grande esodo sportivo nella storia del Sud.",
    href: "./02-cronistoria/stagioni/1982-1983",
  },
  {
    id: "matricola-11700",
    kicker: "MATRICOLA FIGC",
    digits: "11700",
    desc: "La storica matricola federale del Club Calcio Catania custodita con fierezza per 75 anni (1946–2022).",
    href: "./01-societa/epoche/1946-club-calcio-catania",
  },
  {
    id: "presenze-morra-281",
    kicker: "RECORD PRESENZE",
    digits: "281",
    desc: "Le gare ufficiali disputate da Damiano Morra, capitano e primatista assoluto tra il 1975 e il 1984.",
    href: "./03-tesserati/calciatori/storici/damiano-morra",
  },
  {
    id: "gol-nicolosi-74",
    kicker: "BOMBER ASSOLUTO",
    digits: "74 GOL",
    desc: "Le reti storiche siglate dal centravanti Nicolò Nicolosi, miglior marcatore di tutti i tempi.",
    href: "./03-tesserati/calciatori/storici/nicolo-nicolosi",
  },
  {
    id: "coppa-italia-4-2",
    kicker: "COPPA ITALIA",
    digits: "4–2",
    desc: "La rimonta al Massimino contro il Padova nella finale di ritorno di Coppa Italia Serie C 2024.",
    href: "./02-cronistoria/coppa-italia-serie-c",
  },
  {
    id: "inaugurazione-cibali-1937",
    kicker: "STADIO CIBALI",
    digits: "1937",
    desc: "L'inaugurazione del Polisportivo Cibali, tempio del calcio catanese intitolato ad Angelo Massimino.",
    href: "./04-strutture/stadio-massimino/angelo-massimino",
  },
  {
    id: "presidenza-massimino-24",
    kicker: "IL CAVALIERE",
    digits: "24 ANNI",
    desc: "Il quarto di secolo alla presidenza del club del Presidentissimo Angelo Massimino.",
    href: "./01-societa/presidenti/angelo-massimino",
  },
  {
    id: "derby-barbera-0-4",
    kicker: "IL CAPOLAVORO",
    digits: "0–4",
    desc: "Il derby del 1 marzo 2009 al Barbera, nobilitato dal gol da centrocampo di Giuseppe Mascara.",
    href: "./02-cronistoria/partite-storiche/2008-2009/palermo-catania-0-4",
  },
  {
    id: "falange-ultras-1979",
    kicker: "MOVIMENTO ULTRAS",
    digits: "1979",
    desc: "La nascita della Falange d'Assalto Rossazzurra, gruppo capostipite del tifo organizzato al Cibali.",
    href: "./06-tifoseria-e-cultura/settori/curva-sud/falange-d-assalto",
  },
  {
    id: "rinascita-pelligra-88",
    kicker: "RINASCITA D",
    digits: "88 PT",
    desc: "Il record assoluto nel girone I della Serie D 2022-23 con promozione con sei turni d'anticipo.",
    href: "./01-societa/epoche/2022-pelligra-catania-fc",
  },
  {
    id: "inter-triplete-3-1",
    kicker: "NOTTE COLOSSALE",
    digits: "3–1",
    desc: "La memorabile rimonta del 12 marzo 2010 sull'Inter del Triplete guidata da José Mourinho.",
    href: "./02-cronistoria/stagioni/2009-2010",
  },
  {
    id: "abbonati-record-20000",
    kicker: "FEDE DEL PUBBLICO",
    digits: "20.000",
    desc: "I fedelissimi abbonati al Massimino nella stagione 2023-2024, record nazionale per la Serie C.",
    href: "./02-cronistoria/stagioni/2023-2024",
  },
  {
    id: "dossier-vault-1740",
    kicker: "MONUMENTO DIGITALE",
    digits: "1.740+",
    desc: "Il patrimonio complessivo di nodi, schede biografiche e sentenze consultabili in questo archivio.",
    href: "#storie-in-copertina",
  },
]

const MagazineHome: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  if (fileData.slug !== "index") {
    return null
  }

  // Calcolo deterministico orario per render iniziale statico
  const currentHour = Math.floor(Date.now() / 3600000)
  const storyBatchIdx = currentHour % Math.ceil(COVER_STORIES_POOL.length / 6)
  const initialStories = COVER_STORIES_POOL.slice(storyBatchIdx * 6, storyBatchIdx * 6 + 6)

  const portraitBatchIdx = currentHour % Math.ceil(PORTRAITS_POOL.length / 4)
  const initialPortraits = PORTRAITS_POOL.slice(portraitBatchIdx * 4, portraitBatchIdx * 4 + 4)

  const numberBatchIdx = currentHour % Math.ceil(NUMBERS_POOL.length / 5)
  const initialNumbersSlice = NUMBERS_POOL.slice(numberBatchIdx * 5, numberBatchIdx * 5 + 5)
  const initialNumbers =
    initialNumbersSlice.length === 5
      ? initialNumbersSlice
      : [...initialNumbersSlice, ...NUMBERS_POOL.slice(0, 5 - initialNumbersSlice.length)]


  return (
    <div class="nfc-home">
      {/* 1. HERO COPERTINA STILE NO FOOTBALL COLORS */}
      <section class="nfc-hero-cover" aria-label="Copertina del Magazine Wiki Catania Calcio">
        <div class="nfc-hero-cover__bg">
          <img
            src="./static/images/photos/curva-nord-coreografia.jpg"
            alt="Stadio Angelo Massimino illuminato durante una gara notturna del Catania con coreografia rossazzurra"
            loading="eager"
            fetchpriority="high"
            decoding="async"
            width="1200"
            height="800"
          />
          <div class="nfc-hero-cover__overlay" />
        </div>

        <div class="nfc-hero-cover__inner">
          <div class="nfc-split-badge nfc-split-badge--hero">
            <span class="nfc-split-badge__left">ARCHIVIO STORICO</span>
            <span class="nfc-split-badge__right">DAL 1929 A OGGI</span>
          </div>

          <h1 class="nfc-hero-cover__title">
            WIKI CATANIA CALCIO
            <span class="nfc-hero-cover__subtitle-line">
              STORIA, DIRITTO E CULTURA DELL'ELEFANTE
            </span>
          </h1>

          <p class="nfc-hero-cover__deck">
            L'archivio enciclopedico e memoriale d'inchiesta sul calcio a Catania: oltre 1.740 nodi
            certificati, 95 stagioni complete con quadratura algebrica, tabellini storici, sentenze di
            diritto sportivo e memoria antropologica del tifo rossazzurro.
          </p>

          <div class="nfc-hero-cover__ctas">
            <a href="#storie-in-copertina" class="nfc-double-btn nfc-double-btn--primary">
              <span class="nfc-double-btn__inner">
                <span class="nfc-double-btn__square" aria-hidden="true" />
                <span>ESPLORA L'ENCICLOPEDIA</span>
              </span>
            </a>
            <a href="./02-cronistoria/stagioni/" class="nfc-double-btn nfc-double-btn--light">
              <span class="nfc-double-btn__inner">
                <span>ANNALI STAGIONI (1929–OGGI) →</span>
              </span>
            </a>
          </div>
        </div>
      </section>

      {/* 2. SINCRO-STYLE ARCHITECTURAL MANIFESTO & GIANT NUMBERS */}
      <section class="nfc-sincro-manifesto" aria-label="Numeri chiave e manifesto editoriale">
        <div class="nfc-numbers-strip">
          {initialNumbers.map((stat) => (
            <a href={stat.href} class="nfc-number-cell" data-stat-id={stat.id}>
              <div class="nfc-number-cell__header">
                <span class="nfc-number-cell__kicker">{stat.kicker}</span>
                <span class="nfc-number-cell__arrow" aria-hidden="true">↗</span>
              </div>
              <span class="nfc-number-cell__digits">{stat.digits}</span>
              <span class="nfc-number-cell__desc">{stat.desc}</span>
            </a>
          ))}
        </div>

        <div class="nfc-manifesto-split">
          <div class="nfc-manifesto-split__left">
            <div class="nfc-section-kicker">00 / MANIFESTO EDITORIALE</div>
            <h2 class="nfc-manifesto-split__heading">
              IL CALCIO A CATANIA RACCONTATO COME UN'OPERA D'ARCHITETTURA E CULTURA POPOLARE
            </h2>
            <p class="nfc-manifesto-split__lead">
              A Catania il calcio non è mai stato soltanto cronaca domenicale: è stato questione di Stato
              nelle aule del TAR e del Consiglio di Giustizia Amministrativa, laboratorio tattico tra il
              contropiede di Carmelo Di Bella e il <em>Barça dell'Etna</em>, araldica civica scolpita
              nella pietra lavica de <em>u Liotru</em> e rito collettivo sulle gradinate del Cibali.
            </p>
            <div class="nfc-manifesto-split__meta-row">
              <div>
                <strong>RIGORE DELLE FONTI</strong>
                <span>Art. 70 L. 633/1941 · Almanacchi, sentenze federali e archivi storici</span>
              </div>
              <div>
                <strong>QUADRATURA ALGEBRICA</strong>
                <span>Validazione Pydantic v2 su ogni classifica, tabellino e bilancio</span>
              </div>
            </div>
          </div>

          <div class="nfc-manifesto-split__right">
            <figure class="nfc-sincro-photo-card">
              <img
                src="./static/images/photos/fontana-elefante-liotru.jpg"
                alt="La Fontana dell'Elefante (u Liotru) in Piazza Duomo a Catania"
                loading="lazy"
              />
              <figcaption>
                <span>MATRICE ARALDICA · PIAZZA DUOMO</span>
                <span>L'elefante lavico («u Liotru»), emblema perpetuo del calcio rossazzurro dal 1929.</span>
              </figcaption>
            </figure>
          </div>
        </div>
      </section>

      {/* 3. STORIE IN COPERTINA (NO FOOTBALL COLORS EDITORIAL GRID - 3 COLONNE A ROTAZIONE) */}
      <section id="storie-in-copertina" class="nfc-section" aria-label="Storie in copertina">
        <div class="nfc-section-header">
          <div>
            <span class="nfc-section-kicker">01 / IN COPERTINA</span>
            <h2 class="nfc-section-title">STORIE SCELTE DALLA REDAZIONE</h2>
          </div>
          <div class="nfc-section-header__actions">
            <button
              id="nfc-shuffle-stories-btn"
              class="nfc-rotate-btn"
              type="button"
              title="Estrai altri dossier e storie casuali dall'archivio"
            >
              <span class="nfc-rotate-btn__icon">🎲</span>
              <span>MESCOLA STORIE</span>
            </button>
            <a href="./02-cronistoria/partite-storiche/" class="nfc-link-arrow">
              TUTTI I DOSSIER STORICI →
            </a>
          </div>
        </div>

        <div class="nfc-stories-grid">
          {initialStories.map((story) => (
            <article class="nfc-story-card" data-story-id={story.id}>
              <a href={story.href} class="nfc-story-card__link">
                <div class="nfc-story-card__media">
                  <img src={story.image} alt={story.title} loading="lazy" />
                  <div class="nfc-story-card__badge">
                    <span>{story.category}</span>
                    <span>{story.issue}</span>
                  </div>
                </div>
                <div class="nfc-story-card__body">
                  <h3 class="nfc-story-card__title">{story.title}</h3>
                  <p class="nfc-story-card__excerpt">{story.excerpt}</p>
                  <div class="nfc-story-card__footer">
                    <span class="nfc-story-card__cta">LEGGI IL DOSSIER →</span>
                    <span class="nfc-story-card__credit">{story.credit}</span>
                  </div>
                </div>
              </a>
            </article>
          ))}
        </div>

        {/* Pool JSON e script di rotazione client-side */}
        <script
          type="application/json"
          id="nfc-cover-pool"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(COVER_STORIES_POOL) }}
        />
        <script
          type="application/json"
          id="nfc-numbers-pool"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(NUMBERS_POOL) }}
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `
(function() {
  function shuffle(arr) {
    var copy = arr.slice();
    for (var i = copy.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = copy[i];
      copy[i] = copy[j];
      copy[j] = t;
    }
    return copy;
  }

  function renderNumbers(numbers) {
    var strip = document.querySelector(".nfc-numbers-strip");
    if (!strip) return;
    strip.style.transition = "opacity 0.15s ease";
    strip.style.opacity = "0.2";
    setTimeout(function() {
      strip.innerHTML = numbers.map(function(stat) {
        return '<a href="' + stat.href + '" class="nfc-number-cell" data-stat-id="' + stat.id + '">' +
          '<div class="nfc-number-cell__header">' +
            '<span class="nfc-number-cell__kicker">' + stat.kicker + '</span>' +
            '<span class="nfc-number-cell__arrow" aria-hidden="true">↗</span>' +
          '</div>' +
          '<span class="nfc-number-cell__digits">' + stat.digits + '</span>' +
          '<span class="nfc-number-cell__desc">' + stat.desc + '</span>' +
        '</a>';
      }).join("");
      strip.style.opacity = "1";
    }, 120);
  }

  function shuffleNumbers() {
    var numbersPoolEl = document.getElementById("nfc-numbers-pool");
    if (numbersPoolEl) {
      try {
        var pool = JSON.parse(numbersPoolEl.textContent || "[]");
        if (pool.length) {
          var selected = shuffle(pool).slice(0, 5);
          renderNumbers(selected);
        }
      } catch (e) {}
    }
  }

  function renderStories(stories) {
    var storiesGrid = document.querySelector(".nfc-stories-grid");
    if (!storiesGrid) return;
    storiesGrid.style.transition = "opacity 0.15s ease";
    storiesGrid.style.opacity = "0.2";
    setTimeout(function() {
      storiesGrid.innerHTML = stories.map(function(s) {
        return '<article class="nfc-story-card" data-story-id="' + s.id + '">' +
          '<a href="' + s.href + '" class="nfc-story-card__link">' +
            '<div class="nfc-story-card__media">' +
              '<img src="' + s.image + '" alt="' + s.title.replace(/"/g, '&quot;') + '" loading="lazy" />' +
              '<div class="nfc-story-card__badge">' +
                '<span>' + s.category + '</span>' +
                '<span>' + s.issue + '</span>' +
              '</div>' +
            '</div>' +
            '<div class="nfc-story-card__body">' +
              '<h3 class="nfc-story-card__title">' + s.title + '</h3>' +
              '<p class="nfc-story-card__excerpt">' + s.excerpt + '</p>' +
              '<div class="nfc-story-card__footer">' +
                '<span class="nfc-story-card__cta">LEGGI IL DOSSIER →</span>' +
                '<span class="nfc-story-card__credit">' + s.credit + '</span>' +
              '</div>' +
            '</div>' +
          '</a>' +
        '</article>';
      }).join("");
      storiesGrid.style.opacity = "1";
    }, 120);
  }

  function renderPortraits(portraits) {
    var portraitsGrid = document.querySelector(".nfc-portraits-grid");
    if (!portraitsGrid) return;
    portraitsGrid.style.transition = "opacity 0.15s ease";
    portraitsGrid.style.opacity = "0.2";
    setTimeout(function() {
      portraitsGrid.innerHTML = portraits.map(function(p) {
        return '<a href="' + p.href + '" class="nfc-portrait-card" data-person-id="' + p.id + '">' +
          '<div class="nfc-portrait-card__img-wrap">' +
            '<img src="' + p.image + '" alt="' + p.name.replace(/"/g, '&quot;') + '" loading="lazy" />' +
            '<span class="nfc-portrait-card__stat">' + p.stat + '</span>' +
          '</div>' +
          '<div class="nfc-portrait-card__meta">' +
            '<span class="nfc-portrait-card__name">' + p.name + '</span>' +
            '<span class="nfc-portrait-card__role">' + p.role + '</span>' +
          '</div>' +
        '</a>';
      }).join("");
      portraitsGrid.style.opacity = "1";
    }, 120);
  }

  function shuffleStories() {
    var coverPoolEl = document.getElementById("nfc-cover-pool");
    if (coverPoolEl) {
      try {
        var pool = JSON.parse(coverPoolEl.textContent || "[]");
        if (pool.length) {
          var selected = shuffle(pool).slice(0, 6);
          renderStories(selected);
        }
      } catch (e) {}
    }
  }

  function shufflePortraits() {
    var portraitsPoolEl = document.getElementById("nfc-portraits-pool");
    if (portraitsPoolEl) {
      try {
        var pool = JSON.parse(portraitsPoolEl.textContent || "[]");
        if (pool.length) {
          var selected = shuffle(pool).slice(0, 4);
          renderPortraits(selected);
        }
      } catch (e) {}
    }
  }

  function initRandomizer() {
    var storyBtn = document.getElementById("nfc-shuffle-stories-btn");
    if (storyBtn) {
      storyBtn.onclick = function(e) {
        e.preventDefault();
        shuffleStories();
      };
    }

    var portraitBtn = document.getElementById("nfc-shuffle-portraits-btn");
    if (portraitBtn) {
      portraitBtn.onclick = function(e) {
        e.preventDefault();
        shufflePortraits();
      };
    }
  }

  document.addEventListener("nav", initRandomizer);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRandomizer);
  } else {
    initRandomizer();
  }
})();
`,
          }}
        />
</section>

      {/* 4. ICONOGRAFIA: RITRATTI DELLA HALL OF FAME A ROTAZIONE */}
      <section class="nfc-section nfc-section--dark-band" aria-label="Ritratti Hall of Fame">
        <div class="nfc-section-header">
          <div>
            <span class="nfc-section-kicker">02 / ICONOGRAFIA ROSSAZZURRA</span>
            <h2 class="nfc-section-title">I VOLTI DELL'ELEFANTE: CALCIATORI E CONDOTTIERI</h2>
          </div>
          <div class="nfc-section-header__actions">
            <button
              id="nfc-shuffle-portraits-btn"
              class="nfc-rotate-btn"
              type="button"
              title="Estrai altri volti e tesserati casuali dalla Hall of Fame"
            >
              <span class="nfc-rotate-btn__icon">🎲</span>
              <span>MESCOLA VOLTI</span>
            </button>
            <a href="./03-tesserati/" class="nfc-link-arrow">
              ALBO COMPLETO TESSERATI →
            </a>
          </div>
        </div>

        <div class="nfc-portraits-grid">
          {initialPortraits.map((person) => (
            <a href={person.href} class="nfc-portrait-card" data-person-id={person.id}>
              <div class="nfc-portrait-card__img-wrap">
                <img src={person.image} alt={person.name} loading="lazy" />
                <span class="nfc-portrait-card__stat">{person.stat}</span>
              </div>
              <div class="nfc-portrait-card__meta">
                <span class="nfc-portrait-card__name">{person.name}</span>
                <span class="nfc-portrait-card__role">{person.role}</span>
              </div>
            </a>
          ))}
        </div>

        <script
          type="application/json"
          id="nfc-portraits-pool"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(PORTRAITS_POOL) }}
        />
      </section>

      <section class="nfc-section" aria-label="Cronologia delle ere societarie e matricole FIGC">
        <div class="nfc-section-header">
          <div>
            <span class="nfc-section-kicker">03 / CONTINUITÀ STORICA E GIURIDICA</span>
            <h2 class="nfc-section-title">CRONOLOGIA DELLE RAGIONI SOCIALI E MATRICOLE FIGC</h2>
          </div>
          <a href="./01-societa/" class="nfc-link-arrow">
            ARCHIVIO SOCIETARIO COMPLETO →
          </a>
        </div>

        <div class="nfc-eras-list">
          {ERAS.map((era) => (
            <a href={era.href} class="nfc-era-row">
              <div class="nfc-era-row__years">{era.years}</div>
              <div class="nfc-era-row__main">
                <div class="nfc-era-row__title-line">
                  <h3 class="nfc-era-row__name">{era.name}</h3>
                  <span class="nfc-era-row__matricola">{era.matricola}</span>
                </div>
                <p class="nfc-era-row__event">{era.event}</p>
              </div>
              <div class="nfc-era-row__figures">
                <span class="nfc-era-row__figures-label">PROTAGONISTI</span>
                <span class="nfc-era-row__figures-val">{era.figures}</span>
              </div>
              <div class="nfc-era-row__cta">DOSSIER →</div>
            </a>
          ))}
        </div>
      </section>
    </div>
  )
}

export default (() => MagazineHome) satisfies QuartzComponentConstructor
