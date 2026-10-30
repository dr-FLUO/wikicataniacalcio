import csv, re
from pathlib import Path

csv_path = Path('user-content/transfermarket-scraper/dati_catania/storico_allenatori.csv')
with open(csv_path, encoding='utf-8') as f:
    for i, r in enumerate(csv.DictReader(f)):
        print(f"[{i}] {r['Allenatore']} -> {r['Dati_Riga']}")
