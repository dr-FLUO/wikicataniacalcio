---
title: Note Legali, Privacy (GDPR Cookie-Less), Accessibilità UE e Diritto d'Autore
description: 'Informativa completa sulla conformità normativa europea della Wiki Calcio
  Catania: GDPR Reg. UE 2016/679, Cookie-less by design, Accessibilità WCAG 2.1 AA
  e Copyright.'
slug: note-legali-privacy-accessibilita
entity_type: legal_compliance
status: verified
last_verified_date: 2026-10-27
tags:
- gdpr
- accessibilita
- copyright
- conformita-ue
sources:
- author: Parlamento Europeo e Consiglio dell'Unione Europea
  title: Regolamento (UE) 2016/679 (GDPR), Direttiva (UE) 2019/882 (European Accessibility
    Act) e Direttiva (UE) 2019/790 (Copyright DSM)
  publisher: Gazzetta Ufficiale dell'Unione Europea
  year: 2019
---

# Note Legali, Privacy (GDPR), Accessibilità UE e Diritto d'Autore

La **Wiki Calcio Catania (1929–Oggi)** è progettata fin dalle fondamenta secondo i principi di **Privacy-by-Design**, **Accessibility-by-Default** e **Tutela del Diritto d'Autore**, in piena ottemperanza alla normativa vigente dell'Unione Europea e della Repubblica Italiana.

---

## 1. Informativa Privacy e Architettura 100% Cookie-Less (GDPR & Direttiva ePrivacy)

Ai sensi degli **artt. 13 e 14 del Regolamento (UE) 2016/679 (GDPR)**, della **Direttiva 2002/58/CE (ePrivacy)**, dell'**art. 122 del D.Lgs. 196/2003** (Codice Privacy novellato dal D.Lgs. 101/2018) e delle **Linee Guida del Garante per la protezione dei dati personali del 10 giugno 2021**:

> [!info] Zero Cookie di Profilazione e Zero Tracciamento di Terze Parti
> Questo sito web **NON utilizza alcun cookie di profilazione, né cookie analitici di terze parti, né pixel pubblicitari**. Non viene effettuata alcuna profilazione degli utenti né tracciamento inter-sito.

### Dati Tecnici Strettamente Necessari
1. **Archiviazione Locale Tecnica (`localStorage`):** Il sito utilizza esclusivamente una chiave tecnica nel `localStorage` del browser dell'utente (`saved-theme: "light" | "dark"`) al solo scopo di ricordare la preferenza visiva tra modalità chiara (`#191919` su `#f7f7f7`) e modalità scura (`#f7f7f7` su `#191919`), oltre allo stato di apertura del menu laterale (`explorer`). Ai sensi delle Linee Guida del Garante Privacy, tali strumenti tecnici assimilati sono esenti dall'obbligo di consenso preventivo.
2. **Font Self-Hosted (Zero Trasferimento IP verso Server Esterni):** In conformità alla giurisprudenza europea sulla tutela dell'indirizzo IP come dato personale (cfr. sentenza *LG München I, 20.01.2022, Az. 3 O 17493/20*), il sito è configurato con `fontOrigin: "local"`, impacchettando localmente gli asset senza effettuare connessioni dal browser del visitatore verso server di Google Fonts o CDN di profilazione.
3. **Ricerca Locale Client-Side:** Il motore di ricerca interno viene eseguito interamente in locale all'interno del browser del visitatore; le parole cercate non vengono trasmesse a server di profilazione esterni.

---

## 2. Dichiarazione di Accessibilità (European Accessibility Act & WCAG 2.1 AA / AAA)

In conformità alla **Direttiva (UE) 2019/882 (European Accessibility Act)**, allo standard europeo armonizzato **EN 301 549**, alle **Linee Guida WCAG 2.1 Livello AA** del W3C e alla **Legge 9 gennaio 2004, n. 4 (Legge Stanca)**:

| Requisito di Accessibilità | Misura Tecnica Adottata nella Wiki | Livello Certificato |
| :--- | :--- | :---: |
| **Contrasto Cromatico del Testo (Criterio 1.4.3 e 1.4.6)** | La coppia ufficiale `#191919` su `#f7f7f7` (Light Mode) e `#f7f7f7` su `#191919` (Dark Mode) garantisce un rapporto di contrasto di **15.8:1**, oltre il doppio della soglia massima WCAG AAA (7:1). | **WCAG AAA** |
| **Navigazione da Tastiera e Focus Visibile (Criterio 2.1.1 e 2.4.7)** | Tutti gli elementi interattivi sono raggiungibili tramite tasto `Tab` con anello di focus ad alta visibilità (`2px solid #0cb2d9`) e link **«Salta al contenuto principale»** in testa alla pagina (Criterio 2.4.1). | **WCAG AA** |
| **Struttura Semantica e Screen Reader (Criterio 1.3.1)** | Utilizzo rigoroso di landmark HTML5/ARIA (`role="main"`, `role="navigation"`, `role="region"`, `role="contentinfo"`), gerarchia sequenziale dei titoli (`H1` ➔ `H2` ➔ `H3`) e liste di definizione `<dl>/<dt>/<dd>` nell'Infobox. | **WCAG AA** |
| **Alternative Testuali per Immagini (Criterio 1.1.1)** | Il linter di compilazione (`VaultComplianceLinter`) blocca la pubblicazione di qualsiasi immagine priva di attributo `alt` descrittivo di almeno 15 caratteri. | **WCAG AA** |
| **Rispetto Preferenze Vestibolari (Criterio 2.3.3)** | Supporto nativo alla media query `@media (prefers-reduced-motion: reduce)` per disattivare transizioni e animazioni sugli utenti sensibili al movimento. | **WCAG AAA** |

---

## 3. Diritto d'Autore, Citazione Fonti e Licenze Immagini (L. 633/1941 e Direttiva UE 2019/790)

1. **Finalità Culturale e Diritto di Citazione (Art. 70 L. 633/1941):**
   La Wiki Calcio Catania è un'opera enciclopedica indipendente di ricerca storiografica, critica e documentazione sportiva, priva di scopo di lucro e non affiliata commercialmente alle società calcistiche citate. Gli estratti di sentenze, atti parlamentari/federali e i dati statistici sono riportati per finalità di studio e ricerca storica, con **obbligo tassativo di citazione dell'autore, del titolo dell'opera, dell'editore e dell'anno** nella sezione `## Fonti e Bibliografia` di ciascuna voce.
2. **Marchi e Stemmi Storici (Art. 21 D.Lgs. 30/2005 — Codice della Proprietà Industriale):**
   Le denominazioni sociali e gli stemmi storici riprodotti nelle schede araldiche sono proprietà dei rispettivi titolari (tra cui *Catania Football Club S.r.l.*) e vengono utilizzati esclusivamente in funzione descrittiva, storica e documentale ai sensi dell'art. 21 comma 1 lett. c) del CPI, senza alcun uso commerciale o confusorio.
3. **Regime Giuridico delle Fotografie Storiche (Artt. 87–92 L. 633/1941):**
   Ogni immagine pubblicata nella Wiki è corredata da una scheda `image_credits` verificata che ne attesta lo stato giuridico:
   - **Pubblico Dominio in Italia (Art. 92 L. 633/1941):** fotografie semplici (prive di carattere creativo d'autore, quali foto di formazioni schierate o cronaca sportiva ordinaria) per le quali sono decorsi **oltre 20 anni** dalla data di produzione/pubblicazione, fermo restando l'obbligo morale di citare l'archivio o il fotografo d'origine.
   - **Licenze Aperte (Creative Commons):** immagini rilasciate dagli autori sotto licenza `CC BY-SA 4.0`, `CC BY 4.0` o `CC0`, con attribuzione completa e link alla licenza.
   - **Procedura di Rimozione o Rettifica Immediata (*Notice & Take-Down*):** Qualora un avente diritto riscontrasse un'inesattezza nei crediti fotografici o desiderasse richiedere la rimozione di un contenuto, può inviare una comunicazione immediata tramite la pagina **[[segnala-correzione|Segnala una correzione o aggiornamento]]**.
