import fs from 'fs';
import path from 'path';

// Read all jpg files from content/assets/images/maglie
const imagesDir = 'content/assets/images/maglie';
const jpgFiles = fs.readdirSync(imagesDir).filter(f => f.endsWith('.jpg'));

// Group images by season
const seasonImages = {};
jpgFiles.forEach(f => {
  const m = f.match(/^(\d{4}-\d{4})_(.+)\.jpg$/);
  if (m) {
    const season = m[1];
    const rawType = m[2];
    if (!seasonImages[season]) seasonImages[season] = [];
    seasonImages[season].push({ file: f, rawType });
  }
});

// Sort images within each season: prima, seconda, terza, portiere, altre
const typeOrder = (t) => {
  if (t === 'prima' || t === 'prima_v2') return 1;
  if (t === 'seconda' || t === 'seconda_v2') return 2;
  if (t === 'terza' || t === 'terza_v2') return 3;
  if (t.startsWith('portiere')) return 4;
  if (t === 'speciale') return 5;
  return 6;
};

Object.keys(seasonImages).forEach(s => {
  seasonImages[s].sort((a, b) => typeOrder(a.rawType) - typeOrder(b.rawType));
});

// Read seasons info from content/02-cronistoria/stagioni
const stagioniDir = 'content/02-cronistoria/stagioni';
const seasonFiles = fs.readdirSync(stagioniDir).filter(f => f.match(/^\d{4}-\d{4}\.md$/)).sort();

const seasonsData = {};
seasonFiles.forEach(sf => {
  const sName = sf.replace('.md', '');
  const content = fs.readFileSync(path.join(stagioniDir, sf), 'utf-8');
  let division = 'Campionato Ufficiale';
  const mDiv = content.match(/division:\s*(.+)/);
  if (mDiv) division = mDiv[1].trim();
  seasonsData[sName] = { division };
});

// Known technical & commercial sponsors
const sponsorMap = {
  '1979-1980': { tech: 'NR (Ennerre)', comm: '*Nessuno*' },
  '1980-1981': { tech: 'NR (Ennerre)', comm: 'Promo Lemon&Soda' },
  '1981-1982': { tech: 'Bobos', comm: '*Nessuno*' },
  '1982-1983': { tech: 'Degi', comm: 'Haribo' },
  '1983-1984': { tech: 'Adidas', comm: 'S7 Supermercati' },
  '1984-1985': { tech: 'Adidas', comm: 'Pasta Poiatti' },
  '1985-1986': { tech: 'Adidas', comm: 'CasaMercato' },
  '1986-1987': { tech: 'Adidas (Uhlsport)', comm: 'Eurass' },
  '1987-1988': { tech: 'Latas', comm: 'CosmoTV Color' },
  '1988-1989': { tech: 'Latas', comm: 'Proter' },
  '1989-1990': { tech: 'Icos', comm: 'Proter' },
  '1990-1991': { tech: 'Essegi', comm: 'Proter' },
  '1991-1992': { tech: 'Icos', comm: 'Proter' },
  '1992-1993': { tech: 'ABM', comm: 'Jolly Componibili' },
  '1993-1994': { tech: 'California', comm: 'Jolly Componibili' },
  '1994-1995': { tech: 'California / Devis Sport', comm: 'Jolly Componibili' },
  '1995-1996': { tech: 'Devis Sport', comm: 'Tamoil' },
  '1996-1997': { tech: 'Admiral', comm: 'Angelo Massimino / Oranfresh' },
  '1997-1998': { tech: 'Puma', comm: 'SP Energia Siciliana' },
  '1998-1999': { tech: 'Puma', comm: 'SP Energia Siciliana' },
  '1999-2000': { tech: 'Puma', comm: 'SP Energia Siciliana' },
  '2000-2001': { tech: 'Galex', comm: 'SP Energia Siciliana' },
  '2001-2002': { tech: 'Galex', comm: 'SP Energia Siciliana' },
  '2002-2003': { tech: 'Galex', comm: 'SP Energia Siciliana' },
  '2003-2004': { tech: 'Galex', comm: 'Toyota' },
  '2004-2005': { tech: 'Galex', comm: 'SP Energia Siciliana' },
  '2005-2006': { tech: 'Legea', comm: 'SP Energia Siciliana' },
  '2006-2007': { tech: 'Legea', comm: 'SP Energia Siciliana' },
  '2007-2008': { tech: 'Legea', comm: 'SP Energia Siciliana / Wind Jet' },
  '2008-2009': { tech: 'Legea', comm: 'SP Energia Siciliana / Wind Jet' },
  '2009-2010': { tech: 'Legea', comm: 'SP Energia Siciliana' },
  '2010-2011': { tech: 'Givova', comm: 'SP Energia Siciliana' },
  '2011-2012': { tech: 'Givova', comm: 'SP Energia Siciliana' },
  '2012-2013': { tech: 'Givova', comm: 'Arancia Rossa di Sicilia / TTT Lines' },
  '2013-2014': { tech: 'Givova', comm: 'Fiorucci / TTT Lines' },
  '2014-2015': { tech: 'Givova', comm: 'Fortè Discount' },
  '2015-2016': { tech: 'Macron', comm: 'Muracel' },
  '2016-2017': { tech: 'Macron', comm: 'DomusBet' },
  '2017-2018': { tech: 'Givova', comm: 'DomusBet' },
  '2018-2019': { tech: 'Givova', comm: 'DomusBet' },
  '2019-2020': { tech: 'Givova', comm: 'Crai (Gruppo Radenza)' },
  '2020-2021': { tech: 'Givova', comm: 'SuperConveniente (Gruppo Arena)' },
  '2021-2022': { tech: 'Nike', comm: 'SuperConveniente' },
  '2022-2023': { tech: 'Erreà', comm: 'SuperConveniente' },
  '2023-2024': { tech: 'Erreà', comm: 'SuperConveniente' },
  '2024-2025': { tech: 'Erreà', comm: 'SuperConveniente' },
  '2025-2026': { tech: 'Erreà', comm: 'SuperConveniente / Replay' },
  '2026-2027': { tech: 'Erreà', comm: 'Replay / SuperConveniente' }
};

