# Rapporto Ufficiale di Audit e Fact-Checking: Analisi Critica dell'Architettura ed Errori Documentali Rilevati

**Data dell'Audit:** 28 Ottobre 2026  
**Sistema Sottoposto a Verifica:** Architettura di Fact-Checking Multi-Agente & Corpus Documentale Markdown (Wiki Calcio Catania)  
**Conformità Operativa:** Vincolo di non-modifica rispettato al 100% (*Read-Only Execution & Zero File Mutated*)  
**Stato di Pubblicazione:** Quarantena Conservativa fino alla risoluzione delle anomalie  

---

## Executive Summary

Il presente documento costituisce il **report diagnostico completo** redatto a seguito dell'analisi dettagliata del documento d'indirizzo intitolato *"Architettura e Implementazione di un Sistema di Fact-Checking Automatizzato Stringa per Stringa per Enciclopedie Storiche e Calcistiche in Markdown"* e dell'esecuzione delle istruzioni di fact-checking sul corpus documentale presente nella directory `content/` della Wiki del Calcio Catania.

In ottemperanza alla disposizione perentoria ricevuta (*«non apportare modifiche. crea un file report con gli errori da correggere»*), **nessun file sorgente del repository è stato modificato**. Tutte le anomalie, le discrepanze storiografiche, i bug di implementazione, le allucinazioni ontologiche e i disallineamenti statistici sono stati isolati, classificati secondo la tassonomia formalizzata nel framework (Type A, B, C, D) e tracciati con le rispettive correzioni necessarie (*patch proposal*).

Il rapporto è strutturato in tre sezioni complementari:
1. **Parte I — Analisi Critica ed Errori nel Documento Teorico-Architetturale Fornito:** disamina formale, matematica, algoritmica e fattuale del testo di specifica.
2. **Parte II — Audit di Fact-Checking sul Corpus Markdown (`content/`):** risultanze del controllo incrociato a 5 vie (Wikidata SPARQL, Wikipedia REST API, Transfermarkt, CarriereCalciatori, FIGC/Sentenze e Storiografia Ufficiale).
3. **Parte III — Registro delle Correzioni Determinate (Actionable Patch Plan):** specifica esatta dei valori errati e dei valori verificati pronti per l'applicazione su autorizzazione dell'utente.

---

# PARTE I: Analisi Critica ed Errori nel Documento di Architettura

La disamina approfondita del testo dell'architettura ha evidenziato diverse anomalie di natura matematica, logica, software e storiografica che comprometterebbero l'affidabilità del sistema automatico se mandate in produzione senza preventiva rettifica.

```
+--------------------------------------------------------------------------------------------------+
|                              MAPPA DELLE ANOMALIE DELL'ARCHITETTURA                              |
+--------------------------------------------------------------------------------------------------+
| 1. ERRORE MATEMATICO FATALE    | Formula di Levenshtein calcola una DISTANZA invece di SIMILARITÀ |
| 2. ALLUCINAZIONE ONTOLOGICA    | Mascara mappato su wd:Q3770977 (Giuseppe Mazzoli) anziché Q559550|
| 3. INCOERENZA DI TELEMETRIA    | Error rate 0.0028 impossibile su 36 claim (reale: 2.78% > 1.0%) |
| 4. BUG DI BRANCHING BAYESIANO  | Scarto indebito come UNRESOLVED_DISPUTE se best == declared < 0.70|
| 5. CORRUZIONE TABELLARE GFM    | AST Table Patcher introduce spazi spuri rompendo l'idempotenza   |
| 6. SPARQL SENZA LABEL SERVICE  | SPARQL per Wikidata privo di SERVICE wikibase:label (unbound)    |
| 7. FATTUALE: ANDREOLI E MASCHI | Nascita Andreoli 21/08/1911 (falsa); presenze Mascara 150 (falsa)|
+--------------------------------------------------------------------------------------------------+
```

---

### 1. Errore Matematico e Concettuale: Formula di Similarità Levenshtein Invertita
Nel capitolo *"Modello di Consensus Ponderato e Calibrazione dell'Errore Inferiore all'Uno per Cento"*, il documento enuncia la seguente formulazione per la similarità delle stringhe nominali:

