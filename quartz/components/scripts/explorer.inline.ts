import { FileTrieNode } from "../../util/fileTrie"
import { FullSlug, simplifySlug } from "../../util/path"
import { ContentDetails } from "../../plugins/emitters/contentIndex"

type MaybeHTMLElement = HTMLElement | undefined

interface ParsedOptions {
  folderClickBehavior: "collapse" | "link"
  folderDefaultState: "collapsed" | "open"
  useSavedState: boolean
  sortFn: (a: FileTrieNode, b: FileTrieNode) => number
  filterFn: (node: FileTrieNode) => boolean
  mapFn: (node: FileTrieNode) => void
  order: "sort" | "filter" | "map"[]
}

type FolderState = {
  path: string
  collapsed: boolean
}

let currentExplorerState: Array<FolderState>

function toggleExplorer(this: HTMLElement) {
  const nearestExplorer = this.closest(".explorer") as HTMLElement
  if (!nearestExplorer) return
  const explorerCollapsed = nearestExplorer.classList.toggle("collapsed")
  nearestExplorer.setAttribute(
    "aria-expanded",
    nearestExplorer.getAttribute("aria-expanded") === "true" ? "false" : "true",
  )

  if (!explorerCollapsed) {
    document.documentElement.classList.add("mobile-no-scroll")
  } else {
    document.documentElement.classList.remove("mobile-no-scroll")
  }
}

function toggleFolder(evt: MouseEvent) {
  const target = evt.target as MaybeHTMLElement
  if (!target) return
  // If user clicked the direct link icon '↗', let the browser navigate normally
  if (target.closest(".folder-direct-link")) {
    return
  }

  evt.stopPropagation()
  const folderContainer = target.closest(".folder-container") as MaybeHTMLElement
  if (!folderContainer) return
  const childFolderContainer = folderContainer.nextElementSibling as MaybeHTMLElement
  if (!childFolderContainer) return

  childFolderContainer.classList.toggle("open")

  const isCollapsed = !childFolderContainer.classList.contains("open")
  setFolderState(childFolderContainer, isCollapsed)

  const currentFolderState = currentExplorerState.find(
    (item) => item.path === folderContainer.dataset.folderpath,
  )
  if (currentFolderState) {
    currentFolderState.collapsed = isCollapsed
  } else {
    currentExplorerState.push({
      path: folderContainer.dataset.folderpath as FullSlug,
      collapsed: isCollapsed,
    })
  }

  const stringifiedFileTree = JSON.stringify(currentExplorerState)
  localStorage.setItem("fileTree", stringifiedFileTree)
}

function getExplorerNodeHref(_currentSlug: FullSlug, targetSlug: FullSlug): string {
  const isGh = typeof window !== "undefined" && window.location.hostname.endsWith(".github.io")
  const base = isGh ? "/wikicataniacalcio" : ""

  const isFolder = targetSlug.endsWith("/index") || targetSlug === "index"
  const clean = targetSlug.replace(/\/index$/, "")
  if (clean === "" || clean === "index") {
    return base ? `${base}/` : "/"
  }
  const trailing = isFolder ? "/" : ""
  return base ? `${base}/${clean}${trailing}` : `/${clean}${trailing}`
}

function createFileNode(currentSlug: FullSlug, node: FileTrieNode): HTMLLIElement {
  const template = document.getElementById("template-file") as HTMLTemplateElement
  const clone = template.content.cloneNode(true) as DocumentFragment
  const li = clone.querySelector("li") as HTMLLIElement
  const a = li.querySelector("a") as HTMLAnchorElement
  a.href = getExplorerNodeHref(currentSlug, node.slug)
  a.dataset.for = node.slug
  a.textContent = node.displayName

  if (currentSlug === node.slug || simplifySlug(currentSlug) === simplifySlug(node.slug)) {
    a.classList.add("active")
  }

  return li
}

