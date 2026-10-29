import { QuartzComponent, QuartzComponentConstructor } from "./types"

/**
 * Logica client del form "Segnala una correzione" (content/segnala-correzione.md).
 * Il markup del form vive nel markdown; qui c'è solo lo script, eseguito a ogni
 * navigazione SPA (evento "nav"), perché gli <script> inline nel markdown
 * vengono escapati da Quartz e non verrebbero eseguiti.
 *
 * Le segnalazioni finiscono nel Google Sheet privato della redazione tramite
 * la Web App di Google Apps Script (Strada A).
 */
const CorrectionForm: QuartzComponent = () => null

CorrectionForm.afterDOMLoaded = `
(function () {
  var GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbySEHojmpevpJprs5XUFIcpOjPOfgg0Bpls45DplJIbJSHS3n8kcQtWQbEWHNNNv7Zo/exec";
  var BTN_HTML = '<span class="nfc-btn-icon">■</span> <span>INVIA SEGNALAZIONE</span>';

  function init() {
    var form = document.getElementById("nfc-correction-form");
    if (!form || form.dataset.wccReady === "1") return;
    form.dataset.wccReady = "1";

    var targetInput = document.getElementById("corr-target-page");
    var targetBadge = document.getElementById("corr-target-badge");
    var msgInput = document.getElementById("corr-message");
    var contactInput = document.getElementById("corr-contact");
    var statusEl = document.getElementById("nfc-form-status");
    var submitBtn = document.getElementById("nfc-submit-btn");

    // Pagina di provenienza da ?voce=... (ignora la home "index")
    var params = new URLSearchParams(window.location.search);
    var voce = params.get("voce") || params.get("page") || "";
    if (voce && voce !== "index") {
      if (targetInput) targetInput.value = voce;
      if (targetBadge) {
        targetBadge.textContent = "Stai segnalando: " + voce;
        targetBadge.style.display = "inline-block";
      }
    }

    function setStatus(kind, html) {
      if (!statusEl) return;
      statusEl.style.display = "block";
      statusEl.className = "nfc-form-status nfc-form-status--" + kind;
      statusEl.innerHTML = html;
    }

    function resetBtn() {
      if (!submitBtn) return;
      submitBtn.disabled = false;
      submitBtn.style.opacity = "1";
      submitBtn.innerHTML = BTN_HTML;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msgVal = (msgInput && msgInput.value || "").trim();
      if (!msgVal) {
        setStatus("error", "<strong>Attenzione:</strong> scrivi cosa va corretto prima di inviare.");
        if (msgInput) msgInput.focus();
        return;
      }
      var pageVal = (targetInput && targetInput.value || "").trim() || "Non specificata";
      var contactVal = (contactInput && contactInput.value || "").trim() || "Anonimo";

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.7";
        submitBtn.textContent = "INVIO IN CORSO…";
      }

      fetch(GOOGLE_SHEET_URL, {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify({
          pagina: pageVal,
          messaggio: msgVal,
          contatto: contactVal,
          data: new Date().toLocaleString("it-IT")
        })
      })
        .then(function () {
          setStatus("success", "✓ <strong>Segnalazione inviata!</strong><br>Grazie: la redazione la verificherà e aggiornerà la voce.");
          if (msgInput) msgInput.value = "";
          if (contactInput) contactInput.value = "";
          resetBtn();
        })
        .catch(function () {
          setStatus("error", "<strong>Invio non riuscito.</strong> Controlla la connessione e riprova.");
          resetBtn();
        });
    });
  }

  document.addEventListener("nav", init);
  init();
})();
`

CorrectionForm.css = `
.nfc-form-status--success {
  border-left: 4px solid #1f8a3a;
  background: rgba(31, 138, 58, 0.08);
  padding: 0.75rem 1rem;
  margin: 0.75rem 0;
}
.nfc-form-status--error {
  border-left: 4px solid #d11317;
  background: rgba(209, 19, 23, 0.08);
  padding: 0.75rem 1rem;
  margin: 0.75rem 0;
}
`

export default (() => CorrectionForm) satisfies QuartzComponentConstructor
