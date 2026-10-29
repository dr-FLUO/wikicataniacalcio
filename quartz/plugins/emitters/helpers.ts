import path from "path"
import fs from "fs"
import { BuildCtx } from "../../util/ctx"
import { FilePath, FullSlug, joinSegments } from "../../util/path"
import { Readable } from "stream"

type WriteOptions = {
  ctx: BuildCtx
  slug: FullSlug
  ext: `.${string}` | ""
  content: string | Buffer | Readable
}

export const write = async ({ ctx, slug, ext, content }: WriteOptions): Promise<FilePath> => {
  const pathToPage = joinSegments(ctx.argv.output, slug + ext) as FilePath
  const dir = path.dirname(pathToPage)
  for (let i = 0; i < 5; i++) {
    try {
      await fs.promises.mkdir(dir, { recursive: true })
      break
    } catch (e: any) {
      if (i === 4) throw e
      await new Promise((resolve) => setTimeout(resolve, 50))
    }
  }
  await fs.promises.writeFile(pathToPage, content)
  return pathToPage
}
