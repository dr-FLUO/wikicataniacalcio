"""
Fase 1: Allineamento e Arricchimento Schede Calciatori dal dataset storico Transfermarkt (1935-2026).
- Aggiorna metadati frontmatter (presenze, gol, assist, minuti, locked: true).
- Aggiorna la tabella hero o tabella statistica di rendimento.
- Aggiunge la cronistoria stagionale certificata anno per anno in tabella e prosa.
- Registra la firma crittografica nel registro centrale locks/locked_entities.json.
"""
import sys, csv, unicodedata, re, json
from pathlib import Path
from collections import defaultdict
import yaml

sys.stdout.reconfigure(encoding='utf-8')
from scripts.lock_guard import register_lock

ROOT = Path("content")
CSV_PATH = Path("user-content/transfermarket-scraper/dati_catania/storico_giocatori_statistiche.csv")

def normalize_name(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.lower().replace('ç', 'c').replace('ø', 'o').replace('ß', 'ss')
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def format_season(s_str):
    if not s_str.isdigit():
        return s_str
    y = int(s_str)
    return f"{y-1}-{y}"

# 1. Carica e aggrega dataset TM
print("[*] Caricamento dataset statistico Transfermarkt...")
with open(CSV_PATH, 'r', encoding='utf-8', errors='replace') as fp:
    reader = csv.DictReader(fp)
    rows = list(reader)

players = defaultdict(lambda: {
    'name': '',
    'role': '',
    'seasons': set(),
    'appearances': 0,
    'goals': 0,
    'assists': 0,
    'yellows': 0,
    'reds': 0,
    'minutes': 0,
    'breakdown': []
})

for r in rows:
    p_name = r.get('Giocatore', '').strip()
    if not p_name: continue
    key = normalize_name(p_name)
    season = r.get('\ufeffStagione_ID') or r.get('Stagione_ID', '')
    role = r.get('Ruolo', '').strip()
    
    raw_app = r.get('Presenze', '').strip()
    apps = int(raw_app) if raw_app.isdigit() else 0
    
    raw_goals = r.get('Gol', '').strip()
    goals = int(raw_goals) if raw_goals.isdigit() else 0
    
    raw_assists = r.get('Assist', '').strip()
    assists = int(raw_assists) if raw_assists.isdigit() else 0

    raw_y = r.get('Gialli', '').strip()
    yellows = int(raw_y) if raw_y.isdigit() else 0

    raw_r = r.get('Rossi', '').strip()
    reds = int(raw_r) if raw_r.isdigit() else 0
    
    raw_min = r.get('Minuti_Giocati', '').replace("'", "").replace('.', '').strip()
    mins = int(raw_min) if raw_min.isdigit() else 0
    
    p = players[key]
    p['name'] = p_name
    if role: p['role'] = role
    p['seasons'].add(season)
    p['appearances'] += apps
    p['goals'] += goals
    p['assists'] += assists
    p['yellows'] += yellows
    p['reds'] += reds
    p['minutes'] += mins
    p['breakdown'].append({
        'season': season,
        'role': role,
        'apps': apps,
        'goals': goals,
        'assists': assists,
        'yellows': yellows,
        'reds': reds,
        'minutes': mins
    })

print(f"[*] Aggregati {len(players)} calciatori unici dal dataset.")

# 2. Mappa file del vault
vault_players = list((ROOT / "03-tesserati/calciatori").rglob("*.md"))
vault_dict = {}
for vp in vault_players:
    if vp.name == "index.md": continue
    norm_stem = normalize_name(vp.stem)
    vault_dict[norm_stem] = vp

# 3. Aggiorna e arricchisce le schede
updated_count = 0

for norm_key, pdata in players.items():
    if norm_key not in vault_dict:
        continue
    
    file_path = vault_dict[norm_key]
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Errore lettura {file_path}: {e}")
        continue
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        continue
        
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        continue
        
    body = parts[2]
    
    # Aggiorna frontmatter
    fm['total_appearances'] = pdata['appearances']
    fm['total_goals'] = pdata['goals']
    fm['total_assists'] = pdata['assists']
    fm['minutes_played'] = pdata['minutes']
    fm['seasons_count'] = len(pdata['seasons'])
    fm['locked'] = True
    fm['locked_date'] = "2026-10-30"
    fm['locked_by'] = "quadratura_transfermarkt_dataset_1935_2026"
    fm['status'] = "verified"
    fm['last_verified_date'] = "2026-10-30"
    
    # Aggiorna o genera descrizione
    role_str = fm.get('role') or pdata['role'] or "Calciatore"
    fm['description'] = f"Biografia, presenze e statistiche ufficiali di {pdata['name']}, {role_str.lower()} del Calcio Catania con {pdata['appearances']} presenze e {pdata['goals']} gol registrati in maglia rossazzurra."

    # Aggiorna hero table se presente
    if '<table class="nfc-player-table">' in body:
        body = re.sub(r'<th>Presenze totali</th>\s*<td>.*?</td>', f'<th>Presenze totali</th>\n        <td>{pdata["appearances"]}</td>', body)
        body = re.sub(r'<th>Goal totali</th>\s*<td>.*?</td>', f'<th>Goal totali</th>\n        <td>{pdata["goals"]}</td>', body)
        body = re.sub(r'<th>Assist totali</th>\s*<td>.*?</td>', f'<th>Assist totali</th>\n        <td>{pdata["assists"]}</td>', body)

    # Costruisci tabella dettagliata anno per anno
    sorted_breakdown = sorted(pdata['breakdown'], key=lambda x: int(x['season']) if x['season'].isdigit() else 0)
    table_rows = []
    for b in sorted_breakdown:
        s_label = format_season(b['season'])
        table_rows.append(f"| **{s_label}** | {b['role'] or '—'} | {b['apps']} | {b['goals']} | {b['assists']} | {b['yellows']} | {b['reds']} | {b['minutes']}' |")
    
    season_table_md = f"""### Rendimento Stagione per Stagione in Maglia Rossazzurra

| Stagione | Ruolo Tattico | Presenze | Gol | Assist | Ammonizioni | Espulsioni | Minuti Giocati |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
{chr(10).join(table_rows)}
| **TOTALE** | — | **{pdata['appearances']}** | **{pdata['goals']}** | **{pdata['assists']}** | **{pdata['yellows']}** | **{pdata['reds']}** | **{pdata['minutes']}'** |

> [!info] Dettaglio di Rendimento Agonistico
> In maglia rossazzurra, **{pdata['name']}** ha collezionato complessivamente **{pdata['appearances']} presenze ufficiali**, disputando **{pdata['minutes']} minuti** di gioco effettivo, siglando **{pdata['goals']} gol** e servendo **{pdata['assists']} assist** distribuiti su **{len(pdata['seasons'])} stagioni sportive**.
"""

    # Rimuovi eventuale vecchia sezione stagione per stagione se già presente
    body = re.split(r'### Rendimento Stagione per Stagione', body)[0]
    
    # Inserisci la nuova tabella prima di Note/Voci Correlate/Fonti
    insert_marker = None
    for marker in ['## Note e Scheda di Carriera', '## Collegamenti e Voci Correlate', '## Collegamenti Interni Correlate', '## Fonti e Bibliografia']:
        if marker in body:
            insert_marker = marker
            break
            
    if insert_marker:
        body_parts = body.split(insert_marker, 1)
        new_body = body_parts[0].rstrip() + "\n\n" + season_table_md + "\n\n" + insert_marker + body_parts[1]
    else:
        new_body = body.rstrip() + "\n\n" + season_table_md

    # Ricomponi file
    out_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=120)
    full_output = f"---\n{out_yaml}---\n{new_body.lstrip()}"
    
    file_path.write_text(full_output, encoding="utf-8")
    register_lock(file_path, "quadratura_transfermarkt_dataset_1935_2026")
    updated_count += 1

print(f"[+] Completata Quadratura e Blindatura Fase 1: {updated_count} schede calciatore arricchite e blindate!")
