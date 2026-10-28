# Proposta di Riorganizzazione dell'Alberatura (Audit Topologico Vault)

> [!CAUTION]
> **STATO ATTUALE: HOLD RIGIDO / PROPOSTA DOCUMENTALE SOLTANTO**
> In conformità con le direttive operative generali, **nessuna cartella o file del vault reale è stato spostato, rinominato o rimosso**. Qualsiasi futura transizione richiederà la previa approvazione esplicita dell'utente.

---

## 1. Executive Summary e Stato dell'Arte del Vault

In seguito all'ingestione massiva dei profili dei calciatori, all'unificazione delle risorse multimediali e alla creazione dei moduli Live, Media, Giovanili e Tifoseria, il vault di **Wiki Calcio Catania** ha raggiunto una dimensione e un livello di copertura documentale di livello enciclopedico nazionale:

* **File Markdown complessivi nel Vault (`content/`)**: 1.447 documenti
* **Asset Multimediali (`content/assets/images/`)**: 757 file (67 immagini segnaposto integralmente sostituite con fotografie autentiche ad alta risoluzione da archivi storici e Wikimedia Commons; cartella `img` rimossa e unificata al 100% in `images`).
* **Conformità Linter Forense (`agents/test_models.py`)**: 100% superato su 1.447 file (zero violazioni di copyright, WCAG 2.1 AA o quadratura algebrica).
* **Collegamenti Rossi / Broken Links**: 0 (tutti i link a stadi, presidenti, campionati e testate sono attivi e risolti).

---

## 2. Audit Topologico delle Criticità Attuali

L'attuale struttura del vault presenta alcune aree di miglioramento ergonomico dovute alla rapida crescita del corpus informativo:

```
content/
├── assets/
│   └── images/              <- UNIFICATO: 757 foto autentiche suddivise per categorie semantiche
├── giovanili/               <- Primavera, Campionati giovanili e strutture
├── maglie/                  <- Araldica, Simbologia, Scudetti e Sponsor commerciali
├── media/                   <- Testate storiche (La Sicilia, Telecolor, ecc.) e Grandi Firme
├── partite/                 <- Dossier monografici partite leggendarie suddivisi per stagione
├── societa/                 <- Epoche societarie (1929, 1946, 1967, 2004, 2022) e Presidenti
├── stadio/                  <- Massimino, Nesima, Torre del Grifo, Piazza Esposizione
├── stagioni/                <- Monografie annuali (1929-2027) con quadratura algebrica
├── tesserati/
│   ├── allenatori/          <- 25 schede storiche
│   └── calciatori/          <- 1.112 schede anagrafiche in singola directory flat
├── tifoseria/               <- Curva Nord, Curva Sud, Eventi giudiziari, Biografie, Gemellaggi
└── women/                   <- Dipartimento Femminile, Scudetto 1978 e Serie C
```

### Principali Criticità Rilevate:
1. **Sovraffollamento di `content/tesserati/calciatori/`**:
   Oltre 1.100 file in una singola cartella rendono la visualizzazione nell'Explorer laterale di Quartz e negli editor locali (VS Code, Obsidian) densa, rallentando la navigazione ad albero per gli utenti umani, benché il motore di build Quartz non ne risenta.
2. **Eterogeneità nei Prefissi di `societa/`**:
   Coesistono slug temporali con data d'inizio (`1929-ss-catania`, `1946-club-calcio-catania`, `1967-calcio-catania-spa-massimino`) e cartelle tematiche (`societa/presidenti/`).
3. **Dispersione delle Strutture Sportive**:
   In `stadio/` convivono lo stadio principale cittadino (Angelo Massimino), il centro sportivo di allenamento (Torre del Grifo), i campi periferici giovanili (Campo Nesima) e i campi storici scomparsi (Campo dei Due Obelischi, Piazza Esposizione).

---

## 3. Modello Tassonomico Proposto (Target Architecture)

La proposta di riorganizzazione prevede la strutturazione del vault in **8 Macro-Macroambiti Tematici** rigorosamente ordinati per gerarchia logica:

