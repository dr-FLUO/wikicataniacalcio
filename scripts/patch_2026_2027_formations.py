"""
scripts/patch_2026_2027_formations.py
======================================
Script di bonifica semantica per riallineare tutte le pagine che citano la
stagione 2026-2027, eliminando le allucinazioni anacronistiche sulla guida
tecnica (Domenico Toscano vs Emilio Longo) e sulle formazioni/compagni di reparto
(Sturaro, Inglese, Castellini, Adamonis, Montalto).
"""

import os
import re
from pathlib import Path

def patch_file(path_str, replacements):
    p = Path(path_str)
    if not p.exists():
        print(f"[!] File non trovato: {path_str}")
        return False
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()

    original = text
    for old_s, new_s in replacements:
        if isinstance(old_s, re.Pattern):
            text = old_s.sub(new_s, text)
        else:
            text = text.replace(old_s, new_s)

    if text != original:
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[+] Bonificato con successo: {path_str}")
        return True
    else:
        print(f"[-] Nessuna modifica necessaria o pattern non combaciante: {path_str}")
        return False

def run_all():
    print("--- INIZIO BONIFICA SEMANTICA 2026-2027 ---")

    # 1. Alessandro Quaini
    patch_file(
        "content/03-tesserati/calciatori/rosa-attuale/alessandro-quaini.md",
        [
            (
                re.compile(r"sotto la sapiente regia di \[\[tesserati/allenatori/domenico-toscano\|Domenico Toscano\]\],\s*Quaini agisce da diga metodista davanti alla difesa al fianco di \[\[tesserati/calciatori/stefano-sturaro\|Stefano Sturaro\]\],\s*garantendo equilibrio, geometrie pulite e transizioni rapide da difesa ad attacco\.", re.DOTALL),
                "sotto la guida tecnica di [[03-tesserati/allenatori/emilio-longo|Emilio Longo]], Quaini agisce da diga metodista davanti alla difesa al fianco di [[03-tesserati/calciatori/rosa-attuale/salvatore-aloi|Salvatore Aloi]] ed [[03-tesserati/calciatori/rosa-attuale/emanuele-torrasi|Emanuele Torrasi]], garantendo equilibrio, geometrie pulite e transizioni rapide da difesa ad attacco (andando a segno anche nel blitz esterno di Potenza)."
            ),
            (
                "* [[tesserati/calciatori/stefano-sturaro|Stefano Sturaro: Compagno di reparto]]\n* [[tesserati/calciatori/alessio-castellini|Alessio Castellini: Capitano]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore]]",
                "* [[03-tesserati/calciatori/rosa-attuale/salvatore-aloi|Salvatore Aloi: Compagno di reparto]]\n* [[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini: Capitano]]\n* [[03-tesserati/allenatori/emilio-longo|Emilio Longo: Allenatore]]"
            ),
            (
                "precisione per Toscano",
                "precisione per Longo"
            )
        ]
    )

    # 2. Emanuele Cicerelli
    patch_file(
        "content/03-tesserati/calciatori/rosa-attuale/emanuele-cicerelli.md",
        [
            (
                "## 2. Il Protagonismo con Domenico Toscano",
                "## 2. Il Protagonismo nel Catania di Emilio Longo"
            ),
            (
                re.compile(r"Nella \[\[stagioni/2026-2027\|stagione 2026-2027\]\], schierato da \[\[tesserati/allenatori/domenico-toscano\|Domenico Toscano\]\] come trequartista di sinistra o seconda punta a supporto di \[\[tesserati/calciatori/roberto-inglese\|Roberto Inglese\]\]:\s*\* Ha inanellato prestazioni di altissimo livello, servendo 5 assist decisivi e siglando reti di pregevole fattura, tra cui la spettacolare doppietta nel 6-0 contro il Giugliano\.", re.DOTALL),
                "Nella [[stagioni/2026-2027|stagione 2026-2027]], schierato da [[03-tesserati/allenatori/emilio-longo|Emilio Longo]] come trequartista di sinistra o seconda punta a supporto del bomber [[03-tesserati/calciatori/rosa-attuale/massimo-coda|Massimo Coda]]:\n* Ha inanellato prestazioni di altissimo livello, servendo assist decisivi e risultando il miglior marcatore complessivo (5 reti tra campionato e Coppa Italia), tra cui la spettacolare doppietta nel 6-0 contro il Giugliano."
            ),
            (
                "* [[tesserati/calciatori/roberto-inglese|Roberto Inglese: Compagno di reparto offensivo]]\n* [[tesserati/calciatori/alessio-castellini|Alessio Castellini: Il capitano]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore]]",
                "* [[03-tesserati/calciatori/rosa-attuale/massimo-coda|Massimo Coda: Compagno di reparto offensivo]]\n* [[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini: Il capitano]]\n* [[03-tesserati/allenatori/emilio-longo|Emilio Longo: Allenatore]]"
            )
        ]
    )

    # 3. Gabriel Lunetta
    patch_file(
        "content/03-tesserati/calciatori/rosa-attuale/gabriel-lunetta.md",
        [
            ("- toscano\n", "- emilio-longo\n"),
            (
                "* Nella [[stagioni/2026-2027|stagione 2026-2027]] si è distinto per continuità di rendimento e gol pesanti nelle sfide contro le dirette concorrenti alla promozione.",
                "* Nella [[stagioni/2026-2027|stagione 2026-2027]], con l'avvento in panchina di [[03-tesserati/allenatori/emilio-longo|Emilio Longo]], si è distinto come pendolino di centrocampo per continuità di rendimento e 2 gol pesanti nelle sfide di vertice."
            ),
            (
                "* [[tesserati/calciatori/alessio-castellini|Alessio Castellini: Compagno di catena]]\n* [[tesserati/calciatori/stefano-sturaro|Stefano Sturaro: Centrocampista]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore]]",
                "* [[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini: Capitano e compagno di catena]]\n* [[03-tesserati/calciatori/rosa-attuale/salvatore-aloi|Salvatore Aloi: Centrocampista]]\n* [[03-tesserati/allenatori/emilio-longo|Emilio Longo: Allenatore attuale]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Ex allenatore]]"
            )
        ]
    )

    # 4. Stefano Sturaro
    patch_file(
        "content/03-tesserati/calciatori/archivio/s-z/stefano-sturaro.md",
        [
            ("current_squad: true", "current_squad: false"),
            ("- 2024-2027\n", "- 2024-2026\n"),
            ("2024-2027", "2024-2026"),
            (
                re.compile(r"\* Con l'arrivo del tecnico \[\[tesserati/allenatori/domenico-toscano\|Domenico Toscano\]\] nella \[\[stagioni/2026-2027\|stagione 2026-2027\]\], Sturaro è diventato il punto di riferimento tattico davanti alla difesa, formando con il capitano \[\[tesserati/calciatori/alessio-castellini\|Alessio Castellini\]\] e il bomber \[\[tesserati/calciatori/roberto-inglese\|Roberto Inglese\]\] l'asse portante della formazione rossazzurra\.", re.DOTALL),
                "* Con l'arrivo del tecnico [[tesserati/allenatori/domenico-toscano|Domenico Toscano]] nella [[stagioni/2024-2025|stagione 2024-2025]] e nella successiva [[stagioni/2025-2026|2025-2026]], Sturaro è diventato il punto di riferimento tattico davanti alla difesa, formando con il capitano [[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini]] e il bomber [[03-tesserati/calciatori/archivio/g-l/roberto-inglese|Roberto Inglese]] l'asse portante della formazione rossazzurra."
            ),
            (
                "* [[stagioni/2026-2027|Stagione 2026-2027 del Catania FC]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore rossazzurro]]\n* [[tesserati/calciatori/alessio-castellini|Alessio Castellini: Il capitano etneo]]\n* [[tesserati/calciatori/roberto-inglese|Roberto Inglese: Compagno di reparto]]\n* [[societa/presidenti/ross-pelligra|Ross Pelligra: Proprietà societaria]]",
                "* [[stagioni/2024-2025|Stagione 2024-2025 del Catania FC]]\n* [[stagioni/2025-2026|Stagione 2025-2026 del Catania FC]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore]]\n* [[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini: Capitano]]\n* [[03-tesserati/calciatori/archivio/g-l/roberto-inglese|Roberto Inglese: Compagno di reparto]]\n* [[societa/presidenti/ross-pelligra|Ross Pelligra: Proprietà societaria]]"
            )
        ]
    )

    # 5. Marius Adamonis
    patch_file(
        "content/03-tesserati/calciatori/archivio/a-c/marius-adamonis.md",
        [
            ("current_squad: true", "current_squad: false"),
            ("- 2024-2027\n", "- 2024-2026\n"),
            ("sicurezza tra i pali del Catania FC nella stagione 2026-2027.", "sicurezza tra i pali del Catania FC nel biennio 2024-2026."),
            ("è l'estremo difensore titolare del Catania Football Club", "è stato l'estremo difensore del Catania Football Club dal 2024 al 2026"),
            ("## 2. Il Ruolo Decisivo nel Catania di Toscano", "## 2. Il Ruolo Decisivo nel Catania di Toscano (2024-2026)"),
            ("Nella [[stagioni/2026-2027|stagione 2026-2027]] si è distinto", "Nel biennio 2024-2026 si è distinto"),
            ("[[tesserati/calciatori/alessio-castellini|Alessio Castellini]]", "[[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini]]"),
            (
                "* [[stagioni/2026-2027|Stagione 2026-2027 del Catania FC]]\n* [[tesserati/calciatori/alessio-castellini|Alessio Castellini: Capitano e centrale difensivo]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore]]\n* [[societa/presidenti/ross-pelligra|Ross Pelligra: Il patron]]",
                "* [[stagioni/2024-2025|Stagione 2024-2025 del Catania FC]]\n* [[stagioni/2025-2026|Stagione 2025-2026 del Catania FC]]\n* [[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini: Capitano e compagno di squadra]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore]]\n* [[societa/presidenti/ross-pelligra|Ross Pelligra: Il patron]]"
            )
        ]
    )

    # 6. Adriano Montalto
    patch_file(
        "content/03-tesserati/calciatori/archivio/m-o/adriano-montalto.md",
        [
            ("current_squad: true", "current_squad: false"),
            ("- 2024-2027\n", "- 2024-2026\n"),
            (
                "Approdato a Catania nell'estate del **2024**:\n* Costituisce la spalla ideale o l'alternativa di lusso a [[tesserati/calciatori/roberto-inglese|Roberto Inglese]].\n* Nella [[stagioni/2026-2027|stagione 2026-2027]] si è fatto trovare pronto in ogni circostanza, risultando decisivo sia da titolare sia a partita in corso con gol pesanti da palla inattiva.",
                "Approdato a Catania nell'estate del **2024**:\n* Ha costituito la spalla ideale o l'alternativa di lusso a [[03-tesserati/calciatori/archivio/g-l/roberto-inglese|Roberto Inglese]].\n* Nel biennio 2024-2026 si è fatto trovare pronto in ogni circostanza, risultando decisivo sia da titolare sia a partita in corso con gol pesanti da palla inattiva."
            ),
            (
                "* [[stagioni/2026-2027|Stagione 2026-2027 del Catania FC]]\n* [[tesserati/calciatori/roberto-inglese|Roberto Inglese: Compagno di reparto]]",
                "* [[stagioni/2024-2025|Stagione 2024-2025 del Catania FC]]\n* [[stagioni/2025-2026|Stagione 2025-2026 del Catania FC]]\n* [[03-tesserati/calciatori/archivio/g-l/roberto-inglese|Roberto Inglese: Compagno di reparto]]"
            )
        ]
    )

    # 7. Alessio Castellini
    patch_file(
        "content/03-tesserati/calciatori/archivio/a-c/alessio-castellini.md",
        [
            (
                "Impiegabile indifferentemente come terzino sinistro, difensore centrale o terzo di sinistra nella difesa a tre di [[tesserati/allenatori/domenico-toscano|Domenico Toscano]]:\n* Nella [[stagioni/2026-2027|stagione 2026-2027]], Castellini ha tagliato il traguardo storico delle oltre 120 presenze ufficiali in rossazzurro a soli ventitré anni.",
                "Impiegabile indifferentemente come terzino sinistro, difensore centrale o perno della retroguardia, guidata prima da [[tesserati/allenatori/domenico-toscano|Domenico Toscano]] (2024-2026) e poi da [[03-tesserati/allenatori/emilio-longo|Emilio Longo]] (2026-2027):\n* Nella [[stagioni/2026-2027|stagione 2026-2027]], confermato saldamente capitano e bandiera del club, Castellini ha tagliato il traguardo storico delle oltre 120 presenze ufficiali in rossazzurro a soli ventitré anni."
            ),
            (
                "* [[stagioni/2026-2027|Stagione 2026-2027 del Catania FC]]\n* [[tesserati/calciatori/stefano-sturaro|Stefano Sturaro: Compagno di reparto]]\n* [[tesserati/calciatori/roberto-inglese|Roberto Inglese: Il bomber etneo]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Allenatore]]\n* [[societa/presidenti/ross-pelligra|Ross Pelligra: Il patron]]",
                "* [[stagioni/2026-2027|Stagione 2026-2027 del Catania FC]]\n* [[03-tesserati/allenatori/emilio-longo|Emilio Longo: Allenatore attuale]]\n* [[03-tesserati/calciatori/rosa-attuale/massimo-coda|Massimo Coda: Compagno di squadra]]\n* [[03-tesserati/calciatori/archivio/s-z/stefano-sturaro|Stefano Sturaro: Ex compagno di reparto]]\n* [[03-tesserati/calciatori/archivio/g-l/roberto-inglese|Roberto Inglese: Ex compagno di squadra]]\n* [[tesserati/allenatori/domenico-toscano|Domenico Toscano: Ex allenatore]]\n* [[societa/presidenti/ross-pelligra|Ross Pelligra: Il patron]]"
            )
        ]
    )

    # 8. Reintegrazione Alessio Castellini in 2026-2027.md
    castellini_row = "| **22** | [[03-tesserati/calciatori/archivio/a-c/alessio-castellini\\|Alessio Castellini]] | Italia | D | Confermato | **Capitano**, leader e difensore polivalente |\n"
    p8 = Path("content/02-cronistoria/stagioni/2026-2027.md")
    if p8.exists():
        with open(p8, "r", encoding="utf-8") as f:
            t8 = f.read()
        if "alessio-castellini" not in t8:
            anchor = "| **5** | [[03-tesserati/calciatori/rosa-attuale/marco-perrotta\\|Marco Perrotta]]"
            if anchor in t8:
                t8 = t8.replace(anchor, castellini_row + anchor)
                with open(p8, "w", encoding="utf-8") as f:
                    f.write(t8)
                print("[+] Reintegrato Alessio Castellini in 2026-2027.md")
            else:
                print("[!] Impossibile trovare anchor per Castellini in 2026-2027.md")

    # 9. Reintegrazione Alessio Castellini in rosa-attuale/index.md
    p9 = Path("content/03-tesserati/calciatori/rosa-attuale/index.md")
    if p9.exists():
        with open(p9, "r", encoding="utf-8") as f:
            t9 = f.read()
        if "alessio-castellini" not in t9:
            castellini_row_idx = "| **22** | [[03-tesserati/calciatori/archivio/a-c/alessio-castellini\\|Alessio Castellini]] | Italia | 2003 | 11 / 0 | **Capitano**, leader e difensore polivalente |\n"
            anchor_idx = "| **5** | [[03-tesserati/calciatori/rosa-attuale/marco-perrotta\\|Marco Perrotta]]"
            if anchor_idx in t9:
                t9 = t9.replace(anchor_idx, castellini_row_idx + anchor_idx)
            
            # aggiungi capitano nello staff
            staff_anchor = "* **Allenatore Responsabile**: Emilio Longo\n"
            if staff_anchor in t9:
                t9 = t9.replace(staff_anchor, staff_anchor + "* **Capitano**: [[03-tesserati/calciatori/archivio/a-c/alessio-castellini|Alessio Castellini]]\n")
            
            with open(p9, "w", encoding="utf-8") as f:
                f.write(t9)
            print("[+] Reintegrato Alessio Castellini in rosa-attuale/index.md")

    # 10. Correzione refuso 38ª giornata in 2025-2026.md
    patch_file(
        "content/02-cronistoria/stagioni/2025-2026.md",
        [
            (
                "| 37ª giornata | 26 aprile 2026 | Atalanta U23 – Catania",
                "| 38ª giornata | 26 aprile 2026 | Atalanta U23 – Catania"
            )
        ]
    )

    print("--- BONIFICA COMPLETATA ---")

if __name__ == "__main__":
    run_all()
