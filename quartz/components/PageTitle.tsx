import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"

const PageTitle: QuartzComponent = ({ fileData, cfg, displayClass }: QuartzComponentProps) => {
  const title = cfg?.pageTitle ?? i18n(cfg.locale).propertyDefaults.title
  const baseDir = pathToRoot(fileData.slug!)
  return (
    <div class={classNames(displayClass, "page-title-wrapper")}>
      <a href="#main-article-content" class="skip-to-content">
        Salta al contenuto principale
      </a>
      <h2 class="page-title">
        <a href={baseDir} aria-label={`${title} — Torna alla pagina iniziale`}>
          {title}
        </a>
      </h2>
    </div>
  )
}

PageTitle.css = `
.page-title {
  font-size: 1.65rem;
  margin: 0;
  font-family: var(--titleFont);
}
.skip-to-content {
  position: absolute;
  left: -9999px;
  top: 0.5rem;
  z-index: 9999;
  padding: 0.45rem 0.85rem;
  background-color: #191919;
  color: #f7f7f7;
  border: 2px solid #0cb2d9;
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  border-radius: 4px;
}
.skip-to-content:focus {
  left: 0.75rem;
}
`

export default (() => PageTitle) satisfies QuartzComponentConstructor
