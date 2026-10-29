import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/footer.scss"
import { resolveRelative, FullSlug } from "../util/path"

interface Options {
  links: Record<string, string>
}

export default ((opts?: Options) => {
  const Footer: QuartzComponent = ({ displayClass, fileData }: QuartzComponentProps) => {
    const year = new Date().getFullYear()
    const links = opts?.links ?? {}
    const currentSlug = (fileData.slug ?? "index") as FullSlug
    const legalHref = resolveRelative(currentSlug, "note-legali-privacy-accessibilita" as FullSlug)
    const reportHref = resolveRelative(currentSlug, "segnala-correzione" as FullSlug)
    const homeHref = resolveRelative(currentSlug, "index" as FullSlug)

    return (
      <footer class={`${displayClass ?? ""} rossazzurri-footer`} role="contentinfo">
        <div class="footer-compliance-box">
          <div class="footer-brand-row">
            <span class="footer-kicker">COLOPHON EDITORIALE · EDIZIONE {year} (BETA PUBBLICA)</span>
            <p class="footer-brand">
              <strong>WIKI CATANIA CALCIO (1929–OGGI)</strong> — Magazine culturale, statistico e
              giuridico dedicato alla storia dell&apos;Elefante.
            </p>
          </div>
          <p class="footer-legal-notice">
            <strong>Conformità Normativa UE &amp; Diritto d&apos;Autore:</strong> Pubblicazione
            culturale e di ricerca storica senza fini di lucro ai sensi dell&apos;
            <strong>Art. 70 L. 633/1941</strong> e della <strong>Direttiva UE 2019/790</strong>.
            Tutte le fonti bibliografiche e i crediti fotografici (Artt. 87–92 L. 633/1941 e licenze
            Creative Commons) sono citati obbligatoriamente in ogni dossier. Architettura{" "}
            <strong>100% Cookie-Less &amp; Zero-Tracking</strong> conforme al{" "}
            <strong>GDPR (Reg. UE 2016/679)</strong> (uso esclusivo di <em>localStorage</em>{" "}
            tecnico per il tema Light/Dark; font <em>Big Shoulders Display</em> e{" "}
            <em>Plus Jakarta Sans</em> ospitati in locale senza trasmissione di IP a terze parti).
            Interfaccia conforme agli standard <strong>WCAG 2.1 Livello AA / AAA</strong> ed{" "}
            <strong>European Accessibility Act (Direttiva UE 2019/882)</strong>.
          </p>
          <p class="footer-beta-notice">
            <strong>Stato di Sviluppo (Versione Beta):</strong> Il portale è attualmente in versione Beta: nuove monografie, statistiche e dati d&apos;archivio vengono integrati e certificati quotidianamente.
          </p>
        </div>
        <div class="footer-action-row">
          <a
            href={`${reportHref}?voce=${encodeURIComponent(String(fileData.slug ?? "index"))}`}
            class="footer-redazione-btn"
            title="Contatta la redazione, invia una correzione o proponi una fonte"
          >
            <span class="footer-redazione-btn__icon" aria-hidden="true">✎</span>
            <span>REDAZIONE &amp; FACT-CHECKING · SEGNALA CORREZIONE O FONTE →</span>
          </a>
        </div>
        <ul class="footer-links" aria-label="Collegamenti istituzionali e legali">
          <li>
            <a href={homeHref}>Copertina Magazine</a>
          </li>
          <li>
            <a href={legalHref}>Privacy (GDPR), Cookie-Less, Accessibilità &amp; Copyright</a>
          </li>
          <li>
            <a href={`${reportHref}?voce=${encodeURIComponent(String(fileData.slug ?? "index"))}`}>
              Segnala Errore / Proponi Fonte
            </a>
          </li>
          {Object.entries(links).map(([text, link]) => (
            <li>
              <a href={link} rel="noopener noreferrer">
                {text}
              </a>
            </li>
          ))}
          <li>
            <span>© {year} Wiki Catania Calcio</span>
          </li>
        </ul>
      </footer>
    )
  }

  Footer.css = style
  return Footer
}) satisfies QuartzComponentConstructor
