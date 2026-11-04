import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
// @ts-ignore
import topbarScript from "./scripts/topbar.inline"

interface SubNavItem {
  label: string
  slug: string
  matchPrefix?: string
}

interface NavItem {
  num: string
  label: string
  slug: string
  prefix: string
  subItems: SubNavItem[]
}

const NAV_ITEMS: NavItem[] = [
  {
    num: "01",
    label: "Società",
    slug: "01-societa/index",
    prefix: "01-societa",
    subItems: [
      { label: "Epoche Societarie", slug: "01-societa/epoche/index", matchPrefix: "01-societa/epoche" },
      { label: "Presidenti", slug: "01-societa/presidenti/index", matchPrefix: "01-societa/presidenti" },
      { label: "Dirigenti & DS", slug: "01-societa/dirigenti/index", matchPrefix: "01-societa/dirigenti" },
      { label: "Diritto & Giustizia", slug: "01-societa/vicende-legali/index", matchPrefix: "01-societa/vicende-legali" },
    ],
  },
  {
    num: "02",
    label: "Cronistoria",
    slug: "02-cronistoria/index",
    prefix: "02-cronistoria",
    subItems: [
      { label: "Stagioni (1929–2026)", slug: "02-cronistoria/stagioni/index", matchPrefix: "02-cronistoria/stagioni" },
      { label: "Partite Storiche", slug: "02-cronistoria/partite-storiche/index", matchPrefix: "02-cronistoria/partite-storiche" },
      { label: "Precedenti & Derby", slug: "02-cronistoria/partite-storiche/precedenti/index", matchPrefix: "02-cronistoria/partite-storiche/precedenti" },
    ],
  },
  {
    num: "03",
    label: "Tesserati",
    slug: "03-tesserati/index",
    prefix: "03-tesserati",
    subItems: [
      { label: "Archivio Calciatori A–Z", slug: "03-tesserati/calciatori/archivio/index", matchPrefix: "03-tesserati/calciatori/archivio" },
      { label: "Leggende & Storici", slug: "03-tesserati/calciatori/storici/index", matchPrefix: "03-tesserati/calciatori/storici" },
      { label: "Rosa Attuale", slug: "03-tesserati/calciatori/rosa-attuale/index", matchPrefix: "03-tesserati/calciatori/rosa-attuale" },
      { label: "Allenatori (1929–2026)", slug: "03-tesserati/allenatori/index", matchPrefix: "03-tesserati/allenatori" },
    ],
  },
  {
    num: "04",
    label: "Strutture",
    slug: "04-strutture/index",
    prefix: "04-strutture",
    subItems: [
      { label: "Stadio Massimino", slug: "04-strutture/stadio-massimino/index", matchPrefix: "04-strutture/stadio-massimino" },
      { label: "Torre del Grifo", slug: "04-strutture/centri-sportivi/torre-del-grifo", matchPrefix: "04-strutture/centri-sportivi" },
      { label: "Campi Storici (1910–1937)", slug: "04-strutture/campi-storici/index", matchPrefix: "04-strutture/campi-storici" },
    ],
  },
  {
    num: "05",
    label: "Simboli",
    slug: "05-identita-e-simboli/index",
    prefix: "05-identita-e-simboli",
    subItems: [
      { label: "Stemmi & Liotru", slug: "05-identita-e-simboli/araldica-e-scudetti/index", matchPrefix: "05-identita-e-simboli/araldica-e-scudetti" },
      { label: "Divise & Maglie Storiche", slug: "05-identita-e-simboli/maglie-e-divise", matchPrefix: "05-identita-e-simboli/maglie-e-divise" },
      { label: "Sponsor Ufficiali", slug: "05-identita-e-simboli/sponsor/index", matchPrefix: "05-identita-e-simboli/sponsor" },
      { label: "Mascotte & Inni", slug: "05-identita-e-simboli/mascotte-e-inni", matchPrefix: "05-identita-e-simboli/mascotte" },
    ],
  },
  {
    num: "06",
    label: "Tifoseria",
    slug: "06-tifoseria-e-cultura/index",
    prefix: "06-tifoseria-e-cultura",
    subItems: [
      { label: "Curva Nord", slug: "06-tifoseria-e-cultura/settori/curva-nord/index", matchPrefix: "06-tifoseria-e-cultura/settori/curva-nord" },
      { label: "Curva Sud", slug: "06-tifoseria-e-cultura/settori/curva-sud/index", matchPrefix: "06-tifoseria-e-cultura/settori/curva-sud" },
      { label: "Tribuna B", slug: "06-tifoseria-e-cultura/settori/tribuna-b/index", matchPrefix: "06-tifoseria-e-cultura/settori/tribuna-b" },
      { label: "Gemellaggi & Amicizie", slug: "06-tifoseria-e-cultura/relazioni/gemellaggi/index", matchPrefix: "06-tifoseria-e-cultura/relazioni/gemellaggi" },
      { label: "Rivalità & Derby", slug: "06-tifoseria-e-cultura/relazioni/rivalita/index", matchPrefix: "06-tifoseria-e-cultura/relazioni/rivalita" },
      { label: "Biografie & Cronache", slug: "06-tifoseria-e-cultura/biografie/index", matchPrefix: "06-tifoseria-e-cultura/biografie" },
      { label: "Eventi & Giustizia", slug: "06-tifoseria-e-cultura/eventi-e-giustizia/index", matchPrefix: "06-tifoseria-e-cultura/eventi-e-giustizia" },
    ],
  },
  {
    num: "07",
    label: "Media",
    slug: "07-media-e-comunicazione/index",
    prefix: "07-media-e-comunicazione",
    subItems: [
      { label: "Testate & TV", slug: "07-media-e-comunicazione/testate/index", matchPrefix: "07-media-e-comunicazione/testate" },
      { label: "Firme & Voci", slug: "07-media-e-comunicazione/firme-e-voci/index", matchPrefix: "07-media-e-comunicazione/firme-e-voci" },
      { label: "Libri & Almanacchi", slug: "07-media-e-comunicazione/letteratura/index", matchPrefix: "07-media-e-comunicazione/letteratura" },
      { label: "Cinema & TV", slug: "07-media-e-comunicazione/cinema-e-tv/index", matchPrefix: "07-media-e-comunicazione/cinema-e-tv" },
    ],
  },
  {
    num: "08",
    label: "Vivaio & Women",
    slug: "08-settori-paralleli/index",
    prefix: "08-settori-paralleli",
    subItems: [
      { label: "Settore Giovanile & Viareggio", slug: "08-settori-paralleli/giovanili/index", matchPrefix: "08-settori-paralleli/giovanili" },
      { label: "Catania Women & Jolly '78", slug: "08-settori-paralleli/women/index", matchPrefix: "08-settori-paralleli/women" },
    ],
  },
]

