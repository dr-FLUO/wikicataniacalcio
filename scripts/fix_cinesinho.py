import yaml, re, json
from pathlib import Path
from scripts.lock_guard import register_lock
import csv

p = Path("content/03-tesserati/calciatori/storici/sidney-cunha-cinesinho.md")
content = p.read_text(encoding="utf-8")
parts = content.split("---", 2)
fm = yaml.safe_load(parts[1]) or {}
body = parts[2]

# Cerca Chinesinho nel dataset
csv_path = Path("user-content/transfermarket-scraper/dati_catania/storico_giocatori_statistiche.csv")
rows = []
with open(csv_path, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["Giocatore"].strip() == "Chinesinho":
            rows.append(r)

apps = sum(int(r["Presenze"]) for r in rows if r["Presenze"].isdigit())
goals = sum(int(r["Gol"]) for r in rows if r["Gol"].isdigit())
assists = sum(int(r["Assist"]) for r in rows if r["Assist"].isdigit())
minutes = sum(int(r["Minuti_Giocati"].replace("'", "").replace(".", "")) for r in rows if r["Minuti_Giocati"].replace("'", "").replace(".", "").isdigit())

fm["total_appearances"] = apps
fm["total_goals"] = goals
fm["total_assists"] = assists
fm["minutes_played"] = minutes
fm["seasons_count"] = len(rows)
fm["locked"] = True
fm["locked_date"] = "2026-10-30"
fm["locked_by"] = "quadratura_riconciliazione_alias_dataset"

breakdown_lines = [
    "| Stagione | Ruolo | Presenze | Reti | Assist | Ammonizioni | Espulsioni | Minuti Giocati |",
    "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
]
for r in sorted(rows, key=lambda x: x["\ufeffStagione_ID"]):
    s = int(r["\ufeffStagione_ID"])
    s_label = f"{s-1}-{s}"
    mins = r["Minuti_Giocati"]
    breakdown_lines.append(f"| {s_label} | {r['Ruolo']} | {r['Presenze']} | {r['Gol']} | {r['Assist']} | {r['Gialli']} | {r['Rossi']} | {mins} |")

table_md = "\n\n## Rendimento e Presenze Ufficiali per Stagione\n\n" + "\n".join(breakdown_lines) + f"\n\n*Dati statistici ufficiali aggregati e certificati per il Calcio Catania: {apps} presenze e {goals} reti complessive.*\n"

if "## Rendimento e Presenze Ufficiali per Stagione" in body:
    body = re.sub(r'## Rendimento e Presenze Ufficiali per Stagione[\s\S]*?(?=\n## |\Z)', table_md.strip() + "\n\n", body)
else:
    body = body.rstrip() + table_md

new_fm_text = yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False)
p.write_text(f"---\n{new_fm_text}---\n{body.lstrip()}", encoding="utf-8")
register_lock(p, reason="certificato_riconciliazione_alias")
print("[+] Cinesinho aggiornato con successo!")
