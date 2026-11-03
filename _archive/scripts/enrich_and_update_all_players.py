import os
import re
import glob
import json
import yaml

# Load Wikidata people
WIKIDATA_MAP = {}
try:
    with open('data/wikimedia_catania_db/wikidata_people.json', 'r', encoding='utf-8') as f:
        wiki_list = json.load(f)
        for p in wiki_list:
            name_clean = p.get('name', '').strip().lower()
            if name_clean:
                WIKIDATA_MAP[name_clean] = p
except Exception as e:
    print("Warning loading wikidata_people:", e)

# Load Current Squad data
try:
    from scripts.current_squad_data import ROSA_ATTUALE_DATA
except Exception:
    ROSA_ATTUALE_DATA = {}

# Load Historic players data
try:
    from scripts.historic_players_data import HISTORIC_PLAYERS_DATA
except Exception:
    HISTORIC_PLAYERS_DATA = {}

def clean_name(title_or_h1):
    t = re.sub(r'^#\s*', '', title_or_h1)
    parts = re.split(r'\s+[—–\-:]\s+', t)
    name = parts[0].strip()
    return name

def extract_years_from_seasons_table(body):
    # Find all season patterns like 1964-1965, 2008-2009, 1934-1935
    seasons = re.findall(r'\b(19\d\d|20\d\d)-(19\d\d|20\d\d)\b', body)
    if not seasons:
        # try single year matches
        singles = re.findall(r'\b(19\d\d|20\d\d)\b', body)
        return [int(y) for y in singles] if singles else []
    
    start_years = [int(s[0]) for s in seasons]
    end_years = [int(s[1]) for s in seasons]
    all_years = sorted(list(set(start_years + end_years)))
    return all_years

def extract_totals_from_table(body):
    # Match row TOTALE
    m = re.search(r'\|\s*\*{0,2}TOTALE\*{0,2}\s*\|[^|]*\|\s*\*{0,2}(\d+)\*{0,2}\s*\|\s*\*{0,2}(\d+)\*{0,2}\s*\|\s*\*{0,2}(\d+|-|—|ND)\*{0,2}\s*\|', body, re.IGNORECASE)
    if m:
        apps = m.group(1)
        goals = m.group(2)
        assists = m.group(3)
        if assists in ['-', '—', 'ND']:
            assists = 'ND'
        return apps, goals, assists
    
    # Try callout
    m2 = re.search(r'complessivamente\s+\*{0,2}(\d+)\s+presenze\s+ufficiali\*{0,2}.*?siglando\s+\*{0,2}(\d+)\s+gol\*{0,2}.*?servendo\s+\*{0,2}(\d+)\s+assist\*{0,2}', body, re.IGNORECASE | re.DOTALL)
    if m2:
        return m2.group(1), m2.group(2), m2.group(3)

    return None, None, None

def format_period(in_rosa, fm, body):
    if in_rosa:
        periods = fm.get('catania_periods')
        if periods and isinstance(periods, list) and len(periods) > 0:
            first_p = str(periods[0])
            m = re.search(r'\b(20\d\d)\b', first_p)
            if m:
                return f"{m.group(1)}–"
        m_arr = re.search(r'\b(202[0-9])\b', body)
        if m_arr:
            return f"{m_arr.group(1)}–"
        return "2024–"

    # Historic player
    periods = fm.get('catania_periods')
    if periods:
        if isinstance(periods, list):
            return ', '.join(str(p).replace('-', '–') for p in periods)
        return str(periods).replace('-', '–')

    # Calculate from table
    years = extract_years_from_seasons_table(body)
    if years:
        min_y = min(years)
        max_y = max(years)
        if min_y == max_y:
            return str(min_y)
        # Check if single season like 1964-1965
        if max_y - min_y == 1:
            return f"{min_y}–{max_y}"
        return f"{min_y}–{max_y}"

    # Fallback search in text
    m = re.search(r'\b(19\d\d[–\-]19\d\d)\b', body)
    if m:
        return m.group(1).replace('-', '–')

    return "ND"

