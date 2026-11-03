// quartz/components/scripts/topbar.inline.ts

function initTopBarNav() {
  const nav = document.querySelector(".nfc-masthead__nav")
  if (!nav) return

  const itemWraps = nav.querySelectorAll<HTMLElement>(".nfc-nav-item-wrap")
  if (itemWraps.length === 0) return

  const closeAllDropdowns = () => {
    itemWraps.forEach((wrap) => {
      wrap.classList.remove("is-open")
      const trigger = wrap.querySelector<HTMLElement>(".nfc-nav-cell")
      if (trigger) {
        trigger.setAttribute("aria-expanded", "false")
      }
    })
    // Rimuove il focus residuo da link interni per evitare che :focus-within tenga aperto il menu
    if (document.activeElement && nav.contains(document.activeElement)) {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur()
      }
    }
  }

  const openDropdown = (wrap: HTMLElement) => {
    itemWraps.forEach((w) => {
      if (w !== wrap) {
        w.classList.remove("is-open")
        const tr = w.querySelector<HTMLElement>(".nfc-nav-cell")
        if (tr) tr.setAttribute("aria-expanded", "false")
      }
    })
    wrap.classList.add("is-open")
    const trigger = wrap.querySelector<HTMLElement>(".nfc-nav-cell")
    if (trigger) {
      trigger.setAttribute("aria-expanded", "true")
    }
  }

  itemWraps.forEach((wrap) => {
    const trigger = wrap.querySelector<HTMLAnchorElement>(".nfc-nav-cell")
    const dropdown = wrap.querySelector<HTMLElement>(".nfc-nav-dropdown")
    if (!dropdown || !trigger) return

    let closeTimer: number | undefined

    // Hover Mouse Enter (Desktop)
    wrap.addEventListener("mouseenter", () => {
      if (closeTimer) {
        window.clearTimeout(closeTimer)
        closeTimer = undefined
      }
      openDropdown(wrap)
    })

    // Hover Mouse Leave: chiusura immediata e pulita
    wrap.addEventListener("mouseleave", () => {
      closeTimer = window.setTimeout(() => {
        wrap.classList.remove("is-open")
        trigger.setAttribute("aria-expanded", "false")
        if (document.activeElement && wrap.contains(document.activeElement)) {
          if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur()
          }
        }
      }, 80)
    })

    wrap.addEventListener("mousemove", () => {
      if (closeTimer) {
        window.clearTimeout(closeTimer)
        closeTimer = undefined
      }
    })

    // Click su qualsiasi link interno o sul trigger: chiusura istantanea di tutti i dropdown
    const links = wrap.querySelectorAll<HTMLAnchorElement>("a")
    links.forEach((link) => {
      link.addEventListener("click", () => {
        closeAllDropdowns()
      })
    })

    // Supporto Touch / Mobile
    trigger.addEventListener(
      "touchstart",
      (e) => {
        const isOpen = wrap.classList.contains("is-open")
        if (!isOpen) {
          // Primo tap: apre il menu a tendina
          e.preventDefault()
          openDropdown(wrap)
        }
        // Secondo tap sul link già aperto: procede con la normale navigazione
      },
      { passive: false }
    )
  })

  // Event listener globali (registrati una sola volta sul window)
  if (!(window as any).__nfcTopBarEventsBound) {
    ;(window as any).__nfcTopBarEventsBound = true

    // Click fuori dall'area di navigazione: chiude tutto
    document.addEventListener("click", (e) => {
      if (!nav.contains(e.target as Node)) {
        closeAllDropdowns()
      }
    })

    document.addEventListener(
      "touchstart",
      (e) => {
        if (!nav.contains(e.target as Node)) {
          closeAllDropdowns()
        }
      },
      { passive: true }
    )

    // Tasto Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeAllDropdowns()
      }
    })

    // Evento Quartz di navigazione SPA (cambio pagina istantaneo)
    document.addEventListener("nav", () => {
      closeAllDropdowns()
    })
  }
}

// Inizializzazione al caricamento e ad ogni transizione Quartz SPA
document.addEventListener("nav", initTopBarNav)
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initTopBarNav)
} else {
  initTopBarNav()
}