// Helper for image caption
function formatCaption(rawType) {
  if (rawType === 'prima' || rawType === 'prima_v2') {
    return { title: '1ª Maglia', sub: 'Casa Rossazzurra' };
  }
  if (rawType === 'seconda' || rawType === 'seconda_v2') {
    return { title: '2ª Maglia', sub: 'Trasferta Bianca' };
  }
  if (rawType === 'terza' || rawType === 'terza_v2') {
    return { title: '3ª Maglia', sub: 'Terza Divisa' };
  }
  if (rawType.startsWith('portiere')) {
    let num = '';
    if (rawType.includes('v4')) num = ' (4)';
    else if (rawType.includes('v3')) num = ' (3)';
    else if (rawType.includes('v2')) num = ' (2)';
    else if (rawType.includes('-2')) num = ' (1)';
    return { title: 'Portiere' + num, sub: 'Divisa da Portiere' };
  }
  if (rawType === 'speciale') {
    return { title: 'Speciale', sub: 'Edizione Celebrativa' };
  }
  if (rawType.startsWith('altra')) {
    return { title: 'Alternativa', sub: 'Variante di Gara' };
  }
  return { title: 'Divisa', sub: rawType };
}

// Group seasons into decades
const decades = [
  { id: 'anni-20', title: "Anni '20 (1929–1930)", start: 1929, end: 1930, desc: "La fondazione della Società Sportiva Catania nel giugno 1929 e l'esordio al Campo dei Due Obelischi. Maglie pesanti in lana vergine a maniche lunghe con lacci al colletto e strisce verticali rosso cremisi e azzurro ciano." },
  { id: 'anni-30', title: "Anni '30 (1930–1939)", start: 1930, end: 1939, desc: "Gli anni dell'AFC Catania, la prima scalata in Serie B (1933-1934) e la costruzione dello Stadio Cibali (1937). Maglie a girocollo e colletti a polo con calzoncini neri o bianchi e calzettoni neri con risvolto rossazzurro." },
  { id: 'anni-40', title: "Anni '40 (1939–1949)", start: 1939, end: 1949, desc: "Gli anni bellici, la sospensione dei campionati e la storica rinascita del 1946 con la fondazione del Club Calcio Catania e la matricola 11700. Ripresa della tradizione a pali stretti e lana pettinata." },
  { id: 'anni-50', title: "Anni '50 (1949–1959)", start: 1949, end: 1959, desc: "La prima storica promozione in Serie A (1953-1954), le sfide al Cibali contro le grandi del nord e il debutto della seconda maglia bianca con banda diagonale rossazzurra in omaggio al culto di Sant'Agata." },
  { id: 'anni-60', title: "Anni '60 (1959–1969)", start: 1959, end: 1969, desc: "Il decennio leggendario di Carmelo Di Bella in Serie A (ottavi posti, 4-0 all'Inter e il 2-0 alla Juventus del 'Clamoroso al Cibali'). Pali fitti bicolori e le celebri maglie dei portieri monocromatiche di Vavassori e Rado." },
  { id: 'anni-70', title: "Anni '70 (1969–1979)", start: 1969, end: 1979, desc: "Dalla promozione in Serie A del 1970 con Egizio Rubino alle battaglie di Serie B e C. Compare il cotone leggero; sul finire del decennio la storica delibera federale FIGC del 1979 apre all'esposizione del marchio del fornitore tecnico (Ennerre)." },
  { id: 'anni-80', title: "Anni '80 (1979–1989)", start: 1979, end: 1989, desc: "La rivoluzione tessile e pubblicitaria: lanetta NR Ennerre, l'accordo pionieristico con Haribo nel 1982 e la promozione in Serie A a Roma nel 1983; segue l'era quadriennale Adidas con S7, Pasta Poiatti, CasaMercato ed Eurass, fino a Latas e Proter." },
  { id: 'anni-90', title: "Anni '90 (1989–1999)", start: 1989, end: 1999, desc: "I tessuti sintetici lucidi in poliestere (Icos, Essegi), la drammatica radiazione del 1993 e la rinascita di Angelo Massimino con le divise California/Jolly Componibili dall'Eccellenza al CND; poi Devis, Admiral per il cinquantenario e l'arrivo di Puma con SP Energia Siciliana." },
  { id: 'anni-2000', title: "Anni 2000 (1999–2009)", start: 1999, end: 2009, desc: "L'era Gaucci con Galex (promozione in Serie B a Taranto 2002) e il quinquennio d'oro Legea: la promozione in Serie A del 28 maggio 2006, la memorabile vittoria per 0-4 al Barbera contro il Palermo e le divise con il main sponsor SP Energia Siciliana e Wind Jet." },
  { id: 'anni-2010', title: "Anni 2010 (2009–2019)", start: 2009, end: 2019, desc: "L'apice storico del club in Serie A: 56 punti e 8° posto nel 2012-2013 con Givova (Arancia Rossa di Sicilia, Fiorucci, TTT Lines), il biennio Macron in Lega Pro e il ritorno di Givova con le celebrazioni per il centenario di Angelo Massimino." },
  { id: 'anni-2020', title: "Anni 2020 (2019–2027)", start: 2019, end: 2027, desc: "Dal default della matricola 11700 alla rinascita con Ross Pelligra in Serie D (Erreà, record di punti), il trionfo nella Coppa Italia Serie C 2024 e il riscatto del marchio storico all'asta del 2026. Texture laviche dell'Etna, dettagli in oro e partnership internazionali con Replay e SuperConveniente." }
];

