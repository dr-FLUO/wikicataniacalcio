import os

path = "quartz/components/MagazineHome.tsx"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace stories actions
old_stories_actions = """          <div class="nfc-section-header__actions">
            <a href="./02-cronistoria/partite-storiche/index" class="nfc-link-arrow">
              TUTTI I DOSSIER STORICI →
            </a>
          </div>"""

new_stories_actions = """          <div class="nfc-section-header__actions">
            <button
              id="nfc-shuffle-stories-btn"
              class="nfc-rotate-btn"
              type="button"
              title="Estrai altri dossier e storie casuali dall'archivio"
            >
              <span class="nfc-rotate-btn__icon">🎲</span>
              <span>MESCOLA STORIE</span>
            </button>
            <a href="./02-cronistoria/partite-storiche/index" class="nfc-link-arrow">
              TUTTI I DOSSIER STORICI →
            </a>
          </div>"""

old_stories_actions_crlf = old_stories_actions.replace("\n", "\r\n")
if old_stories_actions_crlf in text:
    text = text.replace(old_stories_actions_crlf, new_stories_actions.replace("\n", "\r\n"), 1)
    print("Replaced stories actions (CRLF)")
elif old_stories_actions in text:
    text = text.replace(old_stories_actions, new_stories_actions, 1)
    print("Replaced stories actions (LF)")
else:
    print("WARNING: old_stories_actions not found!")

# Replace portraits actions
old_portraits_actions = """          <div class="nfc-section-header__actions">
            <a href="./03-tesserati/index" class="nfc-link-arrow">
              ALBO COMPLETO TESSERATI →
            </a>
          </div>"""

new_portraits_actions = """          <div class="nfc-section-header__actions">
            <button
              id="nfc-shuffle-portraits-btn"
              class="nfc-rotate-btn"
              type="button"
              title="Estrai altri volti e tesserati casuali dalla Hall of Fame"
            >
              <span class="nfc-rotate-btn__icon">🎲</span>
              <span>MESCOLA VOLTI</span>
            </button>
            <a href="./03-tesserati/index" class="nfc-link-arrow">
              ALBO COMPLETO TESSERATI →
            </a>
          </div>"""

old_portraits_actions_crlf = old_portraits_actions.replace("\n", "\r\n")
if old_portraits_actions_crlf in text:
    text = text.replace(old_portraits_actions_crlf, new_portraits_actions.replace("\n", "\r\n"), 1)
    print("Replaced portraits actions (CRLF)")
elif old_portraits_actions in text:
    text = text.replace(old_portraits_actions, new_portraits_actions, 1)
    print("Replaced portraits actions (LF)")
else:
    print("WARNING: old_portraits_actions not found!")

# Now find script tag and replace it
script_start = text.find("<script\n          dangerouslySetInnerHTML={{\n            __html: `\n(function()")
if script_start == -1:
    script_start = text.find("<script\r\n          dangerouslySetInnerHTML={{\r\n            __html: `\r\n(function()")

script_end = text.find("</section>\n\n      {/* 4. ICONOGRAFIA", script_start)
if script_end == -1:
    script_end = text.find("</section>\r\n\r\n      {/* 4. ICONOGRAFIA", script_start)

assert script_start != -1 and script_end != -1, f"Script range not found: {script_start}, {script_end}"

old_script_block = text[script_start:script_end]

new_script_block = """<script
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

  function renderStories(stories) {
    var storiesGrid = document.querySelector(".nfc-stories-grid");
    if (!storiesGrid) return;
    storiesGrid.style.transition = "opacity 0.15s ease";
    storiesGrid.style.opacity = "0.2";
    setTimeout(function() {
      storiesGrid.innerHTML = stories.map(function(s) {
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

  function renderPortraits(portraits) {
    var portraitsGrid = document.querySelector(".nfc-portraits-grid");
    if (!portraitsGrid) return;
    portraitsGrid.style.transition = "opacity 0.15s ease";
    portraitsGrid.style.opacity = "0.2";
    setTimeout(function() {
      portraitsGrid.innerHTML = portraits.map(function(p) {
        return '<a href="' + p.href + '" class="nfc-portrait-card" data-person-id="' + p.id + '">' +
          '<div class="nfc-portrait-card__img-wrap">' +
            '<img src="' + p.image + '" alt="' + p.name.replace(/"/g, '&quot;') + '" loading="lazy" />' +
            '<span class="nfc-portrait-card__stat">' + p.stat + '</span>' +
          '</div>' +
          '<div class="nfc-portrait-card__meta">' +
            '<span class="nfc-portrait-card__name">' + p.name + '</span>' +
            '<span class="nfc-portrait-card__role">' + p.role + '</span>' +
          '</div>' +
        '</a>';
      }).join("");
      portraitsGrid.style.opacity = "1";
    }, 120);
  }

  function shuffleStories() {
    var coverPoolEl = document.getElementById("nfc-cover-pool");
    if (coverPoolEl) {
      try {
        var pool = JSON.parse(coverPoolEl.textContent || "[]");
        if (pool.length) {
          var selected = shuffle(pool).slice(0, 6);
          renderStories(selected);
        }
      } catch (e) {}
    }
  }

  function shufflePortraits() {
    var portraitsPoolEl = document.getElementById("nfc-portraits-pool");
    if (portraitsPoolEl) {
      try {
        var pool = JSON.parse(portraitsPoolEl.textContent || "[]");
        if (pool.length) {
          var selected = shuffle(pool).slice(0, 4);
          renderPortraits(selected);
        }
      } catch (e) {}
    }
  }

  function initRandomizer() {
    shuffleStories();
    shufflePortraits();

    var storyBtn = document.getElementById("nfc-shuffle-stories-btn");
    if (storyBtn) {
      storyBtn.onclick = function(e) {
        e.preventDefault();
        shuffleStories();
      };
    }

    var portraitBtn = document.getElementById("nfc-shuffle-portraits-btn");
    if (portraitBtn) {
      portraitBtn.onclick = function(e) {
        e.preventDefault();
        shufflePortraits();
      };
    }
  }

  document.addEventListener("nav", initRandomizer);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRandomizer);
  } else {
    initRandomizer();
  }
})();
`,
          }}
        />
"""

if "\r\n" in text:
    new_script_block = new_script_block.replace("\n", "\r\n")

text = text[:script_start] + new_script_block + text[script_end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: MagazineHome.tsx updated with true randomizer and shuffle buttons!")
