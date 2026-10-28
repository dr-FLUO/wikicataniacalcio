import json
import urllib.request
import ssl
import os
import re
import concurrent.futures

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}
dest_dir = 'content/assets/images/players'
os.makedirs(dest_dir, exist_ok=True)

with open('data/calciocatania_all_players.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

to_download = [p for p in players if p.get('thumb')]
print(f"Total avatars to download: {len(to_download)}")

def download_one(p):
    pid = p['id']
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', p['name'].lower().replace(' ', '-'))
    ext = '.jpg'
    if '.png' in p['thumb'].lower():
        ext = '.png'
    filename = f"{pid}_{safe_name}{ext}"
    filepath = os.path.join(dest_dir, filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
        return pid, filename, True

    try:
        req = urllib.request.Request(p['thumb'], headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
        if len(data) > 500:
            with open(filepath, 'wb') as out:
                out.write(data)
            return pid, filename, True
        return pid, None, False
    except Exception:
        return pid, None, False

# Download with 8 threads for speed
downloaded = 0
player_local_images = {}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(download_one, p) for p in to_download]
    for fut in concurrent.futures.as_completed(futures):
        pid, fname, ok = fut.result()
        if ok and fname:
            downloaded += 1
            player_local_images[pid] = f"assets/images/players/{fname}"
        if downloaded % 50 == 0:
            print(f"  Downloaded {downloaded}/{len(to_download)} avatars...", flush=True)

print(f"\nDownload finished! Successfully saved {downloaded} avatar images.")

with open('data/player_local_images.json', 'w', encoding='utf-8') as out:
    json.dump(player_local_images, out, indent=2)

print("Mapping saved to data/player_local_images.json")
