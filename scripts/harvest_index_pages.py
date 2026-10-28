import urllib.request
import ssl
import json
import re
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

all_players = []
seen_ids = set()

print("Harvesting 24 index pages from calciocatania.com...")

for page in range(1, 25):
    url = f"https://www.calciocatania.com/giocatori/?page={page}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
            html = resp.read().decode('utf-8', errors='ignore')

        # Find all player card links:
        # <a class="cc-player__link" href="/giocatori/giocatori.php?..."
        blocks = re.findall(
            r'<a[^>]*class="[^"]*cc-player__link[^"]*"[^>]*href="(/giocatori/giocatori\.php\?[^"]+)"[^>]*>(.*?)</a>',
            html,
            re.DOTALL
        )
        if not blocks:
            # Fallback if href comes before class
            blocks = re.findall(
                r'<a[^>]*href="(/giocatori/giocatori\.php\?[^"]+)"[^>]*class="[^"]*cc-player__link[^"]*"[^>]*>(.*?)</a>',
                html,
                re.DOTALL
            )

        page_count = 0
        for href, inner in blocks:
            m_id = re.search(r'\?.*?(\d+)$', href)
            player_id = m_id.group(1) if m_id else href

            if player_id in seen_ids:
                continue
            seen_ids.add(player_id)

            # img
            m_img = re.search(r'<img[^>]+src="([^"]+)"', inner)
            thumb = m_img.group(1) if m_img else None
            if thumb and not thumb.startswith('http'):
                thumb = "https://www.calciocatania.com" + thumb

            # role
            m_role = re.search(r'class="cc-player__role">\s*([^<]+)\s*</span>', inner)
            role = m_role.group(1).strip() if m_role else "Calciatore"

            # name
            m_name = re.search(r'class="cc-player__name">\s*([^<]+)\s*</strong>', inner)
            name = m_name.group(1).strip() if m_name else "Sconosciuto"

            # appearances
            m_app = re.search(r'Presenze\s*<strong>\s*(\d+)\s*</strong>', inner)
            presenze = int(m_app.group(1)) if m_app else 0

            # seasons count
            m_seas = re.search(r'<span>\s*(\d+)\s*stagion[ie]', inner, re.I)
            stagioni_cnt = int(m_seas.group(1)) if m_seas else 1

            all_players.append({
                'id': player_id,
                'name': name,
                'role': role,
                'appearances': presenze,
                'seasons_count': stagioni_cnt,
                'thumb': thumb,
                'url': f"https://www.calciocatania.com{href}"
            })
            page_count += 1

        print(f"  Page {page}/24: extracted {page_count} players (Total unique so far: {len(all_players)})", flush=True)
        time.sleep(0.2)
    except Exception as e:
        print(f"  Page {page} ERROR: {e}", flush=True)

print(f"\nCompleted! Total unique players harvested: {len(all_players)}")

with open('data/calciocatania_all_players.json', 'w', encoding='utf-8') as out:
    json.dump(all_players, out, indent=2, ensure_ascii=False)

print("Saved to data/calciocatania_all_players.json")
