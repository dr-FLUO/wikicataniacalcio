import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const Header: QuartzComponent = ({ children }: QuartzComponentProps) => {
  return children.length > 0 ? <div class="nfc-top-shell">{children}</div> : null
}

Header.css = `
.nfc-top-shell {
  width: 100%;
}
`

export default (() => Header) satisfies QuartzComponentConstructor
