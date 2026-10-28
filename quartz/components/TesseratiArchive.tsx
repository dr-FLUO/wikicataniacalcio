import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import tesseratiDb from "./tesserati_db.json"

interface TesseratoRecord {
  c: string   // Cognome
  n: string   // Nome
  i: string   // Lettera iniziale del cognome (A-Z)
  r: string   // Ruolo specifico
  cr: string  // Categoria ruolo (Portiere, Difensore, Centrocampista, Attaccante, Allenatore)
  a: number   // Presenze
  s: number   // Stagioni
  u: string   // Slug
  img: string // Immagine
}

const LETTERS = [
  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
  "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

const ROLES = [
  { id: "ALL", label: "Tutti i Ruoli" },
  { id: "Portiere", label: "Portieri" },
  { id: "Difensore", label: "Difensori" },
  { id: "Centrocampista", label: "Centrocampisti" },
  { id: "Attaccante", label: "Attaccanti" },
  { id: "Allenatore", label: "Allenatori" },
]

const TesseratiArchive: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const currentSlug = fileData.slug ?? "index"
  const isArchiveHub =
    currentSlug === "03-tesserati/calciatori/archivio/index" ||
    currentSlug === "03-tesserati/calciatori/archivio" ||
    currentSlug.endsWith("/archivio") ||
    currentSlug.endsWith("/archivio/index") ||
    currentSlug === "calciatori/archivio/index" ||
    currentSlug === "calciatori/archivio"

  if (!isArchiveHub) {
    return null
  }

  const baseDir = pathToRoot(currentSlug)
  const totalCount = tesseratiDb.length

  // Pre-render the first 48 entries for immediate SSR rendering
  const initialBatch = (tesseratiDb as TesseratoRecord[]).slice(0, 48)

  return (
    <section class="tess-archive-root" aria-label="Archivio Generale Tesserati Rossazzurri">
      {/* Intestazione Editoriale */}
      <div class="tess-header-box">
        <div class="tess-header-kicker">
          <span class="tess-pill-brand">ARCHIVIO ANAGRAFICO UFFICIALE</span>
          <span class="tess-pill-count">{totalCount} Tesserati Registrati</span>
        </div>
        <h2 class="tess-header-title">Registro Generale Tesserati (1929–2027)</h2>
        <p class="tess-header-desc">
          Tutti i calciatori e gli allenatori della storia del Catania, rigorosamente indicizzati e ordinati
          per <strong>Cognome</strong>. Utilizza la barra di ricerca rapida, i filtri per lettera iniziale,
          ruolo, presenze e fotografie storiche certificate.
        </p>
      </div>

      {/* Barra Filtri Interattiva */}
      <div class="tess-controls-panel">
        {/* Riga 1: Ricerca e Ordinamento */}
        <div class="tess-search-row">
          <div class="tess-search-box">
            <span class="tess-search-icon" aria-hidden="true">🔍</span>
            <input
              type="search"
              id="tess-search-input"
              class="tess-search-input"
              placeholder="Cerca per cognome, nome, ruolo o presenze..."
              aria-label="Cerca tesserato per cognome o nome"
              autocomplete="off"
            />
          </div>

          <div class="tess-select-group">
            <label for="tess-sort-select" class="tess-field-label">Ordina per:</label>
            <select id="tess-sort-select" class="tess-select">
              <option value="surname-asc">Cognome (A → Z)</option>
              <option value="surname-desc">Cognome (Z → A)</option>
              <option value="apps-desc">Presenze (Maggiori → Minori)</option>
              <option value="seasons-desc">Stagioni Disputate</option>
            </select>
          </div>

          <div class="tess-select-group">
            <label for="tess-apps-filter" class="tess-field-label">Presenze:</label>
            <select id="tess-apps-filter" class="tess-select">
              <option value="0">Tutte le presenze</option>
              <option value="100">100+ Presenze (Bandiere)</option>
              <option value="50">50+ Presenze</option>
              <option value="20">20+ Presenze</option>
              <option value="1">Almeno 1 presenza</option>
            </select>
          </div>

          <label class="tess-photo-toggle" title="Filtra solo i profili con ritratto fotografico storico">
            <input type="checkbox" id="tess-photo-checkbox" />
            <span class="tess-photo-label">📷 Solo con foto</span>
          </label>
        </div>

        {/* Riga 2: Barra Salti Alfabetici per COGNOME (A-Z) */}
        <div class="tess-alphabet-container">
          <span class="tess-alphabet-title">COGNOME:</span>
          <div class="tess-alphabet-bar" role="toolbar" aria-label="Filtro lettera iniziale cognome">
            <button
              type="button"
              class="tess-letter-btn is-active"
              data-letter="ALL"
              aria-pressed="true"
            >
              TUTTI
            </button>
            {LETTERS.map((letter) => (
              <button
                type="button"
                class="tess-letter-btn"
                data-letter={letter}
                aria-pressed="false"
              >
                {letter}
              </button>
            ))}
          </div>
        </div>

        {/* Riga 3: Filtro per Ruolo Tattico */}
        <div class="tess-roles-bar" role="group" aria-label="Filtro ruolo tattico">
          <span class="tess-roles-title">RUOLO:</span>
          <div class="tess-roles-list">
            {ROLES.map((r) => (
              <button
                type="button"
                class={`tess-role-btn ${r.id === "ALL" ? "is-active" : ""}`}
                data-role={r.id}
                aria-pressed={r.id === "ALL" ? "true" : "false"}
              >
                {r.label}
              </button>
            ))}
          </div>
        </div>

        {/* Riga 4: Contatore dinamico e Pulsante Reset */}
        <div class="tess-status-bar">
          <div id="tess-counter" class="tess-counter" aria-live="polite">
            Mostrati <strong>{initialBatch.length}</strong> di <strong>{totalCount}</strong> tesserati (ordinamento per Cognome)
          </div>
          <button type="button" id="tess-reset-btn" class="tess-reset-btn" style="display: none;">
            ✕ Azzera tutti i filtri
          </button>
        </div>
      </div>

      {/* Griglia delle Schede Tesserati */}
      <div id="tess-cards-grid" class="tess-cards-grid" data-basedir={baseDir}>
        {initialBatch.map((p) => {
          const href = `${baseDir}/${p.u}`
          const roleClass = p.cr.toLowerCase()
          return (
            <a href={href} class="tess-card" data-slug={p.u}>
              <div class="tess-card__avatar">
                {p.img ? (
                  <img
                    src={`${baseDir}/${p.img}`}
                    alt={`${p.n} ${p.c}`}
                    loading="lazy"
                    class="tess-card__img"
                  />
                ) : (
                  <div class={`tess-card__initials tess-card__initials--${roleClass}`}>
                    {p.c.substring(0, 1)}
                    {p.n ? p.n.substring(0, 1) : ""}
                  </div>
                )}
              </div>
              <div class="tess-card__body">
                <div class="tess-card__name">
                  <span class="tess-card__cognome">{p.c}</span>
                  {p.n && <span class="tess-card__nome">{p.n}</span>}
                </div>
                <div class="tess-card__tags">
                  <span class={`tess-badge tess-badge--${roleClass}`}>{p.cr}</span>
                  <span class="tess-badge tess-badge--apps">{p.a} presenze</span>
                  {p.s > 1 && (
                    <span class="tess-badge tess-badge--seasons">{p.s} stag.</span>
                  )}
                </div>
              </div>
              <span class="tess-card__arrow" aria-hidden="true">→</span>
            </a>
          )
        })}
      </div>

      {/* Pulsante Carica Altri */}
      <div class="tess-pagination-wrap">
        <button type="button" id="tess-load-more" class="tess-load-more-btn">
          Carica altri tesserati ↓
        </button>
      </div>

      {/* Payload JSON incorporato per idratazione istantanea (zero lag di rete) */}
      <script
        id="tesserati-database-json"
        type="application/json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(tesseratiDb) }}
      />
    </section>
  )
}

