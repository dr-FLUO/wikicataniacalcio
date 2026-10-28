# SCHEMA.md — Contratto Ontologico, Normativo e Sintattico della Wiki Calcio Catania (1929–Oggi)

> **Versione Specifica:** `1.0.0`  
> **Stato:** Vincolante per tutti gli Agenti AI (Squadra 1, Squadra 2 e `FactCheckAgent`) e i Curatori Umani.  
> **Motore Target:** Quartz v4 / Obsidian Flavored Markdown (OFM) + GitHub Flavored Markdown (GFM).

---

## 1. Principi Ingegneristici e Conformità Normativa Europea

Ogni file generato o modificato all'interno della directory `content/` deve rispettare tassativamente quattro vincoli strutturali e legali:

1. **Conformità Europea Privacy & Cookie-Less (GDPR Reg. UE 2016/679 e Direttiva ePrivacy 2002/58/CE):**
   - È vietato incorporare nelle pagine Markdown script di tracciamento di terze parti, iframe non autorizzati (es. embed social che rilasciano cookie di profilazione senza consenso) o risorse ospitate su server esterni non conformi al GDPR.
   - Tutte le risorse tipografiche e iconografiche devono essere servite localmente (*Self-Hosted*).
2. **Accessibilità Universale (European Accessibility Act — Direttiva UE 2019/882 e WCAG 2.1 Livello AA):**
   - **Gerarchia dei Titoli:** Ogni pagina deve contenere un solo `# Titolo H1` (corrispondente al titolo della voce), seguito da sezioni `## H2` e sottosezioni `### H3` senza mai saltare livelli gerarchici.
   - **Testo Alternativo (`alt`) Obbligatorio:** Ogni immagine deve possedere un testo alternativo descrittivo per gli screen reader: `![Descrizione dettagliata del soggetto, anno e contesto](percorso/immagine.webp)`.
   - **Contrasto e Leggibilità:** Il frontend rispetta la palette ufficiale ad altissimo contrasto (`#191919` su `#f7f7f7` in Light Mode e `#f7f7f7` su `#191919` in Dark Mode, rapporto **15.8:1** conforme a WCAG AAA).
3. **Citazione Obbligatoria delle Fonti Storiche e Giuridiche (Art. 70 L. 633/1941 e Direttiva UE 2019/790):**
   - Nessuna pagina può avere `status: "verified"` senza almeno una fonte primaria certificata nell'array `sources` del Frontmatter YAML e senza la sezione finale `## Fonti e Bibliografia` in calce al documento.
4. **Tutela del Diritto d'Autore sulle Immagini (Artt. 87–92 L. 633/1941):**
   - Ogni immagine referenziata nella pagina deve essere censita nell'array `image_credits` del Frontmatter YAML e riportare sotto l'immagine o nella sezione finale l'indicazione di: **Autore/Fotografo**, **Fonte/Archivio**, **Anno** e **Licenza/Base Giuridica** (es. *Pubblico Dominio in Italia ex art. 92 L. 633/1941 — fotografia semplice pubblicata da oltre 20 anni*, *CC BY-SA 4.0*, o *Marchio storico ad uso descrittivo enciclopedico*).

---

## 2. Palette Ufficiale e Tokens del Design System Minimal-Wiki

| Ruolo Semantico | Codice HEX | Utilizzo nel Frontend |
| :--- | :---: | :--- |
| **Principale 1 — Rosso Catania** | `#d11317` | Accenti strutturali, bordi superiori Infobox e tabelle (`2px–3px`), stato `:hover`, nodi societari/legali. |
| **Principale 2 — Azzurro Catania** | `#0cb2d9` | Collegamenti interni `[[wikilinks]]`, pillole dei tag, focus ring di accessibilità (`:focus-visible`), archi attivi del grafo. |
| **Versione Light (Inchiostro / Testo)** | `#191919` | Testo primario e titoli su sfondo `#f7f7f7` in modalità chiara; sfondo principale in modalità scura. |
| **Versione Dark (Inchiostro / Testo)** | `#f7f7f7` | Testo primario e titoli su sfondo `#191919` in modalità scura; sfondo carta editoriale in modalità chiara. |
| **Piccoli Dettagli — Oro Araldico** | `#d29933` | Filetto divisorio (`1px`) sotto l'header dell'Infobox e delle tabelle, badge `verified`, indicatore voce attiva TOC, nodo corrente del grafo. |

---

## 3. Tassonomia delle Cartelle (`content/`) e Convenzioni di Naming

Tutti i nomi dei file e delle cartelle devono utilizzare esclusivamente il formato **`kebab-case`** (lettere minuscole `a-z`, cifre `0-9` e trattini `-`, senza spazi né caratteri accentati):

