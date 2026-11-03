path = 'quartz/styles/custom.scss'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Make footer more compact
old_footer = """  .footer-compliance-box {
    background-color: var(--wiki-surface-elevated);
    border: 1px solid var(--wiki-border-subtle);
    padding: 0.75rem 1rem;
    margin-bottom: 0.85rem;
    box-shadow: 1px 1px 0 rgba(0, 0, 0, 0.04);
  }

  .footer-kicker {
    display: block;
    font-family: var(--font-display);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--rossazzurro-red) !important;
    margin-bottom: 0.15rem;
    text-transform: uppercase;
  }

  .footer-brand {
    font-family: var(--font-display);
    font-size: 1.05rem;
    font-weight: 900;
    letter-spacing: 0.02em;
    margin: 0 0 0.35rem 0;
    color: #111111 !important;
    line-height: 1.25;

    strong {
      color: #000000 !important;
      font-weight: 900;
    }
  }

  .footer-legal-notice {
    margin: 0;
    font-size: 0.73rem;
    line-height: 1.45;
    color: #333333 !important;

    strong {
      color: #111111 !important;
      font-weight: 700;
    }

    em {
      font-style: italic;
      color: #222222 !important;
    }
  }

  .footer-beta-notice {
    margin: 0.45rem 0 0 0;
    padding-top: 0.4rem;
    border-top: 1px dashed var(--wiki-border-hairline);
    font-size: 0.71rem;
    line-height: 1.4;
    color: #333333 !important;"""

new_footer = """  .footer-compliance-box {
    background-color: var(--wiki-surface-elevated);
    border: 1px solid var(--wiki-border-subtle);
    padding: 0.45rem 0.75rem;
    margin-bottom: 0.5rem;
    box-shadow: 1px 1px 0 rgba(0, 0, 0, 0.04);
  }

  .footer-kicker {
    display: block;
    font-family: var(--font-display);
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--rossazzurro-red) !important;
    margin-bottom: 0.1rem;
    text-transform: uppercase;
  }

  .footer-brand {
    font-family: var(--font-display);
    font-size: 0.88rem;
    font-weight: 900;
    letter-spacing: 0.02em;
    margin: 0 0 0.2rem 0;
    color: #111111 !important;
    line-height: 1.2;

    strong {
      color: #000000 !important;
      font-weight: 900;
    }
  }

  .footer-legal-notice {
    margin: 0;
    font-size: 0.65rem;
    line-height: 1.35;
    color: #333333 !important;

    strong {
      color: #111111 !important;
      font-weight: 700;
    }

    em {
      font-style: italic;
      color: #222222 !important;
    }
  }

  .footer-beta-notice {
    margin: 0.25rem 0 0 0;
    padding-top: 0.25rem;
    border-top: 1px dashed var(--wiki-border-hairline);
    font-size: 0.63rem;
    line-height: 1.3;
    color: #333333 !important;"""

c = c.replace(old_footer.replace('\r\n', '\n'), new_footer)
c = c.replace(old_footer, new_footer)

old_grid = """    h2, h3 {
      font-family: var(--font-display, "Big Shoulders Display", sans-serif) !important;
      font-size: 0.95rem !important;
      font-weight: 800 !important;
      letter-spacing: 0.04em !important;
      text-transform: uppercase;
      margin: 0 0 0.5rem 0 !important;
      padding-bottom: 0.25rem;
      border-bottom: 2px solid var(--rossazzurro-red, #d32f2f);
      color: var(--wiki-text-primary, #111111) !important;

      a.internal {
        display: none !important;
      }
    }

    ul, ol {
      font-size: 0.78rem !important;
      line-height: 1.45 !important;
      margin: 0 !important;
      padding-left: 1.15rem !important;"""

new_grid = """    h2, h3 {
      font-family: var(--font-display, "Big Shoulders Display", sans-serif) !important;
      font-size: 0.80rem !important;
      font-weight: 800 !important;
      letter-spacing: 0.04em !important;
      text-transform: uppercase;
      margin: 0 0 0.35rem 0 !important;
      padding-bottom: 0.2rem;
      border-bottom: 2px solid var(--rossazzurro-red, #d32f2f);
      color: var(--wiki-text-primary, #111111) !important;

      a.internal {
        display: none !important;
      }
    }

    ul, ol {
      font-size: 0.70rem !important;
      line-height: 1.35 !important;
      margin: 0 !important;
      padding-left: 1rem !important;"""

c = c.replace(old_grid.replace('\r\n', '\n'), new_grid)
c = c.replace(old_grid, new_grid)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated custom.scss successfully.')
