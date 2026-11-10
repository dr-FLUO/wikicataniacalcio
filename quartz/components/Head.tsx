import { i18n } from "../i18n"
import { FullSlug, getFileExtension, joinSegments, pathToRoot } from "../util/path"
import { CSSResourceToStyleElement, JSResourceToScriptElement } from "../util/resources"
import { googleFontHref, googleFontSubsetHref } from "../util/theme"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { unescapeHTML } from "../util/escape"
import { CustomOgImagesEmitterName } from "../plugins/emitters/ogImage"
export default (() => {
  const Head: QuartzComponent = ({
    cfg,
    fileData,
    externalResources,
    ctx,
  }: QuartzComponentProps) => {
    const titleSuffix = cfg.pageTitleSuffix ?? ""
    const title =
      (fileData.frontmatter?.title ?? i18n(cfg.locale).propertyDefaults.title) + titleSuffix
    const description =
      fileData.frontmatter?.socialDescription ??
      fileData.frontmatter?.description ??
      unescapeHTML(fileData.description?.trim() ?? i18n(cfg.locale).propertyDefaults.description)

    const { css, js, additionalHead } = externalResources

    const url = new URL(`https://${cfg.baseUrl ?? "example.com"}`)
    const path = url.pathname as FullSlug
    const baseDir = fileData.slug === "404" ? path : pathToRoot(fileData.slug!)
    const iconPath = joinSegments(baseDir, "static/icon.png")
    const faviconSvgPath = joinSegments(baseDir, "static/favicon.svg")
    const faviconIcoPath = joinSegments(baseDir, "favicon.ico")

    // Url of current page
    const socialUrl =
      fileData.slug === "404" ? url.toString() : joinSegments(url.toString(), fileData.slug!)

    const usesCustomOgImage = ctx.cfg.plugins.emitters.some(
      (e) => e.name === CustomOgImagesEmitterName,
    )
    const ogImageDefaultPath = `https://${cfg.baseUrl}/static/og-image.png`

    const rawPageImage =
      (fileData.frontmatter?.socialImage as string | undefined) ??
      (fileData.frontmatter?.cover_image as string | undefined) ??
      (fileData.frontmatter?.image as string | undefined)

    let pageOgImage = ogImageDefaultPath
    if (rawPageImage && typeof rawPageImage === "string" && rawPageImage.trim().length > 0) {
      const cleanImg = rawPageImage.trim()
      if (cleanImg.startsWith("http://") || cleanImg.startsWith("https://")) {
        pageOgImage = cleanImg
      } else {
        const pathPart = cleanImg.startsWith("/") ? cleanImg.slice(1) : cleanImg
        pageOgImage = `https://${cfg.baseUrl}/${pathPart}`
      }
    }
    const ogExtRaw = getFileExtension(pageOgImage) ?? "png"
    const cleanExt = ogExtRaw.replace(/^\./, "").toLowerCase()
    const ogMimeType = `image/${cleanExt === "jpg" ? "jpeg" : cleanExt || "png"}`

    return (
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                var isGh = window.location.hostname.endsWith(".github.io");
                var path = window.location.pathname.replace(new RegExp("/+", "g"), "/");
                if (isGh && !path.startsWith("/wikicataniacalcio")) {
                  window.location.replace("/wikicataniacalcio" + path + window.location.search + window.location.hash);
                  return;
                }
                var clean = isGh ? path.slice("/wikicataniacalcio".length) : path;
                var rootSections = [
                  "01-societa", "02-cronistoria", "03-tesserati", "04-strutture",
                  "05-identita-e-simboli", "06-tifoseria-e-cultura", "07-media-e-comunicazione",
                  "08-settori-paralleli", "tags", "note-legali-privacy-accessibilita",
                  "segnala-correzione"
                ];
                var segs = clean.split("/").filter(Boolean);
                var lastIdx = -1;
                for (var i = 0; i < segs.length; i++) {
                  if (rootSections.indexOf(segs[i]) !== -1) lastIdx = i;
                }
                if (lastIdx > 0) {
                  var unnested = (isGh ? "/wikicataniacalcio" : "") + "/" + segs.slice(lastIdx).join("/") + (window.location.pathname.endsWith("/") ? "/" : "");
                  window.location.replace(unnested + window.location.search + window.location.hash);
                }
              })();
            `,
          }}
        />
        <title>{title}</title>
        <meta charSet="utf-8" />
        {cfg.theme.cdnCaching && cfg.theme.fontOrigin === "googleFonts" && (
          <>
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" />
            <link rel="stylesheet" href={googleFontHref(cfg.theme)} />
            {cfg.theme.typography.title && (
              <link rel="stylesheet" href={googleFontSubsetHref(cfg.theme, cfg.pageTitle)} />
            )}
          </>
        )}
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <meta name="og:site_name" content={cfg.pageTitle}></meta>
        <meta property="og:title" content={title} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        <meta property="og:description" content={description} />
        <meta property="og:image:alt" content={description} />

        {!usesCustomOgImage && (
          <>
            <meta property="og:image" content={pageOgImage} />
            <meta property="og:image:url" content={pageOgImage} />
            <meta name="twitter:image" content={pageOgImage} />
            <meta property="og:image:type" content={ogMimeType} />
          </>
        )}

        {cfg.baseUrl && (
          <>
            <meta property="twitter:domain" content={cfg.baseUrl}></meta>
            <meta property="og:url" content={socialUrl}></meta>
            <meta property="twitter:url" content={socialUrl}></meta>
            <link rel="canonical" href={socialUrl} />
          </>
        )}

        {/* Favicon & Web App Icons - Conforme a Google Search Central & Standard W3C/Apple */}
        <link rel="icon" href="/favicon.ico" sizes="48x48 32x32 16x16" />
        <link rel="icon" type="image/svg+xml" href="/static/favicon.svg" />
        <link rel="icon" type="image/png" sizes="48x48" href="/static/icon-48.png" />
        <link rel="icon" type="image/png" sizes="192x192" href="/static/icon-192.png" />
        <link rel="icon" type="image/png" sizes="512x512" href="/static/icon.png" />
        <link rel="shortcut icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/static/icon.png" />
        <meta name="description" content={description} />
        <meta name="generator" content="Quartz" />

        {cfg.analytics?.provider === "umami" && (
          <script
            defer
            src={`${(cfg.analytics.host ?? "https://cloud.umami.is").replace(/\/+$/, "")}/script.js`}
            data-website-id={cfg.analytics.websiteId}
            data-domains="wikicataniacalcio.com,www.wikicataniacalcio.com"
          ></script>
        )}

        {css.map((resource) => CSSResourceToStyleElement(resource, true))}
        {js
          .filter((resource) => resource.loadTime === "beforeDOMReady")
          .map((res) => JSResourceToScriptElement(res, true))}
        {additionalHead.map((resource) => {
          if (typeof resource === "function") {
            return resource(fileData)
          } else {
            return resource
          }
        })}
      </head>
    )
  }

  return Head
}) satisfies QuartzComponentConstructor