```
content/
├── 01-societa/
│   ├── epoche/              <- 1929-ss-catania, 1946-club-catania, 1967-era-massimino, 2004-era-pulvirenti, 2022-pelligra
│   ├── presidenti/          <- Massimino, Pulvirenti, Pelligra, Maimone, Finocchiaro, ecc.
│   ├── dirigenti/           <- Lo Monaco, Grella, Faggiano, ecc.
│   └── matricola-11700.md
├── 02-cronistoria/
│   ├── stagioni/            <- 1929-1930 ... 2026-2027
│   └── partite-storiche/    <- 1960-61/catania-inter-2-0, 2008-09/palermo-catania-0-4, ecc.
├── 03-tesserati/
│   ├── allenatori/          <- Di Bella, Simeone, Marino, Montella, Zenga, Toscano, ecc.
│   └── calciatori/
│       ├── storici/         <- Nicolosi, Biavati, Vavassori, Cantarutti, Morra, Prenna, Mascara
│       ├── rosa-attuale/    <- Inglese, Sturaro, Castellini, Cicerelli, Lunetta, Adamonis, Quaini
│       └── archivio/        <- Sub-cluster alfabetici (A-C, D-F, G-L, M-O, P-R, S-Z) per le 1.100 schede
├── 04-strutture/
│   ├── stadio-massimino/    <- Massimino, Cibali, Cibalino, Tribuna Stampa Stefania Sberna
│   ├── centri-sportivi/     <- Torre del Grifo Village, Nesima
│   └── campi-storici/       <- Piazza Esposizione, Due Obelischi
├── 05-identita-e-simboli/
│   ├── maglie/              <- Prima, seconda, terza divisa per stagione
│   ├── araldica-e-scudetti/ <- Simbologia Liotru, colori cremisi/cobalto
│   └── sponsor/             <- Haribo, SP Energia Siciliana, Giò.Vi, partner tecnici
├── 06-tifoseria-e-cultura/
│   ├── curve/               <- Curva Nord, Curva Sud, gruppi storici
│   ├── eventi-e-giustizia/  <- 1983, 1993, 2001, 2007 (Raciti), 2015, 2024 (Padova)
│   ├── biografie/           <- Ciccio Famoso, Antonino Speziale
│   └── relazioni/           <- Gemellaggi (Genoa, Napoli) e Rivalità
├── 07-media-e-comunicazione/
│   ├── testate/             <- La Sicilia, Espresso Sera, Telecolor, Antenna Sicilia, CalcioCatania.com
│   └── firme-e-voci/        <- Candido Cannavò, Stefania Sberna, Luigi Prestinenza
└── 08-settori-paralleli/
    ├── giovanili/           <- Primavera, Torneo di Viareggio, Campionati giovanili
    └── women/               <- Catania Women, Scudetto 1978 Jolly Componibili
```

---

## 4. Matrice di Migrazione e Salvaguardia del Grafo (Zero Broken Links)

Per garantire che **nessun link interno o segnalibro esterno venga interrotto**, la migrazione adotterebbe la direttiva nativa di Quartz basata sul campo `aliases` nel Frontmatter di ogni pagina spostata.

### Esempi di Mapping con Aliases:
| Vecchio Percorso (Slug Corrente) | Nuovo Percorso Proposto | Configurazione Frontmatter `aliases` |
| :--- | :--- | :--- |
| `stadio/angelo-massimino` | `04-strutture/stadio-massimino/angelo-massimino` | `aliases: ["stadio/angelo-massimino"]` |
| `maglie/sponsor-commerciali` | `05-identita-e-simboli/sponsor/sponsor-commerciali` | `aliases: ["maglie/sponsor-commerciali"]` |
| `tifoseria/biografie/antonino-speziale` | `06-tifoseria-e-cultura/biografie/antonino-speziale` | `aliases: ["tifoseria/biografie/antonino-speziale"]` |
| `tesserati/calciatori/roberto-inglese` | `03-tesserati/calciatori/rosa-attuale/roberto-inglese` | `aliases: ["tesserati/calciatori/roberto-inglese"]` |

Grazie a questa strategia, sia `[[stadio/angelo-massimino]]` sia il nuovo percorso puntano alla medesima pagina HTML compilata, rendendo la transizione al 100% trasparente.

---

## 5. Piano di Implementazione a Fasi (Solo su Approvazione)

Se e quando l'utente riterrà opportuno procedere, la migrazione verrà condotta in 4 fasi controllate:

* **Fase 1: Snapshot di Sicurezza Preventivo**
  Esecuzione automatica di `scripts/backup_vault.py --create --label pre_reorganization_full`.
* **Fase 2: Script di Spostamento Semi-Automatico con Iniezione Aliases**
  Un programma dedicato legge ogni file, inietta il vecchio slug nell'array `aliases: [...]`, sposta il file nella nuova directory target e preserva metadati e timestamp.
* **Fase 3: Riconciliazione Wikilink con Ragnatela Scanner**
  Esecuzione di `scripts/ragnatela_scanner.py --top 50` per validare l'integrità del grafo delle connessioni e verificare che il numero di collegamenti rossi resti pari a zero.
* **Fase 4: Verifica Linter Forense e Build Quartz**
  Esecuzione di `uv run python agents/test_models.py` e `npx.cmd quartz build` per accertare che la build statica e tutti i test di conformità normativa passino senza errori.

---

## 6. Richiesta di Feedback e Decisione

Questo documento è stato depositato a scopo di studio e pianificazione. 
**Nessuna modifica fisica è stata apportata.** 

Si rimette la decisione all'utente circa:
1. Mantenere l'alberatura attuale (che funziona perfettamente, passa tutti i test al 100% e non presenta anomalie).
2. Pianificare la riorganizzazione guidata sopra descritta in una sessione di manutenzione dedicata.
