import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import style from "../styles/panoramica.scss"
import listStyle from "../styles/listPage.scss"
import { Root } from "hast"
import { htmlToJsx } from "../../util/jsx"
import { QuartzPluginData } from "../../plugins/vfile"
import { ComponentChildren } from "preact"
import { concatenateResources } from "../../util/resources"
import { trieFromAllFiles } from "../../util/ctx"
import { FileTrieNode } from "../../util/fileTrie"
import { FullSlug, resolveRelative } from "../../util/path"
import { getEditorialFolderInfo } from "../../util/editorialFolders"

interface FolderContentOptions {
  showFolderCount: boolean
  showSubfolders: boolean
}

const defaultOptions: FolderContentOptions = {
  showFolderCount: true,
  showSubfolders: true,
}

function countLeaves(node: FileTrieNode): number {
  let count = 0
  for (const child of node.children) {
    if (!child.isFolder && child.data && child.slugSegment !== "index") {
      count++
    } else if (child.isFolder) {
      count += countLeaves(child)
    }
  }
  return count
}

function collectAllLeaves(node: FileTrieNode): QuartzPluginData[] {
  const leaves: QuartzPluginData[] = []
  for (const child of node.children) {
    if (!child.isFolder && child.data && child.slugSegment !== "index") {
      leaves.push(child.data)
    } else if (child.isFolder) {
      leaves.push(...collectAllLeaves(child))
    }
  }
  return leaves
}

function getBadgeInfo(entityType: string = "", slug: string = ""): { label: string; cls: string } {
  const t = entityType.toLowerCase()
  if (t === "dirigente") return { label: "DIRIGENTE", cls: "dirigente" }
  if (t === "presidente") return { label: "PRESIDENTE", cls: "presidente" }
  if (t === "season" || slug.includes("stagioni/")) return { label: "STAGIONE UFFICIALE", cls: "partita" }
  if (t === "match_report" || slug.includes("partite-storiche/")) return { label: "TABELLINO STORICO", cls: "partita" }
  if (t === "legal_dossier" || slug.includes("vicende-legali/")) return { label: "DIRITTO SPORTIVO", cls: "dirigente" }
  if (t === "thematic_dossier") return { label: "DOSSIER TEMATICO", cls: "dirigente" }
  if (t === "monograph" || slug.includes("calciatori/")) return { label: "CALCIATORE", cls: "calciatore" }
  if (t === "allenatore" || slug.includes("allenatori/")) return { label: "ALLENATORE", cls: "allenatore" }
  if (t === "biography") return { label: "BIOGRAFIA", cls: "ultras" }
  if (t === "ultras_group" || slug.includes("curve/")) return { label: "GRUPPO ULTRAS", cls: "ultras" }
  if (slug.includes("strutture/")) return { label: "IMPIANTO STORICO", cls: "dirigente" }
  if (slug.includes("identita-e-simboli/")) return { label: "SIMBOLOGIA & ARALDICA", cls: "dirigente" }
  if (slug.includes("media-e-comunicazione/")) return { label: "MEDIA & COMUNICAZIONE", cls: "dirigente" }
  return { label: "SCHEDA UFFICIALE", cls: "dirigente" }
}

