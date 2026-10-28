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
            (function() {
              var isGh = window.location.hostname.endsWith(".github.io");
              var path = window.location.pathname.replace(/\/+/g, "/");
              if (isGh && !path.startsWith("/wikicataniacalcio")) {
                window.location.replace("/wikicataniacalcio" + path + window.location.search + window.location.hash);
                return;
              }
              var clean = isGh ? path.slice("/wikicataniacalcio".length) : path;
              var sections = [
                "01-societa", "02-cronistoria", "03-tesserati", "04-strutture",
                "05-identita-e-simboli", "06-tifoseria-e-cultura", "07-media-e-comunicazione",
                "08-settori-paralleli", "tags", "note-legali-privacy-accessibilita",
                "segnala-correzione", "societa", "cronistoria", "tesserati",
                "strutture", "stadio", "simboli", "tifoseria", "media", "paralleli",
                "stagioni", "partite-storiche", "vicende-legali"
              ];
              var segs = clean.split("/").filter(Boolean);
              var lastIdx = -1;
              for (var i = 0; i < segs.length; i++) {
                if (sections.indexOf(segs[i]) !== -1) lastIdx = i;
              }
              if (lastIdx > 0) {
                var unnested = (isGh ? "/wikicataniacalcio" : "") + "/" + segs.slice(lastIdx).join("/") + (window.location.pathname.endsWith("/") ? "/" : "");
                window.location.replace(unnested + window.location.search + window.location.hash);
                return;
              }

              // In 404, repair any relative links in the DOM to avoid recursive nesting
              var base = isGh ? "/wikicataniacalcio" : "";
              document.querySelectorAll("a").forEach(function(a) {
                var href = a.getAttribute("href");
                if (href && (href.startsWith("./") || href.startsWith("../"))) {
                  var target = href.replace(/^(\.\.?\/)+/, "");
                  a.setAttribute("href", base + "/" + target);
                }
              });
            })();
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