- `content/index.md` ➔ `entity_type: "home_portal"`
- `content/societa/<anno>-<slug>.md` ➔ `entity_type: "era_societaria"`
- `content/societa/presidenti/<nome-cognome>.md` ➔ `entity_type: "dirigente"`
- `content/stagioni/<YYYY-YYYY>.md` ➔ `entity_type: "stagione_agonistica"`
- `content/partite/<YYYY-YYYY>/<squadra1-squadra2-score>.md` ➔ `entity_type: "tabellino_gara"`
- `content/partite/precedenti/<avversario>.md` ➔ `entity_type: "archivio_precedenti"`
- `content/tesserati/calciatori/<nome-cognome>.md` ➔ `entity_type: "calciatore"`
- `content/tesserati/allenatori/<nome-cognome>.md` ➔ `entity_type: "allenatore"`
- `content/stadio/<slug-impianto>.md` ➔ `entity_type: "impianto_sportivo"`
- `content/maglie/<slug-kit-o-logo>.md` ➔ `entity_type: "kit_storico"`
- `content/vicende-legali/<slug-dossier>.md` ➔ `entity_type: "vicenda_legale"`
- `content/tifoseria/<settore-o-categoria>/<slug>.md` ➔ `entity_type: "gruppo_ultras"` | `"relazione_tifo"` | `"evento_tifo"` | `"biografia_tifo"`
- `content/note-legali-privacy-accessibilita.md` ➔ `entity_type: "legal_compliance"`
- `content/segnala-correzione.md` ➔ `entity_type: "feedback_portal"`

---

## 4. Grammatica Obbligatoria dello YAML Frontmatter

### 4.1 Campi Base Obbligatori per TUTTE le Pagine

```yaml
---
title: "Titolo Canonico ed Esplicativo della Voce"
description: "Sintesi SEO/GEO di 120-160 caratteri che riassume il contenuto storico e i dati chiave della pagina."
slug: "percorso/relativo-senza-estensione"
entity_type: "stagione_agonistica" # Uno dei tipi ontologici ammessi
status: "verified"                 # "verified" | "stub" | "under_review"
last_verified_date: 2026-10-27
tags:
  - tag-1
  - tag-2
sources:
  - author: "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino"
    title: "Tutto il Catania minuto per minuto (1929-2010)"
    publisher: "GEO Edizioni, Empoli"
    year: 2010
    reference: "pp. 184-191"
image_credits: []                  # Obbligatorio se la pagina contiene immagini
---
```

### 4.2 Campi Specifici per `stagione_agonistica`
- `season_label`: `"YYYY-YYYY"`
- `club_entity`: `"[[societa/...|Nome Ragione Sociale]]"`
- `figc_matricola`: `"N/A (Pre-1946)"` | `"11700"` | `"955013"`
- `division`: Nome ufficiale del campionato (es. `"Serie A"`, `"Serie B"`, `"Eccellenza Sicilia"`)
- `division_tier`: Intero da `1` a `6`
- `president_ref`: Wikilink al presidente
- `coach_refs`: Lista di Wikilink agli allenatori
- `stadium_ref`: Wikilink allo stadio
- `matches_played`, `wins`, `draws`, `losses`, `goals_for`, `goals_against`: Interi non negativi
- `points_per_win_regime`: `2` (fino al 1993-94) oppure `3` (dal 1994-95)
- `points_field`, `points_penalty`, `points_final`: Interi soggetti a validazione algebrica stretta (`(wins * regime) + draws - penalty == points_final`)
- `final_position`: Posizione finale in classifica
- `top_scorer_ref`, `top_scorer_goals`: Capocannoniere stagionale
- `prev_season`, `next_season`: Wikilink di navigazione cronologica

### 4.3 Campi Specifici per `vicenda_legale`
- `date_start`, `date_end`: Date ISO `YYYY-MM-DD`
- `season_ref`, `club_entity`, `figc_matricola`
- `protagonists`: Lista di soggetti chiave
- `judicial_bodies`: Lista degli organi giudicanti (es. `CAF`, `TFN`, `TAR Sicilia - Sez. Catania`, `CGA`)
- `legal_norms_cited`: Lista delle norme invocate
- `legal_outcome`: Esito sintetico del procedimento

### 4.4 Campi Specifici per `gruppo_ultras` / `relazione_tifo`
- `foundation_year`: Anno di nascita
- `founder`: Wikilink o nome del fondatore
- `origin_district`: Quartiere cittadino o comune etneo
- `stadium_sector`: `"Curva Sud - Anello Inferiore"` | `"Curva Sud - Anello Superiore"` | `"Curva Nord"` | `"Tribuna B"` | `"Tribuna A"`

---

## 5. Regole Sintattiche per il Corpo Markdown

1. **Escape Obbligatorio nelle Tabelle GFM:**
   All'interno di qualsiasi cella di tabella Markdown (`| ... |`), i Wikilinks con alias devono **sempre** avere il carattere pipe preceduto da backslash:
   - ✅ Corretto: `| [[societa/presidenti/angelo-massimino\|Angelo Massimino]] |`
   - ❌ Errato: `| [[societa/presidenti/angelo-massimino|Angelo Massimino]] |` (rompe la colonna della tabella!).
2. **Callout Semantici Standard:**
   Utilizzare la sintassi blockquote di Obsidian:
   - `> [!abstract] Sintesi Storica / Impatto`
   - `> [!info] Nota Metodologica o Statistica`
   - `> [!warning] Provvedimento Disciplinare / Sub Iudice`
   - `> [!quote] Dichiarazione Storica o Estratto Sentenza`
3. **Sezione Finale Obbligatoria `## Fonti e Crediti`:**
   Ogni pagina deve chiudersi con la sezione `## Fonti e Bibliografia` (ed eventuale `### Crediti Fotografici e Licenze`) che rende visibili al lettore umano tutte le fonti strutturate nel Frontmatter.