export default ((opts?: Partial<FolderContentOptions>) => {
  const options: FolderContentOptions = { ...defaultOptions, ...opts }

  const FolderContent: QuartzComponent = (props: QuartzComponentProps) => {
    const { tree, fileData, allFiles, cfg } = props
    const currentSlug = fileData.slug ?? ""

    if (
      currentSlug.endsWith("/archivio") ||
      currentSlug.endsWith("/archivio/index") ||
      currentSlug === "calciatori/archivio"
    ) {
      return null
    }

    const trie = (props.ctx.trie ??= trieFromAllFiles(allFiles))
    const folder = trie.findNode(currentSlug.split("/"))
    if (!folder) {
      return null
    }

    const editorial = getEditorialFolderInfo(currentSlug)
    const pageTitle = fileData.frontmatter?.title && !fileData.frontmatter.title.startsWith("Cartella:") && !fileData.frontmatter.title.startsWith("Folder:")
      ? fileData.frontmatter.title
      : editorial.title
    const pageDescription = fileData.frontmatter?.description ?? editorial.desc

    // Direct files in this folder
    const directFiles: QuartzPluginData[] = folder.children
      .filter((n) => !n.isFolder && n.data && n.slugSegment !== "index")
      .map((n) => n.data!)

    // Subfolders in this folder
    const subfolderNodes = folder.children.filter((n) => n.isFolder && n.slugSegment !== "tags")
    const subfolders = subfolderNodes.map((sf) => {
      const sfInfo = getEditorialFolderInfo(sf.slug)
      const count = countLeaves(sf)
      const href = resolveRelative(currentSlug as FullSlug, sf.slug as FullSlug)
      return {
        slug: sf.slug,
        title: sfInfo.title,
        desc: sfInfo.desc,
        count,
        href,
      }
    })

    // If there are no direct files, but there are subfolders, flatten and surface documents
    let displayDocs = directFiles
    if (displayDocs.length === 0 && subfolders.length > 0) {
      displayDocs = collectAllLeaves(folder)
    }

    // Sort documents alphabetically by title or by season
    displayDocs.sort((a, b) => {
      const aTitle = a.frontmatter?.title ?? a.slug ?? ""
      const bTitle = b.frontmatter?.title ?? b.slug ?? ""
      return aTitle.localeCompare(bTitle, "it", { numeric: true })
    })

    const totalCount = directFiles.length > 0 ? directFiles.length : displayDocs.length

    // Markdown content from index.md (if present)
    const hasMarkdownContent = tree && (tree as Root).children.length > 0
    const renderedContent = hasMarkdownContent ? (htmlToJsx(fileData.filePath!, tree) as ComponentChildren) : null

    const cssClasses: string[] = fileData.frontmatter?.cssclasses ?? []
    const classes = cssClasses.join(" ")

    return (
      <div class="popover-hint nfc-panoramica-container">
        {/* Intestazione Editoriale Panoramica */}
        <header class="nfc-panoramica-hero">
          <div class="nfc-panoramica-stripe" aria-hidden="true" />
          <div class="nfc-panoramica-badge-row">
            <div class="nfc-split-badge">
              <span class="nfc-split-badge__left">{editorial.rubric}</span>
              <span class="nfc-split-badge__right">PANORAMICA DOSSIER</span>
            </div>
            <div class="nfc-verified-tag">
              <span class="nfc-verified-tag__dot" />
              <span>{totalCount} SCHEDE CERTIFICATE</span>
            </div>
          </div>
          <h1 class="nfc-panoramica-title">{pageTitle}</h1>
          <p class="nfc-panoramica-deck">{pageDescription}</p>

          <div class="nfc-panoramica-meta-strip">
            <div class="nfc-meta-pill-item">
              <span>Sezione:</span>
              <strong>{editorial.rubric.split("·")[1]?.trim() ?? "Archivio"}</strong>
            </div>
            <div class="nfc-meta-pill-item">
              <span>Documenti Totali:</span>
              <strong>{totalCount} Schede</strong>
            </div>
            <div class="nfc-meta-pill-item">
              <span>Verifica Fonti:</span>
              <strong>100% Conforme</strong>
            </div>
          </div>
        </header>

        {/* Articolo / Tavola introduttiva (se presente nel markdown di index.md) */}
        {renderedContent && (
          <div class="nfc-panoramica-intro">
            <article class={classes}>{renderedContent}</article>
          </div>
        )}

        {/* Sotto-Dossier (se presenti) */}
        {subfolders.length > 0 && (
          <section class="nfc-dossier-subsections" aria-label="Sotto-sezioni del dossier">
            <h2 class="nfc-section-heading">Sotto-Dossier & Rubriche Tematiche</h2>
            <div class="nfc-subfolders-grid">
              {subfolders.map((sf) => (
                <a href={sf.href} class="nfc-subfolder-card">
                  <div class="nfc-subfolder-card__badge">SOTTO-DOSSIER</div>
                  <h3 class="nfc-subfolder-card__title">{sf.title}</h3>
                  <p class="nfc-subfolder-card__desc">{sf.desc}</p>
                  <div class="nfc-subfolder-card__footer">
                    <span class="nfc-subfolder-card__count">{sf.count} schede</span>
                    <span class="nfc-subfolder-card__arrow">Esplora rubrica →</span>
                  </div>
                </a>
              ))}
            </div>
          </section>
        )}

        {/* Griglia Schede / Documenti */}
        {displayDocs.length > 0 && (
          <section class="nfc-dossier-documents" aria-label="Documenti certificati">
            <h2 class="nfc-section-heading">
              {directFiles.length > 0 ? "Documenti e Schede Monografiche" : "Tutti i Documenti Certificati"}
            </h2>
            <div class="nfc-cards-grid">
              {displayDocs.map((doc) => {
                const fm = doc.frontmatter ?? {}
                const title = fm.title ?? doc.slug ?? ""
                const desc = fm.description ?? doc.description ?? "Scheda monografica dell'archivio storico di Wiki Catania Calcio."
                const entityType = fm.entity_type ?? ""
                const badge = getBadgeInfo(entityType, doc.slug ?? "")
                const period = fm.season_label ?? (fm.date_start ? String(fm.date_start).slice(0, 4) : undefined)
                const tags: string[] = (fm.tags ?? []).slice(0, 3)
                const href = resolveRelative(currentSlug as FullSlug, doc.slug as FullSlug)

                return (
                  <article class="nfc-editorial-card">
                    <div class="nfc-card__header">
                      <span class={`nfc-card__badge is-${badge.cls}`}>{badge.label}</span>
                      {period && <span class="nfc-card__period">{period}</span>}
                    </div>
                    <h3 class="nfc-card__title">
                      <a href={href}>{title}</a>
                    </h3>
                    <p class="nfc-card__excerpt">{desc}</p>
                    <div class="nfc-card__footer">
                      <div class="nfc-card__tags">
                        {tags.map((t) => (
                          <span class="nfc-card__tag-pill">#{t}</span>
                        ))}
                      </div>
                      <a href={href} class="nfc-card__action">
                        Leggi Scheda →
                      </a>
                    </div>
                  </article>
                )
              })}
            </div>
          </section>
        )}
      </div>
    )
  }

  FolderContent.css = concatenateResources(style, listStyle)
  return FolderContent
}) satisfies QuartzComponentConstructor