def build_hero_table(name, year, nationality, height, foot, catania_period, apps, goals, assists, photo_url):
    if photo_url:
        photo_cell = f'<img src="{photo_url}" alt="{name}" class="nfc-player-photo" />'
    else:
        photo_cell = '''<div class="nfc-player-no-photo">
        <span class="nfc-no-photo-badge">ND</span>
        <span class="nfc-no-photo-label">Nessuna foto</span>
      </div>'''

    return f'''<div class="nfc-player-hero-card">
  <table class="nfc-player-table">
    <tbody>
      <tr>
        <td class="nfc-player-photo-cell" rowspan="9">
          {photo_cell}
        </td>
        <th>Nome e cognome</th>
        <td>{name}</td>
      </tr>
      <tr>
        <th>Anno</th>
        <td>{year}</td>
      </tr>
      <tr>
        <th>Nazionalità</th>
        <td>{nationality}</td>
      </tr>
      <tr>
        <th>Altezza</th>
        <td>{height}</td>
      </tr>
      <tr>
        <th>Piede</th>
        <td>{foot}</td>
      </tr>
      <tr>
        <th>Al Catania</th>
        <td>{catania_period}</td>
      </tr>
      <tr>
        <th>Presenze totali</th>
        <td>{apps}</td>
      </tr>
      <tr>
        <th>Goal totali</th>
        <td>{goals}</td>
      </tr>
      <tr>
        <th>Assist totali</th>
        <td>{assists}</td>
      </tr>
    </tbody>
  </table>
</div>'''

