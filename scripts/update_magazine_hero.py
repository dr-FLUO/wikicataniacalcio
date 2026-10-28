import re
from pathlib import Path

path = Path("quartz/components/MagazineArticleHero.tsx")
content = path.read_text(encoding="utf-8")

# 1. Add visit import if not present
if 'import { visit } from "unist-util-visit"' not in content:
    content = 'import { visit } from "unist-util-visit"\n' + content

# 2. Update selectHeroMedia signature to return HeroMedia | null
content = re.sub(
    r'function selectHeroMedia\(slug: string, fm: Record<string, any>\): HeroMedia \{',
    'function selectHeroMedia(slug: string, fm: Record<string, any>): HeroMedia | null {',
    content
)

# 3. Replace the generic category-level fallbacks and final stadio-massimino-tribuna fallback with return null
fallback_pattern = re.compile(
    r'  // Category-level mappings.*?return \{\s*file: "stadio-massimino-tribuna\.jpg",.*?\n  \}\n\}',
    re.DOTALL
)

clean_end = """  // Specific indexes that have dedicated historical infographics
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
}"""

content = fallback_pattern.sub(clean_end, content)

# 4. In MagazineArticleHero, check tree for body images and skip hero figure if body already has image
old_render_start = """const MagazineArticleHero: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
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
  const media = selectHeroMedia(slug, fm)
  const imgSrc =
    baseDir === "."
      ? `./static/images/photos/${media.file}`
      : `${baseDir}/static/images/photos/${media.file}`
  const reportHref = baseDir === "." ? "./segnala-correzione" : `${baseDir}/segnala-correzione`"""

new_render_start = """const MagazineArticleHero: QuartzComponent = ({ fileData, tree }: QuartzComponentProps) => {
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
  const reportHref = baseDir === "." ? "./segnala-correzione" : `${baseDir}/segnala-correzione`"""

content = content.replace(old_render_start, new_render_start)

# 5. Conditionally render the <figure> element only when media and imgSrc exist
old_figure = """      {/* Magazine Editorial Cover Photograph Frame */}
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
      </figure>"""

new_figure = """      {/* Magazine Editorial Cover Photograph Frame — SOLO se media esiste ed è contestuale */}
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
      )}"""

content = content.replace(old_figure, new_figure)

path.write_text(content, encoding="utf-8")
print("[OK] MagazineArticleHero.tsx updated successfully.")
