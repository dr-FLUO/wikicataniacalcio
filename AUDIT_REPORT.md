# AUDIT REPORT — Wiki Catania Calcio (Beta 1.0)

**Data Audit:** 3 Novembre 2026 (Consolidamento Completo: Sezioni 1, 2.1–2.3 e 3.1–3.4 Applicate e Certificate)  
**Ruolo:** Senior Full-Stack Auditor, Data Engineer & Fact-Checker Storico  
**Perimetro Analizzato:** 1.656 file Markdown (8 sezioni enciclopediche), architettura Quartz v4, componenti TypeScript/Prettier/SCSS, dataset `dati_catania` (Transfermarkt), `calciocatania_all_players.json` e `wikimedia_catania_db`.

---

## 🔴 SEZIONE 1 — Modifiche Tecniche e Unificazioni Già Applicate

Tutte le correzioni tecniche sicure, le ristrutturazioni UX/UI, la deduplicazione delle schede calciatori, la creazione delle 18 schede mancanti da `dati_catania`, la pulizia degli script, la quadratura algebrica con scorporo coppe nelle 95 stagioni (ex §2.1), la pulizia delle omonimie (ex §2.2), l'allineamento dei 6 recordmen (ex §2.3) e le verifiche storiografiche su allenatori, vicende legali, Mascara e bibliografia (ex §§3.1–3.4) sono state **applicate e verificate nel codice**.

### 1.1 Architettura Quartz, UI, Accessibilità (WCAG 2.1 AA) e Restyling Navigazione (Proposta A)
- **URL Canonico di Produzione (`quartz.config.ts`)**: sostituito `baseUrl: "sim0n387.github.io/wikicataniacalcio"` con `baseUrl: "wikicataniacalcio.com"`.
- **Self-Hosting Font (`quartz/components/Head.tsx` & `quartz/styles/custom.scss`)**: rimossa ogni dipendenza esterna da `fonts.googleapis.com` / `fonts.gstatic.com` e configurate le dichiarazioni `@font-face` locali (`woff2`) per **Big Shoulders Display**, **Plus Jakarta Sans** e **JetBrains Mono**.
- **Persistenza Tema Light/Dark (`quartz/components/Darkmode.tsx`)**: allineata la chiave `localStorage` a `"theme"` (con sincronizzazione retrocompatibile verso `"saved-theme"`).
- **Accessibilità WCAG 2.1 AA (`MagazineTopBar.tsx`, `Explorer.tsx`, `MagazineArticleHero.tsx`, `content/index.md`)**:
  - Aggiunti `aria-label`, `aria-expanded` e `aria-controls` ai pulsanti hamburger mobile e ai menu a tendina della topbar.
  - Sostituito l'attributo non-standard ` alt="..."` con `aria-label="..."` sui `<button>` dei tab A–Z in `content/03-tesserati/calciatori/index.md`.
  - Aggiunti attributi `alt` descrittivi a tutte le immagini che ne erano prive (incluso `content/index.md`).
- **Tassonomia Editoriale & Restyling Navigazione TopBar + Sidebar (`quartz/util/editorialFolders.ts`, `MagazineTopBar.tsx`, `Explorer.tsx`, `explorer.inline.ts`, `quartz.layout.ts`, `custom.scss`)**:
  - **Mega-Pill Dropdowns nella TopBar**: passando il mouse (o cliccando) sulle 8 sezioni principali della barra superiore si apre un pannello glassmorfico con link diretti alle sotto-sezioni di 2° livello, riducendo da 3–4 a **1 solo click** il salto tra sezioni.
  - **Rimozione Prefissi Numerici Visivi**: i prefissi di ordinamento `01 · `, `02 · `, ..., `08 · ` sono stati rimossi dalle etichette visive della TopBar e dell'Explorer laterale, mantenendo l'ordinamento canonico tramite `SECTION_ORDER`.
  - **Auto-Apertura Sezione Attiva & Deep-Jump `Calciatori A–Z`**: l'albero laterale apre automaticamente il ramo della sezione corrente (`folderDefaultState: "collapsed"` con auto-expand contestuale in `explorer.inline.ts`) e collassa i 6 sotto-rami alfabetici `archivio/a-c ... s-z` in un unico nodo diretto `Calciatori (Archivio A–Z)`.
  - **Allineamento griglie card (`FolderContent.tsx`)**: uniformati tutti gli slug e le etichette di `editorialFolders.ts` con le directory reali del vault (`01-societa` … `08-settori-paralleli`).

