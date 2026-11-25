import { ComponentChildren } from "preact"
import { Root } from "hast"
import { htmlToJsx } from "../../util/jsx"
import { stripRedundantBodyH1 } from "../../util/seo"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"

const Content: QuartzComponent = ({ fileData, tree }: QuartzComponentProps) => {
  const content = htmlToJsx(fileData.filePath!, stripRedundantBodyH1(tree as Root)) as ComponentChildren
  const classes: string[] = fileData.frontmatter?.cssclasses ?? []
  const classString = ["popover-hint", ...classes].join(" ")
  return (
    <article id="main-article-content" role="main" class={classString}>
      {content}
    </article>
  )
}

export default (() => Content) satisfies QuartzComponentConstructor
