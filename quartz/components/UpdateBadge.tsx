import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const UpdateBadge: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <div class={classNames(displayClass, "catania-update-badge-container")}>
      <span class="catania-update-badge" title="Archivio Storico ed Enciclopedico costantemente aggiornato e certificato">
        <span class="catania-update-badge-dot"></span>
        <span class="catania-update-badge-text">Live: Ottobre 2026</span>
      </span>
    </div>
  )
}

UpdateBadge.css = `
.catania-update-badge-container {
  margin: 0.35rem 0 0.85rem 0;
  display: flex;
  align-items: center;
}
.catania-update-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.2rem 0.6rem;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 700;
  color: #10b981;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  font-family: var(--bodyFont);
}
:root[saved-theme="dark"] .catania-update-badge {
  background: rgba(16, 185, 129, 0.18);
  border-color: rgba(16, 185, 129, 0.45);
  color: #34d399;
}
.catania-update-badge-dot {
  width: 7px;
  height: 7px;
  background-color: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: cataniaPulse 2s infinite;
}
@keyframes cataniaPulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
  }
}
`

export default (() => UpdateBadge) satisfies QuartzComponentConstructor
