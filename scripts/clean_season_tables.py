import re
from pathlib import Path

content = Path("content")

fixes = [
    ("02-cronistoria/stagioni/1930-1931.md", r"\| \*\*Presidente\*\* \| \[\[societa/presidenti/avv\.-andrea-gaudioso\\?\|avv\. Andrea Gaudioso\]\]", "| **Presidente** | Avv. Andrea Gaudioso"),
    ("02-cronistoria/stagioni/1966-1967.md", r"\| \*\*Presidente\*\* \| \[\[societa/presidenti/ignazio-marcoccio-commissario-straordinario\\?\|Ignazio Marcoccio \(Commissario Straordinario\)\]\]", "| **Presidente** | [[societa/presidenti/ignazio-marcoccio\\|Ignazio Marcoccio]] (Commissario Straordinario)"),
    ("02-cronistoria/stagioni/2015-2016.md", r"\| \*\*Presidente\*\* \| \[\[societa/presidenti/carmelo-antonio-milazzo-fino-al-07102015-nicol-micena-fino-al-19042016-davide-franco\\?\|Carmelo Antonio Milazzo \(fino al 07/10/2015\)[^|]*Davide Franco\]\]", "| **Presidente** | Carmelo Antonio Milazzo (fino al 07/10/2015), Nicolò Micena (fino al 19/04/2016), [[societa/presidenti/davide-franco\\|Davide Franco]]"),
    ("02-cronistoria/stagioni/1939-1940.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/mario-sernagiotto-smallpoismallbr-gyrgy-orth\\?\|Mario Sernagiotto[^|]*Gy[^|]*rgy Orth\]\]", "| **Allenatore** | [[tesserati/allenatori/mario-sernagiotto\\|Mario Sernagiotto]], poi [[tesserati/allenatori/gyorgy-orth\\|György Orth]]"),
    ("02-cronistoria/stagioni/1948-1949.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/giovanni-degnibrin-seguito-dalla-nona-giornatabr-jzsef-bns\\?\|Giovanni Degni[^|]*J[^|]*zsef B[^|]*n[^|]*s\]\]", "| **Allenatore** | [[tesserati/allenatori/giovanni-degni\\|Giovanni Degni]], poi dalla 9ª giornata [[tesserati/allenatori/jozsef-banas\\|József Bánás]]"),
    ("02-cronistoria/stagioni/1955-1956.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/piero-andreoli-smallpoi-smallbr-enzo-bellini\\?\|Piero Andreoli[^|]*Enzo Bellini\]\]", "| **Allenatore** | [[tesserati/allenatori/piero-andreoli\\|Piero Andreoli]], poi Enzo Bellini"),
    ("02-cronistoria/stagioni/1967-1968.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/dino-ballaccibr-luigi-valsecchi\\?\|Dino Ballacci[^|]*Luigi Valsecchi\]\]", "| **Allenatore** | [[tesserati/allenatori/dino-ballacci\\|Dino Ballacci]], poi [[tesserati/allenatori/luigi-valsecchi\\|Luigi Valsecchi]]"),
    ("02-cronistoria/stagioni/1975-1976.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/egizio-rubino-small\\?\|Egizio Rubino[^|]*Guido Mazzetti[^|]*\]\]", "| **Allenatore** | [[tesserati/allenatori/egizio-rubino\\|Egizio Rubino]] (1ª-25ª), poi [[tesserati/allenatori/guido-mazzetti\\|Guido Mazzetti]] (26ª-38ª)"),
    ("02-cronistoria/stagioni/1994-1995.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/pier-giuseppe-mostipoi-angelo-busetta\\?\|Pier Giuseppe Mostipoi\s*Angelo Busetta\]\]", "| **Allenatore** | [[tesserati/allenatori/pier-giuseppe-mosti\\|Pier Giuseppe Mosti]], poi [[tesserati/allenatori/angelo-busetta\\|Angelo Busetta]]"),
    ("02-cronistoria/stagioni/2000-2001.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/ivo-iaconi-a-seguire-vincenzo-guerini-a-seguire-ivo-iaconi-a-seguire-vincenzo-guerini\\?\|Ivo Iaconi a seguire\s*Vincenzo Guerini[^|]*\]\]", "| **Allenatore** | [[tesserati/allenatori/ivo-iaconi\\|Ivo Iaconi]], poi [[tesserati/allenatori/vincenzo-guerini\\|Vincenzo Guerini]]"),
    ("02-cronistoria/stagioni/2002-2003.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/francesco-graziani-maurizio-pellegrino\\?\|Francesco Graziani & \s*Maurizio Pellegrino[^|]*\]\]", "| **Allenatore** | [[tesserati/allenatori/francesco-graziani\\|Francesco Graziani]] & [[tesserati/allenatori/maurizio-pellegrino\\|Maurizio Pellegrino]], poi [[tesserati/allenatori/john-toshack\\|John Toshack]], poi [[tesserati/allenatori/vincenzo-guerini\\|Vincenzo Guerini]]"),
    ("02-cronistoria/stagioni/2004-2005.md", r"\| \*\*Allenatore\*\* \| \[\[tesserati/allenatori/maurizio-costantini-dalla-12-nedo-sonetti\\?\|Maurizio Costantini dalla 12[^|]*Nedo Sonetti\]\]", "| **Allenatore** | [[tesserati/allenatori/maurizio-costantini\\|Maurizio Costantini]], dalla 12ª [[tesserati/allenatori/nedo-sonetti\\|Nedo Sonetti]]"),
]

for rel, pat, repl in fixes:
    fp = content / rel
    if fp.exists():
        txt = fp.read_text(encoding="utf-8")
        new_txt, count = re.subn(pat, repl, txt)
        if count > 0:
            fp.write_text(new_txt, encoding="utf-8")
            print(f"[CLEANED] {rel}")
        else:
            print(f"[NOT MATCHED] {rel}")
