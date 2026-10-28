import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const NAV_ITEMS = [
  { num: "01", label: "Società", slug: "01-societa/index", prefix: "01-societa" },
  { num: "02", label: "Cronistoria", slug: "02-cronistoria/index", prefix: "02-cronistoria" },
  { num: "03", label: "Tesserati", slug: "03-tesserati/index", prefix: "03-tesserati" },
  { num: "04", label: "Strutture", slug: "04-strutture/index", prefix: "04-strutture" },
  { num: "05", label: "Simboli", slug: "05-identita-e-simboli/index", prefix: "05-identita-e-simboli" },
  { num: "06", label: "Tifoseria", slug: "06-tifoseria-e-cultura/index", prefix: "06-tifoseria-e-cultura" },
  { num: "07", label: "Media", slug: "07-media-e-comunicazione/index", prefix: "07-media-e-comunicazione" },
  { num: "08", label: "Paralleli", slug: "08-settori-paralleli/index", prefix: "08-settori-paralleli" },
]

const MagazineTopBar: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const currentSlug = fileData.slug ?? "index"
  const baseDir = pathToRoot(currentSlug)

  const resolveHref = (target: string) => {
    const isIndex = target.endsWith("/index") || target === "index"
    const cleanTarget = target.replace(/\/index$/, "")
    const trailing = isIndex ? "/" : ""
    if (baseDir === ".") {
      return `./${cleanTarget}${trailing}`
    }
    return `${baseDir}/${cleanTarget}${trailing}`
  }

  const homeHref = baseDir === "." ? "./" : `${baseDir}/`

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

        {/* Cella 2: Navigazione editoriale numerata stile Sincro + No Football Colors */}
        <nav class="nfc-masthead__nav" aria-label="Rubriche del Magazine">
          {NAV_ITEMS.map((item) => {
            const isActive =
              currentSlug === item.slug || currentSlug.startsWith(`${item.prefix}/`)
            return (
              <a
                href={resolveHref(item.slug)}
                class={`nfc-nav-cell ${isActive ? "is-active" : ""}`}
                aria-current={isActive ? "page" : undefined}
              >
                <span class="nfc-nav-cell__num">{item.num}</span>
                <span class="nfc-nav-cell__label">{item.label}</span>
              </a>
            )
          })}
        </nav>

        {/* Cella 3: Issue Tag & Ultimo Aggiornamento Certificato */}
        <div class="nfc-masthead__actions">
          <div class="nfc-issue-pill" aria-label="Edizione Archivio Certificato">
            <span class="nfc-issue-pill__left">ISSUE</span>
            <span class="nfc-issue-pill__right">1929–2026</span>
          </div>
          <div class="nfc-update-meta" title="Data e ora dell'ultimo aggiornamento del vault di Wiki Catania Calcio">
            <span class="nfc-update-meta__dot" aria-hidden="true" />
            <span class="nfc-update-meta__text">
              {new Intl.DateTimeFormat("it-IT", {
                day: "numeric",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              }).format(new Date())}
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default (() => MagazineTopBar) satisfies QuartzComponentConstructor