let md = `---
title: Maglie, Divise da Gioco e Colori Sociali del Calcio Catania (1929–Oggi)
description: Trattato enciclopedico sull'anatomia delle casacche rossazzurre, canoni estetici tradizionali (calzettoni neri con risvolto), evoluzione tessile, riferimenti agli sponsor tecnici e commerciali e timeline fotografica per decenni dal 1929 al 2027.
slug: 05-identita-e-simboli/maglie-e-divise
entity_type: kit_storico
status: verified
last_verified_date: 2026-11-04
tags:
- maglie
- divise
- colori-sociali
- rossazzurro
- kit-storici
- sponsor-tecnici
- sponsor-commerciali
- cultura-materiale
sources:
- author: Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino
  title: Tutto il Catania minuto per minuto (1929-2010)
  publisher: GEO Edizioni, Empoli
  year: 2010
  reference: Appendice Iconografica Maglie, Stemmi, Sponsor e Divise da Gioco
- author: Roberto Quartarone
  title: Gli sponsor tecnici e commerciali del Catania dal 1979 ad oggi
  publisher: tuttoilcataniaminutoperminuto.it
  year: 2024
  reference: Cronologia dei fornitori di abbigliamento sportivo e contratti pubblicitari
- author: Archivio Storico Mimmo Rapisarda
  title: Museo virtuale delle maglie storiche e dei fornitori del Calcio Catania
  publisher: mimmorapisarda.it
  year: 2024
  reference: Collezione fotografica e schede delle divise storiche
- author: Carlo Fontanelli, Roberto Quartarone, Alessandro Russo
  title: Il rosso e l'azzurro. Novant'anni di una maglia
  publisher: GEO Edizioni, Empoli
  year: 2020
  reference: Censimento completo delle maglie e varianti cromatiche 1929-2020
aliases:
- 05-identita-e-simboli/evoluzione-maglia-rossazzurra
- evoluzione-maglia-rossazzurra
- maglie/evoluzione-maglia-rossazzurra
- maglie/index
- maglie/loghi-storici-liotru
---

# Maglie, Divise da Gioco e Colori Sociali del Calcio Catania (1929–Oggi)

L'identità visiva del **Calcio Catania** è custodita nei filati, nelle trame e nei codici cromatici delle sue divise da gioco: fin dalla fondazione del **giugno 1929**, la compagine rossazzurra indossa i colori della natura etnea — il **rosso magma del vulcano (#d11317)** e l'**azzurro limpido del mare Jonio (#0cb2d9)** —, abbinati all'inconfondibile tradizione dei **calzettoni neri con risvolto rossazzurro**.

La presente monografia costituisce il censimento enciclopedico ufficiale della cultura materiale etnea: dall'anatomia sartoriale e dai canoni estetici delle casacche, all'intreccio con la storia dei fornitori tecnici e degli sponsor pubblicitari, fino alla **timeline fotografica continua per decenni** che documenta le mute da gioco stagione per stagione dal 1929 a oggi.

---

## 1. Anatomia e Canoni Identitari delle Divise Rossazzurre

La divisa del Catania possiede regole estetiche codificate da quasi un secolo di storia sportiva:

### 1.1 La Prima Maglia (Home Kit)
Maglia a **strisce verticali alternate rosse (#d11317) e azzurre (#0cb2d9)**. La larghezza della palatura ha conosciuto diverse modulazioni stilistiche:
- **Pali fitti e sottili:** caratteristici degli anni Cinquanta e Sessanta, epoca d'oro di [[03-tesserati/allenatori/carmelo-di-bella|Carmelo Di Bella]], [[03-tesserati/calciatori/adelmo-prenna|Adelmo Prenna]] e [[03-tesserati/calciatori/alvaro-biagini|Alvaro Biagini]].
- **Pali larghi e geometrici:** introdotti a fine anni Settanta da *NR Ennerre* e consolidati negli anni Ottanta (*Adidas*, *Latas*) e Duemila (*Legea*, *Givova*).
- **Trame e texture moderne:** con la rinascita del 2022, *Erreà* ha arricchito i pali con sfumature antracite richiamanti il basalto lavico e finiture dorate (#d29933) in omaggio alle insegne civiche e a Sant'Agata.

### 1.2 La Regola Aurea dei Calzettoni Neri
Mentre la maglia e i pantaloncini (tradizionalmente **azzurri**, talvolta neri negli anni Trenta e Cinquanta o bianchi in trasferta) hanno subito variazioni cromatiche, il vero marchio di fabbrica dell'eleganza etnea risiede nei **calzettoni rigorosamente NERI (#191919)**:
> [!tip] Il Dettaglio Distintivo dei Calzettoni
> La tradizione vuole che il calzettone nero sia sormontato da una **fascetta orizzontale o risvolto superiore rossazzurro**. Questa combinazione cromatica (maglia rossazzurra, pantaloncino azzurro e calzettone nero) distingue inequivocabilmente il Catania da qualsiasi altro club rossoblù d'Europa (Bologna, Genoa, Cagliari, Basilea o Barcellona), rendendo la sagoma del calciatore etneo immediatamente riconoscibile sul terreno di gioco.

### 1.3 La Seconda Divisa (Away Kit)
La divisa da trasferta è storicamente **bianca**, richiamando il candore del tradizionale «sacco» votivo indossato dai devoti durante i festeggiamenti agatini di febbraio e agosto. La casacca bianca è quasi sempre impreziosita da:
- Una **fascia diagonale bicolore rossazzurra** (omaggio alla storica maglia degli spareggi di Roma del 1983);
- Una fascia centrale orizzontale o verticale;
- Bordature e colletto in contrasto cromatico rosso e azzurro.

### 1.4 La Terza Divisa (Third Kit)
Introdotta stabilmente a partire dagli anni Novanta in ossequio alle normative televisive e di contrasto cromatico, la terza divisa attinge rigorosamente al patrimonio identitario etneo:
- **Giallo zolfo o oro (#d29933):** colore ufficiale del gonfalone municipale della città di Catania e dello stemma civico federiciano del 1239.
- **Nero antracite / fumo di lava (#191919):** evocazione diretta della pietra vulcanica eruttata dall'Etna, arricchita spesso da dettagli fluo o bordature rosso magma.

### 1.5 Le Maglie dei Portieri
La scuola dei numeri uno etnei (da [[03-tesserati/calciatori/giuseppe-vavassori|Giuseppe Vavassori]] e Rado a Sorrentino, Muraro, Iezzo e Andújar) ha attraversato due grandi epoche:
- **Epoca Classica (1929–1985):** maglie rigorosamente monocromatiche grigie, nere o verde scuro con colletto a polo bianco, calzoncini neri e stemma sul cuore.
- **Epoca Moderna (1985–Oggi):** kit tecnici multicolori ad alta visibilità (arancione lava, verde acido, giallo sole e celeste), spesso dotati di imbottiture ergonomiche.

---

## 2. I Partner di Maglia: Fornitori Tecnici e Sponsor Commerciali

La storia delle maglie del Catania è indissolubilmente legata alle partnership industriali e commerciali che hanno accompagnato le stagioni agonistiche del club:

* **I Fornitori Tecnici Ufficiali:** Dalla delibera federale FIGC del **1979** che consentì per la prima volta l'esposizione del marchio del produttore di abbigliamento sportivo, sulla casacca etnea si sono alternati marchi prestigiosi: **NR (Ennerre)**, **Bobos**, **Degi**, **Adidas**, **Latas**, **Icos**, **Essegi**, **ABM**, **California**, **Devis Sport**, **Admiral**, **Puma**, **Galex**, **Legea**, **Givova**, **Macron**, **Nike** ed **Erreà**.  
  👉 *Dossier dedicato:* [[05-identita-e-simboli/sponsor/index#1-cronistoria-dei-fornitori-tecnici-e-della-cultura-tessile|Cronistoria Completa dei Fornitori Tecnici (1979–Oggi)]].

* **Gli Sponsor Pubblicitari di Maglia:** Con la delibera FIGC del **1981**, il Catania ha inaugurato una ricca tradizione di sponsorizzazioni commerciali, a partire dalla leggendaria intesa del 1982 con il colosso dolciario **Haribo** (promozione in Serie A con 40.000 tifosi a Roma), proseguendo con **S7 Supermercati**, **Pasta Poiatti**, **Proter**, **Jolly Componibili**, fino al quindicennio record con **SP Energia Siciliana** in Serie A (affiancata da **Wind Jet**, **TTT Lines**, **Fiorucci**) e all'attuale partnership con il marchio internazionale **Replay** e **SuperConveniente (Gruppo Arena)**.  
  👉 *Dossier dedicato:* [[05-identita-e-simboli/sponsor/index#2-evoluzione-economica-degli-sponsor-commerciali-di-maglia|Evoluzione degli Sponsor Commerciali (1982–2026)]] e [[05-identita-e-simboli/sponsor/index#3-matrice-cronologica-integrata-sponsor-tecnici-e-commerciali-1979oggi|Matrice Integrata Fornitori e Sponsor]].

---

## 3. Timeline Fotografica delle Maglie per Decenni (1929–2027)

Navigazione rapida per decennio:
`;

