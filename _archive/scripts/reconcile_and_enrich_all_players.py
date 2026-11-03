import os, sys, glob, re, unicodedata, json, csv
from collections import defaultdict

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.lower().replace('-', ' ').replace('_', ' ')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return ' '.join(s.split())

def norm_k(s):
    return norm(s).replace(' ', '')

print("[1/5] Caricamento dataset statistico Transfermarkt...")
CSV_STAT = "user-content/transfermarket-scraper/dati_catania/storico_giocatori_statistiche.csv"
with open(CSV_STAT, 'r', encoding='utf-8', errors='replace') as fp:
    stat_rows = list(csv.DictReader(fp))

tm_by_norm = {}
tm_by_id = {}

for r in stat_rows:
    p_name = r.get('Giocatore', '').strip()
    if not p_name: continue
    
    season_raw = r.get('\ufeffStagione_ID') or r.get('Stagione_ID', '')
    if not season_raw.isdigit(): continue
    season_id = int(season_raw)
    
    tm_id = r.get('TM_Player_ID', '').strip()
    role = r.get('Ruolo', '').strip()
    profile_url = r.get('URL_Profilo', '').strip()
    eta_raw = r.get('Eta', '').strip()
    eta = int(eta_raw) if eta_raw.isdigit() else None
    
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
    minutes = int(raw_min) if raw_min.isdigit() else 0
    
    key = norm_k(p_name)
    if key not in tm_by_norm:
        tm_by_norm[key] = {
            'tm_id': tm_id,
            'name': p_name,
            'role': role,
            'profile_url': profile_url,
            'etas': [],
            'seasons': set(),
            'breakdown': [],
            'appearances': 0,
            'goals': 0,
            'assists': 0,
            'yellows': 0,
            'reds': 0,
            'minutes': 0
        }
    
    entry = tm_by_norm[key]
    entry['seasons'].add(season_id)
    if eta is not None:
        entry['etas'].append((season_id, eta))
    entry['appearances'] += apps
    entry['goals'] += goals
    entry['assists'] += assists
    entry['yellows'] += yellows
    entry['reds'] += reds
    entry['minutes'] += minutes
    entry['breakdown'].append({
        'season_id': season_id,
        'season_label': f"{season_id}-{season_id+1}",
        'role': role,
        'apps': apps,
        'goals': goals,
        'assists': assists,
        'yellows': yellows,
        'reds': reds,
        'minutes': minutes
    })
    if tm_id:
        tm_by_id[tm_id] = entry

print(f"  -> {len(tm_by_norm)} giocatori unici caricati da Transfermarkt.")

print("[2/5] Caricamento Wikidata People...")
with open('data/wikimedia_catania_db/wikidata_people.json', 'r', encoding='utf-8') as fp:
    wp_list = json.load(fp)

wp_dict = {}
for p in wp_list:
    n_k = norm_k(p.get('name', ''))
    if n_k:
        wp_dict[n_k] = p

print(f"  -> {len(wp_dict)} record Wikidata caricati.")

print("[3/5] Caricamento catania_rosa.csv...")
CSV_ROSA = "user-content/transfermarket-scraper/dati_catania/catania_rosa.csv"
rosa_dict = {}
with open(CSV_ROSA, 'r', encoding='utf-8') as fp:
    for r in csv.DictReader(fp):
        g = r.get('Giocatore', '').strip()
        if g:
            rosa_dict[norm_k(g)] = r

print(f"  -> {len(rosa_dict)} record rosa attuale caricati.")

# Mappature esplicite di alias e soprannomi
SPECIAL_TM_ALIASES = {
    'papugomez': 'papugomez',
    'alejandrogomez': 'papugomez',
    'chinesinho': 'cinesinho',
    'sidneycunhacinesinho': 'cinesinho',
    'guly': 'guly',
    'guilhermeraymundodoprado': 'guly',
    'babu': 'babu',
    'cate': 'cate',
    'jeda': 'jeda',
    'pia': 'pia',
    'marcelinho': 'marcelinho',
    'jefferson': 'jefferson',
    'reginaldo': 'reginaldo',
    'vicente': 'vicente',
    'tinoparisi': 'tinoparisi',
    'agatinoparisi': 'tinoparisi',
    'cristiandefalco': 'cristiandefalco',
    'christiandefalco': 'cristiandefalco',
    'klavsbethers': 'klavsbethers',
    'marianoandujar': 'marianoandujar',
    'marianoizco': 'marianoizco',
    'matiassilvestre': 'matiassilvestre',
    'jorgemartinez': 'jorgemartinez',
    'nicolasspolli': 'nicolasspolli',
    'pablobarrientos': 'pablobarrientos',
    'pabloledesma': 'pabloledesma',
    'pablosebastianalvarez': 'pablosebastianalvarez',
}

