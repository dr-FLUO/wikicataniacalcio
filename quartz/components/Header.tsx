import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const Header: QuartzComponent = ({ children }: QuartzComponentProps) => {
  return children.length > 0 ? (
    <div class="nfc-top-wrapper">
      <div class="nfc-top-stripe" aria-hidden="true" />
      <div class="nfc-top-shell">{children}</div>
    </div>
  ) : null
}

Header.css = `
.nfc-top-wrapper {
  position: sticky;
  top: 0;
  z-index: 120;
  width: 100%;
}
.nfc-top-stripe {
  height: 4px;
  width: 100%;
  background: linear-gradient(
    90deg,
    var(--rossazzurro-red) 0%,
    var(--rossazzurro-red) 50%,
    var(--rossazzurro-blue) 50%,
    var(--rossazzurro-blue) 100%
  );
}
.nfc-top-shell {
  width: 100%;
}
`

export default (() => Header) satisfies QuartzComponentConstructor
