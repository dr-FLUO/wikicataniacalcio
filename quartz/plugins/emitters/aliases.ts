import { FullSlug, isRelativeURL, resolveRelative, simplifySlug } from "../../util/path"
import { QuartzEmitterPlugin } from "../types"
import { write } from "./helpers"
import { BuildCtx } from "../../util/ctx"
import { VFile } from "vfile"
import path from "path"

async function* processFile(ctx: BuildCtx, file: VFile) {
  const ogSlug = simplifySlug(file.data.slug!)

  for (const aliasTarget of file.data.aliases ?? []) {
    const aliasTargetSlug = (
      isRelativeURL(aliasTarget)
        ? path.normalize(path.join(ogSlug, "..", aliasTarget))
        : aliasTarget
    ) as FullSlug

    const redirUrl = resolveRelative(aliasTargetSlug, ogSlug)
    const rootRelUrl = "/" + (ogSlug === "index" ? "" : ogSlug)
    const htmlContent = `
        <!DOCTYPE html>
        <html lang="it">
        <head>
        <title>${ogSlug}</title>
        <link rel="canonical" href="${rootRelUrl}">
        <meta name="robots" content="noindex">
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="0; url=${rootRelUrl}">
        <script>
          window.location.replace("${rootRelUrl}");
        </script>
        </head>
        <body>
          <p>Reindirizzamento in corso verso <a href="${rootRelUrl}">${ogSlug}</a>...</p>
        </body>
        </html>
        `

    yield write({
      ctx,
      content: htmlContent,
      slug: aliasTargetSlug,
      ext: ".html",
    })

    // Also emit index.html / clean url pair so both /dir and /dir/ resolve without 404
    if (aliasTargetSlug !== "index") {
      if (aliasTargetSlug.endsWith("/index")) {
        const cleanSlug = aliasTargetSlug.slice(0, -"/index".length) as FullSlug
        if (cleanSlug && cleanSlug !== ogSlug) {
          yield write({
            ctx,
            content: htmlContent,
            slug: cleanSlug,
            ext: ".html",
          })
        }
      } else {
        const indexSlug = (aliasTargetSlug + "/index") as FullSlug
        if (indexSlug !== ogSlug) {
          yield write({
            ctx,
            content: htmlContent,
            slug: indexSlug,
            ext: ".html",
          })
        }
      }
    }
  }
}

export const AliasRedirects: QuartzEmitterPlugin = () => ({
  name: "AliasRedirects",
  async *emit(ctx, content) {
    for (const [_tree, file] of content) {
      yield* processFile(ctx, file)
    }
  },
  async *partialEmit(ctx, _content, _resources, changeEvents) {
    for (const changeEvent of changeEvents) {
      if (!changeEvent.file) continue
      if (changeEvent.type === "add" || changeEvent.type === "change") {
        // add new ones if this file still exists
        yield* processFile(ctx, changeEvent.file)
      }
    }
  },
})
