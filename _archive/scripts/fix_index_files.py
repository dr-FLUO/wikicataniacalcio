from pathlib import Path

# 1. Fix 01-societa/presidenti/index.md
p_pres = Path("content/01-societa/presidenti/index.md")
raw_pres = p_pres.read_text(encoding="utf-8")
if "## Fonti e Bibliografia" not in raw_pres:
    raw_pres += """

## Fonti e Bibliografia

- Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino, *Tutto il Catania minuto per minuto (1929-2010)*, GEO Edizioni, Empoli, 2010.
- [Presidenti del Catania Football Club](https://it.wikipedia.org/wiki/Catania_Football_Club#Presidenti) su *Wikipedia, L'enciclopedia libera*.
- Archivio Storico Federale FIGC e registri della Camera di Commercio di Catania.
"""
    p_pres.write_text(raw_pres, encoding="utf-8")

# 2. Fix 03-tesserati/calciatori/archivio/index.md
p_calc = Path("content/03-tesserati/calciatori/archivio/index.md")
raw_calc = p_calc.read_text(encoding="utf-8")
if "## Fonti e Bibliografia" not in raw_calc:
    raw_calc += """

## Fonti e Bibliografia

- Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino, *Tutto il Catania minuto per minuto (1929-2010)*, GEO Edizioni, Empoli, 2010.
- [Archivio Giocatori CalcioCatania.com](https://www.calciocatania.com/giocatori/) a cura di Salvatore Giovanni Emanuele e Max Licari.
- Archivio Storico Federale della Federazione Italiana Giuoco Calcio (FIGC).
"""
    p_calc.write_text(raw_calc, encoding="utf-8")

# 3. Fix 03-tesserati/allenatori/index.md
p_all = Path("content/03-tesserati/allenatori/index.md")
raw_all = p_all.read_text(encoding="utf-8")
# Escape pipes inside the table
raw_all = raw_all.replace("[[03-tesserati/allenatori/carmelo-di-bella|Carmelo Di Bella]]", r"[[03-tesserati/allenatori/carmelo-di-bella\|Carmelo Di Bella]]")
raw_all = raw_all.replace("[[03-tesserati/allenatori/guido-mazzetti|Guido Mazzetti]]", r"[[03-tesserati/allenatori/guido-mazzetti\|Guido Mazzetti]]")
raw_all = raw_all.replace("[[03-tesserati/allenatori/geza-kertesz|Géza Kertész]]", r"[[03-tesserati/allenatori/geza-kertesz\|Géza Kertész]]")
raw_all = raw_all.replace("[[03-tesserati/allenatori/pasquale-marino|Pasquale Marino]]", r"[[03-tesserati/allenatori/pasquale-marino\|Pasquale Marino]]")
raw_all = raw_all.replace("[[03-tesserati/allenatori/gianni-di-marzio|Gianni Di Marzio]]", r"[[03-tesserati/allenatori/gianni-di-marzio\|Gianni Di Marzio]]")
raw_all = raw_all.replace("[[02-cronistoria/partite-storiche/1982-1983/spareggi-roma-1983|Spareggi di Roma 1983]]", r"[[02-cronistoria/partite-storiche/1982-1983/spareggi-roma-1983\|Spareggi di Roma 1983]]")
raw_all = raw_all.replace("[[03-tesserati/allenatori/domenico-toscano|Domenico Toscano]]", r"[[03-tesserati/allenatori/domenico-toscano\|Domenico Toscano]]")

if "## Fonti e Bibliografia" not in raw_all:
    raw_all += """

## Fonti e Bibliografia

- Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino, *Tutto il Catania minuto per minuto (1929-2010)*, GEO Edizioni, Empoli, 2010.
- [Allenatori del Catania Football Club](https://it.wikipedia.org/wiki/Catania_Football_Club#Allenatori) su *Wikipedia, L'enciclopedia libera*.
- Archivio Storico Federale FIGC e Settore Tecnico di Coverciano.
"""
p_all.write_text(raw_all, encoding="utf-8")

print("[OK] All index files fixed.")