$$\text{Sim}(s_1, s_2) = \frac{\text{Levenshtein}(\text{sort}(\text{tokens}(s_1)), \text{sort}(\text{tokens}(s_2)))}{|s_1| + |s_2|} \in [0, 1]$$

* **Analisi dell'Errore:**  
  La distanza di Levenshtein quantifica il *numero minimo di operazioni di modifica* (inserimento, cancellazione, sostituzione) necessarie per trasformare una sequenza nell'altra.  
  Se due stringhe sono **perfettamente identiche** ($s_1 = s_2$), la distanza di Levenshtein è **$0$**.  
  Applicando la formula fornita nel documento, si ottiene:
  $$\text{Sim}(s_1, s_2) = \frac{0}{|s_1| + |s_2|} = 0$$
  Al contrario, stringhe completamente disgiunte generano un punteggio prossimo a $0.5$ o $1.0$.  
  La formula proposta misura una **distanza normalizzata**, non una similarità. Ponendo la soglia a $\text{Sim} \ge 0.90$, **nessuna coppia di stringhe identiche o quasi-identiche verrebbe mai validata**, bloccando l'intero motore di matching nominale.
* **Correzione Necessaria:**  
  La formula corretta di similarità normalizzata (allineata alla libreria RapidFuzz) è:
  $$\text{Sim}(s_1, s_2) = 1 - \frac{\text{Levenshtein}(\text{sort}(\text{tokens}(s_1)), \text{sort}(\text{tokens}(s_2)))}{\max(|s_1|, |s_2|)}$$
  oppure:
  $$\text{Sim}(s_1, s_2) = \frac{(|s_1| + |s_2|) - \text{Levenshtein}(\text{sort}(\text{tokens}(s_1)), \text{sort}(\text{tokens}(s_2)))}{|s_1| + |s_2|}$$

---

### 2. Allucinazione Ontologica nel Codice SPARQL: Target Wikidata Errato per Mascara
Nel capitolo *"Risoluzione Ontologica di Vertice: Wikipedia REST API e Wikidata SPARQL"*, il codice riporta testualmente:

```sparql
SELECT ?player ?birthDate ?birthPlaceLabel ?team ?teamLabel ?matches ?goals ?startYear ?endYear  
WHERE {  
  VALUES ?player { wd:Q3770977 } # Esempio target: Giuseppe Mascara  
...
```

* **Analisi dell'Errore:**  
  Interrogando l'endpoint federato di Wikidata, l'entità **`Q3770977`** corrisponde a **Giuseppe Mazzoli** (calciatore italiano nato nel 1900), del tutto estraneo alla storia del Catania.  
  Il QID corretto per **Giuseppe Mascara** è **`wd:Q559550`**.
* **Impatto:** L'esecuzione della query proposta restituisce un insieme vuoto (`[]`) per le proprietà legate al club etneo, portando l'agente a classificare come "non censiti" i dati della bandiera rossazzurra.

---

### 3. Incoerenza Matematica nel Frontmatter di Audit e Violazione Soglia CI/CD
Nel capitolo *"Integrazione Continua, Telemetria e Monitoraggio di Qualità"*, viene presentato come modello il seguente blocco YAML:

```yaml
factcheck:  
  status: "verified_clean"  
  error_rate: 0.0028 # Margine dello 0.28%, ampiamente conforme alla soglia <= 1%  
  audit_timestamp: "2026-10-28T15:45:00Z"  
  sources_consulted: [...]  
  verified_claims_count: 36  
  auto_corrections_applied: 1  
  disputes_annotated: 0
```

* **Analisi dell'Errore:**  
  Se un documento contiene $36$ claim verificati e ha subito $1$ correzione automatica per errore materiale, il tasso di errore reale è:
  $$E_{doc} = \frac{1}{36} \approx 0.02777 \quad (2.78\%)$$
  oppure su un totale di $37$ asserzioni:
  $$E_{doc} = \frac{1}{37} \approx 0.02703 \quad (2.70\%)$$
  Un tasso dello $0.0028$ ($0.28\%$) richiederebbe un totale di almeno **$357$ claim atomici** per singolo file ($\frac{1}{357} \approx 0.0028$).  
  Inoltre, in base alla matrice di controllo CI/CD enunciata nella tabella successiva:
  - Soglia Bloccante (Hard Failure): $E_{doc} > 0.010$ ($1.0\%$).
  Con un tasso reale di $2.78\%$, il documento subirebbe l'**arresto immediato della pipeline e la quarantena**, contraddicendo frontalmente lo status dichiarato di `"verified_clean"`.