// Add navigation pills
const navPills = decades.map(d => `[${d.title.split(' ')[0]} ${d.title.split(' ')[1]}](#${d.id})`).join(' · ');
md += `> ${navPills}\n\n---\n\n`;

// Generate Decades
decades.forEach((dec, idx) => {
  md += `## ${idx + 1}. ${dec.title}\n\n`;
  md += `<a id="${dec.id}"></a>\n\n`;
  md += `> [!info] Contesto Storico e Stile del Decennio\n`;
  md += `> ${dec.desc}\n\n`;

  // Filter seasons in this decade
  const decSeasons = Object.keys(seasonsData).filter(s => {
    const yr = parseInt(s.split('-')[0], 10);
    return yr >= dec.start && yr <= dec.end;
  }).sort();

  decSeasons.forEach(s => {
    const sInfo = seasonsData[s];
    const sSponsor = sponsorMap[s];
    const images = seasonImages[s] || [];

    let techLabel = sSponsor ? sSponsor.tech : 'Sartoria Locale / Non formalizzato';
    let commLabel = sSponsor ? sSponsor.comm : '*Nessuno sponsor* (Pre-1981)';

    md += `### Stagione ${s} (${sInfo.division})\n\n`;
    md += `> **Fornitore Tecnico:** ${techLabel} | **Sponsor Commerciale:** ${commLabel} | **Scheda Stagione:** [[02-cronistoria/stagioni/${s}|${s}]]\n\n`;

    if (images.length > 0) {
      md += `<div class="jersey-gallery-grid" style="display: flex; gap: 1.2rem; flex-wrap: wrap; margin-top: 0.8rem; margin-bottom: 2rem;">\n`;
      images.forEach(img => {
        const cap = formatCaption(img.rawType);
        md += `  <div style="text-align: center; max-width: 160px; background: var(--light); padding: 0.5rem; border-radius: 8px; border: 1px solid var(--lightgray);">\n`;
        md += `    <a href="/assets/images/maglie/${img.file}" target="_blank" title="Clicca per ingrandire ad alta risoluzione">\n`;
        md += `      <img src="/assets/images/maglie/${img.file}" alt="${cap.title} Catania ${s}" style="width: 140px; height: auto; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.15); transition: transform 0.2s;" />\n`;
        md += `    </a>\n`;
        md += `    <p style="font-size: 0.82rem; margin: 0.4rem 0 0 0; line-height: 1.25;">\n`;
        md += `      <strong>${cap.title}</strong><br>\n`;
        md += `      <span style="font-size: 0.75rem; color: var(--gray);">${cap.sub}</span>\n`;
        md += `    </p>\n`;
        md += `  </div>\n`;
      });
      md += `</div>\n\n`;
    } else {
      md += `<p style="font-size: 0.88rem; color: var(--gray); margin-top: 0.4rem; margin-bottom: 1.8rem;">\n`;
      md += `  <em>Divisa tradizionale a strisce verticali rosse e azzurre con calzoncini azzurri e calzettoni neri con risvolto. Dati fotografici e reperti di maglia in corso di catalogazione archivistica.</em>\n`;
      md += `</p>\n\n`;
    }
  });

  md += `---\n\n`;
});