# Bio arricchite manuali per casi specifici
MANUAL_BIO = {
    'klavsbethers': {
        'anno': '2003',
        'birth_date': '2003-12-24',
        'birth_place': 'Aizpute',
        'nationality': 'Lettonia',
        'height': '191 cm',
        'foot': 'Destro'
    },
    'marianoandujar': {
        'anno': '1983',
        'birth_date': '1983-07-30',
        'birth_place': 'Buenos Aires',
        'nationality': 'Argentina',
        'height': '194 cm',
        'foot': 'Destro'
    },
    'alejandrogomez': {
        'anno': '1988',
        'birth_date': '1988-02-15',
        'birth_place': 'Buenos Aires',
        'nationality': 'Argentina',
        'height': '167 cm',
        'foot': 'Destro'
    },
    'marianoizco': {
        'anno': '1983',
        'birth_date': '1983-03-13',
        'birth_place': 'Buenos Aires',
        'nationality': 'Argentina',
        'height': '178 cm',
        'foot': 'Destro'
    },
    'matiassilvestre': {
        'anno': '1984',
        'birth_date': '1984-09-25',
        'birth_place': 'Mercedes',
        'nationality': 'Argentina',
        'height': '185 cm',
        'foot': 'Destro'
    },
    'jorgemartinez': {
        'anno': '1983',
        'birth_date': '1983-04-05',
        'birth_place': 'Montevideo',
        'nationality': 'Uruguay',
        'height': '178 cm',
        'foot': 'Destro'
    },
    'tinoparisi': {
        'anno': '1995',
        'birth_date': '1995-06-14',
        'birth_place': 'Siracusa',
        'nationality': 'Italia',
        'height': '175 cm',
        'foot': 'Destro'
    },
    'agatinoparisi': {
        'anno': '1995',
        'birth_date': '1995-06-14',
        'birth_place': 'Siracusa',
        'nationality': 'Italia',
        'height': '175 cm',
        'foot': 'Destro'
    },
    'alessandroalbertini': {
        'anno': '1994',
        'birth_date': '1994-04-25',
        'birth_place': 'Bologna',
        'nationality': 'Italia',
        'height': '179 cm',
        'foot': 'Destro'
    },
    'alessandroarena': {
        'anno': '2000',
        'birth_date': '2000-08-03',
        'birth_place': 'Marina di Ragusa',
        'nationality': 'Italia',
        'height': '171 cm',
        'foot': 'Sinistro'
    },
    'alessandrocelli': {
        'anno': '1994',
        'birth_date': '1994-01-28',
        'birth_place': 'Roma',
        'nationality': 'Italia',
        'height': '186 cm',
        'foot': 'Sinistro'
    },
    'agapiosvrikkis': {
        'anno': '2001',
        'birth_date': '2001-05-03',
        'birth_place': 'Nicosia',
        'nationality': 'Cipro',
        'height': '184 cm',
        'foot': 'Destro'
    }
}

print("[4/5] Elaborazione e riparazione schede calciatori...")
files = glob.glob('content/03-tesserati/calciatori/**/*.md', recursive=True)
files = [f.replace('\\', '/') for f in files if not f.endswith('index.md') and not f.endswith('contributo-nazionali.md')]