### 1.2 Pulizia, Archiviazione e Unificazione degli Script di Sviluppo
- **Archiviazione Script Obsoleti**: spostati **168 script one-off** da `scripts/` a `_archive/scripts/` e **7 script** da `scratch/` a `_archive/scratch/` (entrambi esclusi dal build Quartz tramite `ignorePatterns`).
- **Nuova Suite Modulare Unificata (`scripts/`)**:
  1. [`scripts/wiki_validator.py`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/scripts/wiki_validator.py): validatore Frontmatter YAML (`SCHEMA.md`), integrità grafo `[[wikilink]]`, controllo URL corrotti e attributi `alt` WCAG.
  2. [`scripts/wiki_players.py`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/scripts/wiki_players.py): gestore anagrafica tesserati con guardia anti-duplicazione basata su `transfermarkt_id`, `calciocatania_id`, `birth_date` normalizzata e indice invertito `aliases`.
  3. [`scripts/wiki_seasons.py`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/scripts/wiki_seasons.py): verificatore di quadratura algebrica delle 95 stagioni ($G = V + N + P$, regime 2 pt / 3 pt, penalizzazioni e separazione Campionato vs Coppe/Playoff).
  4. [`scripts/wiki_audit.py`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/scripts/wiki_audit.py): orchestratore CLI completo (`python scripts/wiki_audit.py`).
