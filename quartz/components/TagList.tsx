import { FullSlug, resolveRelative } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const TagList: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const tags = fileData.frontmatter?.tags
  if (tags && tags.length > 0) {
    return (
      <div class={classNames(displayClass, "article-tags-wrapper")}>
        <div class="article-tags-header">
          <span class="article-tags-icon">🏷️</span>
          <span class="article-tags-label">Dossier correlati & Argomenti archivistici</span>
        </div>
        <ul class="tags">
          {tags.map((tag) => {
            const linkDest = resolveRelative(fileData.slug!, `tags/${tag}` as FullSlug)
            return (
              <li>
                <a href={linkDest} class="internal tag-link" aria-label={`Consulta tutti i contenuti con tag ${tag}`}>
                  <span class="tag-hash">#</span>
                  {tag}
                </a>
              </li>
            )
          })}
        </ul>
      </div>
    )
  } else {
    return null
  }
}

TagList.css = `
.article-tags-wrapper {
  margin: 2.25rem 0 1.25rem 0;
  padding: 0.85rem 1.1rem;
  background-color: var(--wiki-surface-elevated);
  border: 1px solid var(--wiki-border-hairline);
  border-left: 3.5px solid var(--rossazzurro-gold);
  box-shadow: 2px 2px 0 var(--wiki-border-hairline);
}

.article-tags-header {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  margin-bottom: 0.65rem;
}

.article-tags-icon {
  font-size: 0.85rem;
  line-height: 1;
}

.article-tags-label {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--dark);
  line-height: 1;
}

.tags {
  list-style: none;
  display: flex;
  padding-left: 0;
  gap: 0.35rem 0.45rem;
  margin: 0;
  flex-wrap: wrap;
}

.tags > li {
  display: inline-flex;
  white-space: nowrap;
  margin: 0;
}

a.internal.tag-link {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--darkgray) !important;
  background-color: var(--light);
  border: 1px solid var(--wiki-border-hairline);
  border-radius: 3px;
  padding: 0.18rem 0.45rem;
  text-decoration: none !important;
  line-height: 1.25;
  transition: all 0.15s ease;

  .tag-hash {
    color: var(--rossazzurro-red);
    font-weight: 700;
  }

  &:hover {
    color: var(--rossazzurro-red) !important;
    border-color: var(--dark);
    background-color: rgba(0, 0, 0, 0.04);
  }
}
`

export default (() => TagList) satisfies QuartzComponentConstructor
