# 📥 Inbox Immagini — Calcio Catania Wiki

Questa è la cartella dedicata all'acquisizione, catalogazione e posizionamento automatico delle immagini nel sito.

---

## 🚀 Come Funziona il Flusso di Lavoro

1. **Trascina e rilascia le tue immagini qui dentro:**
   - Puoi inserire qualsiasi immagine nei formati `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`.
   - Non preoccuparti del nome del file (può essere anche un nome grezzo come `IMG_1024.jpg`, `schermata.png` o `whatsapp_image.jpeg`).
   - Se desideri specificare dettagli opzionali (ad es. partita specifica, data o fotografo), puoi nominare il file con un indizio o semplicemente scriverlo in chat.

2. **Chiedi all'assistente in chat:**
   > *"Ho inserito nuove immagini in inbox, analizzale e posizionale nel sito"*

3. **Cosa fa l'assistente in automatico per ogni foto:**
   - **Audit Visivo & Multimodale:** apre e guarda l'immagine con visione multimodale per identificare con precisione storica chi è ritratto, l'azione di gioco, l'evento, la stagione o il settore dello stadio.
   - **Controllo Univocità (Zero Duplicati):** calcola l'hash MD5 per assicurarsi che non sia un clone di una foto già presente nell'archivio.
   - **Ridenominazione Ottimizzata per la SEO:** assegna al file un nome semantico e parlante in kebab-case (es. `mascara-gol-centrocampo-palermo-catania-serie-a-2008-2009.webp`).
   - **Archiviazione Organizzata:** sposta il file nella sottocartella corretta di `content/assets/images/`:
     - `partite-storiche/`
     - `presidenti-dirigenti/`
     - `tifoseria-e-curva/`
     - `strutture-e-stadi/`
     - `maglie-e-simboli/`
     - `media-e-stampa/`
   - **Innestamento nel Sito:** inserisce l'immagine nella pagina wiki pertinente con il layout compatto `.wiki-inset-photo` (alternanza sinistra/destra, badge tematico, lightbox universale ad alta risoluzione).
   - **Metadati SEO e Accessibilità:** compila:
     - `alt`: testo descrittivo accessibile e per indicizzazione motori di ricerca.
     - `data-caption`: didascalia autentica e fedele al 100% alla realtà della foto.
     - `data-lightbox-title`: titolo essenziale visualizzato a schermo intero.
     - `image_credits`: aggiornamento del frontmatter con fonte, anno e licenza.
   - **Pulizia dell'Inbox:** l'immagine viene archiviata e la cartella inbox rimane pulita per i caricamenti successivi.
