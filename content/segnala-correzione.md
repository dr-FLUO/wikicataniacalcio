---
title: Segnala una Correzione o Proponi una Fonte
description: Segnala in pochi secondi un refuso statistico, una data errata o proponi una fonte documentale per la Wiki Calcio Catania.
slug: segnala-correzione
entity_type: feedback_portal
status: verified
last_verified_date: 2026-10-29
tags:
- fact-checking
- collabora
- fonti
sources:
- author: Redazione & Fact-Checking Wiki Calcio Catania
  title: Protocollo di Revisione e Fact-Checking
  publisher: Wiki Calcio Catania
  year: 2026
---

# Segnala un Errore o Invia una Correzione

Hai notato un refuso statistico, una data imprecisa o vuoi proporre una nuova fonte d'archivio?  
Questa enciclopedia è un'opera aperta e indipendente: ogni segnalazione verificabile ci aiuta a rendere l'archivio sempre più accurato.

<!-- NB: non inserire righe vuote né indentazioni dentro questo blocco HTML, altrimenti il markdown lo trasforma in codice. La logica di invio è in quartz/components/CorrectionForm.tsx -->
<div class="nfc-correction-box">
<div class="nfc-correction-header">
<div class="nfc-correction-kicker">SPORTELLO DI REVISIONE RAPIDA · WIKI CATANIA CALCIO</div>
<h2 class="nfc-correction-title">Cosa c'è da correggere o integrare?</h2>
<div id="corr-target-badge" class="nfc-correction-badge" style="display:none;"></div>
</div>
<form id="nfc-correction-form" class="nfc-form-grid" novalidate>
<div class="nfc-form-row" id="corr-page-row">
<label for="corr-target-page"><span>Pagina di riferimento</span> <span class="nfc-opt">compilata in automatico, modificabile</span></label>
<input type="text" id="corr-target-page" name="target_page" placeholder="Es. stagione 2012-2013, Giuseppe Mascara, Stadio Cibali…" />
</div>
<div class="nfc-form-row">
<label for="corr-message"><span>Cosa va corretto o aggiunto? <span class="nfc-req">*</span></span></label>
<textarea id="corr-message" name="message" rows="5" placeholder="Es. «Il gol del 2-1 contro il Palermo lo ha segnato Martínez, non Morimoto. Fonte: tabellino Gazzetta dello Sport del 12/03/2012»" required></textarea>
<span class="nfc-form-hint">Scrivi liberamente. Se puoi, indica dove l'hai verificato (almanacco, giornale, sito…).</span>
</div>
<div class="nfc-form-row">
<label for="corr-contact"><span>Nome o email <span class="nfc-opt">(facoltativo, solo se vuoi una risposta)</span></span></label>
<input type="text" id="corr-contact" name="contact" placeholder="Es. Mario Rossi – mario.rossi@email.it" />
</div>
<div class="nfc-form-actions">
<button type="submit" id="nfc-submit-btn" class="nfc-correction-submit-btn"><span class="nfc-btn-icon">■</span> <span>INVIA SEGNALAZIONE</span></button>
<div id="nfc-form-status" class="nfc-form-status" style="display:none;" role="status" aria-live="polite"></div>
<p class="nfc-form-privacy-note">🔒 <strong>Zero cookie e massima riservatezza:</strong> i dati inseriti non vengono ceduti a terzi e sono letti unicamente dalla redazione per correggere la voce.</p>
</div>
</form>
</div>

---

> [!tip] Come trattiamo le segnalazioni
> Ogni correzione viene confrontata con le fonti primarie dell'archivio (almanacchi, comunicati ufficiali FIGC/Lega e atti giudiziari). Non appena riscontrata la quadratura del dato, la voce viene aggiornata e pubblicata.
