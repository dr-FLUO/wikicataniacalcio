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

function getRubricLabel(slug: string, entityType: string): { left: string; right: string } {
  if (slug.startsWith("stagioni/")) {
    return { left: "RUBRICA 02 · STAGIONI", right: entityType === "season" ? "ANNALE UFFICIALE" : "INDICE GENERALE" }
  }
  if (slug.startsWith("societa/")) {
    return { left: "RUBRICA 01 · SOCIETÀ", right: slug.includes("presidenti/") ? "PROFILO PRESIDENZIALE" : "ERA SOCIETARIA" }
  }
  if (slug.startsWith("partite/")) {
    return { left: "RUBRICA 03 · PARTITE", right: slug.includes("precedenti/") ? "ARCHIVIO PRECEDENTI" : "TABELLINO STORICO" }
  }
  if (slug.startsWith("vicende-legali/")) {
    return { left: "RUBRICA 04 · DIRITTO SPORTIVO", right: "DOSSIER GIURISPRUDENZIALE" }
  }
  if (slug.startsWith("tesserati/")) {
    return { left: "RUBRICA 05 · HALL OF FAME", right: slug.includes("allenatori/") ? "PROFILO ALLENATORE" : "PROFILO CALCIATORE" }
  }
  if (slug.startsWith("stadio/")) {
    return { left: "RUBRICA 06 · ARCHITETTURA & STADI", right: "IMPIANTO STORICO" }
  }
  if (slug.startsWith("maglie/")) {
    return { left: "RUBRICA 07 · ESTETICA & MAGLIE", right: "ARALDICA ROSSAZZURRA" }
  }
  if (slug.startsWith("tifoseria/")) {
    return { left: "RUBRICA 08 · CULTURA ULTRAS", right: "ETNOGRAFIA DELLE CURVE" }
  }
  return { left: "REDAZIONE WIKI CATANIA CALCIO", right: "DOSSIER UFFICIALE" }
}

const MagazineArticleHero: QuartzComponent = ({ fileData, tree }: QuartzComponentProps) => {
  const slug = fileData.slug ?? "index"
  if (slug === "index") {
    return null
  }

  const fm = fileData.frontmatter ?? {}
  const title = String(fm.title ?? slug)
  const description = fm.description ? String(fm.description) : null
  const entityType = String(fm.entity_type ?? "article")
  const status = String(fm.status ?? "verified")
  const lastVerified = fm.last_verified_date ? String(fm.last_verified_date) : "2026-10-27"
  const sources = Array.isArray(fm.sources) ? fm.sources : []

  const baseDir = pathToRoot(slug)
  const rubric = getRubricLabel(slug, entityType)

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
      {/* Top Badge stile No Football Colors */}
      <div class="nfc-article-hero__top-row">
        <div class="nfc-split-badge">
          <span class="nfc-split-badge__left">{rubric.left}</span>
          <span class="nfc-split-badge__right">{rubric.right}</span>
        </div>

        {status === "verified" && (
          <div class="nfc-verified-tag" title={`Fonti verificate il ${lastVerified}`}>
            <span class="nfc-verified-tag__dot" aria-hidden="true" />
            <span>DOSSIER CERTIFICATO ({sources.length || 1} FONTI)</span>
          </div>
        )}
      </div>

      {/* Giant Condensed Headline (Big Shoulders Display) */}
      <h1 class="nfc-article-hero__title">{title}</h1>

      {/* Editorial Deck / Standfirst */}
      {description && <p class="nfc-article-hero__deck">{description}</p>}

      {/* Sincro-style Architectural Metadata Strip */}
      <div class="nfc-article-hero__meta-grid">
        <div class="nfc-meta-cell">
          <span class="nfc-meta-cell__label">REDAZIONE</span>
          <span class="nfc-meta-cell__val">Wiki Catania Calcio</span>
        </div>
        <div class="nfc-meta-cell">
          <span class="nfc-meta-cell__label">VERIFICA STORICA</span>
          <span class="nfc-meta-cell__val">{lastVerified}</span>
        </div>
        <div class="nfc-meta-cell">
          <span class="nfc-meta-cell__label">FONTE PRIMARIA</span>
          <span class="nfc-meta-cell__val">
            {sources[0]?.author
              ? `${String(sources[0].author).split(",")[0]} (${sources[0]?.year ?? ""})`
              : "Archivio Storico Rossazzurro"}
          </span>
        </div>
        <div class="nfc-meta-cell nfc-meta-cell--action">
          <a href={`${reportHref}?page=${encodeURIComponent(slug)}`} class="nfc-meta-link">
            ✎ Segnala correzione o fonte →
          </a>
        </div>
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
