import fs from "fs"
import sharp from "sharp"
import { joinSegments, QUARTZ, FullSlug } from "../../util/path"
import { QuartzEmitterPlugin } from "../types"
import { write } from "./helpers"
import { BuildCtx } from "../../util/ctx"

export const Favicon: QuartzEmitterPlugin = () => ({
  name: "Favicon",
  async *emit({ argv }) {
    const staticIcoPath = joinSegments(QUARTZ, "static", "favicon.ico")
    let faviconContent: Buffer

    if (fs.existsSync(staticIcoPath)) {
      faviconContent = await fs.promises.readFile(staticIcoPath)
    } else {
      const iconPath = joinSegments(QUARTZ, "static", "icon.png")
      faviconContent = await sharp(iconPath).resize(48, 48).toFormat("png").toBuffer()
    }

    yield write({
      ctx: { argv } as BuildCtx,
      slug: "favicon" as FullSlug,
      ext: ".ico",
      content: faviconContent,
    })
  },
  async *partialEmit() {},
})
