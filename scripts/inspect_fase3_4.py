import csv
from pathlib import Path

csv_part = Path("user-content/transfermarket-scraper/dati_catania/storico_partite.csv")
csv_trasf = Path("user-content/transfermarket-scraper/dati_catania/storico_trasferimenti.csv")

with open(csv_part, encoding="utf-8") as f:
    r_part = list(csv.DictReader(f))
    print(f"Partite totali: {len(r_part)}")
    print("Campi partite:", list(r_part[0].keys()) if r_part else [])
    print("Esempio partita:", r_part[0] if r_part else {})

with open(csv_trasf, encoding="utf-8") as f:
    r_trasf = list(csv.DictReader(f))
    print(f"Trasferimenti totali: {len(r_trasf)}")
    print("Campi trasferimenti:", list(r_trasf[0].keys()) if r_trasf else [])
    print("Esempio trasferimento:", r_trasf[0] if r_trasf else {})
