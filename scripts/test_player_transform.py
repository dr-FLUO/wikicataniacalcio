import os
import re
import yaml

def clean_name_from_title(title, h1_text=None):
    text = h1_text or title
    # Remove leading '# '
    text = re.sub(r'^#\s*', '', text)
    # Remove subtitles after — or : or |
    text = re.split(r'\s+[—–\-:]\s+', text)[0]
    return text.strip()

def extract_year(birth_date):
    if not birth_date:
        return 'ND'
    s = str(birth_date).strip()
    m = re.search(r'\b(19\d\d|20\d\d)\b', s)
    return m.group(1) if m else 'ND'

def format_catania_period(fm, in_rosa):
    periods = fm.get('catania_periods')
    if in_rosa:
        # Se ancora in rosa inserire un -, es. 2023-
        if periods and isinstance(periods, list) and len(periods) > 0:
            first_p = str(periods[0])
            m = re.search(r'\b(20\d\d)\b', first_p)
            if m:
                return f"{m.group(1)}–"
        # fallback to search in file
        return "2024–"
    else:
        if periods:
            if isinstance(periods, list):
                # Clean up each period
                cleaned = [str(p).replace('-', '–') for p in periods]
                return ', '.join(cleaned)
            return str(periods).replace('-', '–')
        return 'ND'

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
</div>
'''
    return html

# Test on alessandro-raimo.md
path = 'content/03-tesserati/calciatori/rosa-attuale/alessandro-raimo.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---', 2)
fm = yaml.safe_load(parts[1])
body = parts[2]

in_rosa = fm.get('current_squad') is True or 'rosa-attuale' in path
name = clean_name_from_title(fm.get('title', 'Alessandro Raimo'))
year = extract_year(fm.get('birth_date'))
nationality = fm.get('nationality') or fm.get('citizenship') or 'Italia'
height = fm.get('height') or 'ND'
foot = fm.get('foot') or fm.get('preferred_foot') or 'ND'
catania_period = format_catania_period(fm, in_rosa)
appearances = fm.get('total_appearances') or fm.get('league_appearances') or 'ND'
goals = fm.get('total_goals') if fm.get('total_goals') is not None else (fm.get('league_goals') if fm.get('league_goals') is not None else 'ND')
assists = fm.get('total_assists') or fm.get('assists') or 'ND'

# Image
photo_url = None
if fm.get('image'):
    img_raw = str(fm['image']).strip()
    if img_raw.startswith('http'):
        photo_url = img_raw
    else:
        photo_url = '/' + img_raw.lstrip('./').lstrip('/')
else:
    m = re.search(r'!\[.*?\]\((/assets/images/[^)]+)\)', body)
    if m:
        photo_url = m.group(1)

table = build_player_table(name, year, nationality, height, foot, catania_period, appearances, goals, assists, photo_url)
print("Generated Table snippet:")
print(table[:400])