- **Allineamento Modelli (`SCHEMA.md` & `agents/models.py`)**: documentati tutti i campi statistici e identificativi (`transfermarkt_id`, `calciocatania_id`, `total_appearances`, `total_goals`, `total_assists`, `minutes_played`, `seasons_count`, `locked`) nella §3 di [`SCHEMA.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/SCHEMA.md) e in [`agents/models.py`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/agents/models.py).

### 1.3 Deduplicazione Calciatori, Creazione 18 Schede da `dati_catania` e Ripristino Foto
- **45 Coppie di Schede Duplicate Unificate**: unite tutte le 45 coppie di schede duplicate (nome completo anagrafico/sudamericano vs nome sportivo/breve, inclusi `lucas-castro`, `pablo-barrientos`, `juan-manuel-ramos`, `gaston-sirenko`, `francisco-riestra`, `ertijon-guli`, `claudio-pelosi`, `marco-baroni`, `leite-pereira-marcelinho`, ecc.), preservando tutte le statistiche, le foto e gli `aliases` YAML e aggiornando i puntamenti in tutto il vault.
- **Rinomina 10 Schede con Slug Corrotto `dapos`**: rinominati i 10 file con apostrofo mal-sanitizzato (`daposagostino` → `dagostino`, `daposangelo` → `dangelo`, `daposeramo` → `deramo`, `daposintrono` → `dintrono`, `daposavanzo` → `davanzo`, `daposisidoro` → `disidoro`, `daposursi` → `dursi`, `dapossanto` → `dossanto`, `dapostilio` → `dostilio`, `daposottavio` → `dottavio`) con mantenimento degli alias retrocompatibili.
- **Creazione delle 18 Schede Calciatori Mancanti da `dati_catania`**: create e indicizzate le 18 schede presenti nei CSV verificati di `user-content/transfermarket-scraper/dati_catania` che non avevano ancora una pagina nel vault (`alessio-castellini`, `andrea-corbari`, `clavs-bethers`, `davide-rennella`, `francesco-golubovic`, `francesco-strianese`, `gabriel-lunetta`, `gergely-rollo`, `gianluca-frabotta`, `kaleb-jimenez`, `lorenzo-d-beni`, `matteo-stoppa`, `mattia-montalto`, `michele-d-avino`, `nicola-dalmonte`, `nicolo-fazzi`, `salvatore-molina`, `simone-pieraccini`).
- **Ripristino Foto e Crediti Fotografici**: collegata la foto verificata `176321_Hicham_Miftah.jpg` a `muolaij-micham-miftah.md` e convertiti 246 `[[wikilink]]` grezzi dentro `<div class="nfc-player-photo-credit">` in link HTML cliccabili.

### 1.4 Riparazione Totale del Grafo (`0` Link Rotti su 1.656 File)
- Riparati tutti i **634 `[[wikilink]]` rotti**, i **261 URL Markdown corrotti**, i **50 `[[wikilink]]` annidati** nei profili società/presidenti/allenatori, le chiusure anomale di `club_entity` in 51 file stagionali e i link residui post-deduplicazione.
- Stato attuale certificato da `python scripts/wiki_audit.py`:
  - **Broken `[[wikilinks]]`**: `0`
  - **Corrupted URLs**: `0`
  - **Nested `[[wikilinks]]`**: `0`
  - **Missing `alt` attributes**: `0`
  - **Valid YAML seasonal identities**: `95 / 95` (`0` errori algebrici, `0` stagioni con coppe mescolate in classifica)
  - **Build Quartz (`node quartz/bootstrap-cli.mjs build`)**: completato con codice `0` (`19.365` file emessi in `public/`).

### 1.5 Scorporo Gare di Coppa / Playoff / Spareggi dalla Classifica di Campionato nelle 95 Stagioni (ex §2.1 — ✅ APPLICATA)
- **Intervento eseguito su 72 file stagionali (`content/02-cronistoria/stagioni/*.md`) e su [`content/02-cronistoria/stagioni/index.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/index.md)**:
  - **Frontmatter YAML e Tabella `## Classifica Finale e Verdetti Ufficiali`**: ripristinati i dati puri della **sola stagione regolare di campionato** (`matches_played`, `wins`, `draws`, `losses`, `goals_for`, `goals_against`, `points_field`, `points_penalty`, `points_final`), eliminando la distorsione generata dalla somma automatica delle gare di Coppa Italia, Coppa Italia Serie C/D, Playoff, Poule Scudetto e Spareggi.
  - **Nota Ufficiale Competizioni Extra e Accordion `## Verifica Metodologica e Statistica`**: aggiunto sotto la tabella di classifica e nell'accordion metodologico il dettaglio separato tra **Bilancio Campionato (Stagione Regolare)**, **Bilancio Competizioni Extra (Coppe / Play-off / Spareggi)** e **Totale Gare Ufficiali Stagionali**.
  - **Correzioni puntuali nei tabellini stagionali**:
    - Inserita in [`1948-1949.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/1948-1949.md) la `15ª giornata` (`Catania – ACR Messina 0–0` del 2 gennaio 1949), ripristinando l'esatto bilancio di 34 gare (`16 V, 13 N, 5 P; 48 GF, 27 GS; 45 punti`) + 1 gara di Spareggio (`Avellino – Catania 1–0`).
    - Rettificata in [`1952-1953.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/1952-1953.md) l'`8ª giornata` (`Catania – Genoa 1–1 | N` del 9 novembre 1952), allineando il bilancio delle 34 gare di campionato a `16 V, 9 N, 9 P; 40 GF, 28 GS; 41 punti` + 1 gara di Spareggio (`Legnano – Catania 4–1`).
    - Corrette **15 righe di tabellino in trasferta** con `Esito` (`V`/`P`) e colonne marcatori invertiti in [`1955-1956.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/1955-1956.md) (5 gare, bilancio ripristinato a `34 G: 14 V, 12 N, 8 P; 42:28; 40 pt`), [`1956-1957.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/1956-1957.md) (7 gare, bilancio ripristinato a `34 G: 18 V, 6 N, 10 P; 53:31; 42 pt`), [`1996-1997.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/1996-1997.md) (1 gara) e [`2000-2001.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/2000-2001.md) (2 gare).
  - **Pulizia [`content/02-cronistoria/stagioni/index.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/index.md)**: rimossi i caratteri mojibake UTF-8, eliminato il link ridondante in coda a `2026-2027` e aggiornata la tabella cronologica mostrando i punti ufficiali di campionato e le gare nel formato `G_camp (G_tot)`.

### 1.6 Pulizia Collisioni di Omonimia su 28 Schede Calciatori (ex §2.2 — ✅ APPLICATA)
- Rimosso il blocco rendimento errato iniettato per collisione di cognome dallo script legacy e ripristinati nel frontmatter YAML e nella hero card i dati storici certificati su tutte le 28 schede (`armando-perrone`, `loris-boni`, `cesar-maximiliano-grabinski`, `cesare-panebianco`, `roberto-jose-battaglia`, `fernando-lomi`, `luca-bogdan`, `adrian-bic-b-dan`, `lido-nelli`, `juan-rizzo`, `rosario-rizzo`, `francesco-castro`, `marco-piampiani`, `tommaso-de-cara`, `marco-coppa`, `marco-di-fatta`, `marco-romano`, `dario-pellegrino`, `giuseppe-sciuto`, `mario-fontana`, `luigi-bosco`, `roberto-calanna`, `giuseppe-finocchiaro`, `carmelo-bonanno`, `graziano-la-terra`, `michele-marino`, `antonio-caruso`, `domenico-rescigno`).

### 1.7 Allineamento KPI Recordmen Rossazzurri (ex §2.3 — ✅ APPLICATA)
- Allineate e armonizzate su **5 fonti ufficiali indipendenti** (Wikipedia, Transfermarkt, TuttoCalciatori, CarriereCalciatori, *Tutto il Catania minuto per minuto*) le schede monografiche, il frontmatter YAML, le hero table e le tabelle di riepilogo in [`content/03-tesserati/index.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/index.md) e [`content/03-tesserati/calciatori/storici/index.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/index.md):
  1. **[`damiano-morra.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/damiano-morra.md)**: YAML `total_appearances: 321`, `league_appearances: 281`, `serie_a_appearances: 25`, `total_goals: 28`, `league_goals: 27`. Hero table: Presenze `321` (281 camp.), Goal/Assist `28 / 2`. Testo aggiornato chiarendo le **281 presenze in campionato** (284 con i 3 spareggi 1978 e 1983) e le **321 presenze ufficiali complessive** con 28 reti (di cui 37 gare e 1 rete nelle coppe).
  2. **[`nicolo-nicolosi.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/nicolo-nicolosi.md)**: ripristinato il grave errore del parser TM (che riportava 7 presenze e 7 gol). YAML `total_appearances: 156`, `league_appearances: 149`, `total_goals: 78`, `league_goals: 71`, `seasons_count: 8`, periodi `1932–1937, 1939–1940, 1942–1943, 1947–1949`. Hero table: Presenze `156`, Goal `78`. Aggiunta nota archivistica sulla **79ª rete** documentata nell'ottobre 2023 dagli autori di *Tutto il Catania minuto per minuto* (Catania-Novara 2-0 del 27/01/1935).
  3. **[`marco-biagianti.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/marco-biagianti.md)**: YAML `total_appearances: 284`, `league_appearances: 255`, `serie_a_appearances: 148`, `total_goals: 12`, `league_goals: 11`. Hero table: Presenze `284`, Goal/Assist `12 / 11`. Dettaglio: 255 gare regolari (148 A con 3 reti, 107 C con 8 reti) + 11 playoff C + 18 nelle coppe (11 C.I., 7 C.I. C con 1 rete) = **284 gare e 12 reti**.
  4. **[`mariano-izco.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/mariano-izco.md)**: YAML `total_appearances: 258`, `league_appearances: 239`, `serie_a_appearances: 218`, `total_goals: 7`, `league_goals: 6`. Hero table: Presenze `258 (280 tot.)`, Goal/Assist `7 / 16`. Nel testo è chiarito il 1º ciclo in Serie A (218 in A e 17 in C.I. = 235 presenze e 7 reti) e il bilancio finale: **258 presenze ufficiali omologate FIGC** e **280 presenze effettive** sul campo (includendo le 22 gare di Serie C 2021-22 giocate prima dell'esclusione ex art. 53 NOIF).
  5. **[`francesco-lodi.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/francesco-lodi.md)**: YAML `total_appearances: 239`, `league_appearances: 215`, `serie_a_appearances: 105`, `total_goals: 54`, `league_goals: 47`, `serie_a_goals: 20`. Hero table: Presenze `239`, Goal/Assist `54 / 50`. Chiarito il bilancio: 215 gare regolari (47 reti) + 10 post-season (3 reti) + 14 coppe (4 reti) = **239 presenze ufficiali e 54 reti** (238/53 nei soli tornei professionistici FIGC).
  6. **[`gonzalo-bergessio.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/gonzalo-bergessio.md)**: YAML `total_appearances: 113`, `league_appearances: 109`, `serie_a_appearances: 109`, `total_goals: 37`, `league_goals: 35`, `serie_a_goals: 35`. Hero table: `Al Catania: 2011–2014`, Presenze `113`, Goal/Assist `37 / 14`. Primatista assoluto di reti in Serie A (35).

### 1.8 Conduzione Tecnica Piero Andreoli vs Enzo Bellini (1953–1956) e Salvezza sul Campo 1954-1955 (ex §3.1 — ✅ APPLICATA)
- **[`piero-andreoli.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/allenatori/piero-andreoli.md)**:
  - Rettificata la cronistoria: Andreoli **vinse la Serie B 1953-1954** con 43 punti conquistando la prima storica promozione in Serie A; guidò la squadra in Serie A nel **1954-1955 per tutte le 34 giornate conquistando la salvezza sul campo al 12º posto (30 punti)**, revocata solo a tavolino per lo scandalo Scaramella.
  - Nella Serie B 1955-1956 guidò la squadra dalla **1ª alla 27ª giornata** (fino alle dimissioni del 16 aprile 1956), collezionando **95 panchine consecutive di campionato** (34 in B + 34 in A + 27 in B, più lo spareggio del 1953).
- **[`enzo-bellini.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/allenatori/enzo-bellini.md)**:
  - Eliminato il blocco tabella duplicato e l'extra tag `</div>` che rompeva la struttura HTML.
  - Confermato il subentro nelle ultime **7 giornate** della Serie B 1955-1956 (dalla 28ª alla 34ª giornata, dal 29/04/1956 al 10/06/1956, 3V 2N 2P).
- **[`1955-1956.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/02-cronistoria/stagioni/1955-1956.md)**: indicata nella tabella staff la ripartizione esatta: `Piero Andreoli (1ª–27ª), poi Enzo Bellini (28ª–34ª)`.

### 1.9 Datazione Catania–Siena 1–1 (12 aprile 2003) e Cronologia del Caso Catania 2003 / Caso Martinelli (ex §3.2 — ✅ APPLICATA)
- **[`caso-catania-2003.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/01-societa/vicende-legali/caso-catania-2003.md)** e **[`caso-martinelli-2003.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/01-societa/vicende-legali/caso-martinelli-2003.md)**:
  - Confermato che la gara Catania–Siena 1–1 si disputò **sabato 12 aprile 2003** (30ª giornata di Serie B), mentre il 19 aprile si giocò Palermo–Catania 3–3.
  - Cronologia dei gradi di giudizio verificata e allineata:
    1. Reclamo Catania: 17 aprile 2003
    2. Commissione Disciplinare LNP (rigetto): 24 aprile 2003
    3. Commissione d'Appello Federale (CAF - 2-0 a tavolino per il Catania): 28 aprile / 15 maggio 2003
    4. Corte Federale FIGC (revoca delibera CAF e ripristino 1-1): 22/28 maggio 2003
    5. TAR Sicilia - Catania (Ord. n. 1054/2003, sospensiva pro-Catania): 5 giugno 2003
    6. CGAR Sicilia (annullamento procedurale) e nuovo ricorso TAR Catania: 26 giugno – 13 agosto 2003
    7. Decreto-Legge 19 agosto 2003, n. 220 (conv. in L. 280/2003) e delibera FIGC 20 agosto 2003: allargamento Serie B 2003-2004 a 24 squadre con Catania, Genoa, Salernitana e Fiorentina.

### 1.10 Totale Presenze e Reti di Giuseppe Mascara: 238 Presenze e 60 Reti Ufficiali (ex §3.3 — ✅ APPLICATA)
- **[`giuseppe-mascara.md`](file:///c:/Users/sim0n/.gemini/antigravity/scratch/wikicalciocatania/content/03-tesserati/calciatori/storici/giuseppe-mascara.md)**:
  - Frontmatter YAML e Hero Card aggiornati a: `total_appearances: 238`, `league_appearances: 226`, `serie_a_appearances: 149`, `total_goals: 60`, `league_goals: 58`, `serie_a_goals: 31`.
  - Inserito box informativo dedicato che spiega e dissipa l'origine della vecchia dicitura non aggiornata "235 presenze": 226 gare in campionato (77 B con 27 reti + 149 A con 31 reti) + 12 gare in Coppa Italia (2 reti) = **238 presenze e 60 reti ufficiali** (il conteggio a 235 presenze non includeva le 3 presenze del gennaio 2011 prima del passaggio al Napoli).

### 1.11 Normalizzazione Bibliografica di *Tutto il Catania minuto per minuto* nelle Stagioni Post-2011 (ex §3.4 — ✅ APPLICATA)
- **Nelle 15 stagioni dal 2011-2012 al 2025-2026 (`content/02-cronistoria/stagioni/*.md`)**:
  - Rimosso l'anacronistico riferimento al volume cartaceo del 2010 (*"Tutto il Catania minuto per minuto (1929-2010), GEO Edizioni (Sezione Stagione 201X-201Y)"*).
  - Sostituito in YAML e Markdown con la citazione corretta al portale di aggiornamento continuo degli stessi autori:
    `Roberto Quartarone, Alessandro Russo, Filippo Solarino, Antonio Buemi, Carlo Fontanelli, Tutto il Catania minuto per minuto — Portale e Archivio Storico Online (tuttoilcataniaminutoperminuto.it)`.
  - Nelle stagioni storiche dal 1929-1930 al 2010-2011 rimane canonica la citazione dell'opera cartacea GEO Edizioni (2010 / 2011).

### 1.12 Risoluzione Definitiva Bug Navigazione TopBar (Menu Dropdown Incastrati, Scrollbar Orizzontale e Comportamento Responsive — ✅ APPLICATA)
- **Causa Radice Individuata**:
  1. *Menu incastrato e barre di scorrimento*: `.nfc-masthead__nav` conteneva la regola CSS `overflow-x: auto;` (e `@media (max-width: 820px)` conteneva `overflow-x: clip;` e `hidden !important;`). In CSS, impostare `overflow-x` su auto/clip forza il calcolo di `overflow-y` ad auto/hidden, impedendo ai sottomenu a tendina assoluti (`top: 100%`) di renderizzare all'esterno e generando barre di scorrimento orizzontali e verticali all'interno della barra di 68px.
  2. *Menu che restavano aperti dopo il click o all'uscita del cursore*: la regola CSS `&:focus-within .nfc-nav-dropdown { display: block; }` manteneva il sottomenu permanentemente aperto dopo qualsiasi click o tabulazione finché il browser non spostava il focus.
  3. *Mancato adattamento responsive e troncamento*: sotto i 1180px la barra forzava un flex con celle da 88px minimi e l'etichetta `VIVAIO & WOMEN` veniva troncata (`VIVAIO & WOM...`).
- **Interventi Applicati e Verificati**:
  - **`quartz/components/scripts/topbar.inline.ts`**: creato controller JavaScript client-side che gestisce l'apertura/chiusura dei dropdown con debounce (80ms), chiude istantaneamente tutti i sottomenu al click su un link (`closeAllDropdowns()` e sfocatura `blur()`), supporta touch per dispositivi mobili, click all'esterno, tasto Escape e transizioni SPA di Quartz (`nav` event).
  - **`quartz/components/MagazineTopBar.tsx`**: agganciato `topbar.inline.ts` via `afterDOMLoaded`, aggiunti attributi ARIA accessibili (`aria-haspopup`, `aria-expanded`) e separata l'etichetta dell'ottava voce in `<span class="nfc-label-main">Vivaio</span><span class="nfc-label-extra"> & Women</span>`.
  - **`quartz/components/Header.tsx`**: elevato `z-index` a `1000` e impostato `overflow: visible !important;` sia su `.nfc-top-wrapper` che su `.nfc-top-shell`.
  - **`quartz/styles/custom.scss`**:
    - Impostato `overflow: visible !important;` sull'intera gerarchia della testata (`.nfc-top-shell`, `.nfc-masthead`, `.nfc-masthead__grid`, `.nfc-masthead__nav`, `.nfc-nav-item-wrap`).
    - Eliminata la regola `&:focus-within .nfc-nav-dropdown`; visibilità delegata a `@media (hover: hover)` e alla classe controllata `.is-open`.
    - Aggiunto ponte di hover invisibile (`&::before`) per evitare micro-flicker nel passaggio del cursore tra cella e sottomenu.
    - Allineati a destra i menu delle ultime tre sezioni (`&:nth-last-child(-n+3) .nfc-nav-dropdown { left: auto; right: 0; }`) per prevenire fuoriuscite oltre il bordo destro dello schermo.
    - Semplificato il responsive: a schermi medi (< 1360px) la pillola versione viene nascosta e l'etichetta diventa "VIVAIO" senza troncamenti; su tablet e mobile (< 880px) la navigazione si dispone in una griglia ordinata 4×2 senza scrollbar; su schermi stretti (< 600px) il dropdown aperto galleggia in overlay centrato.
- **Verifica**: Compilazione Quartz completata con codice `0` (`19.365` file in `public/`) e `python scripts/wiki_audit.py` a `0` errori.

### 1.13 Correzione Puntamento Slug TopBar e Rete di Reindirizzamento Aliases (ex 404 Sponsor / Campi Storici / Donne — ✅ APPLICATA)
- **Causa Radice Individuata**:
  - In `MagazineTopBar.tsx`, 5 voci dei sottomenu della testata puntavano a slug convenzionali privi di file Markdown corrispondente (es. `05-identita-e-simboli/sponsor/storia-sponsor-tecnici-e-ufficiali`, `04-strutture/campi-storici/piazza-esposizione-e-due-obelischi`, `05-identita-e-simboli/evoluzione-maglia-rossazzurra`, `07-media-e-comunicazione/letteratura/grandi-opere-e-almanacchi`, `08-settori-paralleli/women/dipartimento-catania-women`).
  - La cartella reale conteneva file indice canonici (`sponsor/index.md`, `campi-storici/index.md`, `letteratura/index.md`, `women/index.md`) e dossier dedicati (`araldica-e-scudetti/loghi-storici-liotru.md`), ma gli slug legacy non erano inclusi nell'array `aliases: [...]` del frontmatter, causando risposta HTTP 404 da parte del server locale.
- **Interventi Applicati e Verificati**:
  - **`quartz/components/MagazineTopBar.tsx`**: aggiornati i 5 slug verso gli indici e dossier canonici effettivi (`05-identita-e-simboli/sponsor/index`, `04-strutture/campi-storici/index`, `05-identita-e-simboli/araldica-e-scudetti/loghi-storici-liotru`, `07-media-e-comunicazione/letteratura/index`, `08-settori-paralleli/women/index`), e aggiunta la voce `Mascotte & Inni` (`05-identita-e-simboli/mascotte-e-inni`).
  - **Frontmatter `aliases: [...]`**: registrati tutti i vecchi slug e varianti negli array `aliases` dei file Markdown corrispondenti, garantendo il reindirizzamento automatico trasparente per chiunque utilizzi vecchi URL o cronologie browser.
  - **`quartz/plugins/emitters/aliases.ts`**: normalizzata la generazione degli URL di redirect per prevenire doppi slash (`//`).
  - **`quartz/build.ts`**: aggiunti parametri di retry (`maxRetries: 10, retryDelay: 100`) per la rimozione della cartella `public/` su Windows in presenza di dev server attivi.
- **Verifica**: Compilazione completata con codice `0` (`19.383` file generati), verifica file `public/` superata per tutti i 10 target (pagine canoniche e file HTML di redirect alias).

---

## 🟢 QUADRO GENERALE DI SALUTE DEL PROGETTO

| Ambito di Verifica | Stato Pre-Audit | Stato Post-Audit | Esito |
| :--- | :---: | :---: | :---: |
| **[[Wikilink]] rotti** | 634 | **0** | ✅ Perfetto |
| **URL Markdown corrotti** | 261 | **0** | ✅ Perfetto |
| **Slug TopBar / Pagine 404** | 5 link 404 | **0 link 404 + Redirect Aliases** | ✅ Risolto |
| **[[Wikilink]] annidati / sintassi malformata** | 50 | **0** | ✅ Perfetto |
| **Tag HTML e attributi accessibilità WCAG 2.1 AA** | Errori su tab/alt | **Conformi** | ✅ Piena accessibilità |
| **Font Google Fonts esterni** | Dipendenze remote | **100% Self-Hosted WOFF2** | ✅ GDPR & offline compliant |
| **Navigazione UI (TopBar + Explorer)** | Macchinosa (3-4 click) | **Mega-Pill 1-click + Auto-expand** | ✅ Ottimizzata |
| **Script di sviluppo attivi** | 175 script disorganizzati | **4 tool modulari puliti (`scripts/`)** | ✅ Architettura snella |
| **Schede calciatori duplicate** | 45 coppie duplicate | **0 duplicati** (45 fusioni perfette) | ✅ Risolto |
| **Schede calciatori mancanti da `dati_catania`** | 18 mancanti | **18 create e indicizzate** | ✅ Completato |
| **Collisioni omonimia calciatori** | 28 schede contaminate | **28 schede storiche ripristinate** | ✅ Ripristinato |
| **Quadratura 95 stagioni (Campionato vs Coppe)** | 72 stagioni con coppe sommate | **95/95 stagioni pure + scorporo coppe** | ✅ Quadrato |
| **Recordmen storici (Morra, Nicolosi, Biagianti, Izco, Lodi, Bergessio, Mascara)** | Discrepanze TM vs Storia | **Allineati al 100% su 5 fonti** | ✅ Certificato |
| **Compilazione statica Quartz** | Rischio warning/errori | **Build pulito (`0` errori, 19.383 file)** | ✅ Pronto per il deploy |