function createFolderNode(
  currentSlug: FullSlug,
  node: FileTrieNode,
  opts: ParsedOptions,
): HTMLLIElement {
  const template = document.getElementById("template-folder") as HTMLTemplateElement
  const clone = template.content.cloneNode(true) as DocumentFragment
  const li = clone.querySelector("li") as HTMLLIElement
  const folderContainer = li.querySelector(".folder-container") as HTMLElement
  const titleContainer = folderContainer.querySelector("div") as HTMLElement
  const directLink = folderContainer.querySelector(".folder-direct-link") as HTMLAnchorElement | null
  const folderOuter = li.querySelector(".folder-outer") as HTMLElement
  const ul = folderOuter.querySelector("ul") as HTMLUListElement

  const folderPath = node.slug
  folderContainer.dataset.folderpath = folderPath

  if (currentSlug === folderPath || simplifySlug(currentSlug) === simplifySlug(folderPath)) {
    folderContainer.classList.add("active")
  }

  if (directLink) {
    directLink.href = getExplorerNodeHref(currentSlug, folderPath)
    directLink.title = `Apri indice: ${node.displayName}`
  }

  if (opts.folderClickBehavior === "link") {
    const button = titleContainer.querySelector(".folder-button") as HTMLElement
    const a = document.createElement("a")
    a.href = getExplorerNodeHref(currentSlug, folderPath)
    a.dataset.for = folderPath
    a.className = "folder-title"
    a.textContent = node.displayName
    button.replaceWith(a)
  } else {
    const span = titleContainer.querySelector(".folder-title") as HTMLElement
    span.textContent = node.displayName
  }

  const isCollapsed =
    currentExplorerState.find((item) => item.path === folderPath)?.collapsed ??
    opts.folderDefaultState === "collapsed"

  const simpleFolderPath = simplifySlug(folderPath)
  const folderIsPrefixOfCurrentSlug =
    simpleFolderPath.length > 0 && currentSlug.startsWith(simpleFolderPath)

  if (!isCollapsed || folderIsPrefixOfCurrentSlug) {
    folderOuter.classList.add("open")
  }

  for (const child of node.children) {
    const childNode =
      child.isFolder && child.children.length > 0
        ? createFolderNode(currentSlug, child, opts)
        : createFileNode(currentSlug, child)
    ul.appendChild(childNode)
  }

  return li
}

/**
 * Restructures the FileTrieNode tree according to the "Max 2 Levels" Information Architecture
 * (Section 7.3) without modifying any underlying page slugs or URLs.
 */