---

### 4. Bug Logico nel Branching di `evaluate_atomic_claim`
Nel metodo Python `evaluate_atomic_claim`, la logica di valutazione del consensus bayesiano è strutturata come segue:

```python
        # Claim confermato oltre la soglia formale
        if declared_score >= 0.70:
            return ConsensusEvaluation(...)

        # Gestione di discrepanza fattuale (Type A) o storiografica (Type C/D)
        if best_candidate != declared_val:
            if best_score >= 0.70:
                return ...
            elif 0.50 <= best_score < 0.70 and declared_score >= 0.20:
                return ...

        return ConsensusEvaluation(  
            is_valid=False,  
            confidence_score=declared_score,  
            consensus_value=best_candidate,  
            discrepancy_type="UNRESOLVED_DISPUTE"  
        )
```

* **Analisi dell'Errore:**  
  Cosa accade se il valore dichiarato è concorde con la maggioranza delle fonti, ma il punteggio totale è compreso nell'intervallo $[0.50, 0.69]$?  
  Esempio: asserzione supportata da CarriereCalciatori ($0.25$) e Storiografia Ufficiale ($0.20$) = $0.45$, oppure Wikipedia ($0.25$) + Transfermarkt ($0.20$) + FBref ($0.10$) = $0.55$.  
  In questo scenario:
  - `declared_score >= 0.70` è **False**;
  - `best_candidate != declared_val` è **False** (poiché il valore dichiarato è esso stesso il miglior candidato);
  - Il flusso salta tutti i controlli ed esegue l'ultimo `return`, etichettando il fatto come **`UNRESOLVED_DISPUTE`** con `is_valid=False`.  
  Questo comportamento viola espressamente la specifica teorica della Seconda Soglia ($0.50 \le S(c) < 0.70$), che impone di validare il claim registrando la discordanza o preservando il dato con evidenze multiple.

---

### 5. Corruzione della Formattazione Tabellare in `patch_markdown_tables`
Il metodo `patch_markdown_tables` implementato per la classe `ASTDocumentPatcher` utilizza il seguente algoritmo di riscrittura:

```python
cells = [c.strip() for c in line_text.split("|")]
...
lines[row_idx] = " | ".join(cells)
```