const clientScript = `
(function() {
  function initTesseratiArchive() {
    var root = document.querySelector('.tess-archive-root');
    if (!root) return;

    var scriptEl = document.getElementById('tesserati-database-json');
    if (!scriptEl) return;

    var db;
    try {
      db = JSON.parse(scriptEl.textContent || '[]');
    } catch(e) {
      console.error('Errore parsing database tesserati:', e);
      return;
    }

    var grid = document.getElementById('tess-cards-grid');
    var baseDir = grid ? (grid.getAttribute('data-basedir') || '.') : '.';
    var searchInput = document.getElementById('tess-search-input');
    var sortSelect = document.getElementById('tess-sort-select');
    var appsFilter = document.getElementById('tess-apps-filter');
    var photoCheckbox = document.getElementById('tess-photo-checkbox');
    var letterBtns = document.querySelectorAll('.tess-letter-btn');
    var roleBtns = document.querySelectorAll('.tess-role-btn');
    var counterEl = document.getElementById('tess-counter');
    var resetBtn = document.getElementById('tess-reset-btn');
    var loadMoreBtn = document.getElementById('tess-load-more');

    var state = {
      search: '',
      letter: 'ALL',
      role: 'ALL',
      minApps: 0,
      onlyPhoto: false,
      sort: 'surname-asc',
      limit: 48
    };

    function normalizeText(s) {
      if (!s) return '';
      return s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
    }

    function filterAndSort() {
      var q = normalizeText(state.search);
      var results = db.filter(function(item) {
        if (state.letter !== 'ALL' && item.i !== state.letter) {
          return false;
        }
        if (state.role !== 'ALL' && item.cr !== state.role) {
          return false;
        }
        if (state.minApps > 0 && item.a < state.minApps) {
          return false;
        }
        if (state.onlyPhoto && !item.img) {
          return false;
        }
        if (q) {
          var target = normalizeText(item.c + ' ' + item.n + ' ' + item.r + ' ' + item.cr);
          if (target.indexOf(q) === -1) {
            return false;
          }
        }
        return true;
      });

      // Sorting
      results.sort(function(a, b) {
        if (state.sort === 'surname-asc') {
          var ca = normalizeText(a.c), cb = normalizeText(b.c);
          if (ca !== cb) return ca.localeCompare(cb);
          return normalizeText(a.n).localeCompare(normalizeText(b.n));
        } else if (state.sort === 'surname-desc') {
          var ca = normalizeText(a.c), cb = normalizeText(b.c);
          if (ca !== cb) return cb.localeCompare(ca);
          return normalizeText(b.n).localeCompare(normalizeText(a.n));
        } else if (state.sort === 'apps-desc') {
          if (b.a !== a.a) return b.a - a.a;
          return normalizeText(a.c).localeCompare(normalizeText(b.c));
        } else if (state.sort === 'seasons-desc') {
          if (b.s !== a.s) return b.s - a.s;
          return normalizeText(a.c).localeCompare(normalizeText(b.c));
        }
        return 0;
      });

      return results;
    }

    function renderCard(p) {
      var href = baseDir + '/' + p.u;
      var roleClass = p.cr.toLowerCase();
      var avatarHtml = '';
      if (p.img) {
        avatarHtml = '<img src=\"' + baseDir + '/' + p.img + '\" alt=\"' + p.n + ' ' + p.c + '\" loading=\"lazy\" class=\"tess-card__img\" />';
      } else {
        var init = p.c.charAt(0) + (p.n ? p.n.charAt(0) : '');
        avatarHtml = '<div class=\"tess-card__initials tess-card__initials--' + roleClass + '\">' + init + '</div>';
      }

      var seasonsHtml = p.s > 1 ? '<span class=\"tess-badge tess-badge--seasons\">' + p.s + ' stag.</span>' : '';

      return '<a href=\"' + href + '\" class=\"tess-card\" data-slug=\"' + p.u + '\">' +
        '<div class=\"tess-card__avatar\">' + avatarHtml + '</div>' +
        '<div class=\"tess-card__body\">' +
          '<div class=\"tess-card__name\">' +
            '<span class=\"tess-card__cognome\">' + p.c + '</span>' +
            (p.n ? '<span class=\"tess-card__nome\">' + p.n + '</span>' : '') +
          '</div>' +
          '<div class=\"tess-card__tags\">' +
            '<span class=\"tess-badge tess-badge--' + roleClass + '\">' + p.cr + '</span>' +
            '<span class=\"tess-badge tess-badge--apps\">' + p.a + ' presenze</span>' +
            seasonsHtml +
          '</div>' +
        '</div>' +
        '<span class=\"tess-card__arrow\" aria-hidden=\"true\">→</span>' +
      '</a>';
    }

    function updateView() {
      var filtered = filterAndSort();
      var totalMatches = filtered.length;
      var visible = filtered.slice(0, state.limit);

      if (grid) {
        if (visible.length === 0) {
          grid.innerHTML = '<div class=\"tess-empty-state\">' +
            '<div class=\"tess-empty-icon\">🔍</div>' +
            '<h3>Nessun tesserato trovato</h3>' +
            '<p>Nessun calciatore o allenatore corrisponde ai filtri selezionati. Prova a modificare la ricerca o azzera i filtri.</p>' +
          '</div>';
        } else {
          var html = '';
          for (var i = 0; i < visible.length; i++) {
            html += renderCard(visible[i]);
          }
          grid.innerHTML = html;
        }
      }

      if (counterEl) {
        counterEl.innerHTML = 'Mostrati <strong>' + visible.length + '</strong> di <strong>' + totalMatches + '</strong> tesserati (totale archivio: ' + db.length + ')';
      }

      if (loadMoreBtn) {
        if (state.limit >= totalMatches) {
          loadMoreBtn.style.display = 'none';
        } else {
          loadMoreBtn.style.display = 'inline-flex';
          loadMoreBtn.textContent = 'Carica altri tesserati (' + (totalMatches - state.limit) + ' rimanenti) ↓';
        }
      }

      var hasActiveFilters = state.search || state.letter !== 'ALL' || state.role !== 'ALL' || state.minApps > 0 || state.onlyPhoto || state.sort !== 'surname-asc';
      if (resetBtn) {
        resetBtn.style.display = hasActiveFilters ? 'inline-flex' : 'none';
      }
    }

    // Event Listeners
    if (searchInput) {
      searchInput.addEventListener('input', function(e) {
        state.search = e.target.value.trim();
        state.limit = 48;
        updateView();
      });
    }

    if (sortSelect) {
      sortSelect.addEventListener('change', function(e) {
        state.sort = e.target.value;
        updateView();
      });
    }

    if (appsFilter) {
      appsFilter.addEventListener('change', function(e) {
        state.minApps = parseInt(e.target.value, 10) || 0;
        state.limit = 48;
        updateView();
      });
    }

    if (photoCheckbox) {
      photoCheckbox.addEventListener('change', function(e) {
        state.onlyPhoto = e.target.checked;
        state.limit = 48;
        updateView();
      });
    }

    letterBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var letter = btn.getAttribute('data-letter');
        state.letter = letter;
        state.limit = 48;
        letterBtns.forEach(function(b) {
          b.classList.remove('is-active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('is-active');
        btn.setAttribute('aria-pressed', 'true');
        updateView();
      });
    });

    roleBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var role = btn.getAttribute('data-role');
        state.role = role;
        state.limit = 48;
        roleBtns.forEach(function(b) {
          b.classList.remove('is-active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('is-active');
        btn.setAttribute('aria-pressed', 'true');
        updateView();
      });
    });

    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', function() {
        state.limit += 48;
        updateView();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', function() {
        state.search = '';
        state.letter = 'ALL';
        state.role = 'ALL';
        state.minApps = 0;
        state.onlyPhoto = false;
        state.sort = 'surname-asc';
        state.limit = 48;

        if (searchInput) searchInput.value = '';
        if (sortSelect) sortSelect.value = 'surname-asc';
        if (appsFilter) appsFilter.value = '0';
        if (photoCheckbox) photoCheckbox.checked = false;

        letterBtns.forEach(function(b) {
          var isAll = b.getAttribute('data-letter') === 'ALL';
          b.classList.toggle('is-active', isAll);
          b.setAttribute('aria-pressed', isAll ? 'true' : 'false');
        });

        roleBtns.forEach(function(b) {
          var isAll = b.getAttribute('data-role') === 'ALL';
          b.classList.toggle('is-active', isAll);
          b.setAttribute('aria-pressed', isAll ? 'true' : 'false');
        });

        updateView();
      });
    }
  }

  document.addEventListener('nav', initTesseratiArchive);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTesseratiArchive);
  } else {
    initTesseratiArchive();
  }
})();
`

