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
    href: "./02-cronistoria/stagioni/2023-2024",
    image: "./static/images/photos/catania-fc-match-cibali.jpg",
    credit: "Foto: SonoGrazy (CC BY-SA 4.0)",
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
    href: "./vicende-legali/decreto-2-febbraio-2007",
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
    href: "./vicende-legali/fallimento-2021-art52-noif",
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
    href: "./stadio/piazza-esposizione",
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
    href: "./societa/presidenti/ignazio-marcoccio",
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
    href: "./tesserati/calciatori/marco-biagianti",
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
    href: "./tesserati/calciatori/giuseppe-mascara",
    image: "./static/images/photos/mascara-tifosi.jpg",
  },
  {
    id: "marco-biagianti",
    name: "Marco Biagianti",
    role: "CAPITANO · 2007–2020",
    stat: "284 PRES · RECORD A",
    href: "./tesserati/calciatori/marco-biagianti",
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

  // Batch 2 (Campioni, Condottieri e Rinascite)
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
    href: "./tesserati/calciatori/gionatha-spinesi",
    image: "./static/images/photos/mascara-spinesi.jpg",
  },

  // Batch 3 (Registi, Protagonisti del ciclo A e Presidenti storici)
  {
    id: "maxi-lopez",
    name: "Maxi López",
    role: "ATTACCANTE · 2010–2014",
    stat: "70 PRES · 27 GOL",
    href: "./tesserati/calciatori/maxi-lopez",
    image: "./static/images/photos/maxi-lopez.jpg",
  },
  {
    id: "mariano-izco",
    name: "Mariano Julio Izco",
    role: "CENTROCAMPISTA · 2006–2014",
    stat: "280 PRES · 8 ANNI A",
    href: "./tesserati/calciatori/mariano-izco",
    image: "./static/images/photos/mariano-izco.jpg",
  },
  {
    id: "pablo-barrientos",
    name: "Pablo Barrientos",
    role: "TREQUARTISTA · 2011–2014",
    stat: "86 PRES · 14 GOL",
    href: "./tesserati/calciatori/pablo-barrientos",
    image: "./static/images/photos/pablo-barrientos.jpg",
  },
  {
    id: "rolando-maran",
    name: "Rolando Maran",
    role: "ALLENATORE · 2012–2014",
    stat: "56 PT · 8° IN SERIE A",
    href: "./tesserati/allenatori/rolando-maran",
    image: "./static/images/photos/rolando-maran.jpg",
  },
  {
    id: "gianni-di-marzio",
    name: "Gianni Di Marzio",
    role: "ALLENATORE · 1982–1984",
    stat: "SPAREGGI ROMA 1983",
    href: "./tesserati/allenatori/gianni-di-marzio",
    image: "./static/images/photos/gianni-di-marzio.jpg",
  },
  {
    id: "ignazio-marcoccio",
    name: "Ignazio Marcoccio",
    role: "PRESIDENTE · 1959–1969",
    stat: "SERIE A D'ORO",
    href: "./societa/presidenti/ignazio-marcoccio",
    image: "./static/images/photos/szymaniak-marcoccio.jpg",
  },
  {
    id: "walter-zenga",
    name: "Walter Zenga",
    role: "ALLENATORE · 2008–2009",
    stat: "SALVEZZA A · DERBY 0-4",
    href: "./tesserati/allenatori/walter-zenga",
    image: "./static/images/photos/walter-zenga.jpg",
  },
  {
    id: "vincenzo-montella",
    name: "Vincenzo Montella",
    role: "ALLENATORE · 2011–2012",
    stat: "48 PT · BEL GIOCO A",
    href: "./tesserati/allenatori/vincenzo-montella",
    image: "./static/images/photos/vincenzo-montella.jpg",
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
    figures: "Rosario Pelligra, V. Grella, M. Zeoli",
    event: "Rinascita ex Art. 52 NOIF, trionfo in Serie D (88 pt), 1ª Coppa Italia Serie C (2024) e riacquisto logo.",
    href: "./01-societa/epoche/2022-pelligra-catania-fc",
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


  return (
    <div class="nfc-home">
      {/* 1. HERO COPERTINA STILE NO FOOTBALL COLORS */}
      <section class="nfc-hero-cover" aria-label="Copertina del Magazine Wiki Catania Calcio">
        <div class="nfc-hero-cover__bg">
          <img
            src="./static/images/photos/curva-nord-coreografia.jpg"
            alt="Stadio Angelo Massimino illuminato durante una gara notturna del Catania con coreografia rossazzurra"
            loading="eager"
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
            Il magazine enciclopedico indipendente dedicato alla memoria agonistica, giurisprudenziale,
            araldica e sociale del calcio catanese. Ottantasette dossier certificati, classifiche
            verificate algebricamente e fonti primarie controllate.
          </p>

          <div class="nfc-hero-cover__ctas">
            <a href="#storie-in-copertina" class="nfc-double-btn nfc-double-btn--primary">
              <span class="nfc-double-btn__inner">
                <span class="nfc-double-btn__square" aria-hidden="true" />
                <span>SFOGLIA IL MAGAZINE</span>
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
          <div class="nfc-number-cell">
            <span class="nfc-number-cell__kicker">FONDAZIONE</span>
            <span class="nfc-number-cell__digits">1929</span>
            <span class="nfc-number-cell__desc">
              Dalla Società Sportiva Catania di Piazza Esposizione all'attuale Catania Football Club.
            </span>
          </div>
          <div class="nfc-number-cell">
            <span class="nfc-number-cell__kicker">MASSIMA SERIE</span>
            <span class="nfc-number-cell__digits">17</span>
            <span class="nfc-number-cell__desc">
              Campionati di Serie A disputati tra il debutto del 1954-55 e gli otto tornei consecutivi 2006–2014.
            </span>
          </div>
          <div class="nfc-number-cell">
            <span class="nfc-number-cell__kicker">RECORD STORICO A</span>
            <span class="nfc-number-cell__digits">56 PT</span>
            <span class="nfc-number-cell__desc">
              L'ottavo posto della stagione 2012-2013 con 15 vittorie in Serie A sotto la guida di Rolando Maran.
            </span>
          </div>
          <div class="nfc-number-cell">
            <span class="nfc-number-cell__kicker">OLIMPICO 1983</span>
            <span class="nfc-number-cell__digits">40.000</span>
            <span class="nfc-number-cell__desc">
              Catanesi in trasferta a Roma il 25 giugno 1983: il più grande esodo sportivo nella storia d'Italia.
            </span>
          </div>
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
    shuffleStories();
    shufflePortraits();

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
