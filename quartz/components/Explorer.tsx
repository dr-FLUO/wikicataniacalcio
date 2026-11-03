import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/explorer.scss"

// @ts-ignore
import script from "./scripts/explorer.inline"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"
import { FileTrieNode } from "../util/fileTrie"
import OverflowListFactory from "./OverflowList"
import { concatenateResources } from "../util/resources"

type OrderEntries = "sort" | "filter" | "map"

export interface Options {
  title?: string
  folderDefaultState: "collapsed" | "open"
  folderClickBehavior: "collapse" | "link"
  useSavedState: boolean
  sortFn: (a: FileTrieNode, b: FileTrieNode) => number
  filterFn: (node: FileTrieNode) => boolean
  mapFn: (node: FileTrieNode) => void
  order: OrderEntries[]
}

const defaultOptions: Options = {
  folderDefaultState: "collapsed",
  folderClickBehavior: "collapse",
  useSavedState: true,
  mapFn: (node) => {
    return node
  },
  sortFn: (a, b) => {
    if ((!a.isFolder && !b.isFolder) || (a.isFolder && b.isFolder)) {
      return a.displayName.localeCompare(b.displayName, undefined, {
        numeric: true,
        sensitivity: "base",
      })
    }

    if (!a.isFolder && b.isFolder) {
      return 1
    } else {
      return -1
    }
  },
  filterFn: (node) => node.slugSegment !== "tags",
  order: ["filter", "map", "sort"],
}

export type FolderState = {
  path: string
  collapsed: boolean
}

let numExplorers = 0
export default ((userOpts?: Partial<Options>) => {
  const opts: Options = { ...defaultOptions, ...userOpts }
  const { OverflowList, overflowListAfterDOMLoaded } = OverflowListFactory()

  const Explorer: QuartzComponent = ({ cfg, displayClass }: QuartzComponentProps) => {
    const id = `explorer-${numExplorers++}`

    return (
      <div
        class={classNames(displayClass, "explorer")}
        data-behavior={opts.folderClickBehavior}
        data-collapsed={opts.folderDefaultState}
        data-savestate={opts.useSavedState}
        data-data-fns={JSON.stringify({
          order: opts.order,
          sortFn: opts.sortFn.toString(),
          filterFn: opts.filterFn.toString(),
          mapFn: opts.mapFn.toString(),
        })}
      >
        <button
          type="button"
          class="explorer-toggle mobile-explorer hide-until-loaded"
          data-mobile={true}
          aria-controls={id}
          aria-label="Apri archivio dossier"
        >
          <span class="mobile-explorer-left">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              stroke-width="2.2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide-menu"
              aria-hidden="true"
            >
              <line x1="4" y1="12" x2="20" y2="12" />
              <line x1="4" y1="6" x2="20" y2="6" />
              <line x1="4" y1="18" x2="20" y2="18" />
            </svg>
            <span class="mobile-explorer-label">{opts.title ?? "Archivio Dossier"}</span>
          </span>
          <span class="mobile-explorer-pill">1929–2026</span>
        </button>
        <button
          type="button"
          class="title-button explorer-toggle desktop-explorer"
          data-mobile={false}
          aria-expanded={true}
        >
          <h2>{opts.title ?? i18n(cfg.locale).components.explorer.title}</h2>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="14"
            height="14"
            viewBox="5 8 14 8"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="fold"
            aria-hidden="true"
          >
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
        <div id={id} class="explorer-content" aria-expanded={false} role="group">
          <div class="mobile-explorer-header">
            <div class="mobile-explorer-header-text">
              <span class="mobile-explorer-header-kicker">ARCHIVIO STORICO · DAL 1929</span>
              <span class="mobile-explorer-header-title">{opts.title ?? "Archivio Dossier"}</span>
            </div>
            <button
              type="button"
              class="explorer-toggle mobile-explorer-close-btn"
              aria-label="Chiudi archivio dossier"
            >
              <span>CHIUDI</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
          <div class="explorer-quick-filter">
            <input
              type="search"
              class="explorer-filter-input"
              placeholder="Filtra stagione o dossier..."
              aria-label="Filtra rapidamente voci nell'archivio"
              autocomplete="off"
            />
          </div>
          <OverflowList class="explorer-ul" />
        </div>
        <template id="template-file">
          <li>
            <a href="#"></a>
          </li>
        </template>
        <template id="template-folder">
          <li>
            <div class="folder-container">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="12"
                height="12"
                viewBox="5 8 14 8"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="folder-icon"
                aria-hidden="true"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
              <div>
                <button type="button" class="folder-button">
                  <span class="folder-title"></span>
                </button>
              </div>
              <a
                href="#"
                class="folder-direct-link"
                title="Apri pagina indice della sezione"
                aria-label="Apri pagina indice della sezione"
              >
                ↗
              </a>
            </div>
            <div class="folder-outer">
              <ul class="content"></ul>
            </div>
          </li>
        </template>
      </div>
    )
  }

  Explorer.css = style
  Explorer.afterDOMLoaded = concatenateResources(script, overflowListAfterDOMLoaded)
  return Explorer
}) satisfies QuartzComponentConstructor