TesseratiArchive.afterDOMLoaded = clientScript

TesseratiArchive.css = `
.tess-archive-root {
  width: 100%;
  margin: 1.5rem 0 3rem 0;
  box-sizing: border-box;
}

.tess-header-box {
  background: var(--wiki-surface-elevated);
  border: 1.5px solid var(--wiki-border-strong);
  padding: 1.5rem 1.75rem;
  margin-bottom: 1.5rem;
  box-shadow: 2px 2px 0 var(--wiki-border-strong);
}

.tess-header-kicker {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.tess-pill-brand {
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: var(--dark);
  color: var(--light);
  padding: 0.2rem 0.55rem;
}

.tess-pill-count {
  font-family: var(--font-display);
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: var(--rossazzurro-red);
  border: 1.5px solid var(--rossazzurro-red);
  padding: 0.15rem 0.5rem;
  background: var(--wiki-surface-elevated);
}

.tess-header-title {
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.2vw, 2.6rem);
  font-weight: 900;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: var(--dark);
  margin: 0 0 0.5rem 0;
  line-height: 1.1;
}

.tess-header-desc {
  font-size: 1rem;
  line-height: 1.55;
  color: var(--darkgray);
  margin: 0;
}

.tess-controls-panel {
  background: var(--wiki-surface-elevated);
  border: 1.5px solid var(--wiki-border-strong);
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 2px 2px 0 var(--wiki-border-strong);
}

.tess-search-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.tess-search-box {
  flex: 1 1 280px;
  position: relative;
  display: flex;
  align-items: center;
}

.tess-search-icon {
  position: absolute;
  left: 0.85rem;
  font-size: 0.95rem;
  pointer-events: none;
  opacity: 0.7;
}

.tess-search-input {
  width: 100%;
  padding: 0.65rem 0.85rem 0.65rem 2.4rem;
  border: 1.5px solid var(--wiki-border-strong);
  background: var(--light);
  color: var(--dark);
  font-family: var(--font-body);
  font-size: 0.95rem;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;

  &:focus {
    border-color: var(--rossazzurro-blue);
    box-shadow: 0 0 0 2px rgba(12, 178, 217, 0.2);
  }
}

.tess-select-group {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.tess-field-label {
  font-family: var(--font-display);
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--dark);
  white-space: nowrap;
}

.tess-select {
  padding: 0.55rem 0.75rem;
  border: 1.5px solid var(--wiki-border-strong);
  background: var(--light);
  color: var(--dark);
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  outline: none;
  cursor: pointer;
}

.tess-photo-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  cursor: pointer;
  user-select: none;
  padding: 0.45rem 0.65rem;
  border: 1px solid var(--wiki-border-hairline);
  background: var(--light);

  input[type="checkbox"] {
    cursor: pointer;
    accent-color: var(--rossazzurro-red);
  }

  .tess-photo-label {
    font-family: var(--font-display);
    font-size: 0.85rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--dark);
  }
}

.tess-alphabet-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding-top: 0.5rem;
  border-top: 1px solid var(--wiki-border-hairline);
}

.tess-alphabet-title,
.tess-roles-title {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: var(--dark);
  white-space: nowrap;
}

.tess-alphabet-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.tess-letter-btn {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 800;
  min-width: 28px;
  height: 28px;
  padding: 0 0.4rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--wiki-border-hairline);
  background: var(--light);
  color: var(--dark);
  cursor: pointer;
  transition: all 0.15s ease;

  &:hover {
    background: var(--rossazzurro-red);
    color: #fff;
    border-color: var(--rossazzurro-red);
  }

  &.is-active {
    background: var(--dark);
    color: var(--light);
    border-color: var(--dark);
    font-weight: 900;
  }
}

.tess-roles-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding-top: 0.5rem;
  border-top: 1px solid var(--wiki-border-hairline);
}

.tess-roles-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tess-role-btn {
  font-family: var(--font-display);
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 0.35rem 0.65rem;
  border: 1.5px solid var(--wiki-border-strong);
  background: var(--light);
  color: var(--dark);
  cursor: pointer;
  transition: all 0.15s ease;

  &:hover {
    background: var(--rossazzurro-blue);
    color: #fff;
    border-color: var(--rossazzurro-blue);
  }

  &.is-active {
    background: var(--rossazzurro-blue);
    color: #fff;
    border-color: var(--rossazzurro-blue);
  }
}

.tess-status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--wiki-border-hairline);
}

.tess-counter {
  font-family: var(--font-mono, monospace);
  font-size: 0.85rem;
  color: var(--darkgray);

  strong {
    color: var(--dark);
    font-weight: 700;
  }
}

.tess-reset-btn {
  font-family: var(--font-display);
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background: none;
  border: 1px solid var(--rossazzurro-red);
  color: var(--rossazzurro-red);
  padding: 0.25rem 0.65rem;
  cursor: pointer;

  &:hover {
    background: var(--rossazzurro-red);
    color: #fff;
  }
}

.tess-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 1rem;
  width: 100%;
}

.tess-card {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  background: var(--wiki-surface-elevated);
  border: 1.5px solid var(--wiki-border-strong);
  padding: 0.75rem 0.95rem;
  text-decoration: none !important;
  color: var(--dark) !important;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  position: relative;
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.05);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 3px 3px 0 var(--wiki-border-strong);
    border-color: var(--rossazzurro-red);

    .tess-card__arrow {
      color: var(--rossazzurro-red);
      transform: translateX(3px);
    }
  }
}

.tess-card__avatar {
  flex: 0 0 46px;
  width: 46px;
  height: 46px;
  border: 1px solid var(--wiki-border-strong);
  background: var(--light);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tess-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.tess-card__initials {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 900;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--dark);

  &--portiere { color: #d97706; }
  &--difensore { color: var(--rossazzurro-blue); }
  &--centrocampista { color: #059669; }
  &--attaccante { color: var(--rossazzurro-red); }
  &--allenatore { color: #7c3aed; }
}

.tess-card__body {
  flex: 1 1 auto;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.tess-card__name {
  display: flex;
  align-items: baseline;
  gap: 0.35rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tess-card__cognome {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--dark);
}

.tess-card__nome {
  font-family: var(--font-body);
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--darkgray);
}

.tess-card__tags {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.tess-badge {
  font-family: var(--font-display);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 0.15rem 0.4rem;
  line-height: 1;

  &--portiere {
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #f59e0b;
  }
  &--difensore {
    background: rgba(12, 178, 217, 0.12);
    color: #0284c7;
    border: 1px solid var(--rossazzurro-blue);
  }
  &--centrocampista {
    background: #d1fae5;
    color: #065f46;
    border: 1px solid #10b981;
  }
  &--attaccante {
    background: rgba(217, 4, 41, 0.1);
    color: var(--rossazzurro-red);
    border: 1px solid var(--rossazzurro-red);
  }
  &--allenatore {
    background: #ede9fe;
    color: #5b21b6;
    border: 1px solid #8b5cf6;
  }
  &--apps {
    background: var(--light);
    color: var(--dark);
    border: 1px solid var(--wiki-border-hairline);
    font-weight: 800;
  }
  &--seasons {
    background: var(--light);
    color: var(--gray);
    border: 1px solid var(--wiki-border-hairline);
  }
}

.tess-card__arrow {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 900;
  color: var(--gray);
  transition: transform 0.15s ease, color 0.15s ease;
}

.tess-pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.tess-load-more-btn {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 900;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  background: var(--wiki-surface-elevated);
  border: 2px solid var(--wiki-border-strong);
  color: var(--dark);
  padding: 0.75rem 2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0 var(--wiki-border-strong);

  &:hover {
    background: var(--rossazzurro-red);
    color: #fff;
    border-color: var(--rossazzurro-red);
    transform: translateY(-2px);
    box-shadow: 3px 3px 0 var(--dark);
  }
}

.tess-empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3.5rem 1.5rem;
  background: var(--wiki-surface-elevated);
  border: 1.5px dashed var(--wiki-border-strong);

  .tess-empty-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
  }

  h3 {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 900;
    text-transform: uppercase;
    color: var(--dark);
    margin: 0 0 0.5rem 0;
  }

  p {
    color: var(--darkgray);
    margin: 0;
    font-size: 0.95rem;
  }
}

@media (max-width: 768px) {
  .tess-search-row {
    flex-direction: column;
    align-items: stretch;
  }
  .tess-select-group {
    width: 100%;
    justify-content: space-between;
  }
  .tess-select {
    flex: 1;
  }
  .tess-cards-grid {
    grid-template-columns: 1fr;
  }
}
`

export default (() => TesseratiArchive) satisfies QuartzComponentConstructor