function restructureEditorialTrie(trie: FileTrieNode, currentSlug: FullSlug) {
  const collectLeaves = (folder: FileTrieNode, prefixYear: boolean = false): FileTrieNode[] => {
    const out: FileTrieNode[] = []
    for (const ch of folder.children) {
      if (!ch.isFolder) {
        if (prefixYear) {
          const m = ch.slug.match(/\/(\d{4})-(\d{4})\//)
          if (m && !ch.displayName.startsWith(m[1]) && !ch.displayName.startsWith(m[2])) {
            ch.displayName = `${m[2]} · ${ch.displayName}`
          }
        }
        out.push(ch)
      } else {
        const subLeaves = collectLeaves(ch, prefixYear)
        if (subLeaves.length === 0) {
          // Se la sotto-cartella non ha file annidati (es. ha solo il proprio index.md),
          // la preserviamo come nodo foglia di 2° livello invece di scartarla!
          out.push(ch)
        } else {
          out.push(...subLeaves)
        }
      }
    }
    return out
  }

  for (const topNode of trie.children) {
    if (!topNode.isFolder) continue
    const seg = topNode.slugSegment

    // 1. 02-cronistoria: promote 'precedenti' to level 2 & flatten single-year subfolders inside 'partite-storiche'
    if (seg === "02-cronistoria") {
      const partiteNode = topNode.children.find((c) => c.slugSegment === "partite-storiche")
      if (partiteNode && partiteNode.isFolder) {
        const precIdx = partiteNode.children.findIndex((c) => c.slugSegment === "precedenti")
        if (precIdx !== -1) {
          const [precNode] = partiteNode.children.splice(precIdx, 1)
          precNode.displayName = "Precedenti & Derby"
          topNode.children.push(precNode)
        }
        // Flatten year folders inside partite-storiche
        partiteNode.children = collectLeaves(partiteNode, true)
      }
    }

    // 2. 03-tesserati: unwrap intermediate 'calciatori' container & convert 'archivio' into a direct 1-click portal link
    if (seg === "03-tesserati") {
      const calcIdx = topNode.children.findIndex((c) => c.slugSegment === "calciatori")
      if (calcIdx !== -1) {
        const [calcNode] = topNode.children.splice(calcIdx, 1)
        for (const sub of calcNode.children) {
          if (sub.slugSegment === "archivio") {
            // Make 'Archivio Calciatori (Filtri A–Z)' a 1-click portal leaf
            sub.children = []
            sub.displayName = "Archivio Calciatori (A–Z)"
          } else if (sub.slugSegment === "storici") {
            sub.displayName = "Leggende & Storici"
          } else if (sub.slugSegment === "rosa-attuale") {
            sub.displayName = "Rosa Attuale"
          }
          topNode.children.unshift(sub)
        }
      }
    }

    // 3. 04-strutture, 05-identita-e-simboli, 08-settori-paralleli: flatten single-item subfolders to level 2
    if (seg === "04-strutture" || seg === "05-identita-e-simboli" || seg === "08-settori-paralleli") {
      topNode.children = collectLeaves(topNode, false)
    }

    // 4. 06-tifoseria-e-cultura: unwrap intermediate 'settori' and 'relazioni' wrappers
    if (seg === "06-tifoseria-e-cultura") {
      const nextChildren: FileTrieNode[] = []
      for (const ch of topNode.children) {
        if (ch.isFolder && (ch.slugSegment === "settori" || ch.slugSegment === "relazioni")) {
          nextChildren.push(...ch.children)
        } else {
          nextChildren.push(ch)
        }
      }
      topNode.children = nextChildren
    }

    // 5. 07-media-e-comunicazione: unwrap single-file 'letteratura' & 'cinema-e-tv' if <= 2 items
    if (seg === "07-media-e-comunicazione") {
      const nextChildren: FileTrieNode[] = []
      for (const ch of topNode.children) {
        if (ch.isFolder && ch.children.length <= 2) {
          nextChildren.push(...collectLeaves(ch, false))
        } else {
          nextChildren.push(ch)
        }
      }
      topNode.children = nextChildren
    }
  }

  // Contextual Focus: move the active top-level rubric to the first position when inside a rubric
  const activeTopIdx = trie.children.findIndex(
    (c) => c.isFolder && c.slugSegment && currentSlug.startsWith(c.slugSegment),
  )
  if (activeTopIdx > 0) {
    const [activeTop] = trie.children.splice(activeTopIdx, 1)
    trie.children.unshift(activeTop)
  }
}

async function setupExplorer(currentSlug: FullSlug) {
  const allExplorers = document.querySelectorAll("div.explorer") as NodeListOf<HTMLElement>

  for (const explorer of allExplorers) {
    const dataFns = JSON.parse(explorer.dataset.dataFns || "{}")
    const opts: ParsedOptions = {
      folderClickBehavior: (explorer.dataset.behavior || "collapse") as "collapse" | "link",
      folderDefaultState: (explorer.dataset.collapsed || "collapsed") as "collapsed" | "open",
      useSavedState: explorer.dataset.savestate === "true",
      order: dataFns.order || ["filter", "map", "sort"],
      sortFn: new Function("return " + (dataFns.sortFn || "undefined"))(),
      filterFn: new Function("return " + (dataFns.filterFn || "undefined"))(),
      mapFn: new Function("return " + (dataFns.mapFn || "undefined"))(),
    }

    const storageTree = localStorage.getItem("fileTree")
    const serializedExplorerState = storageTree && opts.useSavedState ? JSON.parse(storageTree) : []
    const oldIndex = new Map<string, boolean>(
      serializedExplorerState.map((entry: FolderState) => [entry.path, entry.collapsed]),
    )

    const data = await fetchData
    const entries = [...Object.entries(data)] as [FullSlug, ContentDetails][]
    const trie = FileTrieNode.fromEntries(entries)

    for (const fn of opts.order) {
      switch (fn) {
        case "filter":
          if (opts.filterFn) trie.filter(opts.filterFn)
          break
        case "map":
          if (opts.mapFn) trie.map(opts.mapFn)
          break
        case "sort":
          if (opts.sortFn) trie.sort(opts.sortFn)
          break
      }
    }

    restructureEditorialTrie(trie, currentSlug)

    const folderPaths = trie.getFolderPaths()
    currentExplorerState = folderPaths.map((path) => {
      const previousState = oldIndex.get(path)
      return {
        path,
        collapsed:
          previousState === undefined ? opts.folderDefaultState === "collapsed" : previousState,
      }
    })

    const explorerUl = explorer.querySelector(".explorer-ul") as HTMLElement | null
    if (!explorerUl) continue

    const fragment = document.createDocumentFragment()
    for (const child of trie.children) {
      const node = child.isFolder
        ? createFolderNode(currentSlug, child, opts)
        : createFileNode(currentSlug, child)

      fragment.appendChild(node)
    }
    explorerUl.insertBefore(fragment, explorerUl.firstChild)

    const scrollTop = sessionStorage.getItem("explorerScrollTop")
    if (scrollTop) {
      explorerUl.scrollTop = parseInt(scrollTop)
    } else {
      const activeElement = explorerUl.querySelector(".active")
      if (activeElement) {
        activeElement.scrollIntoView({ behavior: "smooth", block: "nearest" })
      }
    }

    const explorerButtons = explorer.getElementsByClassName(
      "explorer-toggle",
    ) as HTMLCollectionOf<HTMLElement>
    for (const button of explorerButtons) {
      button.addEventListener("click", toggleExplorer)
      window.addCleanup(() => button.removeEventListener("click", toggleExplorer))
    }

    // Make the entire .folder-container clickable to expand/collapse immediately (Fitts's Law fix)
    const folderContainers = explorer.getElementsByClassName(
      "folder-container",
    ) as HTMLCollectionOf<HTMLElement>
    for (const fc of folderContainers) {
      fc.addEventListener("click", toggleFolder)
      window.addCleanup(() => fc.removeEventListener("click", toggleFolder))
    }

    // Wire up instant text filter inside the sidebar
    const filterInput = explorer.querySelector(".explorer-filter-input") as HTMLInputElement | null
    if (filterInput) {
      const handleFilter = () => {
        const q = filterInput.value.trim().toLowerCase()
        const allItems = explorerUl.querySelectorAll("li") as NodeListOf<HTMLLIElement>
        if (!q) {
          allItems.forEach((li) => {
            li.style.display = ""
          })
          return
        }
        allItems.forEach((li) => {
          const text = (li.textContent || "").toLowerCase()
          const matches = text.includes(q)
          li.style.display = matches ? "" : "none"
          if (matches) {
            const outer = li.querySelector(":scope > .folder-outer") as HTMLElement | null
            if (outer) outer.classList.add("open")
          }
        })
      }
      filterInput.addEventListener("input", handleFilter)
      window.addCleanup(() => filterInput.removeEventListener("input", handleFilter))
    }
  }
}

document.addEventListener("prenav", async () => {
  const explorer = document.querySelector(".explorer-ul")
  if (!explorer) return
  sessionStorage.setItem("explorerScrollTop", explorer.scrollTop.toString())
})

document.addEventListener("nav", async (e: CustomEventMap["nav"]) => {
  const currentSlug = e.detail.url
  await setupExplorer(currentSlug)

  for (const explorer of document.getElementsByClassName("explorer")) {
    const mobileExplorer = explorer.querySelector(".mobile-explorer")
    if (!mobileExplorer) return

    if (mobileExplorer.checkVisibility()) {
      explorer.classList.add("collapsed")
      explorer.setAttribute("aria-expanded", "false")
      document.documentElement.classList.remove("mobile-no-scroll")
    }

    mobileExplorer.classList.remove("hide-until-loaded")
  }
})

window.addEventListener("resize", function () {
  const explorer = document.querySelector(".explorer")
  if (explorer && !explorer.classList.contains("collapsed")) {
    const mobileExplorer = explorer.querySelector(".mobile-explorer")
    if (mobileExplorer?.checkVisibility()) {
      document.documentElement.classList.add("mobile-no-scroll")
      return
    }
  }
  document.documentElement.classList.remove("mobile-no-scroll")
})

function setFolderState(folderElement: HTMLElement, collapsed: boolean) {
  return collapsed ? folderElement.classList.remove("open") : folderElement.classList.add("open")
}