const MagazineTopBar: QuartzComponent = ({ cfg, fileData }: QuartzComponentProps) => {
  const currentSlug = fileData.slug ?? "index"
  const baseDir = pathToRoot(currentSlug)
  const url = new URL(`https://${cfg.baseUrl ?? "example.com"}`)
  const basePrefix = url.pathname.replace(/\/$/, "")

  const resolveHref = (target: string) => {
    const isIndex = target.endsWith("/index") || target === "index"
    const cleanTarget = target.replace(/\/index$/, "")
    const trailing = isIndex ? "/" : ""
    if (currentSlug === "404") {
      return basePrefix ? `${basePrefix}/${cleanTarget}${trailing}` : `/${cleanTarget}${trailing}`
    }
    if (baseDir === ".") {
      return `./${cleanTarget}${trailing}`
    }
    return `${baseDir}/${cleanTarget}${trailing}`
  }

  const homeHref =
    currentSlug === "404"
      ? basePrefix
        ? `${basePrefix}/`
        : "/"
      : baseDir === "."
        ? "./"
        : `${baseDir}/`

  const activeNav = NAV_ITEMS.find(
    (item) => currentSlug === item.slug || currentSlug.startsWith(`${item.prefix}/`),
  )

  return (
    <header class="nfc-masthead" role="banner" aria-label="Testata editoriale Wiki Catania Calcio">
      <a href="#main-article-content" class="skip-to-content">
        Salta al contenuto principale
      </a>
      <div class="nfc-masthead__grid">
        {/* Cella 1: Brand Box editoriale in stile No Football Colors */}
        <div class="nfc-masthead__brand-cell">
          <a
            href={homeHref}
            class="nfc-brand-box"
            aria-label="Wiki Catania Calcio — Torna alla copertina del Magazine"
          >
            <span class="nfc-brand-box__text">
              <span class="nfc-brand-box__kicker">ARCHIVIO STORICO · DAL 1929</span>
              <span class="nfc-brand-box__title">WIKI CATANIA CALCIO</span>
            </span>
          </a>
        </div>

        {/* Cella 2: Navigazione editoriale numerata con accesso 1-Click al 2° livello */}
        <nav class="nfc-masthead__nav" aria-label="Rubriche del Magazine">
          {NAV_ITEMS.map((item) => {
            const isActive =
              currentSlug === item.slug || currentSlug.startsWith(`${item.prefix}/`)
            return (
              <div class={`nfc-nav-item-wrap ${isActive ? "is-active-wrap" : ""}`}>
                <a
                  href={resolveHref(item.slug)}
                  class={`nfc-nav-cell ${isActive ? "is-active" : ""}`}
                  aria-current={isActive ? "page" : undefined}
                  aria-haspopup={item.subItems.length > 0 ? "true" : undefined}
                  aria-expanded={item.subItems.length > 0 ? "false" : undefined}
                >
                  <span class="nfc-nav-cell__num">{item.num}</span>
                  <span class="nfc-nav-cell__label">
                    {item.num === "08" ? (
                      <>
                        <span class="nfc-label-main">Vivaio</span>
                        <span class="nfc-label-extra"> & Women</span>
                      </>
                    ) : (
                      item.label
                    )}
                  </span>
                </a>
                {item.subItems.length > 0 && (
                  <div class="nfc-nav-dropdown" role="menu" aria-label={`Sottosezioni ${item.label}`}>
                    <div class="nfc-nav-dropdown__header">
                      <span>{item.num} · {item.label.toUpperCase()}</span>
                      <a href={resolveHref(item.slug)} class="nfc-nav-dropdown__all">
                        Indice sezione →
                      </a>
                    </div>
                    <div class="nfc-nav-dropdown__links">
                      {item.subItems.map((sub) => {
                        const isSubActive =
                          currentSlug === sub.slug ||
                          (sub.matchPrefix && currentSlug.startsWith(sub.matchPrefix))
                        return (
                          <a
                            href={resolveHref(sub.slug)}
                            role="menuitem"
                            class={`nfc-nav-dropdown__link ${isSubActive ? "is-active" : ""}`}
                          >
                            {sub.label}
                          </a>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </nav>

        {/* Cella 3: Issue Tag & Versione */}
        <div class="nfc-masthead__actions">
          <div class="nfc-issue-pill" aria-label="Edizione Archivio Certificato">
            <span class="nfc-issue-pill__left">ISSUE</span>
            <span class="nfc-issue-pill__right">1929–2026</span>
          </div>
          <div class="nfc-beta-version" title="Versione di sviluppo attivo del vault">
            <span class="nfc-beta-version__text">BETA 1.2</span>
          </div>
        </div>
      </div>

      {/* Sub-Bar Contestuale di 2° Livello (visibile quando si naviga dentro una rubrica) */}
      {activeNav && activeNav.subItems.length > 0 && (
        <nav
          class="nfc-subbar"
          aria-label={`Navigazione rapida sezione ${activeNav.label}`}
        >
          <div class="nfc-subbar__inner">
            <a href={resolveHref(activeNav.slug)} class="nfc-subbar__section-tag">
              <span class="nfc-subbar__num">{activeNav.num}</span>
              <span>{activeNav.label.toUpperCase()}</span>
            </a>
            <span class="nfc-subbar__sep" aria-hidden="true">›</span>
            <div class="nfc-subbar__links">
              {activeNav.subItems.map((sub) => {
                // Evita falso positivo di 'partite-storiche' quando siamo in 'partite-storiche/precedenti'
                const isPrecedenti = currentSlug.includes("partite-storiche/precedenti")
                const isSubActive =
                  currentSlug === sub.slug ||
                  (sub.matchPrefix &&
                    currentSlug.startsWith(sub.matchPrefix) &&
                    !(sub.matchPrefix === "02-cronistoria/partite-storiche" && isPrecedenti))
                return (
                  <a
                    href={resolveHref(sub.slug)}
                    class={`nfc-subbar__pill ${isSubActive ? "is-active" : ""}`}
                    aria-current={isSubActive ? "page" : undefined}
                  >
                    {sub.label}
                  </a>
                )
              })}
            </div>
          </div>
        </nav>
      )}
    </header>
  )
}

MagazineTopBar.afterDOMLoaded = topbarScript

export default (() => MagazineTopBar) satisfies QuartzComponentConstructor
