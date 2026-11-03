with open('quartz/styles/custom.scss', 'r', encoding='utf-8') as f:
    scss = f.read()

new_styles = """
// ============================================================================
// 12. GRIGLIA A DUE COLONNE: COLLEGAMENTI CORRELATI & FONTI (COMPATTO)
// ============================================================================
.nfc-sources-and-links-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--wiki-border-strong, #e0e0e0);

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .nfc-grid-column {
    background-color: var(--wiki-surface-elevated, #fafafa);
    border: 1px solid var(--wiki-border-subtle, #e5e5e5);
    padding: 0.75rem 1rem;
    box-shadow: 1px 1px 0 rgba(0, 0, 0, 0.03);

    h2, h3 {
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
      padding-left: 1.15rem !important;
      color: var(--wiki-text-secondary, #333333);

      li {
        margin-bottom: 0.25rem !important;

        a {
          font-weight: 600;
          color: var(--rossazzurro-blue, #1565c0);
          text-decoration: underline;
          text-decoration-thickness: 1px;

          &:hover {
            color: var(--rossazzurro-red, #d32f2f);
          }
        }
      }
    }

    p {
      font-size: 0.78rem !important;
      line-height: 1.45 !important;
      margin: 0 0 0.35rem 0 !important;
    }
  }
}

// ============================================================================
// 13. SCHEDA CALCIATORE: TABELLA ANAGRAFICA & RENDIMENTO IN TESTA
// ============================================================================
.nfc-player-hero-card {
  margin: 1.25rem 0 1.75rem 0;
  background-color: var(--wiki-surface-elevated, #fafafa);
  border: 1.5px solid var(--wiki-border-strong, #333333);
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.08);
  overflow: hidden;

  .nfc-player-table {
    width: 100%;
    border-collapse: collapse;
    margin: 0;
    font-size: 0.88rem;

    tbody tr {
      border-bottom: 1px solid var(--wiki-border-subtle, #e5e5e5);

      &:last-child {
        border-bottom: none;
      }

      &:hover {
        background-color: rgba(211, 47, 47, 0.03);
      }
    }

    th {
      width: 130px;
      font-family: var(--font-display, "Big Shoulders Display", sans-serif);
      font-size: 0.88rem;
      font-weight: 800;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      color: #333333;
      padding: 0.35rem 0.65rem;
      vertical-align: middle;
      border-right: 1px solid var(--wiki-border-subtle, #e5e5e5);
      background-color: rgba(0, 0, 0, 0.02);
    }

    td {
      padding: 0.35rem 0.75rem;
      color: #111111;
      font-weight: 600;
      vertical-align: middle;
    }

    .nfc-player-photo-cell {
      width: 145px;
      min-width: 145px;
      max-width: 145px;
      padding: 0.5rem;
      vertical-align: top;
      text-align: center;
      border-right: 1.5px solid var(--wiki-border-strong, #333333);
      background-color: #f0f0f0;

      .nfc-player-photo {
        width: 100%;
        height: auto;
        max-height: 200px;
        object-fit: cover;
        display: block;
        border: 1px solid var(--wiki-border-subtle, #cccccc);
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
      }

      .nfc-player-no-photo {
        width: 100%;
        height: 175px;
        background-color: #e2e8f0;
        border: 1.5px dashed #cbd5e1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #64748b;
        font-family: var(--font-display, "Big Shoulders Display", sans-serif);
        font-weight: 800;
        letter-spacing: 0.05em;

        .nfc-no-photo-badge {
          font-size: 1.15rem;
          color: #94a3b8;
          margin-bottom: 0.2rem;
        }

        .nfc-no-photo-label {
          font-size: 0.72rem;
          text-transform: uppercase;
          color: #64748b;
        }
      }
    }
  }

  @media (max-width: 600px) {
    .nfc-player-table {
      .nfc-player-photo-cell {
        display: block;
        width: 100% !important;
        max-width: 100% !important;
        border-right: none;
        border-bottom: 1.5px solid var(--wiki-border-strong);
        
        .nfc-player-photo, .nfc-player-no-photo {
          max-width: 160px;
          margin: 0 auto;
        }
      }
      
      tbody tr {
        display: flex;
        
        th {
          width: 40%;
          min-width: 110px;
        }
        td {
          width: 60%;
        }
      }
    }
  }
}

:root[saved-theme="dark"] {
  .nfc-player-hero-card {
    background-color: var(--wiki-surface-elevated, #1a1a1a);
    border-color: #444444;

    .nfc-player-table {
      tbody tr {
        border-bottom-color: #333333;
        &:hover {
          background-color: rgba(255, 255, 255, 0.03);
        }
      }

      th {
        color: #cccccc;
        border-right-color: #333333;
        background-color: rgba(255, 255, 255, 0.02);
      }

      td {
        color: #f1f5f9;
      }

      .nfc-player-photo-cell {
        background-color: #222222;
        border-right-color: #444444;

        .nfc-player-no-photo {
          background-color: #262626;
          border-color: #404040;
          color: #94a3b8;
        }
      }
    }
  }

  .nfc-sources-and-links-grid {
    border-top-color: #444444;
    .nfc-grid-column {
      background-color: #1e1e1e;
      border-color: #333333;

      h2, h3 {
        color: #f1f5f9 !important;
      }

      ul, ol {
        color: #cccccc;
      }
    }
  }
}
"""

if '.nfc-sources-and-links-grid' not in scss:
    scss += new_styles
    with open('quartz/styles/custom.scss', 'w', encoding='utf-8') as f:
        f.write(scss)
    print("New styles added to custom.scss!")
else:
    print("Styles already present in custom.scss")
