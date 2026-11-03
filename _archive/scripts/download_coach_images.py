import json, os, urllib.request, urllib.parse, time, glob
from pathlib import Path

USER_AGENT = "WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org; Binary Downloader)"

coach_files = glob.glob("content/03-tesserati/allenatori/**/*.md", recursive=True)
out_dir_allenatori = Path("content/assets/images/allenatori")
out_dir_allenatori.mkdir(parents=True, exist_ok=True)

# Find coach files without image
coaches_to_fetch = []
for cf in coach_files:
    raw = Path(cf).read_text(encoding="utf-8", errors="ignore")
    if "![" not in raw:
        slug = Path(cf).stem
        # Extract title from frontmatter
        title_line = [l for l in raw.splitlines() if l.startswith("title:")][0]
        # title usually: "Achille Piccini — ..."
        coach_name = title_line.replace("title:", "").split("—")[0].split("-")[0].strip().strip('"\'')
        coaches_to_fetch.append((slug, coach_name, cf))

print(f"Total coaches without image: {len(coaches_to_fetch)}")

# Batch query Wikipedia API in chunks of 20
chunk_size = 20
downloaded = 0

for i in range(0, len(coaches_to_fetch), chunk_size):
    chunk = coaches_to_fetch[i:i+chunk_size]
    name_map = {name: (slug, cf) for slug, name, cf in chunk}
    pipe_titles = "|".join(urllib.parse.quote(name) for name in name_map.keys())
    url = f"https://it.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=500&titles={pipe_titles}&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
        pages = data.get("query", {}).get("pages", {})
        for pid, pdata in pages.items():
            t = pdata.get("title")
            thumb = pdata.get("thumbnail", {}).get("source")
            if thumb and t in name_map:
                slug, cf = name_map[t]
                dest = out_dir_allenatori / f"{slug}.jpg"
                if not dest.exists() or dest.stat().st_size < 1000:
                    try:
                        req_img = urllib.request.Request(thumb, headers={"User-Agent": USER_AGENT})
                        with urllib.request.urlopen(req_img) as img_resp:
                            dest.write_bytes(img_resp.read())
                        print(f"  [OK] Downloaded coach image for {slug} ({t})")
                        downloaded += 1
                        time.sleep(0.2)
                    except Exception as err:
                        print(f"  [ERR] {slug}: {err}")
    except Exception as e:
        print(f"  [CHUNK ERR]: {e}")
    time.sleep(0.5)

print(f"[DONE] Total coach images downloaded: {downloaded}")
