import { Components, Jsx, toJsxRuntime } from "hast-util-to-jsx-runtime"
import { Node, Root } from "hast"
import { Fragment, jsx, jsxs } from "preact/jsx-runtime"
import { trace } from "./trace"
import { type FilePath } from "./path"

const customComponents: Components = {
  table: (props) => {
    // Se la tabella appartiene alla scheda anagrafica calciatore o allenatore, non racchiuderla in .table-container
    // per evitare doppi bordi, sporgenze o scrollbar proprietarie
    if (props.className?.includes("nfc-player-table") || props.className?.includes("nfc-coach-table")) {
      return <table {...props} />
    }
    return (
      <div class="table-container">
        <table {...props} />
      </div>
    )
  },
}

export function htmlToJsx(fp: FilePath, tree: Node) {
  try {
    return toJsxRuntime(tree as Root, {
      Fragment,
      jsx: jsx as Jsx,
      jsxs: jsxs as Jsx,
      elementAttributeNameCase: "html",
      components: customComponents,
    })
  } catch (e) {
    trace(`Failed to parse Markdown in \`${fp}\` into JSX`, e as Error)
  }
}
