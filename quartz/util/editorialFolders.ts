export interface EditorialFolderMeta {
  title: string
  desc: string
  rubric: string
}

export const EDITORIAL_FOLDERS: Record<string, EditorialFolderMeta> = {
  "01-societa": {
    title: "Società, Ere Giuridiche & Presidenti",
    desc: "L'evoluzione istituzionale del Calcio Catania dal 1929 a oggi: le sette ere societarie, le matricole federali FIGC (11700 e 955013), i presidenti storici, i quadri dirigenziali e i dossier di diritto sportivo.",
    rubric: "RUBRICA 01 · SOCIETÀ",
  },
  "01-societa/dirigenti": {
    title: "Quadri Dirigenziali & Direttori Sportivi",
    desc: "Archivio biografico e cronistoria dei dirigenti generali, amministratori delegati e direttori sportivi che hanno governato la gestione tecnica e amministrativa del club etneo.",
    rubric: "RUBRICA 01 · SOCIETÀ",
  },
  "01-societa/epoche": {
    title: "Le Sette Ere Societarie del Calcio Catania (1929–Oggi)",
    desc: "Dalla fondazione della SS Catania nel 1929 alla matricola 11700 del Club Calcio Catania nel 1946, fino alla rifondazione del Catania Football Club nel 2022 con Ross Pelligra.",
    rubric: "RUBRICA 01 · SOCIETÀ",
  },
  "01-societa/presidenti": {
    title: "I Presidenti Storici del Calcio Catania",
    desc: "Tutte le figure presidenziali del club etneo: dai pionieri Santi Quasimodo e Vespasiano Trigona alla leggendaria presidenza di Angelo Massimino, fino all'era moderna.",
    rubric: "RUBRICA 01 · SOCIETÀ",
  },
  "01-societa/vicende-legali": {
    title: "Archivio Giuridico, Diritto Sportivo & Sentenze",
    desc: "Dossier analitici sui procedimenti della giustizia sportiva e amministrativa (TAR, CGA, TFN, CAF): il Caso Scaramella, il Caso Catania 1993, il 2015 e il fallimento 2021.",
    rubric: "RUBRICA 01 · SOCIETÀ",
  },
  "02-cronistoria": {
    title: "Cronistoria Ufficiale & Archivio Campionati",
    desc: "Il registro cronologico completo delle stagioni sportive, delle partite storiche memorabili, degli spareggi promozione, delle finali e dei precedenti ufficiali dal 1929 a oggi.",
    rubric: "RUBRICA 02 · CRONISTORIA",
  },
  "02-cronistoria/stagioni": {
    title: "Tutte le Stagioni del Calcio Catania (1929–Oggi)",
    desc: "Annali completi con classifiche ufficiali, tabellini gara per gara, marcatori con minutaggio, presidenti, allenatori e quadratura algebrica per ogni campionato disputato.",
    rubric: "RUBRICA 02 · CRONISTORIA",
  },
  "02-cronistoria/partite-storiche": {
    title: "Partite Storiche, Spareggi & Nodi Memorabili",
    desc: "I confronti indimenticabili scolpiti nella storia rossazzurra: «Clamoroso al Cibali», gli spareggi dell'Olimpico di Roma del 1983, Taranto 2002, il trionfo nel derby del 2009 e la Coppa Italia 2024.",
    rubric: "RUBRICA 02 · CRONISTORIA",
  },
  "02-cronistoria/partite-storiche/precedenti": {
    title: "Archivio Precedenti Storici per Club Avversario",
    desc: "Bilanci completi dei confronti diretti contro le grandi avversarie storiche del Catania in Serie A, Serie B, Serie C e Coppa Italia.",
    rubric: "RUBRICA 02 · CRONISTORIA",
  },
  "03-tesserati": {
    title: "Archivio Storico Tesserati (Calciatori & Allenatori)",
    desc: "La memoria enciclopedica degli oltre 1.400 protagonisti in maglia rossazzurra: la rosa attuale, le leggende storiche, l'albo degli allenatori e il registro generale tesserati.",
    rubric: "RUBRICA 03 · TESSERATI",
  },
  "03-tesserati/allenatori": {
    title: "Albo Storico degli Allenatori Rossazzurri",
    desc: "Tutte le guide tecniche dal 1929 a oggi: presenze in panchina, statistiche, promozioni storiche (Di Bella, Maran, Zenga, Simeone, Lucarelli, Toscano).",
    rubric: "RUBRICA 03 · TESSERATI",
  },
  "03-tesserati/calciatori": {
    title: "Archivio Monografie Calciatori",
    desc: "Monografie certificate dei calciatori che hanno disputato almeno una gara ufficiale con il Catania: presenze, reti, stagioni, ruoli e note biografiche.",
    rubric: "RUBRICA 03 · TESSERATI",
  },
  "03-tesserati/calciatori/rosa-attuale": {
    title: "Rosa Attuale Catania Football Club (2026–2027)",
    desc: "Organigramma tecnico ufficiale, rosa dei calciatori tesserati suddivisi per reparto, numeri di maglia e rendimento nella stagione in corso.",
    rubric: "RUBRICA 03 · TESSERATI",
  },
  "03-tesserati/calciatori/storici": {
    title: "Leggende Rossazzurre & Hall of Fame",
    desc: "I capitani, i recordmen di presenze e i bomber leggendari: da Nicolosi e Prenna a Mascara, Spinesi, Biagianti, Izco, Bergessio, Lodi e Gomez.",
    rubric: "RUBRICA 03 · TESSERATI",
  },
  "03-tesserati/calciatori/archivio": {
    title: "Archivio Generale Tesserati A–Z",
    desc: "Consultazione alfabetica di tutte le monografie certificate dei calciatori rossazzurri.",
    rubric: "RUBRICA 03 · TESSERATI",
  },
  "04-strutture": {
    title: "Strutture, Stadi & Centri Sportivi",
    desc: "I luoghi del calcio etneo: lo Stadio Angelo Massimino (Cibali), il centro sportivo di Torre del Grifo Village e i campi da gioco pionieristici delle origini.",
    rubric: "RUBRICA 04 · STRUTTURE",
  },
  "04-strutture/stadio-massimino": {
    title: "Stadio Angelo Massimino (Cibali)",
    desc: "Inaugurato nel 1937, il Cibali è la casa storica del Catania: evoluzione architettonica, settori, curve, capienza e ristrutturazioni moderne.",
    rubric: "RUBRICA 04 · STRUTTURE",
  },
  "04-strutture/centri-sportivi": {
    title: "Centri Sportivi & Torre del Grifo Village",
    desc: "I complessi dedicati alla preparazione atletica, al ritiro e al settore giovanile, con il polo d'eccellenza di Torre del Grifo a Mascalucia.",
    rubric: "RUBRICA 04 · STRUTTURE",
  },
  "04-strutture/campi-storici": {
    title: "I Campi da Gioco delle Origini (1908–1937)",
    desc: "I terreni storici del calcio pionieristico a Catania: da Piazza Esposizione (Piazza Verga) al Campo dei Due Obelischi prima della costruzione del Cibali.",
    rubric: "RUBRICA 04 · STRUTTURE",
  },
  "05-identita-e-simboli": {
    title: "Simboli, Araldica & Colori Sociali",
    desc: "L'identità estetica e simbolica del club: il rosso fuoco dell'Etna e l'azzurro del cielo, l'elefante Liotru, l'araldica degli stemmi e la storia delle maglie e degli sponsor.",
    rubric: "RUBRICA 05 · SIMBOLI",
  },
  "05-identita-e-simboli/araldica-e-scudetti": {
    title: "Araldica, Scudetti & Evoluzione Liotru",
    desc: "La genealogia degli stemmi sociali dal 1929 a oggi: le forme a scudo, la transizione dell'elefante Liotru, le varianti cromatiche e l'acquisizione del marchio storico.",
    rubric: "RUBRICA 05 · SIMBOLI",
  },
  "05-identita-e-simboli/sponsor": {
    title: "Sponsor Tecnici & Main Sponsor Commerciali",
    desc: "Tutte le divise e i marchi che hanno accompagnato le stagioni del Catania: da Ennerre a Puma, Legea, Givova ed Erreà, insieme agli storici sponsor sul petto.",
    rubric: "RUBRICA 05 · SIMBOLI",
  },
  "06-tifoseria-e-cultura": {
    title: "Cultura Ultras, Tifoseria & Antropologia di Curva",
    desc: "La passione delle curve del Massimino, la nascita del movimento ultras dal 1979, i cori, le coreografie, i grandi esodi, i gemellaggi e le rivalità storiche.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/curve": {
    title: "Le Curve del Massimino (Curva Nord & Curva Sud)",
    desc: "I due poli del tifo organizzato etneo: le origini, le filosofie di curva, gli striscioni storici e il legame viscerale con i quartieri di Catania.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/curve/curva-nord": {
    title: "Curva Nord: Movimento, Gruppi & Coreografie",
    desc: "La storia della Curva Nord: dalle prime sigle a Mecha Katane e A Sostegno di una Fede, con le coreografie monumentali che hanno riempito lo stadio.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/curve/curva-sud": {
    title: "Curva Sud: Falange d'Assalto & Irriducibili 1991",
    desc: "Le radici storiche del tifo popolare: la Falange fondata nel 1979 da Ciccio Famoso, gli Irriducibili e l'identità del Castello Ursino e di San Cristoforo.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/biografie": {
    title: "Figure Iconiche della Tifoseria",
    desc: "Le biografie e i profili dei protagonisti carismatici del tifo rossazzurro che hanno dedicato la vita ai gradoni del Cibali.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/eventi-e-giustizia": {
    title: "Eventi Storici, Esodi & Cronache del Tifo",
    desc: "L'esodo dei 40.000 a Roma nel 1983, la legislazione speciale sugli stadi (DASPO), l'analisi dei procedimenti giudiziari e la memoria storica.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/relazioni": {
    title: "Mappa Geopolitica del Tifo: Gemellaggi & Rivalità",
    desc: "Le alleanze fraterne (Genoa, Napoli, Triestina) e gli storici antagonismi campanilistici (Palermo, Messina, Siracusa, Verona).",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/relazioni/gemellaggi": {
    title: "Gemellaggi & Rapporti di Fratellanza",
    desc: "Lo storico e indissolubile gemellaggio con la tifoseria del Genoa e i legami di stima con Napoli, Triestina, Crotone e Borussia Dortmund.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/relazioni/rivalita": {
    title: "Rivalità Storiche & Grandi Derby",
    desc: "Il Derby di Sicilia contro il Palermo, il derby dello Stretto con il Messina e le accese sfide contro club del panorama regionale e nazionale.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "07-media-e-comunicazione": {
    title: "Media, Stampa, TV & Voci Rossazzurre",
    desc: "La narrazione giornalistica, letteraria e radiotelevisiva delle vicende del Calcio Catania: testate storiche, emittenti regionali, grandi firme e saggi enciclopedici.",
    rubric: "RUBRICA 07 · MEDIA",
  },
  "07-media-e-comunicazione/testate": {
    title: "Testate Giornalistiche, Emittenti TV & Web",
    desc: "La Sicilia, Espresso Sera, Telecolor, Antenna Sicilia e i portali dell'informazione digitale legati alla cronaca etnea.",
    rubric: "RUBRICA 07 · MEDIA",
  },
  "07-media-e-comunicazione/firme-e-voci": {
    title: "Grandi Firme, Cronisti & Voci Storiche",
    desc: "I maestri del giornalismo etneo (Luigi Prestinenza, Candido Cannavò, Stefania Sberna e i radiocronisti storici) che hanno dato voce alla passione rossazzurra.",
    rubric: "RUBRICA 07 · MEDIA",
  },
  "07-media-e-comunicazione/letteratura": {
    title: "Letteratura & Grandi Almanacchi Rossazzurri",
    desc: "Le opere bibliografiche di riferimento, dagli almanacchi statistici di Tutto il Catania minuto per minuto ai saggi storici sul club.",
    rubric: "RUBRICA 07 · MEDIA",
  },
  "08-settori-paralleli": {
    title: "Settori Paralleli, Cantera & Altre Discipline",
    desc: "Il vivaio rossazzurro, la valorizzazione dei giovani talenti, la squadra femminile e le altre discipline che hanno portato i colori del Catania alla ribalta.",
    rubric: "RUBRICA 08 · PARALLELI",
  },
  "08-settori-paralleli/giovanili": {
    title: "Settore Giovanile, Cantera & Viareggio",
    desc: "La cantera dell'Elefante, la formazione Berretti e Primavera e le storiche partecipazioni alla Coppa Carnevale di Viareggio.",
    rubric: "RUBRICA 08 · PARALLELI",
  },
  "08-settori-paralleli/women": {
    title: "Catania Women & Tradizione Femminile",
    desc: "Dallo scudetto 1978 della Jolly Componibili Catania alla rinascita del dipartimento femminile del Catania Football Club.",
    rubric: "RUBRICA 08 · PARALLELI",
  },
}

export function getEditorialFolderInfo(rawSlug: string): EditorialFolderMeta {
  const clean = rawSlug.replace(/\/index$/, "").replace(/^\/+|\/+$/g, "")
  if (EDITORIAL_FOLDERS[clean]) {
    return EDITORIAL_FOLDERS[clean]
  }

  // Derive rubric from leading segment
  let rubric = "ARCHIVIO STORICO"
  if (clean.startsWith("01-") || clean.startsWith("societa")) rubric = "RUBRICA 01 · SOCIETÀ"
  else if (clean.startsWith("02-") || clean.startsWith("cronistoria") || clean.startsWith("stagioni")) rubric = "RUBRICA 02 · CRONISTORIA"
  else if (clean.startsWith("03-") || clean.startsWith("tesserati")) rubric = "RUBRICA 03 · TESSERATI"
  else if (clean.startsWith("04-") || clean.startsWith("strutture") || clean.startsWith("stadio")) rubric = "RUBRICA 04 · STRUTTURE"
  else if (clean.startsWith("05-") || clean.startsWith("identita") || clean.startsWith("simboli")) rubric = "RUBRICA 05 · SIMBOLI"
  else if (clean.startsWith("06-") || clean.startsWith("tifoseria")) rubric = "RUBRICA 06 · TIFOSERIA"
  else if (clean.startsWith("07-") || clean.startsWith("media")) rubric = "RUBRICA 07 · MEDIA"
  else if (clean.startsWith("08-") || clean.startsWith("settori")) rubric = "RUBRICA 08 · PARALLELI"

  // Check season pattern
  const seasonMatch = clean.match(/(\d{4}-\d{4})/)
  if (seasonMatch) {
    if (clean.includes("partite")) {
      return {
        title: `Partite Storiche — Stagione ${seasonMatch[1]}`,
        desc: `Tabellini ufficiali e cronache certificate delle partite storiche disputate nella stagione ${seasonMatch[1]}.`,
        rubric,
      }
    }
    return {
      title: `Stagione ${seasonMatch[1]}`,
      desc: `Resoconto ufficiale della stagione agonistica ${seasonMatch[1]} del Calcio Catania.`,
      rubric,
    }
  }

  // Fallback humanizer: strip number prefix, replace dashes, capitalize
  const lastSeg = clean.split("/").pop() || clean
  const title = lastSeg
    .replace(/^\d{2}-/, "")
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ")

  return {
    title,
    desc: `Esplora i documenti certificati e le schede storiche raccolte in questa sezione dell'archivio.`,
    rubric,
  }
}
