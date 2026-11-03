import re

path = "quartz/components/MagazineHome.tsx"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add shuffle button in section header
old_actions = """          <div class="nfc-section-header__actions">
            <a href="./02-cronistoria/partite-storiche/index" class="nfc-link-arrow">
              TUTTI I DOSSIER STORICI →
            </a>
          </div>"""

new_actions = """          <div class="nfc-section-header__actions">
            <button
              id="nfc-shuffle-stories-btn"
              class="nfc-action-btn"
              type="button"
              title="Estrai altri dossier e storie casuali dall'archivio"
            >
              🎲 MESCOLA STORIE
            </button>
            <a href="./02-cronistoria/partite-storiche/index" class="nfc-link-arrow">
              TUTTI I DOSSIER STORICI →
            </a>
          </div>"""

assert old_actions in text, "old_actions block not found"
text = text.replace(old_actions, new_actions, 1)

# 2. Replace client-side script with true randomizer
script_pattern = re.compile(r"<script\s*dangerouslySetInnerHTML=\{\{\s*__html:\s*`\(function\(\)\s*\{.*?\}\)\(\);\s*`\s*\}\}\s*/>", re.DOTALL)

new_script = """<script
          dangerouslySetInnerHTML={{
            __html: `
(function() {
  function shuffle(arr) {
    var copy = arr.slice();
    for (var i = copy.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = copy[i];
      copy[i] = copy[j];
      copy[j] = t;
    }
    return copy;
  }

  function randomizeContent() {
    var storiesGrid = document.querySelector(".nfc-stories-grid");
    var portraitsGrid = document.querySelector(".nfc-portraits-grid");
    var coverPoolEl = document.getElementById("nfc-cover-pool");
    var portraitsPoolEl = document.getElementById("nfc-portraits-pool");

    if (storiesGrid && coverPoolEl) {
      try {
        var pool = JSON.parse(coverPoolEl.textContent || "[]");
        if (pool.length) {
          var selected = shuffle(pool).slice(0, 6);
          storiesGrid.style.transition = "opacity 0.15s ease";
          storiesGrid.style.opacity = "0.2";
          setTimeout(function() {
            storiesGrid.innerHTML = selected.map(function(s) {
              return '<article class="nfc-story-card" data-story-id="' + s.id + '">' +
                '<a href="' + s.href + '" class="nfc-story-card__link">' +
                  '<div class="nfc-story-card__media">' +
                    '<img src="' + s.image + '" alt="' + s.title.replace(/"/g, '&quot;') + '" loading="lazy" />' +
                    '<div class="nfc-story-card__badge">' +
                      '<span>' + s.category + '</span>' +
                      '<span>' + s.issue + '</span>' +
                    '</div>' +
                  '</div>' +
                  '<div class="nfc-story-card__body">' +
                    '<h3 class="nfc-story-card__title">' + s.title + '</h3>' +
                    '<p class="nfc-story-card__excerpt">' + s.excerpt + '</p>' +
                    '<div class="nfc-story-card__footer">' +
                      '<span class="nfc-story-card__cta">LEGGI IL DOSSIER →</span>' +
                      '<span class="nfc-story-card__credit">' + s.credit + '</span>' +
                    '</div>' +
                  '</div>' +
                '</a>' +
              '</article>';
            }).join("");
            storiesGrid.style.opacity = "1";
          }, 120);
        }
      } catch(e) {}
    }

    if (portraitsGrid && portraitsPoolEl) {
      try {
        var pPool = JSON.parse(portraitsPoolEl.textContent || "[]");
        if (pPool.length) {
          var pSelected = shuffle(pPool).slice(0, 4);
          portraitsGrid.style.transition = "opacity 0.15s ease";
          portraitsGrid.style.opacity = "0.2";
          setTimeout(function() {
            portraitsGrid.innerHTML = pSelected.map(function(p) {
              return '<a href="' + p.href + '" class="nfc-portrait-card" data-person-id="' + p.id + '">' +
                '<div class="nfc-portrait-card__media">' +
                  '<img src="' + p.image + '" alt="' + p.name + '" loading="lazy" />' +
                '</div>' +
                '<div class="nfc-portrait-card__meta">' +
                  '<span class="nfc-portrait-card__name">' + p.name + '</span>' +
                  '<span class="nfc-portrait-card__role">' + p.role + '</span>' +
                  '<span class="nfc-portrait-card__stat">' + p.stat + '</span>' +
                '</div>' +
              '</a>';
            }).join("");
            portraitsGrid.style.opacity = "1";
          }, 120);
        }
      } catch(e) {}
    }
  }

  function bindEvents() {
    randomizeContent();
    var btn = document.getElementById("nfc-shuffle-stories-btn");
    if (btn) {
      btn.onclick = function(e) {
        e.preventDefault();
        randomizeContent();
      };
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindEvents);
  } else {
    bindEvents();
  }
  document.addEventListener("nav", bindEvents);
})();
`
          }}
        />"""

m = script_pattern.search(text)
assert m, "script_pattern not matched in MagazineHome.tsx"
text = script_pattern.sub(new_script, text, count=1)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Randomized MagazineHome.tsx with shuffle button!")