def process_player(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    fm_raw = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except Exception:
        return False

    slug = os.path.splitext(os.path.basename(file_path))[0]
    in_rosa = fm.get('current_squad') is True or 'rosa-attuale' in file_path.replace('\\', '/')

    # Match name
    h1_m = re.search(r'^#\s+([^\n]+)', body, re.MULTILINE)
    h1_val = h1_m.group(1) if h1_m else ''
    name = clean_name(h1_val or fm.get('title', ''))
    name_lower = name.lower()

    # Pre-fill from current squad or historic data dicts
    ref_data = ROSA_ATTUALE_DATA.get(slug) or HISTORIC_PLAYERS_DATA.get(slug) or {}

    # 1. Year
    year = 'ND'
    b_date = ref_data.get('birth_date') or fm.get('birth_date')
    if b_date:
        ym = re.search(r'\b(19\d\d|20\d\d)\b', str(b_date))
        if ym:
            year = ym.group(1)
    if year == 'ND' and name_lower in WIKIDATA_MAP:
        w_b = WIKIDATA_MAP[name_lower].get('birth_date', '')
        ym = re.search(r'\b(19\d\d|20\d\d)\b', str(w_b))
        if ym:
            year = ym.group(1)
    if year == 'ND':
        ym = re.search(r'\b(?:nato|il)\s+(?:\d{1,2}\s+\w+\s+)?(19\d\d|20\d\d)\b', body, re.IGNORECASE)
        if ym:
            year = ym.group(1)

    # 2. Nationality
    nat = ref_data.get('nationality') or fm.get('nationality') or fm.get('citizenship')
    if not nat and name_lower in WIKIDATA_MAP:
        nat = WIKIDATA_MAP[name_lower].get('country')
    if not nat:
        if 'italiano' in body.lower() or 'italia' in body.lower():
            nat = 'Italia'
        elif 'argentino' in body.lower() or 'argentina' in body.lower():
            nat = 'Argentina'
        else:
            nat = 'Italia'
    nationality = str(nat).strip() if nat else 'Italia'

    # 3. Height
    h_val = ref_data.get('height') or fm.get('height')
    if h_val:
        h_str = str(h_val).strip()
        height = f"{h_str} cm" if h_str.isdigit() else h_str
    else:
        height = 'ND'

    # 4. Foot
    foot = ref_data.get('foot') or fm.get('foot') or fm.get('preferred_foot') or 'ND'

    # 5. Period
    catania_period = format_period(in_rosa, fm, body)

    # 6. Totals
    t_apps, t_goals, t_assists = extract_totals_from_table(body)

    apps_fm = ref_data.get('total_appearances') or fm.get('total_appearances') or fm.get('league_appearances')
    apps = str(apps_fm) if apps_fm is not None else (t_apps or 'ND')

    goals_fm = ref_data.get('total_goals') if ref_data.get('total_goals') is not None else fm.get('total_goals')
    if goals_fm is None:
        goals_fm = fm.get('league_goals')
    goals = str(goals_fm) if goals_fm is not None else (t_goals or 'ND')

    assists_fm = ref_data.get('total_assists') if ref_data.get('total_assists') is not None else fm.get('total_assists')
    if assists_fm is None:
        assists_fm = fm.get('assists')
    assists = str(assists_fm) if assists_fm is not None else (t_assists or 'ND')

    # Photo URL
    photo_url = None
    candidate_img = fm.get('image') or fm.get('cover_image')
    if not candidate_img and 'image_credits' in fm and isinstance(fm['image_credits'], list):
        for ic in fm['image_credits']:
            if isinstance(ic, dict) and 'image_path' in ic:
                ip = str(ic['image_path']).strip()
                if any(ip.lower().endswith(ext) for ext in ['.webp', '.png', '.jpg', '.jpeg']) and not ip.startswith('http'):
                    candidate_img = ip
                    break

    if candidate_img:
        img_str = str(candidate_img).strip()
        if img_str.startswith('http'):
            photo_url = img_str
        else:
            norm = img_str.replace('\\', '/').lstrip('./').lstrip('/')
            idx_assets = norm.find('assets/')
            if idx_assets != -1:
                norm = norm[idx_assets:]
            photo_url = '/' + norm

    if not photo_url:
        m_src = re.search(r'src="([^"]+assets/[^"]+\.(?:webp|png|jpg|jpeg))"', body, re.IGNORECASE)
        if m_src:
            photo_url = m_src.group(1)

    new_table = build_hero_table(name, year, nationality, height, foot, catania_period, apps, goals, assists, photo_url)

    # Replace hero card
    if '<div class="nfc-player-hero-card">' in body:
        body = re.sub(r'<div class="nfc-player-hero-card">[\s\S]*?</table>\s*</div>', new_table, body, count=1)
    else:
        h1_match = re.search(r'^#\s+[^\n]+\n', body, re.MULTILINE)
        if h1_match:
            end_pos = h1_match.end()
            body = body[:end_pos] + '\n' + new_table + '\n\n' + body[end_pos:]
        else:
            body = new_table + '\n\n' + body

    # Fix request 5: "è stato" -> "è" for current squad
    if in_rosa:
        body = re.sub(rf'\*\*{re.escape(name)}\*\*\s+è\s+stato\s+un\s+calciatore', f'**{name}** è un calciatore', body, flags=re.IGNORECASE)
        body = re.sub(r'\bè\s+stato\s+un\s+calciatore\s+del\s+\[\[societa/2022-pelligra-catania-fc\|Catania', 'è un calciatore del [[societa/2022-pelligra-catania-fc|Catania', body, flags=re.IGNORECASE)
        body = re.sub(r'\bè\s+stato\s+un\s+calciatore\s+del\s+Catania', 'è un calciatore del Catania', body, flags=re.IGNORECASE)

    new_content = f"---{fm_raw}---{body}"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

all_files = glob.glob('content/03-tesserati/calciatori/**/*.md', recursive=True)
count = 0
for f in all_files:
    if f.endswith('index.md'):
        continue
    if process_player(f):
        count += 1

print(f"Processed and enriched {count} player files successfully.")