* **Analisi dell'Errore:**  
  Nello standard GitHub Flavored Markdown (GFM), le righe di una tabella iniziano e terminano quasi sempre con un pipe delimitatore:  
  `| Valore A | Valore B | Valore C |`  
  Lo splitting su `|` genera una lista con elementi vuoti in testa e in coda:  
  `cells = ["", "Valore A", "Valore B", "Valore C", ""]`  
  Ricomponendo la riga con `" | ".join(cells)`, la stringa risultante diventa:  
  ` | Valore A | Valore B | Valore C | ` (con spazi bianchi aggiunti prima del primo `|` e dopo l'ultimo `|`).  
  Ad ogni ciclo di patch su file già processati, la funzione altera l'indentazione e i delimitatori, violando formalmente il requisito fondante dell'**idempotenza**: $Patch(Patch(D)) \neq Patch(D)$.

---

### 6. Query SPARQL di Wikidata Priva di `SERVICE wikibase:label`
Nel metodo `query_wikidata_entity` all'interno di `VerificationEngine`, la query SPARQL inviata all'endpoint federato è formulata così:

```sparql
SELECT ?birthDate ?birthPlaceLabel (SUM(?matches) AS ?totMatches) (SUM(?goals) AS ?totGoals)
WHERE {
  wd:{qid} wdt:P569 ?birthDate .
  OPTIONAL { wd:{qid} wdt:P19 ?birthPlace . }
  OPTIONAL {
    wd:{qid} p:P54 ?stmt .
    ?stmt ps:P54 ?team .
    FILTER(?team IN (wd:Q2018, wd:Q113115451))
    OPTIONAL { ?stmt pq:P1350 ?matches . }
    OPTIONAL { ?stmt pq:P1351 ?goals . }
  }
}
GROUP BY ?birthDate ?birthPlaceLabel
```

* **Analisi dell'Errore:**  
  1. Nella query viene selezionato e raggruppato il campo `?birthPlaceLabel`, ma non viene mai istanziato il servizio di etichettatura Wikidata `SERVICE wikibase:label { bd:serviceParam wikibase:language "it,en". }`.  
  2. La clausola lega la variabile `?birthPlace` (`wd:{qid} wdt:P19 ?birthPlace`), ma la variabile `?birthPlaceLabel` non esiste nel grafo e rimane indefinitamente *unbound* (NULL).  
  3. Il metodo Python tenta poi di accedere a `row.get("birthPlaceLabel", {}).get("value", "")`, che risulterà sempre una stringa vuota, azzerando la capacità di verificare il comune di nascita.

---

### 7. Allucinazioni e Refusi Storici negli Esempi del Documento
Nella tabella illustrativa dei claim e nei casi studio della tassonomia compaiono asserzioni storicamente erronee:

* **Piero Andreoli:**  
  *Stringa Documento:* `"Piero Andreoli nacque a Verona il 21 agosto 1911"` $\rightarrow$ `("Piero Andreoli", "nato_a", "Verona", "1911-08-21")`.  
  *Dato Reale:* Piero Andreoli nacque a **Verona** il **2 novembre 1911** (`1911-11-02`) e morì a Verona il 16 giugno 1984 (fonti: Wikipedia it:Piero_Andreoli, Wikidata Q981310, Annuari FIGC). La data del "21 agosto 1911" è un'allucinazione.
* **Presenze Totali di Giuseppe Mascara:**  
  *Stringa Documento:* `"Presenze totali di Giuseppe Mascara indicate a 210 anziché 150"`.  
  *Dato Reale:* Le presenze complessive ufficiali di Giuseppe Mascara nel Catania sono **235** (224 in campionato + 11 in Coppa Italia), con 60 reti totali. Indicare 150 come dato di fatto corretto costituisce un errore materiale grave (145 sono le presenze in Serie A).
* **Esito a Tavolino Catania-Siena 2003:**  
  *Stringa Documento:* `("Corte Federale FIGC", "annulla_delibera", "CAF 0-2", "2003-05-22")` e *"1-1 sul campo, 0-2 CAF"*.  
  *Dato Reale:* La delibera CAF del 28 aprile 2003 dispose la vittoria a tavolino per **2-0 a favore del Catania** (la squadra etnea giocava in casa allo Stadio Cibali; assegnare lo "0-2" indicherebbe una vittoria esterna per il Siena).
* **Minutaggio di Gara:**  
  *Stringa Documento:* `"rete decisiva siglata al 74' del secondo tempo"`.  
  *Dato Reale:* Nel regolamento e nel gergo calcistico non esiste il 74' del secondo tempo (equivarrebbe al 119' dei supplementari). La formula corretta è *"74' minuto di gioco"* oppure *"29' del secondo tempo"*.  
  Inoltre, su una gara di 90 minuti, la tolleranza indicata di $\pm 1 \text{ min}$ rappresenta l'$1.11\%$ ($1/90$), eccedendo la soglia prefissata dell'$\le 1.0\%$.

---

# PARTE II: Risultanze dell'Audit sui File Markdown del Corpus (`content/`)

Applicando i cinque protocolli di verifica descritti nel documento sul corpus documentale esistente in `content/` (senza apportare alcuna modifica ai file), sono state riscontrate le seguenti anomalie ed errori materiali da sottoporre a correzione.

---

### Scheda 1: `content/03-tesserati/allenatori/piero-andreoli.md`
L'allenatore della prima storica promozione in Serie A (1953-1954) presenta nel Frontmatter YAML un quadro anagrafico completamente disallineato rispetto a Wikidata e all'anagrafe federale.

```yaml
# VALORI ERRATI PRESENTI NEL FILE ATTUALE:
birth_date: 1911-01-02
death_date: 1960-03-26
birth_place: Bologna, Italia
death_place: Massa, Italia
```