html_fixes = 0
stat_updates = 0
bio_updates = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    stem = os.path.splitext(os.path.basename(f))[0]
    norm_s = norm_k(stem)
    
    modified = False
    
    # 1. RIPARAZIONE HTML CORROTTO (PHOTO CREDIT)
    # Cerca la corruzione dove dentro nfc-player-photo-credit c'è ## Fonti o ---
    if 'nfc-player-photo-credit' in content:
        # Ripara blocco malformato
        bad_credit_match = re.search(r'<div class="nfc-player-photo-credit">[\s\S]*?(?:## Fonti e Bibliografia[\s\S]*?)(?:1\.)?</div>', content)
        if bad_credit_match:
            fixed_credit = '<div class="nfc-player-photo-credit">[[07-media-e-comunicazione/testate/calciocatania-com|Archivio Storico CalcioCatania.com]]</div>'
            content = content[:bad_credit_match.start()] + fixed_credit + content[bad_credit_match.end():]
            html_fixes += 1
            modified = True
            
        # Pulisci eventuali doppi div non chiusi
        content = re.sub(r'<div class="nfc-player-photo-credit">([^<]*?)---[\s\S]*?</div>', r'<div class="nfc-player-photo-credit">\1</div>', content)

    # 2. MATCHING CON TRANSFERMARKT
    matched_tm = None
    # 2.1 Alias esplicito
    if norm_s in SPECIAL_TM_ALIASES:
        target = SPECIAL_TM_ALIASES[norm_s]
        if target in tm_by_norm:
            matched_tm = tm_by_norm[target]
    # 2.2 Norm diretto
    if not matched_tm and norm_s in tm_by_norm:
        matched_tm = tm_by_norm[norm_s]
    # 2.3 Stem contiene o è contenuto
    if not matched_tm:
        for tmk, pdata in tm_by_norm.items():
            if len(tmk) > 4 and (tmk == norm_s or tmk in norm_s or norm_s in tmk):
                matched_tm = pdata
                break

    # 3. AGGIORNAMENTO STATISTICHE E STAGIONI CORRETTE (y a y+1)
    if matched_tm:
        tm_apps = matched_tm['appearances']
        tm_goals = matched_tm['goals']
        tm_assists = matched_tm['assists']
        tm_minutes = matched_tm['minutes']
        
        # Genera tabella breakdown con formula y a y+1
        breakdown_rows = []
        seasons_sorted = sorted(matched_tm['breakdown'], key=lambda x: x['season_id'])
        for b in seasons_sorted:
            s_label = f"**{b['season_label']}**"
            r_label = b['role'] if b['role'] else 'ND'
            breakdown_rows.append(
                f"| {s_label} | {r_label} | {b['apps']} | {b['goals']} | {b['assists']} | {b['yellows']} | {b['reds']} | {b['minutes']}' |"
            )
        
        tot_row = f"| **TOTALE** | — | **{tm_apps}** | **{tm_goals}** | **{tm_assists}** | **{matched_tm['yellows']}** | **{matched_tm['reds']}** | **{tm_minutes}'** |"
        
        new_breakdown_table = (
            "### Rendimento Stagione per Stagione in Maglia Rossazzurra\n\n"
            "| Stagione | Ruolo Tattico | Presenze | Gol | Assist | Ammonizioni | Espulsioni | Minuti Giocati |\n"
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n" +
            "\n".join(breakdown_rows) + "\n" +
            tot_row + "\n\n" +
            f"> [!info] Dettaglio di Rendimento Agonistico\n"
            f"> In maglia rossazzurra, il calciatore ha collezionato complessivamente **{tm_apps} presenze ufficiali**, disputando **{tm_minutes} minuti** di gioco effettivo, siglando **{tm_goals} gol** e servendo **{tm_assists} assist** distribuiti su **{len(matched_tm['seasons'])} stagioni sportive**."
        )
        
        # Sostituisci o aggiorna tabella rendimento
        if "### Rendimento Stagione per Stagione in Maglia Rossazzurra" in content:
            pattern = r'### Rendimento Stagione per Stagione in Maglia Rossazzurra[\s\S]*?(?=\n## |\n---|\Z)'
            content = re.sub(pattern, new_breakdown_table + "\n\n", content)
            stat_updates += 1
            modified = True
        elif "## Rendimento e Presenze Ufficiali per Stagione" in content:
            pattern = r'## Rendimento e Presenze Ufficiali per Stagione[\s\S]*?(?=\n## |\n---|\Z)'
            content = re.sub(pattern, new_breakdown_table + "\n\n", content)
            stat_updates += 1
            modified = True

        # Aggiorna frontmatter
        content = re.sub(r'^total_appearances:\s*\d+', f"total_appearances: {tm_apps}", content, flags=re.MULTILINE)
        content = re.sub(r'^total_goals:\s*\d+', f"total_goals: {tm_goals}", content, flags=re.MULTILINE)
        content = re.sub(r'^total_assists:\s*\d+', f"total_assists: {tm_assists}", content, flags=re.MULTILINE)
        content = re.sub(r'^minutes_played:\s*\d+', f"minutes_played: {tm_minutes}", content, flags=re.MULTILINE)
        content = re.sub(r'^seasons_count:\s*\d+', f"seasons_count: {len(matched_tm['seasons'])}", content, flags=re.MULTILINE)

    # 4. ARRICCHIMENTO BIOGRAFICO (ANNO, NAZIONALITÀ, ALTEZZA, PIEDE, AL CATANIA)
    anno = None
    nationality = None
    height = None
    foot = None
    
    # 4.1 Manual override
    if norm_s in MANUAL_BIO:
        mb = MANUAL_BIO[norm_s]
        anno = mb.get('anno')
        nationality = mb.get('nationality')
        height = mb.get('height')
        foot = mb.get('foot')
        
    # 4.2 Wikidata
    if norm_s in wp_dict:
        wp_data = wp_dict[norm_s]
        if not anno and wp_data.get('birth_date'):
            anno = wp_data['birth_date'][:4]
        if not nationality and wp_data.get('country'):
            nationality = wp_data['country']
            
    # 4.3 Rosa attuale
    if norm_s in rosa_dict:
        rd = rosa_dict[norm_s]
        eta_str = rd.get('Età', '')
        m_eta = re.search(r'\b(19\d\d|20\d\d)\b', eta_str)
        if m_eta and not anno:
            anno = m_eta.group(1)
            
    # 4.4 Stima Anno da Transfermarkt (Stagione - Età)
    if not anno and matched_tm and matched_tm['etas']:
        s_id, e_val = matched_tm['etas'][0]
        calc_year = s_id - e_val
        anno = str(calc_year)

    # 4.5 Se nazionalità è ancora None o ND, verifica se nel body c'è un'indicazione esplicita
    if not nationality:
        if 'argentin' in content.lower():
            nationality = 'Argentina'
        elif 'brasilian' in content.lower():
            nationality = 'Brasile'
        elif 'urugua' in content.lower():
            nationality = 'Uruguay'
        elif 'letton' in content.lower():
            nationality = 'Lettonia'
        elif 'tedesc' in content.lower():
            nationality = 'Germania'

    # 4.6 Calcolo periodo Al Catania
    catania_period = None
    if matched_tm and matched_tm['seasons']:
        min_s = min(matched_tm['seasons'])
        max_s = max(matched_tm['seasons'])
        if 'rosa-attuale' in f:
            catania_period = f"{min_s}–"
        elif min_s == max_s:
            catania_period = f"{min_s}–{min_s+1}"
        else:
            catania_period = f"{min_s}–{max_s+1}"

    # 4.7 Aggiornamento nfc-player-table
    if 'class="nfc-player-table"' in content:
        # Sostituisci riga Anno e Nazionalità
        if anno:
            content = re.sub(
                r'<th>Anno</th>\s*<td>[^<]*</td>\s*<th>Nazionalità</th>\s*<td>[^<]*</td>',
                f'<th>Anno</th>\n        <td>{anno}</td>\n        <th>Nazionalità</th>\n        <td>{nationality or "ND"}</td>',
                content
            )
            bio_updates += 1
            modified = True
            
        if height or foot:
            curr_h = height or "ND"
            curr_f = foot or "ND"
            content = re.sub(
                r'<th>Altezza</th>\s*<td>[^<]*</td>\s*<th>Piede</th>\s*<td>[^<]*</td>',
                f'<th>Altezza</th>\n        <td>{curr_h}</td>\n        <th>Piede</th>\n        <td>{curr_f}</td>',
                content
            )
            modified = True
            
        if catania_period:
            content = re.sub(
                r'<th>Al Catania</th>\s*<td colspan="3">[^<]*</td>',
                f'<th>Al Catania</th>\n        <td colspan="3">{catania_period}</td>',
                content
            )
            modified = True

        if matched_tm:
            content = re.sub(
                r'<th>Presenze</th>\s*<td>[^<]*</td>\s*<th>Goal / Assist</th>\s*<td>[^<]*</td>',
                f'<th>Presenze</th>\n        <td>{matched_tm["appearances"]}</td>\n        <th>Goal / Assist</th>\n        <td>{matched_tm["goals"]} / {matched_tm["assists"]}</td>',
                content
            )
            modified = True

    if modified:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)

print(f"[5/5] Completato con successo!")
print(f"  - Correzioni HTML photo-credit: {html_fixes}")
print(f"  - Schede con stagioni e statistiche ricalcolate (formula corretta y/y+1): {stat_updates}")
print(f"  - Schede con dati anagrafici e nazionalità arricchiti: {bio_updates}")
