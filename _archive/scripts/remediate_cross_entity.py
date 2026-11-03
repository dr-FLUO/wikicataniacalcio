"""
scripts/remediate_cross_entity.py
=================================
Script per l'esecuzione della Fase 3: Bonifica Automatica Deterministica delle
55 anomalie relazionali identificate durante l'audit.

Azioni eseguite:
1. Ristrutturazione di coach_refs in 22 file di stagioni ufficiali:
   - separazione delle stringhe concatenate in elementi individuali della lista YAML;
   - normalizzazione degli slug con diacritici/accenti (gyorgy-orth, nicolo-nicolosi, jozsef-banas, blagoje-marjanovic, ecc.);
   - trasformazione del testo semplice in wikilink canonici.
2. Correzione di 'current_squad: false' per i 10 calciatori archiviati in 'archivio/'.
3. Inserimento di 'current_squad: true' per i 19 calciatori della rosa attiva 2026-2027 in 'rosa-attuale/'.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from pathlib import Path

VAULT_CONTENT = Path("content")

def patch_file(rel_path, old_pattern, replacement):
    path = VAULT_CONTENT / rel_path
    if not path.exists():
        print(f"[!] File non trovato: {rel_path}")
        return False
    
    text = path.read_text(encoding="utf-8")
    if isinstance(old_pattern, re.Pattern):
        new_text = old_pattern.sub(replacement, text)
    else:
        new_text = text.replace(old_pattern, replacement)
        
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"[+] Bonificato con successo: {rel_path}")
        return True
    else:
        print(f"[-] Nessuna modifica necessaria o pattern non trovato: {rel_path}")
        return False

def remediate_all():
    print("--- AVVIO BONIFICA CROSS-ENTITY (FASE 3) ---")

    # =========================================================================
    # 1. BONIFICA COACH_REFS NELLE STAGIONI
    # =========================================================================
    season_patches = {
        "02-cronistoria/stagioni/1939-1940.md": (
            "- '[[03-tesserati/allenatori/gy-rgy-orth|György Orth]]'",
            "- '[[03-tesserati/allenatori/gyorgy-orth|György Orth]]'"
        ),
        "02-cronistoria/stagioni/1947-1948.md": (
            "- '[[03-tesserati/allenatori/nicol-nicolosi|Nicolò Nicolosi]]'",
            "- '[[03-tesserati/allenatori/nicolo-nicolosi|Nicolò Nicolosi]]'"
        ),
        "02-cronistoria/stagioni/1948-1949.md": (
            "- '[[03-tesserati/allenatori/j-zsef-b-n-s|József Bánás]]'",
            "- '[[03-tesserati/allenatori/jozsef-banas|József Bánás]]'"
        ),
        "02-cronistoria/stagioni/1951-1952.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/nereo-marini-poi-rodolfo-brondi-poi-fioravante-baldi\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/nereo-marini|Nereo Marini]]'\n- '[[03-tesserati/allenatori/rodolfo-brondi|Rodolfo Brondi]]'\n- '[[03-tesserati/allenatori/fioravante-baldi|Fioravante Baldi]]'"
        ),
        "02-cronistoria/stagioni/1952-1953.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/giulio-cappelli-poi-fioravante-baldi\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/giulio-cappelli|Giulio Cappelli]]'\n- '[[03-tesserati/allenatori/fioravante-baldi|Fioravante Baldi]]'"
        ),
        "02-cronistoria/stagioni/1957-1958.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/gipo-poggi-ii\|[^\]]+\]\]'\s*\n-\s*'\[\[03-tesserati/allenatori/riccardo-carapellese\|[^\]]+\]\]'\s*\n-\s*'\[\[03-tesserati/allenatori/nicol-nicolosi\|[^\]]+\]\]'\s*\n-\s*'\[\[03-tesserati/allenatori/francesco-capocasale\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/gipo-poggi|Gipo Poggi]]'\n- '[[03-tesserati/allenatori/riccardo-carapellese|Riccardo Carapellese]]'\n- '[[03-tesserati/allenatori/nicolo-nicolosi|Nicolò Nicolosi]]'\n- '[[03-tesserati/allenatori/francesco-capocasale|Francesco Capocasale]]'"
        ),
        "02-cronistoria/stagioni/1958-1959.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/blagoje-marjanovi\|[^\]]+\]\]'\s*\n-\s*'\[\[03-tesserati/allenatori/carmelo-di-bella\|[^\]]+\]\]'\s*\n-\s*'\[\[03-tesserati/allenatori/felice-borel-ii\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/blagoje-marjanovic|Blagoje Marjanović]]'\n- '[[03-tesserati/allenatori/carmelo-di-bella|Carmelo Di Bella]]'\n- '[[03-tesserati/allenatori/felice-borel|Felice Borel]]'"
        ),
        "02-cronistoria/stagioni/1979-1980.md": (
            re.compile(r"coach_refs:\s*\n-\s*Gennaro Rambone\s*\n-\s*Lino De Petrillo"),
            "coach_refs:\n- '[[03-tesserati/allenatori/gennaro-rambone|Gennaro Rambone]]'\n- '[[03-tesserati/allenatori/lino-de-petrillo|Lino De Petrillo]]'"
        ),
        "02-cronistoria/stagioni/1980-1981.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/lino-de-petrillo-poi-guido-mazzetti\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/lino-de-petrillo|Lino De Petrillo]]'\n- '[[03-tesserati/allenatori/guido-mazzetti|Guido Mazzetti]]'"
        ),
        "02-cronistoria/stagioni/1987-1988.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/osvaldo-jaconi-poi-pietro-santin-poi-bruno-pace\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/osvaldo-jaconi|Osvaldo Jaconi]]'\n- '[[03-tesserati/allenatori/pietro-santin|Pietro Santin]]'\n- '[[03-tesserati/allenatori/bruno-pace|Bruno Pace]]'"
        ),
        "02-cronistoria/stagioni/1989-1990.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/carmelo-russo-poi-angelo-sormani\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/carmelo-russo|Carmelo Russo]]'\n- '[[03-tesserati/allenatori/angelo-sormani|Angelo Sormani]]'"
        ),
        "02-cronistoria/stagioni/1993-1994.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/franco-indelicato-poi-lorenzo-barlassina\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/franco-indelicato|Franco Indelicato]]'\n- '[[03-tesserati/allenatori/lorenzo-barlassina|Lorenzo Barlassina]]'"
        ),
        "02-cronistoria/stagioni/1994-1995.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/pier-giuseppe-mostipoi-angelo-busetta\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/pier-giuseppe-mosti|Pier Giuseppe Mosti]]'\n- '[[03-tesserati/allenatori/angelo-busetta|Angelo Busetta]]'"
        ),
        "02-cronistoria/stagioni/1996-1997.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/angelo-busetta-poi-giovanni-mei\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/angelo-busetta|Angelo Busetta]]'\n- '[[03-tesserati/allenatori/giovanni-mei|Giovanni Mei]]'"
        ),
        "02-cronistoria/stagioni/1997-1998.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/giovanni-mei-poi-franco-gagliardi\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/giovanni-mei|Giovanni Mei]]'\n- '[[03-tesserati/allenatori/franco-gagliardi|Franco Gagliardi]]'"
        ),
        "02-cronistoria/stagioni/1999-2000.md": (
            "- '[[03-tesserati/allenatori/giovanni-simonelli|Giovanni Simonelli]]'",
            "- '[[03-tesserati/allenatori/gianni-simonelli|Gianni Simonelli]]'"
        ),
        "02-cronistoria/stagioni/2000-2001.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/ivo-iaconi-a-seguire-vincenzo-guerini-a-seguire-ivo-iaconi-a-seguire-vincenzo-guerini\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/ivo-iaconi|Ivo Iaconi]]'\n- '[[03-tesserati/allenatori/vincenzo-guerini|Vincenzo Guerini]]'"
        ),
        "02-cronistoria/stagioni/2001-2002.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/aldo-ammazzalorso-poi-pietro-vierchowod-poi-francesco-graziani\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/aldo-ammazzalorso|Aldo Ammazzalorso]]'\n- '[[03-tesserati/allenatori/pietro-vierchowod|Pietro Vierchowod]]'\n- '[[03-tesserati/allenatori/francesco-graziani|Francesco Graziani]]'"
        ),
        "02-cronistoria/stagioni/2002-2003.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/francesco-graziani-maurizio-pellegrino\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/francesco-graziani|Francesco Graziani]]'\n- '[[03-tesserati/allenatori/maurizio-pellegrino|Maurizio Pellegrino]]'\n- '[[03-tesserati/allenatori/john-toshack|John Toshack]]'\n- '[[03-tesserati/allenatori/edoardo-reja|Edoardo Reja]]'\n- '[[03-tesserati/allenatori/vincenzo-guerini|Vincenzo Guerini]]'"
        ),
        "02-cronistoria/stagioni/2004-2005.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/maurizio-costantini-dalla-12-nedo-sonetti\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/maurizio-costantini|Maurizio Costantini]]'\n- '[[03-tesserati/allenatori/nedo-sonetti|Nedo Sonetti]]'"
        ),
        "02-cronistoria/stagioni/2007-2008.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/silvio-baldini-poi-walter-zenga\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/silvio-baldini|Silvio Baldini]]'\n- '[[03-tesserati/allenatori/walter-zenga|Walter Zenga]]'"
        ),
        "02-cronistoria/stagioni/2016-2017.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/giuseppe-rigoli-poi-mario-petrone-poi-giovanni-pulvirenti\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/giuseppe-rigoli|Giuseppe Rigoli]]'\n- '[[03-tesserati/allenatori/mario-petrone|Mario Petrone]]'\n- '[[03-tesserati/allenatori/giovanni-pulvirenti|Giovanni Pulvirenti]]'"
        ),
        "02-cronistoria/stagioni/2020-2021.md": (
            re.compile(r"coach_refs:\s*\n-\s*'\[\[03-tesserati/allenatori/giuseppe-raffaele-poi-francesco-baldini\|[^\]]+\]\]'"),
            "coach_refs:\n- '[[03-tesserati/allenatori/giuseppe-raffaele|Giuseppe Raffaele]]'\n- '[[03-tesserati/allenatori/francesco-baldini|Francesco Baldini]]'"
        ),
    }

    for rel_p, (old_p, new_p) in season_patches.items():
        patch_file(rel_p, old_p, new_p)

    # =========================================================================
    # 2. BONIFICA ARCHIVED CALCIATORI (current_squad: false)
    # =========================================================================
    archived_10 = [
        "03-tesserati/calciatori/archivio/a-c/armando-anastasio.md",
        "03-tesserati/calciatori/archivio/a-c/gianluca-carpani.md",
        "03-tesserati/calciatori/archivio/a-c/klavs-bethers.md",
        "03-tesserati/calciatori/archivio/d-f/francesco-de-rose.md",
        "03-tesserati/calciatori/archivio/d-f/francesco-di-tacchio.md",
        "03-tesserati/calciatori/archivio/g-l/gregorio-luperini.md",
        "03-tesserati/calciatori/archivio/g-l/roberto-inglese.md",
        "03-tesserati/calciatori/archivio/m-o/salvatore-monaco.md",
        "03-tesserati/calciatori/archivio/s-z/luca-verna.md",
        "03-tesserati/calciatori/archivio/s-z/matteo-stoppa.md"
    ]

    for rel_p in archived_10:
        patch_file(rel_p, "current_squad: true", "current_squad: false")

    # =========================================================================
    # 3. BONIFICA ROSA-ATTUALE CALCIATORI (current_squad: true)
    # =========================================================================
    rosa_19 = [
        "03-tesserati/calciatori/rosa-attuale/andrea-allegretto.md",
        "03-tesserati/calciatori/rosa-attuale/andrea-corbari.md",
        "03-tesserati/calciatori/rosa-attuale/andrea-dini.md",
        "03-tesserati/calciatori/rosa-attuale/catello-amendola.md",
        "03-tesserati/calciatori/rosa-attuale/christian-de-falco.md",
        "03-tesserati/calciatori/rosa-attuale/christian-torre.md",
        "03-tesserati/calciatori/rosa-attuale/daniele-donnarumma.md",
        "03-tesserati/calciatori/rosa-attuale/edoardo-masciangelo.md",
        "03-tesserati/calciatori/rosa-attuale/emanuele-torrasi.md",
        "03-tesserati/calciatori/rosa-attuale/filippo-rinaldi.md",
        "03-tesserati/calciatori/rosa-attuale/flavio-russo.md",
        "03-tesserati/calciatori/rosa-attuale/gabriele-pagliai.md",
        "03-tesserati/calciatori/rosa-attuale/giovanni-bruzzaniti.md",
        "03-tesserati/calciatori/rosa-attuale/marco-perrotta.md",
        "03-tesserati/calciatori/rosa-attuale/massimo-coda.md",
        "03-tesserati/calciatori/rosa-attuale/michael-liguori.md",
        "03-tesserati/calciatori/rosa-attuale/nicolo-catania.md",
        "03-tesserati/calciatori/rosa-attuale/salvatore-aloi.md",
        "03-tesserati/calciatori/rosa-attuale/tommaso-di-marco.md"
    ]

    for rel_p in rosa_19:
        p = VAULT_CONTENT / rel_p
        if p.exists():
            txt = p.read_text(encoding="utf-8")
            if "current_squad: true" not in txt:
                # Se c'è un campo role:, inseriamo current_squad: true subito dopo
                m = re.search(r"(role:\s*[^\n]+\n)", txt)
                if m:
                    txt = txt.replace(m.group(1), m.group(1) + "current_squad: true\n")
                    p.write_text(txt, encoding="utf-8")
                    print(f"[+] Impostato current_squad: true in: {rel_p}")
                else:
                    print(f"[!] Impossibile trovare campo role in: {rel_p}")

    print("--- BONIFICA CROSS-ENTITY COMPLETATA ---")

if __name__ == "__main__":
    remediate_all()
