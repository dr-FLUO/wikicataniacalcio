import os
import re
import yaml

def clean_name_from_title(text):
    if not text:
        return 'ND'
    # Remove leading '# '
    text = re.sub(r'^#\s*', '', text)
    # Remove subtitles after —, –, - or :
    parts = re.split(r'\s+[—–\-:]\s+', text)
    name = parts[0].strip()
    return name

def extract_year(birth_date):
    if not birth_date:
        return 'ND'
    s = str(birth_date).strip()
    m = re.search(r'\b(19\d\d|20\d\d)\b', s)
    return m.group(1) if m else 'ND'

def format_catania_period(fm, in_rosa, body):
    periods = fm.get('catania_periods')
    if in_rosa:
        if periods and isinstance(periods, list) and len(periods) > 0:
            first_p = str(periods[0])
            m = re.search(r'\b(20\d\d)\b', first_p)
            if m:
                return f"{m.group(1)}–"
        m = re.search(r'\b(202[0-9])\b', body)
        if m:
            return f"{m.group(1)}–"
        return "2024–"
    else:
        if periods:
            if isinstance(periods, list):
                cleaned = [str(p).replace('-', '–') for p in periods]
                return ', '.join(cleaned)
            return str(periods).replace('-', '–')
        # check if in text there is a year range like (1958-1964)
        m = re.search(r'\b(19\d\d[–\-]19\d\d)\b', body)
        if m:
            return m.group(1).replace('-', '–')
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
</div>'''
    return html

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return False, "No frontmatter"

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, "Invalid frontmatter split"

    fm_raw = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except Exception as e:
        return False, f"YAML error: {e}"

    in_rosa = fm.get('current_squad') is True or 'rosa-attuale' in file_path.replace('\\', '/')

    # Extract name
    h1_match = re.search(r'^#\s+([^\n]+)', body, re.MULTILINE)
    h1_raw = h1_match.group(1) if h1_match else None
    name = clean_name_from_title(h1_raw or fm.get('title', ''))

    # Extract fields
    year = extract_year(fm.get('birth_date'))
    nationality = fm.get('nationality') or fm.get('citizenship') or 'ND'
    
    height_val = fm.get('height')
    if height_val:
        h_str = str(height_val).strip()
        if h_str.isdigit():
            height = f"{h_str} cm"
        else:
            height = h_str
    else:
        height = 'ND'

    foot = fm.get('foot') or fm.get('preferred_foot') or 'ND'
    catania_period = format_catania_period(fm, in_rosa, body)

    app_val = fm.get('total_appearances') if fm.get('total_appearances') is not None else fm.get('league_appearances')
    appearances = str(app_val) if app_val is not None else 'ND'

    goal_val = fm.get('total_goals') if fm.get('total_goals') is not None else fm.get('league_goals')
    goals = str(goal_val) if goal_val is not None else 'ND'

    assist_val = fm.get('total_assists') if fm.get('total_assists') is not None else fm.get('assists')
    assists = str(assist_val) if assist_val is not None else 'ND'

    # Extract photo URL
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
        else:
            m_md = re.search(r'!\[.*?\]\(([^)]*assets/[^)]+\.(?:webp|png|jpg|jpeg))\)', body, re.IGNORECASE)
            if m_md:
                norm = m_md.group(1).replace('\\', '/').lstrip('./').lstrip('/')
                idx_assets = norm.find('assets/')
                if idx_assets != -1:
                    norm = norm[idx_assets:]
                photo_url = '/' + norm

    # Check if there's already an nfc-player-hero-card
    if '<div class="nfc-player-hero-card">' in body:
        # replace existing card
        body = re.sub(r'<div class="nfc-player-hero-card">[\s\S]*?</div>', '', body)

    # Remove isolated image & caption immediately after H1
    # Match: ![...](...) followed optionally by *...*
    body = re.sub(r'(#\s+[^\n]+\n+)\s*!\[.*?\]\(.*?\)\s*\n+(\*.*?\*\s*\n+)?', r'\1\n', body)

    # Remove redundant statistics sections
    # 1. ## 1. Dati di Rendimento in Maglia Rossazzurra
    body = re.sub(r'---\s*\n+## 1\. Dati di Rendimento in Maglia Rossazzurra\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)
    body = re.sub(r'## 1\. Dati di Rendimento in Maglia Rossazzurra\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)

    # 2. ## Dettaglio Statistico di Rendimento (table or bullet list)
    body = re.sub(r'---\s*\n+## Dettaglio Statistico di Rendimento\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)
    body = re.sub(r'## Dettaglio Statistico di Rendimento\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)

    # 3. ## Riepilogo Statistico nel Catania
    body = re.sub(r'---\s*\n+## Riepilogo Statistico nel Catania\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)
    body = re.sub(r'## Riepilogo Statistico nel Catania\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)

    # 4. ## Statistiche di Rendimento nel Calcio Catania
    body = re.sub(r'---\s*\n+## Statistiche di Rendimento nel Calcio Catania\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)
    body = re.sub(r'## Statistiche di Rendimento nel Calcio Catania\s*\n+[\s\S]*?(?=---\s*\n+##|\Z)', '', body)

    # Rename numbering of remaining sections
    body = body.replace('## 2. Note e Scheda di Carriera', '## Note e Scheda di Carriera')
    body = body.replace('## 3. Collegamenti e Voci Correlate', '## Collegamenti e Voci Correlate')
    body = body.replace('## 4. Collegamenti e Voci Correlate', '## Collegamenti e Voci Correlate')

    # Punto 5: For players currently in squad, fix past tense to present
    if in_rosa:
        body = re.sub(r'\bè stato un calciatore\b', 'è un calciatore', body)
        body = re.sub(r'\bè stato un centrocampista\b', 'è un centrocampista', body)
        body = re.sub(r'\bè stato un difensore\b', 'è un difensore', body)
        body = re.sub(r'\bè stato un attaccante\b', 'è un attaccante', body)
        body = re.sub(r'\bè stato un portiere\b', 'è un portiere', body)
        body = re.sub(r'\bè stato il portiere\b', 'è il portiere', body)
        body = re.sub(r'\bè stato\b', 'è', body)
        # Update club link if it links to old matricola 11700
        body = body.replace('[[societa/matricola-11700|Calcio Catania]]', '[[societa/2022-pelligra-catania-fc|Catania Football Club]]')

    # Insert table right after H1
    table_html = build_player_table(name, year, nationality, height, foot, catania_period, appearances, goals, assists, photo_url)
    
    if h1_match:
        h1_full = h1_match.group(0)
        body = body.replace(h1_full, f"{h1_full}\n\n{table_html}\n", 1)
    else:
        body = f"{table_html}\n\n{body}"

    # Clean up double triple blank lines
    body = re.sub(r'\n{3,}', '\n\n', body)

    new_content = f"---{fm_raw}---{body}"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Updated"

def main():
    root_dir = 'content/03-tesserati/calciatori'
    updated = 0
    errors = 0
    for r, d, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                p = os.path.join(r, file)
                success, msg = process_file(p)
                if success:
                    updated += 1
                else:
                    errors += 1
                    print(f"Error on {p}: {msg}")

    print(f"\nProcessing complete! Successfully updated: {updated} player files. Errors: {errors}")

if __name__ == '__main__':
    main()
