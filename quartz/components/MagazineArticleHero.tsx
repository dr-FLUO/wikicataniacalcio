import { visit } from "unist-util-visit"
import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

interface HeroMedia {
  file: string
  caption: string
  credit: string
  fit?: "cover" | "contain"
  aspect?: "wide" | "portrait" | "cinema"
}

function selectHeroMedia(slug: string, fm: Record<string, any>): HeroMedia | null {
  if (fm.cover_image) {
    return {
      file: String(fm.cover_image),
      caption: String(fm.cover_caption ?? fm.title ?? "Archivio Storico Wiki Catania Calcio"),
      credit: String(fm.cover_credit ?? "Archivio Storico / Wikimedia Commons"),
      fit: "cover",
      aspect: "wide",
    }
  }

  // Specific player / coach / president portraits
  if (slug.includes("marco-biagianti")) {
    return {
      file: "marco-biagianti.jpg",
      caption:
        "Marco Biagianti, capitano e primatista di presenze in Serie A (284 gare totali in rossazzurro), intervistato a Massannunziata.",
      credit: "Foto: Manku 7 · Licenza: Public Domain (Wikimedia Commons)",
      aspect: "wide",
    }
  }
  if (slug.includes("giuseppe-mascara")) {
    return {
      file: "mascara-tifosi.jpg",
      caption:
        "Giuseppe Mascara acclamato dai tifosi rossazzurri: 236 presenze e 61 reti complessive con la maglia dell'Elefante.",
      credit: "Foto: Roberto Quartarone · Licenza: CC BY-SA 2.5",
      aspect: "portrait",
    }
  }
  if (slug.includes("gionatha-spinesi") || slug.includes("2005-2006")) {
    return {
      file: "mascara-spinesi.jpg",
      caption:
        "Giuseppe Mascara e Gionatha Spinesi (#24) al calcio d'inizio: la coppia d'oro della promozione in Serie A 2005-2006 (36 reti in due).",
      credit: "Foto: Roberto Quartarone · Licenza: CC BY-SA 2.5",
      aspect: "wide",
    }
  }
  if (slug.includes("mariano-izco")) {
    return {
      file: "mariano-izco.jpg",
      caption:
        "Mariano Julio Izco, 280 presenze in otto stagioni consecutive di Serie A con il Calcio Catania (2006–2014).",
      credit: "Foto: Emi1929 · Licenza: CC BY-SA 4.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("gonzalo-bergessio")) {
    return {
      file: "gonzalo-bergessio.jpg",
      caption:
        "Gonzalo Rubén Bergessio («El Lavandina»), miglior marcatore in Serie A dell'era moderna rossazzurra con 35 reti.",
      credit: "Foto: Phil1m · Licenza: CC BY-SA 3.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("maxi-lopez")) {
    return {
      file: "maxi-lopez.jpg",
      caption:
        "Maxi López («La Galina») al centro sportivo di Torre del Grifo: 27 reti complessive e trascinatore della salvezza 2009-2010.",
      credit: "Foto: Phil1m · Licenza: CC BY-SA 3.0 (Wikimedia Commons)",
      aspect: "portrait",
    }
  }
  if (slug.includes("pablo-barrientos")) {
    return {
      file: "pablo-barrientos.jpg",
      caption:
        "Pablo César Barrientos («El Pitu») durante la preparazione con il Calcio Catania a Torre del Grifo (86 gare e 14 reti in Serie A).",
      credit: "Foto: Phil1m · Licenza: CC BY-SA 3.0 (Wikimedia Commons)",
      aspect: "portrait",
    }
  }
  if (slug.includes("orazio-russo")) {
    return {
      file: "orazio-russo.jpg",
      caption:
        "Orazio Russo con la divisa sociale del Calcio Catania: bandiera etnea e unico calciatore ad aver disputato tutte le serie professionistiche con la maglia del Catania.",
      credit: "Archivio Storico Calcio Catania · Pubblico Dominio",
      aspect: "portrait",
    }
  }
  if (slug.includes("alejandro-gomez") || slug.includes("papu-gomez")) {
    return {
      file: "papu-gomez.jpg",
      caption:
        "Alejandro Darío «Papu» Gómez, protagonista assoluto del triennio di Serie A 2010–2013 con 111 presenze e 18 gol nel Catania dei record.",
      credit: "Foto: Wikimedia Commons · Licenza: CC BY-SA 4.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("francesco-lodi")) {
    return {
      file: "francesco-lodi.jpg",
      caption:
        "Francesco «Ciccio» Lodi, regista e specialista dei calci piazzati in tre diversi cicli storici a Catania (52 reti complessive).",
      credit: "Foto: Filippo Mancuso · Licenza: CC BY-SA 3.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("carmelo-di-bella") || slug.includes("1960-1961") || slug.includes("catania-inter-2-0")) {
    return {
      file: "catania-1960-61.jpg",
      caption:
        "La storica formazione del Club Calcio Catania 1960-1961 guidata da Carmelo Di Bella, protagonista dell'8° posto in Serie A e del «Clamoroso al Cibali!».",
      credit: "Archivio Storico · Pubblico Dominio (Art. 87 L. 633/1941)",
      aspect: "wide",
    }
  }
  if (slug.includes("diego-pablo-simeone") || slug.includes("2010-2011")) {
    return {
      file: "diego-simeone.jpg",
      caption:
        "Diego Pablo Simeone («El Cholo»), artefice della salvezza record a 46 punti nella stagione di Serie A 2010-2011.",
      credit: "Foto: Carlos Delgado · Licenza: CC BY-SA 3.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("rolando-maran") || slug.includes("2012-2013")) {
    return {
      file: "rolando-maran.jpg",
      caption:
        "Rolando Maran, tecnico del Catania dei record nella stagione 2012-2013 (56 punti e 8° posto in Serie A).",
      credit: "Foto: Pottercomuneo · Licenza: CC BY-SA 4.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("sinisa-mihajlovic") || slug.includes("2009-2010")) {
    return {
      file: "sinisa-mihajlovic.jpg",
      caption:
        "Siniša Mihajlović, tecnico del Catania nella prodigiosa cavalcata salvezza 2009-2010, culminata con il 3-1 sull'Inter del Triplete al Cibali.",
      credit: "Foto: Wikimedia Commons · Licenza: CC BY-SA 3.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("pasquale-marino")) {
    return {
      file: "pasquale-marino.jpg",
      caption:
        "Pasquale Marino, allenatore dell'indimenticabile ritorno in Serie A nel 2005-2006 e della salvezza a Bologna nel 2007.",
      credit: "Foto: Roberto Vicario · Licenza: CC BY-SA 3.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("vincenzo-montella") || slug.includes("2011-2012")) {
    return {
      file: "vincenzo-montella.jpg",
      caption:
        "Vincenzo Montella, condottiero del Catania nella brillante stagione di Serie A 2011-2012 (48 punti complessivi).",
      credit: "Foto: Roberto Vicario · Licenza: CC BY-SA 3.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("walter-zenga") || slug.includes("2008-2009")) {
    return {
      file: "walter-zenga.jpg",
      caption:
        "Walter Zenga, allenatore rossazzurro nella memorabile stagione 2008-2009, coronata dal clamoroso 0-4 nel derby di Palermo.",
      credit: "Foto: Neogeolegend · Licenza: CC BY 3.0",
      aspect: "portrait",
    }
  }
  if (slug.includes("gianni-di-marzio") || slug.includes("1982-1983")) {
    return {
      file: "gianni-di-marzio.jpg",
      caption:
        "Gianni Di Marzio, tecnico della memorabile promozione in Serie A conquistata agli spareggi di Roma nel giugno 1983.",
      credit: "Archivio Storico · Licenza: CC BY-SA 3.0",
      aspect: "portrait",
    }
  }

  // Presidents & Leadership
  if (slug.includes("ross-pelligra") || slug.includes("2022-pelligra")) {
    return {
      file: "ross-pelligra.jpg",
      caption:
        "Ross Pelligra, presidente del Catania Football Club, sotto la Tribuna B dello Stadio Angelo Massimino dopo la rinascita del 2022.",
      credit: "Foto: Supergaefs · Licenza: CC BY-SA 4.0 (Wikimedia Commons)",
      aspect: "wide",
    }
  }
  if (slug.includes("vincenzo-grella")) {
    return {
      file: "dirigenza-catania-ssd.jpg",
      caption:
        "La dirigenza del Catania SSD (Ross Pelligra e Vincenzo Grella) alla conferenza inaugurale del nuovo corso rossazzurro (2022).",
      credit: "Foto: Devis Parker · Licenza: CC BY-SA 4.0",
      aspect: "wide",
    }
  }
  if (slug.includes("angelo-massimino") || slug.includes("1967-calcio-catania-spa-massimino") || slug.includes("caso-catania-1993")) {
    return {
      file: "angelo-massimino.jpg",
      caption:
        "Angelo Massimino (1927–1996), il «Presidentissimo» per eccellenza del Calcio Catania per 27 stagioni sportive tra promozioni e contenziosi federali.",
      credit: "Archivio Storico Calcio Catania · Pubblico Dominio",
      aspect: "portrait",
    }
  }
  if (slug.includes("luciano-gaucci") || slug.includes("2000-era-gaucci") || slug.includes("caso-catania-2003")) {
    return {
      file: "luciano-gaucci.jpg",
      caption:
        "Luciano Gaucci (1938–2020), patron del Calcio Catania dal 1993 al 2000 e protagonista della vertenza giurisdizionale del Caso Catania 2003.",
      credit: "Archivio Storico · Pubblico Dominio",
      aspect: "portrait",
    }
  }
  if (slug.includes("ignazio-marcoccio")) {
    return {
      file: "szymaniak-marcoccio.jpg",
      caption:
        "Il Commissario Straordinario Ignazio Marcoccio con Horst Szymaniak nel 1961, anni del primo grande ciclo etneo in Serie A.",
      credit: "Archivio Storico · Pubblico Dominio",
      aspect: "portrait",
    }
  }
  if (slug.includes("antonino-pulvirenti") || slug.includes("2004-era-pulvirenti")) {
    return {
      file: "torre-del-grifo-village.jpg",
      caption:
        "Veduta aerea del centro sportivo Torre del Grifo Village a Mascalucia, avveniristico centro sociale e quartier generale inaugurato dall'era Pulvirenti nel 2011.",
      credit: "Foto: Salvosmav · Licenza: CC BY-SA 4.0 (Wikimedia Commons)",
      aspect: "wide",
    }
  }

  // Legal Dossiers (Specific matching to prevent fallback to generic timeline diagram)
  if (slug.includes("treni-del-gol")) {
    return {
      file: "torre-del-grifo-village.jpg",
      caption:
        "Il centro sportivo Torre del Grifo Village a Mascalucia, sede operativa del club ed epicentro delle notifiche giudiziarie nell'operazione «I Treni del Gol» (23 giugno 2015).",
      credit: "Foto: Salvosmav · Licenza: CC BY-SA 4.0 (Wikimedia Commons)",
      aspect: "wide",
    }
  }
  if (slug.includes("fallimento-2021") || slug.includes("blocco-ripescaggi-2018") || slug.includes("trattativa-sigi")) {
    return {
      file: "palazzo-giustizia-catania.jpg",
      caption:
        "Il Palazzo di Giustizia di Catania in Piazza Giovanni Verga, sede della sezione fallimentare che sancì il fallimento del Calcio Catania S.p.A. (22 dicembre 2021).",
      credit: "Foto: DMarx22 · Licenza: CC BY-SA 4.0 (Wikimedia Commons)",
      aspect: "wide",
    }
  }
  if (slug.includes("decreto-2-febbraio-2007") || slug.includes("filippo-raciti")) {
    return {
      file: "pala-spedini-raciti-2007.jpg",
      caption:
        "L'omaggio floreale e gli striscioni al PalaSpedini e allo Stadio Cibali all'indomani del derby del 2 febbraio 2007, spartiacque della sicurezza negli stadi (Legge 41/2007).",
      credit: "Foto: Wikimedia Commons · Licenza: CC BY-SA 2.5",
      aspect: "wide",
    }
  }

  // Stadium & Grounds
  if (slug.includes("torre-del-grifo")) {
    return {
      file: "torre-del-grifo-village.jpg",
      caption:
        "Veduta aerea del centro sportivo Torre del Grifo Village a Mascalucia, polo polifunzionale d'eccellenza per la preparazione atletica e societaria.",
      credit: "Foto: Salvosmav · Licenza: CC BY-SA 4.0 (Wikimedia Commons)",
      aspect: "wide",
    }
  }
  if (slug.includes("piazza-esposizione")) {
    return {
      file: "piazza-verga-malavoglia.jpg",
      caption:
        "Piazza Giovanni Verga (già Piazza Esposizione) e la monumentale Fontana dei Malavoglia: primo campo da gioco storico del calcio a Catania (1910–1930).",
      credit: "Foto: Drunkpiper · Licenza: Pubblico Dominio (Wikimedia Commons)",
      aspect: "wide",
    }
  }

  // Specific indexes that have dedicated historical infographics
  if (slug === "vicende-legali/index" || slug === "01-societa/vicende-legali/index") {
    return {
      file: "cronistoria-giudiziaria.png",
      caption:
        "Tavola sinottica dei procedimenti giudiziari, ricorsi amministrativi (TAR/CGA) e sentenze federali nella storia del Calcio Catania (1929–2024).",
      credit: "Infografica Redazionale Wiki Catania Calcio — Fonti: FIGC / TAR Sicilia",
      fit: "contain",
      aspect: "wide",
    }
  }

  // Nessuna foto fuori contesto: dove non è disponibile una foto specifica autenticata, non viene mostrato alcun box
  return null
}

function getPageEditorialBadges(slug: string, fm: Record<string, any>): { left: string; right: string } {
  // Se il frontmatter specifica esplicitamente le etichette editoriali
  if (fm.category && fm.issue) {
    return { left: String(fm.category).toUpperCase(), right: String(fm.issue).toUpperCase() }
  }
  if (fm.editorial_category && fm.editorial_badge) {
    return { left: String(fm.editorial_category).toUpperCase(), right: String(fm.editorial_badge).toUpperCase() }
  }

  const s = slug.toLowerCase()
  const title = String(fm.title ?? slug)
  const t = title.toLowerCase()

  // 02 - Cronistoria / Stagioni / Partite
  if (s.includes("02-cronistoria") || s.includes("stagioni") || s.includes("partite-storiche") || s.includes("partite/")) {
    if (s.includes("partite")) {
      const mYear = title.match(/(19\d\d|20\d\d)/)
      const yearStr = mYear ? mYear[1] : ""
      return {
        left: "PARTITE STORICHE",
        right: yearStr ? `TABELLINO · ${yearStr}` : "TABELLINO STORICO",
      }
    } else {
      const mSeason = slug.match(/(\d{4}[–-]\d{4})/)
      const season = mSeason ? mSeason[1].replace("-", "–") : (fm.season_label ? String(fm.season_label).replace("-", "–") : "")
      let cat = "ANNALI CAMPIONATO"
      const mDivision = title.match(/[—–-]\s*(Serie [ABCD]|Lega Pro|Prima Divisione|Seconda Divisione|CND|Interregionale|Divisione Nazionale)/i)
      if (mDivision) {
        cat = mDivision[1].toUpperCase()
      } else if (t.includes("serie b")) {
        cat = "SERIE B"
      } else if (t.includes("serie a")) {
        cat = "SERIE A"
      } else if (t.includes("serie c") || t.includes("lega pro") || t.includes("serie c1") || t.includes("serie c2")) {
        cat = "SERIE C"
      } else if (t.includes("serie d") || t.includes("interregionale") || t.includes("cnd")) {
        cat = "SERIE D"
      } else if (t.includes("prima divisione")) {
        cat = "PRIMA DIVISIONE"
      }

      return {
        left: cat,
        right: season ? `ANNALE UFFICIALE · ${season}` : "ANNALE UFFICIALE",
      }
    }
  }

  // 03 - Tesserati (Calciatori / Allenatori)
  if (s.includes("03-tesserati") || s.includes("calciatori") || s.includes("allenatori") || s.includes("tesserati/")) {
    if (s.includes("allenatori")) {
      const mYears = title.match(/(\d{4}[–-]\d{4})/)
      const years = mYears ? mYears[1].replace("-", "–") : ""
      return {
        left: "GUIDA TECNICA",
        right: years ? `ALLENATORE · ${years}` : "PROFILO ALLENATORE",
      }
    } else {
      const role = String(fm.role ?? "")
      const roleShort = role ? role.split("(")[0].trim().toUpperCase() : "CALCIATORE"
      const mYears = title.match(/(\d{4}[–-]\d{4})/)
      let years = mYears ? mYears[1].replace("-", "–") : ""
      if (!years && Array.isArray(fm.catania_periods) && fm.catania_periods.length > 0) {
        const first = String(fm.catania_periods[0]).split("-")[0]
        const last = String(fm.catania_periods[fm.catania_periods.length - 1]).split("-").pop()
        years = first !== last ? `${first}–${last}` : first
      }
      return {
        left: "CALCIATORI ROSSAZZURRI",
        right: years ? `${roleShort} · ${years}` : roleShort,
      }
    }
  }

  // 01 - Società / Presidenti / Dirigenti / Epoche / Vicende Legali
  if (s.includes("01-societa") || s.includes("societa/") || s.includes("vicende-legali/")) {
    if (s.includes("vicende-legali")) {
      const mYear = (slug + " " + title).match(/(19\d\d|20\d\d)/)
      const y = mYear ? mYear[1] : ""
      return {
        left: "DIRITTO SPORTIVO",
        right: y ? `DOSSIER GIURIDICO · ${y}` : "DOSSIER GIURISPRUDENZIALE",
      }
    }
    if (s.includes("presidenti")) {
      const mYears = title.match(/(\d{4}[–-]\d{4})/)
      const years = mYears ? mYears[1].replace("-", "–") : ""
      return {
        left: "PRESIDENTI & PATRON",
        right: years ? `PRESIDENZA · ${years}` : "PROFILO PRESIDENZIALE",
      }
    }
    if (s.includes("dirigenti")) {
      return {
        left: "QUADRI DIRIGENZIALI",
        right: "MANAGEMENT STORICO",
      }
    }
    if (s.includes("epoche")) {
      const mYears = title.match(/(\d{4}[–-]\d{4})/) || title.match(/(19\d\d|20\d\d)/)
      const years = mYears ? mYears[0].replace("-", "–") : ""
      return {
        left: "STORIA SOCIETARIA",
        right: years ? `ERA SOCIETARIA · ${years}` : "ERA SOCIETARIA",
      }
    }
    return {
      left: "SOCIETÀ & ASSETTI",
      right: "ORGANIZZAZIONE CLUB",
    }
  }

  // 04 - Strutture / Stadi / Centri Sportivi / Campi Storici
  if (s.includes("04-strutture") || s.includes("strutture/") || s.includes("stadio/")) {
    if (s.includes("stadio") || s.includes("massimino") || s.includes("cibali")) {
      return {
        left: "ARCHITETTURA & STADI",
        right: "STADIO CIBALI · DAL 1937",
      }
    }
    if (s.includes("centri-sportivi") || s.includes("torre-del-grifo")) {
      return {
        left: "CENTRI SPORTIVI",
        right: "TORRE DEL GRIFO · 2011–2022",
      }
    }
    if (s.includes("campi-storici")) {
      return {
        left: "CAMPI PIONIERISTICI",
        right: "ORIGINI CITTADINE · 1910–1937",
      }
    }
    return {
      left: "IMPIANTI & INFRASTRUTTURE",
      right: "PATRIMONIO IMMOBILIARE",
    }
  }

  // 05 - Identità e Simboli / Araldica / Sponsor / Maglie
  if (s.includes("05-identita-e-simboli") || s.includes("identita/") || s.includes("maglie/")) {
    if (s.includes("araldica") || s.includes("scudett") || s.includes("marchio")) {
      const isAsta = s.includes("asta") || s.includes("acquisizione")
      return {
        left: "ARALDICA & COLORI",
        right: isAsta ? "RISCATTO MARCHIO · 2026" : "STEMMI & COLORI · DAL 1929",
      }
    }
    if (s.includes("sponsor")) {
      return {
        left: "SPONSOR & DIVISE",
        right: "MAGLIE UFFICIALI",
      }
    }
    return {
      left: "SIMBOLI ROSSAZZURRI",
      right: "IDENTITÀ & ICONOGRAFIA",
    }
  }

  // 06 - Tifoseria e Cultura / Relazioni / Settori / Eventi
  if (s.includes("06-tifoseria-e-cultura") || s.includes("tifoseria/")) {
    if (s.includes("gemellaggi")) {
      return {
        left: "CULTURA ULTRAS",
        right: "GEMELLAGGIO STORICO",
      }
    }
    if (s.includes("amicizie")) {
      return {
        left: "CULTURA ULTRAS",
        right: "FRATELLANZA & RISPETTO",
      }
    }
    if (s.includes("rivalita")) {
      return {
        left: "CULTURA ULTRAS",
        right: "RIVALITÀ & DERBY",
      }
    }
    if (s.includes("settori") || s.includes("curva")) {
      const mYear = (title + " " + slug).match(/(19\d\d|20\d\d)/)
      const y = mYear ? mYear[1] : ""
      return {
        left: "CURVE & GRADINATE",
        right: y ? `TIFO ORGANIZZATO · DAL ${y}` : "TIFO ORGANIZZATO",
      }
    }
    if (s.includes("eventi-e-giustizia")) {
      const mYear = (title + " " + slug).match(/(19\d\d|20\d\d)/)
      const y = mYear ? mYear[1] : ""
      return {
        left: "CRONACA & GIUSTIZIA",
        right: y ? `FATTI E MEMORIA · ${y}` : "FATTI E MEMORIA",
      }
    }
    if (s.includes("biografie")) {
      return {
        left: "MEMORIA POPOLARE",
        right: "FIGURE DEL TIFO",
      }
    }
    return {
      left: "TIFOSERIA ROSSAZZURRA",
      right: "ETNOGRAFIA DELLE CURVE",
    }
  }

  // 07 - Media e Comunicazione / Cinema / Firme / Letteratura
  if (s.includes("07-media-e-comunicazione") || s.includes("media/")) {
    if (s.includes("cinema") || s.includes("tv")) {
      return {
        left: "CULTURA POPOLARE",
        right: "CINEMA & TELEVISIONE · 1973–2010",
      }
    }
    if (s.includes("firme") || s.includes("voci")) {
      const mYears = title.match(/(\d{4}[–-]\d{4})/)
      const years = mYears ? mYears[1].replace("-", "–") : ""
      return {
        left: "GIORNALISMO & VOCI",
        right: years ? `RACCONTO CIVILE · ${years}` : "TESTIMONIANZE",
      }
    }
    if (s.includes("letteratura")) {
      return {
        left: "LETTERATURA & SAGGI",
        right: "PUBBLICAZIONI ROSSAZZURRE",
      }
    }
    if (s.includes("testate")) {
      return {
        left: "STAMPA SPORTIVA",
        right: "PERIODICI E QUOTIDIANI",
      }
    }
    return {
      left: "MEDIA & COMUNICAZIONE",
      right: "RACCONTO EDITORIALE",
    }
  }

  // 08 - Settori Paralleli / Women / Giovanili
  if (s.includes("08-settori-paralleli") || s.includes("settori-paralleli/")) {
    if (s.includes("women") || s.includes("femminile")) {
      return {
        left: "CALCIO FEMMINILE",
        right: "SCUDETTO JOLLY · DAL 1970",
      }
    }
    if (s.includes("giovanili")) {
      return {
        left: "SETTORE GIOVANILE",
        right: "CANTERA & PRIMAVERA",
      }
    }
    return {
      left: "SETTORI PARALLELI",
      right: "DISCIPLINE AFFINI",
    }
  }

  // Se è impostato un tag specifico nel frontmatter
  if (Array.isArray(fm.tags) && fm.tags.length > 0) {
    return {
      left: "DOSSIER ARCHIVIO",
      right: String(fm.tags[0]).replace(/-/g, " ").toUpperCase(),
    }
  }

  return { left: "WIKI CATANIA CALCIO", right: "DOSSIER MONOGRAFICO" }
}

interface BreadcrumbCrumb {
  label: string
  target: string
}

function getHeroBreadcrumbs(slug: string): BreadcrumbCrumb[] {
  const crumbs: BreadcrumbCrumb[] = [{ label: "Home", target: "index" }]
  const clean = slug.replace(/\/index$/, "")
  const segs = clean.split("/").filter(Boolean)
  if (segs.length === 0) return crumbs

  const topMap: Record<string, string> = {
    "01-societa": "01 · Società",
    "02-cronistoria": "02 · Cronistoria",
    "03-tesserati": "03 · Tesserati",
    "04-strutture": "04 · Strutture",
    "05-identita-e-simboli": "05 · Simboli",
    "06-tifoseria-e-cultura": "06 · Tifoseria",
    "07-media-e-comunicazione": "07 · Media",
    "08-settori-paralleli": "08 · Vivaio & Women",
  }

  const subMap: Record<string, string> = {
    "epoche": "Epoche Societarie",
    "presidenti": "Presidenti",
    "dirigenti": "Dirigenti & DS",
    "vicende-legali": "Diritto & Giustizia",
    "stagioni": "Stagioni",
    "partite-storiche": "Partite Storiche",
    "precedenti": "Precedenti & Derby",
    "allenatori": "Allenatori",
    "storici": "Leggende & Storici",
    "rosa-attuale": "Rosa Attuale",
    "archivio": "Archivio Calciatori A–Z",
    "stadio-massimino": "Stadio Massimino",
    "centri-sportivi": "Centri Sportivi",
    "campi-storici": "Campi Storici",
    "araldica-e-scudetti": "Stemmi & Liotru",
    "sponsor": "Sponsor",
    "curva-nord": "Curva Nord",
    "curva-sud": "Curva Sud",
    "tribuna-b": "Tribuna B",
    "gemellaggi": "Gemellaggi",
    "amicizie": "Amicizie",
    "rivalita": "Rivalità",
    "biografie": "Biografie Ultras",
    "eventi-e-giustizia": "Eventi & Giustizia",
    "testate": "Testate & TV",
    "firme-e-voci": "Firme & Voci",
    "letteratura": "Libri & Almanacchi",
    "cinema-e-tv": "Cinema & TV",
    "giovanili": "Settore Giovanile",
    "women": "Catania Women",
  }

  if (topMap[segs[0]]) {
    crumbs.push({ label: topMap[segs[0]], target: `${segs[0]}/index` })
  }

  // Build 2nd level crumb following the Max-2-Levels rule
  if (segs.length >= 2) {
    if (segs[0] === "02-cronistoria" && segs[1] === "partite-storiche" && segs[2] === "precedenti") {
      crumbs.push({ label: "Precedenti & Derby", target: "02-cronistoria/partite-storiche/precedenti/index" })
    } else if (segs[0] === "03-tesserati" && segs[1] === "calciatori" && segs[2] && subMap[segs[2]]) {
      crumbs.push({ label: subMap[segs[2]], target: `03-tesserati/calciatori/${segs[2]}/index` })
    } else if (
      segs[0] === "06-tifoseria-e-cultura" &&
      (segs[1] === "settori" || segs[1] === "relazioni") &&
      segs[2] &&
      subMap[segs[2]]
    ) {
      crumbs.push({ label: subMap[segs[2]], target: `06-tifoseria-e-cultura/${segs[1]}/${segs[2]}/index` })
    } else if (subMap[segs[1]] && segs.length > 2) {
      crumbs.push({ label: subMap[segs[1]], target: `${segs[0]}/${segs[1]}/index` })
    }
  }

  return crumbs
}

const MagazineArticleHero: QuartzComponent = ({ fileData, tree, allFiles }: QuartzComponentProps) => {
  const slug = fileData.slug ?? "index"
  if (slug === "index") {
    return null
  }

  const fm = (fileData.frontmatter ?? {}) as Record<string, any>
  const title = String(fm.title ?? slug)
  const description = fm.description ? String(fm.description) : null
  const status = String(fm.status ?? "verified")
  const lastVerified = fm.last_verified_date ? String(fm.last_verified_date) : "2026-10-27"
  const sources = Array.isArray(fm.sources) ? fm.sources : []

  const baseDir = pathToRoot(slug)
  const badges = getPageEditorialBadges(slug, fm)
  const breadcrumbs = getHeroBreadcrumbs(slug)

  const resolveRel = (target: string) => {
    const isIdx = target.endsWith("/index") || target === "index"
    const cleanT = target.replace(/\/index$/, "")
    const trail = isIdx ? "/" : ""
    if (cleanT === "" || cleanT === "index") {
      return baseDir === "." ? "./" : `${baseDir}/`
    }
    return baseDir === "." ? `./${cleanT}${trail}` : `${baseDir}/${cleanT}${trail}`
  }

  // Season Quick-Switcher for any page in 02-cronistoria/stagioni/YYYY-YYYY
  const seasonMatch = slug.match(/^02-cronistoria\/stagioni\/(\d{4}-\d{4})$/)
  const currentSeasonId = seasonMatch ? seasonMatch[1] : null
  let allSeasonIds: string[] = []
  let prevSeasonId: string | null = null
  let nextSeasonId: string | null = null

  if (currentSeasonId && allFiles) {
    const seasonSet = new Set<string>()
    for (const f of allFiles) {
      const m = f.slug?.match(/^02-cronistoria\/stagioni\/(\d{4}-\d{4})$/)
      if (m) seasonSet.add(m[1])
    }
    allSeasonIds = Array.from(seasonSet).sort((a, b) => a.localeCompare(b))
    const curIdx = allSeasonIds.indexOf(currentSeasonId)
    if (curIdx > 0) prevSeasonId = allSeasonIds[curIdx - 1]
    if (curIdx !== -1 && curIdx < allSeasonIds.length - 1) nextSeasonId = allSeasonIds[curIdx + 1]
  }

  // Primary source label
  const primarySourceLabel = sources[0]?.author
    ? `${String(sources[0].author).split(",")[0]} (${sources[0]?.year ?? ""})`
    : sources[0]?.title
      ? String(sources[0].title).slice(0, 32)
      : `${sources.length || 1} fonte verificata`

  // Verifica se il corpo dell'articolo contiene già un'immagine (<img>)
  let hasBodyImage = false
  if (tree) {
    visit(tree, "element", (node: any) => {
      if (node.tagName === "img") {
        hasBodyImage = true
      }
    })
  }

  // Se il body ha già la foto (o se non c'è una foto specifica per l'entità), nessun box foto in hero
  const media = hasBodyImage ? null : selectHeroMedia(slug, fm)
  const imgSrc = media
    ? baseDir === "."
      ? `./static/images/photos/${media.file}`
      : `${baseDir}/static/images/photos/${media.file}`
    : null
  const reportHref = baseDir === "." ? "./segnala-correzione" : `${baseDir}/segnala-correzione`

  return (
    <section class="nfc-article-hero" aria-label="Intestazione editoriale dell'articolo">
      {/* Top Row: Clickable Breadcrumbs + Split Editorial Badge */}
      <div class="nfc-article-hero__top-row">
        <nav class="nfc-hero-breadcrumbs" aria-label="Percorso di navigazione">
          {breadcrumbs.map((crumb, idx) => (
            <>
              {idx > 0 && (
                <span class="nfc-hero-breadcrumbs__sep" aria-hidden="true">
                  ›
                </span>
              )}
              <a href={resolveRel(crumb.target)} class="nfc-hero-breadcrumbs__link">
                {crumb.label}
              </a>
            </>
          ))}
        </nav>
        <div class="nfc-split-badge">
          <span class="nfc-split-badge__left">{badges.left}</span>
          <span class="nfc-split-badge__right">{badges.right}</span>
        </div>
      </div>

      {/* Season Quick-Switcher Bar (1-Click jump across all 95 seasons) */}
      {currentSeasonId && allSeasonIds.length > 0 && (
        <nav class="nfc-season-switcher" aria-label="Navigazione rapida tra le stagioni">
          {prevSeasonId ? (
            <a
              href={resolveRel(`02-cronistoria/stagioni/${prevSeasonId}`)}
              class="nfc-season-switcher__btn nfc-season-switcher__btn--prev"
              title={`Vai alla stagione precedente (${prevSeasonId})`}
            >
              ← {prevSeasonId}
            </a>
          ) : (
            <span class="nfc-season-switcher__btn is-disabled" aria-disabled="true">
              ← Inizio
            </span>
          )}

          <div class="nfc-season-switcher__select-wrap">
            <label htmlFor="nfc-season-select" class="sr-only">
              Seleziona stagione
            </label>
            <select
              id="nfc-season-select"
              class="nfc-season-switcher__select"
              aria-label="Salta direttamente a una stagione (1929–2026)"
              // @ts-ignore
              onchange="if(this.value) window.location.href = this.value;"
            >
              {[...allSeasonIds].reverse().map((sId) => (
                <option
                  value={resolveRel(`02-cronistoria/stagioni/${sId}`)}
                  selected={sId === currentSeasonId}
                >
                  Stagione {sId}
                </option>
              ))}
            </select>
          </div>

          {nextSeasonId ? (
            <a
              href={resolveRel(`02-cronistoria/stagioni/${nextSeasonId}`)}
              class="nfc-season-switcher__btn nfc-season-switcher__btn--next"
              title={`Vai alla stagione successiva (${nextSeasonId})`}
            >
              {nextSeasonId} →
            </a>
          ) : (
            <span class="nfc-season-switcher__btn is-disabled" aria-disabled="true">
              Oggi →
            </span>
          )}
        </nav>
      )}

      {/* Giant Condensed Headline (Big Shoulders Display) */}
      <h1 class="nfc-article-hero__title">{title}</h1>

      {/* Editorial Deck / Standfirst */}
      {description && <p class="nfc-article-hero__deck">{description}</p>}

      {/* Micro-riga minimale salva-spazio (Opzione B approvata) */}
      <div class="nfc-article-hero__meta-inline">
        {status === "verified" ? (
          <span class="nfc-meta-pill nfc-meta-pill--verified" title="Dati e fonti archivistici verificati">
            <span class="nfc-meta-pill__check" aria-hidden="true">✓</span> Dossier Verificato
          </span>
        ) : (
          <span class="nfc-meta-pill nfc-meta-pill--draft">
            Revisione in corso
          </span>
        )}
        <span class="nfc-meta-sep">·</span>
        <span class="nfc-meta-inline-item">
          <span class="nfc-meta-inline-label">Revisione:</span> {lastVerified}
        </span>
        <span class="nfc-meta-sep">·</span>
        <span class="nfc-meta-inline-item">
          <span class="nfc-meta-inline-label">Fonti:</span> {primarySourceLabel}
        </span>
        <span class="nfc-meta-sep">·</span>
        <a href={`${reportHref}?page=${encodeURIComponent(slug)}`} class="nfc-meta-inline-action">
          ✎ Segnala correzione →
        </a>
      </div>

      {/* Magazine Editorial Cover Photograph Frame — SOLO se media esiste ed è contestuale */}
      {media && imgSrc && (
        <figure
          class={`nfc-article-hero__figure nfc-article-hero__figure--${media.aspect ?? "wide"}`}
        >
          <div class="nfc-article-hero__img-wrap">
            <img
              src={imgSrc}
              alt={media.caption}
              loading="eager"
              class={`nfc-article-hero__img ${media.fit === "contain" ? "is-contain" : ""}`}
            />
          </div>
          <figcaption class="nfc-article-hero__caption">
            <span class="nfc-article-hero__caption-text">{media.caption}</span>
            <span class="nfc-article-hero__caption-credit">{media.credit}</span>
          </figcaption>
        </figure>
      )}
    </section>
  )
}

export default (() => MagazineArticleHero) satisfies QuartzComponentConstructor
