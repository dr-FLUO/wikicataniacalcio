import os
import re
import yaml

from current_squad_data import ROSA_ATTUALE_DATA
from historic_players_data import HISTORIC_PLAYERS_DATA

def build_player_table(name, year, nationality, height, foot, catania_period, appearances, goals, assists, photo_url):
    if photo_url:
        photo_cell = f'<img src="{photo_url}" alt="{name}" class="nfc-player-photo" />'
    else:
        photo_cell = '''<div class="nfc-player-no-photo">
        <span class="nfc-no-photo-badge">ND</span>
        <span class="nfc-no-photo-label">Nessuna foto</span>
      </div>'''

    html = f'''<div class="nfc-player-hero-card">
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
        <td>{appearances}</td>
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
    return html

def process_file(p):
    with open(p, 'r', encoding='utf-8') as fp:
        content = fp.read()

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

    basename = os.path.splitext(os.path.basename(p))[0]
    in_rosa = fm.get('current_squad') is True or 'rosa-attuale' in p.replace('\\', '/')

    # Check if we have enriched data for this player
    enriched = ROSA_ATTUALE_DATA.get(basename) or HISTORIC_PLAYERS_DATA.get(basename)

    if enriched:
        for k, v in enriched.items():
            fm[k] = v

    # Extract name
    h1_match = re.search(r'^#\s+([^\n]+)', body, re.MULTILINE)
    h1_raw = h1_match.group(1) if h1_match else None
    if h1_raw:
        h1_clean = re.sub(r'^#\s*', '', h1_raw)
        name = re.split(r'\s+[—–\-:]\s+', h1_clean)[0].strip()
    else:
        title = fm.get('title', basename.replace('-', ' ').title())
        name = re.split(r'\s+[—–\-:]\s+', title)[0].strip()

    # Extract Year
    birth_date = fm.get('birth_date')
    if birth_date:
        m_yr = re.search(r'\b(19\d\d|20\d\d)\b', str(birth_date))
        year = m_yr.group(1) if m_yr else 'ND'
    else:
        m_body_yr = re.search(r'nato (?:a|il) [^,\n]*\b(19\d\d|20\d\d)\b', body, re.IGNORECASE)
        year = m_body_yr.group(1) if m_body_yr else 'ND'

    # Extract Nationality (Default to Italia for historical Italian leagues if empty)
    nationality = fm.get('nationality') or fm.get('citizenship')
    if not nationality:
        if any(c in body.lower() for c in ['argentina', 'brasil', 'uruguay', 'francia', 'spagna']):
            m_nat = re.search(r'calciatore (argentino|brasiliano|uruguaiano|francese|spagnolo|tedesco)', body, re.IGNORECASE)
            nationality = m_nat.group(1).title() if m_nat else 'Italia'
        else:
            nationality = 'Italia'

    # Height
    height_val = fm.get('height')
    if height_val:
        h_str = str(height_val).strip()
        height = f"{h_str} cm" if h_str.isdigit() else h_str
    else:
        m_h = re.search(r'alto\s+(\d[.,]\d\d|\d{3})\s*(?:m|cm)?', body, re.IGNORECASE)
        if m_h:
            h_raw = m_h.group(1).replace(',', '.')
            if '.' in h_raw:
                height = f"{int(float(h_raw)*100)} cm"
            else:
                height = f"{h_raw} cm"
        else:
            height = 'ND'

    # Foot
    foot = fm.get('foot') or fm.get('preferred_foot')
    if not foot:
        m_foot = re.search(r'piede\s+(destro|sinistro|ambidestro)', body, re.IGNORECASE)
        foot = m_foot.group(1).title() if m_foot else 'ND'

    # Catania period
    periods = fm.get('catania_periods')
    if in_rosa:
        if periods and isinstance(periods, list) and len(periods) > 0:
            first_p = str(periods[0])
            m_p = re.search(r'\b(20\d\d)\b', first_p)
            catania_period = f"{m_p.group(1)}–" if m_p else "2024–"
        else:
            catania_period = "2024–"
    else:
        if periods:
            if isinstance(periods, list):
                cleaned = [str(item).replace('-', '–') for item in periods]
                catania_period = ', '.join(cleaned)
            else:
                catania_period = str(periods).replace('-', '–')
        else:
            m_p = re.search(r'\b(19\d\d[–\-]19\d\d)\b', body)
            catania_period = m_p.group(1).replace('-', '–') if m_p else 'ND'

    # Appearances
    app_val = fm.get('total_appearances') if fm.get('total_appearances') is not None else fm.get('league_appearances')
    appearances = str(app_val) if app_val is not None else 'ND'

    # Goals (If goalkeeper or defender with no goals registered, display '0' instead of 'ND')
    role_str = str(fm.get('role', '')).lower()
    goal_val = fm.get('total_goals') if fm.get('total_goals') is not None else fm.get('league_goals')
    if goal_val is not None:
        goals = str(goal_val)
    elif 'portiere' in role_str or 'difensore' in role_str:
        goals = '0'
    else:
        goals = 'ND'

    # Assists
    assist_val = fm.get('total_assists') if fm.get('total_assists') is not None else fm.get('assists')
    if assist_val is not None:
        assists = str(assist_val)
    elif 'portiere' in role_str:
        assists = '0'
    else:
        assists = 'ND'

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
        m_src = re.search(r'src="([^"]*assets/[^"]+\.(?:webp|png|jpg|jpeg))"', body, re.IGNORECASE)
        if m_src:
            photo_url = m_src.group(1)

    # Clean previous table from body
    body = re.sub(r'<div class="nfc-player-hero-card">[\s\S]*?</table>\s*</div>', '', body)
    body = re.sub(r'<table class="nfc-player-table">[\s\S]*?</table>', '', body)

    # Build new enriched table
    table_html = build_player_table(name, year, nationality, height, foot, catania_period, appearances, goals, assists, photo_url)

    if h1_match:
        h1_full = h1_match.group(0)
        body = body.replace(h1_full, f"{h1_full}\n\n{table_html}\n", 1)
    else:
        body = f"{table_html}\n\n{body}"

    body = re.sub(r'\n{3,}', '\n\n', body)

    # Re-dump frontmatter with updated fields
    new_fm_lines = []
    # keep existing YAML lines and add/update enriched fields
    new_fm_raw = yaml.dump(fm, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{new_fm_raw}---{body}"

    with open(p, 'w', encoding='utf-8') as fp:
        fp.write(new_content)

    return True

def main():
    root_dir = 'content/03-tesserati/calciatori'
    count = 0
    for r, d, files in os.walk(root_dir):
        for f in files:
            if f.endswith('.md') and f not in ['index.md', 'contributo-nazionali.md']:
                p = os.path.join(r, f)
                if process_file(p):
                    count += 1
    print(f"Enriched and updated {count} player files!")

if __name__ == '__main__':
    main()
