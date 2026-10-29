import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// Componenti condivisi su tutte le pagine di Wiki Catania Calcio
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [Component.MagazineTopBar(), Component.Search(), Component.Darkmode()],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "Contratto Dati (SCHEMA.md)": "https://github.com/wikicalciocatania/wiki",
    },
  }),
}

// Explorer compatto ed editoriale per la navigazione archivistica
const editorialExplorer = Component.Explorer({
  title: "Archivio Dossier",
  folderClickBehavior: "link",
  folderDefaultState: "collapsed",
  useSavedState: false,
  filterFn: (node) => {
    if (node.slugSegment === "tags" || node.slugSegment === "index") return false
    // Mantiene il nodo 'archivio' come portale unico, ma esclude tutti i sotto-cluster A-Z e i 1.400+ file foglia
    // dalla sidebar sinistra, per garantire un albero di navigazione ultra-pulito, leggero e immediato.
    if (
      node.slug &&
      node.slugSegment !== "archivio" &&
      (node.slug.includes("archivio/") ||
        node.slugSegment === "a-c" ||
        node.slugSegment === "d-f" ||
        node.slugSegment === "g-l" ||
        node.slugSegment === "m-o" ||
        node.slugSegment === "p-r" ||
        node.slugSegment === "s-z")
    ) {
      return false
    }
    return true
  },
  mapFn: (node) => {
    const folderMap: Record<string, string> = {
      "01-societa": "01 · Società",
      "02-cronistoria": "02 · Cronistoria",
      "03-tesserati": "03 · Tesserati",
      "04-strutture": "04 · Strutture",
      "05-identita-e-simboli": "05 · Simboli & Identità",
      "06-tifoseria-e-cultura": "06 · Tifoseria & Cultura",
      "07-media-e-comunicazione": "07 · Media & Informazione",
      "08-settori-paralleli": "08 · Settori Paralleli",
      "epoche": "Epoche Societarie",
      "presidenti": "Presidenti",
      "dirigenti": "Dirigenti",
      "vicende-legali": "Diritto & Giustizia",
      "stagioni": "Stagioni (1929–2027)",
      "partite-storiche": "Partite Storiche",
      "allenatori": "Allenatori",
      "calciatori": "Calciatori",
      "rosa-attuale": "Rosa Attuale (2026–2027)",
      "storici": "Calciatori Storici",
      "archivio": "Archivio Tesserati (Filtri A–Z)",
      "a-c": "Lettere A–C",
      "d-f": "Lettere D–F",
      "g-l": "Lettere G–L",
      "m-o": "Lettere M–O",
      "p-r": "Lettere P–R",
      "s-z": "Lettere S–Z",
      "stadio-massimino": "Stadio Massimino",
      "centri-sportivi": "Centri Sportivi",
      "campi-storici": "Campi Storici",
      "maglie": "Maglie e Divise",
      "araldica-e-scudetti": "Araldica e Scudetti",
      "sponsor": "Sponsor Commerciali",
      "curve": "Curve Cibali",
      "curva-nord": "Curva Nord",
      "curva-sud": "Curva Sud",
      "eventi-e-giustizia": "Eventi & Giustizia",
      "biografie": "Biografie Ultras",
      "relazioni": "Gemellaggi e Rivalità",
      "gemellaggi": "Gemellaggi",
      "rivalita": "Rivalità",
      "testate": "Testate Storiche",
      "firme-e-voci": "Firme & Giornalisti",
      "letteratura": "Letteratura & Saggi Storici",
      "giovanili": "Settore Giovanile",
      "women": "Catania Women",
      "precedenti": "Precedenti",
    }
    if (node.isFolder) {
      const seg = node.slugSegment
      if (folderMap[seg]) {
        node.displayName = folderMap[seg]
      }
    } else {
      const fileTitleMap: Record<string, string> = {
        "lo-scudetto-1978-della-jolly-componibili": "Scudetto 1978 (Jolly)",
        "dipartimento-catania-women": "Catania Women (Serie C)",
        "albo-doro-e-torneo-di-viareggio": "Torneo di Viareggio",
        "talenti-e-cantera-rossazzurra": "Cantera & Talenti",
        "grandi-opere-e-almanacchi": "Grandi Opere & Almanacchi",
        "saggi-e-biografie": "Saggi & Biografie",
      }
      if (node.slugSegment && fileTitleMap[node.slugSegment]) {
        node.displayName = fileTitleMap[node.slugSegment]
        return
      }
      if (node.slug === "note-legali-privacy-accessibilita") {
        node.displayName = "Note Legali & Privacy"
        return
      }
      if (node.slug === "segnala-correzione") {
        node.displayName = "Segnala Correzione"
        return
      }
      if (node.slug && node.slug.includes("stagioni/")) {
        const m = node.slug.match(/\d{4}-\d{4}/)
        if (m) {
          node.displayName = m[0]
          return
        }
      }
      if (node.displayName) {
        const parts = node.displayName.split(" — ")
        if (parts.length > 1 && parts[0].length >= 6 && parts[0].length <= 32) {
          node.displayName = parts[0].replace(/^[«"]|[»"]$/g, "").trim()
        } else if (node.displayName.length > 30) {
          node.displayName = node.displayName.substring(0, 28) + "…"
        }
      }
    }
  },
  sortFn: (a, b) => {
    if (a.isFolder && !b.isFolder) return -1
    if (!a.isFolder && b.isFolder) return 1
    // Ordine inverso per le stagioni: dalla più recente alla più vecchia
    const isSeasonA = /^\d{4}-\d{4}$/.test(a.displayName)
    const isSeasonB = /^\d{4}-\d{4}$/.test(b.displayName)
    if (isSeasonA && isSeasonB) {
      return b.displayName.localeCompare(a.displayName, undefined, {
        numeric: true,
        sensitivity: "base",
      })
    }
    return a.displayName.localeCompare(b.displayName, undefined, {
      numeric: true,
      sensitivity: "base",
    })
  },
})

// Layout Magazine per la Homepage e per i singoli Dossier
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.MagazineHome(),
    Component.MagazineArticleHero(),
    Component.TesseratiArchive(),
  ],
  afterBody: [
    Component.ConditionalRender({
      component: Component.TagList(),
      condition: (page) => page.fileData.slug !== "index",
    }),
  ],
  left: [editorialExplorer],
  right: [
    Component.RossazzurriInfobox(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Graph({
      localGraph: {
        depth: 1,
        scale: 1.1,
        repelForce: 0.5,
        centerForce: 0.3,
        linkDistance: 30,
        fontSize: 0.6,
        opacityScale: 1,
      },
      globalGraph: {
        depth: -1,
        scale: 0.9,
        repelForce: 0.5,
        centerForce: 0.3,
        linkDistance: 30,
        fontSize: 0.6,
        opacityScale: 1,
      },
    }),
    Component.Backlinks(),
  ],
}

// Layout per le pagine indice automatiche di cartella o tag
export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TesseratiArchive(),
  ],
  left: [editorialExplorer],
  right: [Component.Graph()],
}
