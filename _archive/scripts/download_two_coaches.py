import json, os, urllib.request, urllib.parse, sys
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

USER_AGENT = "WikiCalcioCataniaBot/1.0"
out_dir = Path("content/assets/images/allenatori")

for slug, title in [("sinisa-mihajlovic", "Siniša Mihajlović"), ("blagoje-marjanovic", "Blagoje Marjanović")]:
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
            dest = out_dir / f"{slug}.jpg"
            req_img = urllib.request.Request(thumb, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req_img) as img_resp:
                dest.write_bytes(img_resp.read())
            print(f"Downloaded {slug}")
    except Exception as e:
        print(f"Error {slug}: {e}")