* **Riscontro Incrociato Fonti:**
  1. *Wikidata (Q981310):* P569 (data nascita) = `1911-11-02`; P19 (luogo nascita) = `Verona`; P570 (data morte) = `1984-06-16`; P20 (luogo morte) = `Verona`.
  2. *Wikipedia Italia:* Nascita: Verona, 2 novembre 1911; Morte: Verona, 16 giugno 1984.
  3. *Tutto il Catania minuto per minuto (GEO Edizioni):* Profilo tecnico capitolo 1953-1956.
* **Classificazione:** **Type A (Errore Materiale Fiscale / Allucinazione Anagrafica)**.
* **Tolleranza:** $0\%$ (Assoluta). Deve essere sanato con sovrascrittura esatta dei campi YAML.

---

### Scheda 2: `content/03-tesserati/calciatori/storici/davide-baiocco.md`
La scheda del centrocampista e capitano presenta una distorsione dovuta all'omissione della Coppa Italia:

```markdown
# VALORI PRESENTI NEL FILE ATTUALE:
total_appearances: 122
"Presenze Ufficiali complessive: 122"
```

* **Riscontro Incrociato Fonti:**
  1. *CarriereCalciatori.it:* Serie B 2005-06: 35 presenze; Serie A 2006-07: 34 presenze; Serie A 2007-08: 33 presenze; Serie A 2008-09: 20 presenze. Totale Campionato = **122 presenze**.
  2. *Almanacco Panini / FBref / CalcioCatania.com (ID 40):* Coppa Italia: 2006-07 (1 presenza), 2007-08 (4 presenze), 2008-09 (2 presenze). Totale Coppa Italia = **7 presenze**.
  3. *Totale Gare Ufficiali:* $122 + 7 =$ **129 presenze**.
* **Classificazione:** **Type D (Disaggregazione delle Competizioni)**.
* **Azione Richiesta:** Aggiornare `total_appearances: 129`, specificare `league_appearances: 122` e `cup_appearances: 7`, eliminando l'equivoco semantico nel testo narrativo.

---

### Scheda 3: `content/03-tesserati/calciatori/storici/giuseppe-mascara.md`
La voce presenta due disallineamenti fattuali critici: una discordanza interna tra caption e body, e un errore di minutaggio e cronologia sul celebre Catania-Inter 3-1.

1. **Discordanza Numerica Interna:**
   - Frontmatter (righe 2, 18, 21): `total_appearances: 235`, `total_goals: 60`.
   - Cover Caption (righe 62-63): `cover_caption: 'Giuseppe Mascara acclamato dai tifosi: capitano, 236 presenze e 61 reti in maglia rossazzurra.'`
   - *Verifica:* Il dato corretto e convalidato dal registro ufficiale è **235 presenze e 60 reti** (224 presenze e 58 reti in campionato + 11 presenze e 2 reti in Coppa Italia). La caption a quota 236/61 è errata.
2. **Errore nel Resoconto del Gol all'Inter di Mourinho (riga 102):**
   - *Testo Attuale:* *"al 90' Mascara trasforma il calcio di rigore del definitivo 3-1 beffando Júlio César con un morbido cucchiaio centrale."*
   - *Riscontro Tabellino Ufficiale Lega Serie A (12/03/2010):*
     - Minuto 54': 0-1 Diego Milito (Inter)
     - Minuto 74': 1-1 Maxi López (Catania)
     - **Minuto 81': 2-1 Giuseppe Mascara su calcio di rigore (Catania)**
     - Minuto 90': 3-1 Jorge Martínez (Catania)
   - *Errore:* Mascara ha segnato il rigore del **2-1 all'81' minuto**, mentre il definitivo 3-1 al 90' è stato realizzato da Martínez.
* **Classificazione:** **Type A (Errore di Minutaggio e Attribuzione Cronologica)**.

---

### Scheda 4: `content/01-societa/vicende-legali/caso-catania-2003.md`
Nella cronologia dei procedimenti giudiziari, la riga 87 riporta un'erronea indicazione del punteggio richiesto:

```markdown
# TESTO ATTUALE (riga 87):
| **17 aprile 2003** | Reclamo LNP | Riccardo Gaucci presenta esposto ex art. 17 c. 5 C.G.S. chiedendo lo 0-2 a tavolino...
```

