import json, os, urllib.request, urllib.parse, time
from pathlib import Path

USER_AGENT = "WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org; Binary Downloader)"

# 1. Download missing high priority players
high_priority_targets = [
    ("benedetto-stella", "Benedetto Stella"),
    ("carlo-ravizzoli", "Carlo Ravizzoli"),
    ("christian-kanyengele", "Christian Kanyengele"),
    ("generoso-rossi", "Generoso Rossi"),
    ("gyula-mikossy", "Gyula Mikossy"),
    ("paolo-dall-oro", "Paolo Dall'Oro"),
    ("pier-luigi-nicoli", "Pier Luigi Nicoli"),
    ("renato-miglioli", "Renato Miglioli"),
]

out_dir_calciatori = Path("content/assets/images/calciatori")
out_dir_calciatori.mkdir(parents=True, exist_ok=True)

for slug, title in high_priority_targets:
    dest = out_dir_calciatori / f"{slug}.jpg"
    if dest.exists() and dest.stat().st_size > 1000:
        print(f"[SKIP] {slug} already exists")
        continue
    url = f"https://it.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=500&titles={urllib.parse.quote(title)}&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
        pages = data.get("query", {}).get("pages", {})
        thumb = None
        for pid, pdata in pages.items():
            thumb = pdata.get("thumbnail", {}).get("source")
            if thumb:
                break
        if thumb:
            print(f"[DOWNLOAD] {slug} from {thumb}")
            req_img = urllib.request.Request(thumb, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req_img) as img_resp:
                dest.write_bytes(img_resp.read())
            time.sleep(0.3)
        else:
            print(f"[NO THUMB] {slug} ({title})")
    except Exception as e:
        print(f"[ERROR] {slug}: {e}")

print("[DONE] High priority players images downloaded.")
