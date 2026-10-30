import csv, re, json
from pathlib import Path

csv_path = Path('user-content/transfermarket-scraper/dati_catania/storico_allenatori.csv')
with open(csv_path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Pattern di Dati_Riga:
# Es 1: "Emilio Longo25/08/1973 | 03/07/2026 | 119 giorni | 14 | 1,57" (in carica)
# Es 2: "Domenico Toscano04/08/1971 | 15/04/2026 | 30/06/2026 | 76 giorni | 6 | 1,17"
# Es 3: "Giovan Battista Fabbri08/03/1926 | 15/12/1983 | 30/06/1984 | 198 giorni | 18 | 0,33"
# Es 4: "Maurizio Pellegrino01/03/1966 | 11/09/2002 | 03/11/2002 | 53 giorni | 0 | -"

print(f"Totale righe: {len(rows)}")

parsed = []
for r in rows:
    name = r['Allenatore'].strip()
    data_str = r['Dati_Riga'].strip()
    parts = [p.strip() for p in data_str.split('|')]
    
    # Primo pezzo contiene Nome + data nascita opzionale
    birth_date = ""
    m = re.search(r'(\d{2}/\d{2}/\d{4})', parts[0])
    if m:
        birth_date = m.group(1)
        
    start_date = ""
    end_date = ""
    tenure_days = ""
    matches = ""
    ppm = ""
    
    if len(parts) == 5:
        # start_date, tenure_days, matches, ppm (allenatore in carica o data fine assente)
        start_date = parts[1]
        tenure_days = parts[2]
        matches = parts[3]
        ppm = parts[4]
    elif len(parts) >= 6:
        start_date = parts[1]
        end_date = parts[2]
        tenure_days = parts[3]
        matches = parts[4]
        ppm = parts[5]
    elif len(parts) == 4:
        start_date = parts[1]
        end_date = parts[2]
        tenure_days = parts[3]
    
    parsed.append({
        "name": name,
        "birth_date": birth_date,
        "start_date": start_date,
        "end_date": end_date,
        "tenure_days": tenure_days,
        "matches": matches,
        "ppm": ppm,
        "raw": data_str
    })

print(f"Parsati con successo: {len(parsed)}")
for p in parsed[:10]:
    print(p)