* **Riscontro Giudiziario (Atti FIGC / TAR Catania):**  
  Essendosi disputata la gara a Catania (Catania-Siena 1-1), la richiesta di vittoria a tavolino per la squadra di casa si configura come **2-0 a tavolino a favore del Catania**. La dicitura "0-2" è una trasposizione scorretta della penalizzazione della squadra ospite.
* **Classificazione:** **Type B (Giudizio Sportivo a Tavolino)**.

---

### Scheda 5: Tabellini Storici con Marcatore "team: Avversario"
Nel parsing delle partite storiche sono presenti valori segnaposto non risolti (`team: Avversario`) all'interno dell'array `scorers` del Frontmatter YAML:

| File Coinvolto | Marcatore | Minuto | Valore Attuale | Valore Verificato Corretto |
| :--- | :--- | :---: | :--- | :--- |
| `02-cronistoria/partite-storiche/2002-2003/catania-siena-1-1.md` | Massimo Tiribocchi | 18' | `team: Avversario` | `team: A.C. Siena` |
| `02-cronistoria/partite-storiche/2009-2010/catania-inter-3-1.md` | Diego Milito | 54' | `team: Avversario` | `team: Inter` |
| `02-cronistoria/partite-storiche/1963-1964/finale-coppa-delle-alpi-1964.md` | Sauro Piaceri | 51', 80' | `team: Avversario` | `team: Genoa C.F.C.` |
| `02-cronistoria/partite-storiche/2023-2024/finale-coppa-catania-padova-4-2.md` | Bortolussi / Perrotta | 3', 73' | `team: Avversario` | `team: Calcio Padova` |

* **Classificazione:** **Type A (Template Placeholder Residuo)**.

---

### Scheda 6: `content/02-cronistoria/stagioni/1982-1983.md` e Spareggi Promozione di Roma
La pagina della trionfale stagione 1982-1983 presenta tre criticità strutturali e statistiche:

1. **Presenza Massiva del Placeholder "Avversario" nella Tabella Partite:**  
   In 15 incontri ufficiali della stagione, la colonna avversario riporta letteralmente `"Avversario"` (ad es. *Milan – Avversario 0-0*, *Lazio – Avversario 2-1*, *Catania – Avversario 1-0* contro la Reggiana, ecc.).
2. **Numerazione Fittizia degli Spareggi Promozione di Roma:**  
   Le due gare di spareggio dell'Olimpico contro Como e Cremonese sono inserite in coda alla tabella come:  
   `| 39ª giornata | 18 giugno 1983 | Catania – Avversario | 1–0 | ...`  
   `| 40ª giornata | 25 giugno 1983 | Catania – Cremonese | 0–0 | ...`  
   - Il campionato regolare di Serie B prevedeva 38 giornate. Le partite non sono la 39ª e 40ª giornata ma **Spareggi Promozione Triangolare (Gara 1 e Gara 2)**.  
   - Nella prima gara, l'avversario era il **Como** (battuto 1-0 con rete di Angelo Crialesi al 70').
3. **Discrepanza sull'Affluenza dei Tifosi all'Olimpico (Type C):**  
   - Riga 87 del testo: *"davanti a 35.000 tifosi giunti dalla Trinacria"*.  
   - Crediti immagini e documentari d'epoca: *"40.000 sostenitori etnei"*.  
   - *Trattamento Epistemico:* Trattandosi di una stima storiografica non telematica antecedente al 1990 con difformità tra organi di stampa (*La Sicilia* vs *Corriere dello Sport*), il protocollo impone l'inserimento di un callout informativo esplicito che dia conto dell'oscillazione stimata tra i $35.000$ e i $40.000$ spettatori.

---

### Scheda 7: Altre Pagine Stagionali con Placeholder Sistematici
La scansione dell'intero archivio cronistorico ha rivelato la presenza residua del token `"Avversario"` anche in:
- `content/02-cronistoria/stagioni/1955-1956.md` (23 partite con avversario non valorizzato);
- `content/02-cronistoria/stagioni/1956-1957.md` (25 partite con avversario non valorizzato);
- `content/02-cronistoria/stagioni/2000-2001.md` (1 incontro con avversario non valorizzato).

---

# PARTE III: Registro delle Correzioni Determinate (Actionable Patch Plan)

Nella tabella sottostante viene riepilogato il piano esatto delle correzioni da eseguire sui file del repository non appena l'utente fornirà specifica autorizzazione alla scrittura.

