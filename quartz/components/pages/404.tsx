import { i18n } from "../../i18n"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"

const NotFound: QuartzComponent = ({ cfg }: QuartzComponentProps) => {
  // If baseUrl contains a pathname after the domain, use this as the home link
  const url = new URL(`https://${cfg.baseUrl ?? "example.com"}`)
  const baseDir = url.pathname

  return (
    <article class="popover-hint">
      <script
        dangerouslySetInnerHTML={{
          __html: `
            // GitHub Pages Subpath Auto-Recovery:
            // Se una richiesta atterra fuori da /wikicataniacalcio/, reindirizza all'istante
            if (window.location.hostname.endsWith(".github.io") && !window.location.pathname.startsWith("/wikicataniacalcio")) {
              var target = "/wikicataniacalcio" + window.location.pathname + window.location.search + window.location.hash;
              window.location.replace(target);
            }
          `,
        }}
      />
      <h1>404</h1>
      <p>{i18n(cfg.locale).pages.error.notFound}</p>
      <a href={baseDir}>{i18n(cfg.locale).pages.error.home}</a>
    </article>
  )
}

export default (() => NotFound) satisfies QuartzComponentConstructor
