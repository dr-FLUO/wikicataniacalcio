---
title: Segnala una Correzione o Proponi una Fonte (Fact-Checking AI + Operatore)
description: Procedura di segnalazione errori, refusi statistici o invio di nuove
  fonti storiche per la Wiki Calcio Catania, sottoposta a verifica FactCheckAgent
  e revisione umana.
slug: segnala-correzione
entity_type: feedback_portal
status: verified
last_verified_date: 2026-10-27
tags:
- fact-checking
- collabora
- fonti
sources:
- author: Redazione & Architettura Wiki Calcio Catania
  title: Protocollo di Verifica Documentale e Fact-Checking Multi-Agente (SCHEMA.md)
  publisher: Wiki Calcio Catania
  year: 2026
---

# Segnala una Correzione o Proponi una Fonte

La **Wiki Calcio Catania** adotta un modello di **revisione controllata (*AI Fact-Checking + Human-in-the-Loop*)**: chiunque — storici locali, giornalisti, collezionisti o tifosi — può segnalare un errore statistico, una data imprecisa o proporre l'aggiunta di una fonte documentale per una specifica pagina.

> [!info] Come funziona il Processo di Verifica in 3 Passi
> 1. **Invio della Segnalazione con Fonte:** Compili i dati della rettifica indicando obbligatoriamente la **fonte verificabile** (volume, pagina d'almanacco, comunicato ufficiale FIGC, sentenza o articolo d'epoca).
> 2. **Pre-Istruttoria del `FactCheckAgent` (Squadra 1):** L'agente AI confronta la tua segnalazione con l'indice documentale interno (*Tutto il Catania minuto per minuto*, archivi storici, atti giudiziari) e valida la quadratura matematica tramite gli schemi **Pydantic v2** (`ExternalCorrectionSubmission`).
> 3. **Approvazione dell'Operatore e Pubblicazione Git:** Se la verifica ha esito positivo, viene generata una Pull Request (`git diff`) che l'operatore umano approva con un clic, aggiornando il sito statico in 30 secondi.

---

## Modulo Guidato di Segnalazione (Zero-Cookie & Conforme GDPR)

Il modulo sottostante prepara in locale nel tuo browser (senza alcun cookie di tracciamento) il pacchetto strutturato conforme al modello `ExternalCorrectionSubmission` pronto per l'invio alla coda di revisione:

| Campo Richiesto | Specifica di Validazione (`agents/models.py`) | Esempio di Compilazione Corretta |
| :--- | :--- | :--- |
| **1. Voce / Slug della Pagina** | `target_page_slug` (Percorso della voce nella Wiki) | `stagioni/2012-2013` oppure `vicende-legali/caso-catania-2003` |
| **2. Tipologia di Segnalazione** | `Errore Statistico` \| `Data o Fatto Storico` \| `Nuova Fonte Bibliografica` \| `Credito Fotografico` | `Errore Statistico` |
| **3. Testo o Dato Attuale** | Estratto del passaggio presente oggi nella pagina | *"Minuto 25: rete di Lodi su azione"* |
| **4. Correzione Proposta** | Il dato corretto da sostituire o integrare | *"Minuto 25: rete di Francesco Lodi su calcio di rigore"* |
| **5. Fonte Obbligatoria a Supporto** | **Autore, Titolo Opera/Testata, Anno, Pagina o URL** | *Lega Serie A, Tabellino Ufficiale Catania-Lazio 4-0 del 04/11/2012* |

---

## Schema Tecnico del Payload di Verifica (`FactCheckAgent`)

Ogni segnalazione viene validata contro il seguente schema JSON prima di entrare in coda di revisione:

```json
{
  "target_page_slug": "stagioni/2012-2013",
  "claim_type": "Errore Statistico",
  "current_text_excerpt": "4 novembre 2012 — Catania-Lazio 4-0",
  "proposed_correction": "Integrazione spettatori ufficiali: 12.987 paganti + abbonati",
  "supporting_source": {
    "author": "Lega Nazionale Professionisti Serie A",
    "title": "Comunicato Statistico 11ª Giornata Serie A 2012-2013",
    "publisher": "Lega Serie A",
    "year": 2012,
    "reference": "Tabellino gara Catania-Lazio 04/11/2012"
  }
}
```

> [!warning] Segnalazioni sul Diritto d'Autore (*Notice & Take-Down*)
> Per richieste relative alla paternità di fotografie storiche o all'aggiornamento delle licenze d'uso (`image_credits`), seleziona la tipologia **`Credito Fotografico`** indicando il nome dell'autore o dell'archivio titolare: la richiesta viene inoltrata con priorità immediata all'operatore responsabile.