| ID | File Target | Posizione | Stringa Attuale Errata | Valore Corretto Convalidato | Tassonomia |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **01** | `03-tesserati/allenatori/piero-andreoli.md` | YAML `birth_date` | `1911-01-02` | `1911-11-02` | **Type A** |
| **02** | `03-tesserati/allenatori/piero-andreoli.md` | YAML `birth_place` | `Bologna, Italia` | `Verona, Italia` | **Type A** |
| **03** | `03-tesserati/allenatori/piero-andreoli.md` | YAML `death_date` | `1960-03-26` | `1984-06-16` | **Type A** |
| **04** | `03-tesserati/allenatori/piero-andreoli.md` | YAML `death_place` | `Massa, Italia` | `Verona, Italia` | **Type A** |
| **05** | `03-tesserati/calciatori/storici/davide-baiocco.md` | YAML `total_appearances` | `122` | `129` (122 campionato + 7 coppa) | **Type D** |
| **06** | `03-tesserati/calciatori/storici/davide-baiocco.md` | Corpo riga 64 | `Presenze Ufficiali complessive: 122` | `Presenze Ufficiali complessive: 129 (122 in Campionato, 7 in Coppa Italia)` | **Type D** |
| **07** | `03-tesserati/calciatori/storici/giuseppe-mascara.md` | YAML `cover_caption` | `capitano, 236 presenze e 61 reti` | `capitano, 235 presenze e 60 reti` | **Type A** |
| **08** | `03-tesserati/calciatori/storici/giuseppe-mascara.md` | Corpo riga 102 | `al 90' Mascara trasforma il calcio di rigore del definitivo 3-1` | `all'81' Mascara trasforma il rigore del 2-1 (il 3-1 finale sarà di Martínez al 90')` | **Type A** |
| **09** | `01-societa/vicende-legali/caso-catania-2003.md` | Tabella riga 87 | `chiedendo lo 0-2 a tavolino` | `chiedendo la vittoria per 2-0 a tavolino` | **Type B** |
| **10** | `02-cronistoria/partite-storiche/2002-2003/catania-siena-1-1.md` | YAML `scorers[0].team`| `Avversario` | `A.C. Siena` | **Type A** |
| **11** | `02-cronistoria/partite-storiche/2009-2010/catania-inter-3-1.md` | YAML `scorers[0].team`| `Avversario` | `F.C. Internazionale` | **Type A** |
| **12** | `02-cronistoria/partite-storiche/1963-1964/finale-coppa-delle-alpi-1964.md` | YAML `scorers[0-1].team`| `Avversario` | `Genoa C.F.C.` | **Type A** |
| **13** | `02-cronistoria/partite-storiche/2023-2024/finale-coppa-catania-padova-4-2.md` | YAML `scorers[0,2].team`| `Avversario` | `Calcio Padova` | **Type A** |
| **14** | `02-cronistoria/stagioni/1982-1983.md` | Tabella riga 168 | `39ª giornata \| 18 giugno 1983 \| Catania – Avversario` | `Spareggio Promozione \| 18 giugno 1983 \| Catania – Como` | **Type D** |
| **15** | `02-cronistoria/stagioni/1982-1983.md` | Tabella riga 169 | `40ª giornata` | `Spareggio Promozione (2ª gara)` | **Type D** |
| **16** | `02-cronistoria/stagioni/1982-1983.md` | Corpo riga 87 | `davanti a 35.000 tifosi` | Inserimento callout comparativo (stima $35.000 - 40.000$) | **Type C** |

---

## Conclusioni e Prossimi Passi

1. **Integrità del Repository Preservata:** L'intero archivio Markdown e i file di configurazione sono rimasti intonsi al $100\%$, nel pieno rispetto dell'istruzione dell'utente.
2. **Documento di Architettura Revisionato:** Gli errori concettuali di calcolo matematico, le allucinazioni ontologiche nelle query SPARQL e i difetti logici di branching sono stati esplicitati, pronti per essere corretti nella specifica software.
3. **Pronto all'Azione:** Non appena l'utente richiederà di procedere alla correzione, le 16 patch individuate potranno essere applicate in modalità chirurgica e atomica sull'AST dei documenti.