// Final sections
md += `## 4. Collegamenti e Voci Correlate

* [[05-identita-e-simboli/araldica-e-scudetti/index|Araldica, Simbologia e Stemmi Storici del Calcio Catania (u Liotru)]]
* [[05-identita-e-simboli/sponsor/index|Sponsor Tecnici e Commerciali del Calcio Catania (1979–Oggi)]]
* [[05-identita-e-simboli/araldica-e-scudetti/acquisizione-marchio-storico-2026|Acquisizione Marchio Storico all'Asta del 2026 (Matricola 11700)]]
* [[05-identita-e-simboli/mascotte-e-inni|Mascotte Agatino e Inni Ufficiali del Club]]
* [[07-media-e-comunicazione/letteratura/il-rosso-l-azzurro-novant-anni-di-una-maglia|Il rosso e l'azzurro. Novant'anni di una maglia (Opera Bibliografica GEO Edizioni)]]

---

## Fonti Certificate e Bibliografia

1. **Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino**, *Tutto il Catania minuto per minuto (1929–2010)*, GEO Edizioni, Empoli, 2010.
2. **Carlo Fontanelli, Roberto Quartarone, Alessandro Russo**, *Il rosso e l'azzurro. Novant'anni di una maglia*, GEO Edizioni, Empoli, 2020.
3. **Roberto Quartarone**, *Gli sponsor tecnici e commerciali del Catania dal 1979 ad oggi*, in [tuttoilcataniaminutoperminuto.it](https://www.tuttoilcataniaminutoperminuto.it/), 2024.
4. **Archivio Storico Mimmo Rapisarda** ([mimmorapisarda.it](https://www.mimmorapisarda.it/)), *Museo virtuale e archivio iconografico delle divise da gioco del Calcio Catania (1929–2026)*.
5. **Football Kit Archive** ([footballkitarchive.com](https://www.footballkitarchive.com/)), *Catania FC Kit History and Archive*.
`;

fs.writeFileSync('content/05-identita-e-simboli/maglie-e-divise.md', md, 'utf-8');
console.log('Successfully generated content/05-identita-e-simboli/maglie-e-divise.md');
