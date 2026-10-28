import json
import pathlib
import re
import urllib.parse
import urllib.request

queries = [
    "Calcio Catania",
    "Stadio Angelo Massimino",
    "Stadio Cibali",
    "Giuseppe Mascara",
    "Gonzalo Bergessio",
    "Francesco Lodi",
    "Diego Simeone",
    "Rolando Maran",
    "Fontana dell Elefante Catania",
    "Marco Biagianti",
    "Mariano Izco",
    "Gionatha Spinesi",
    "Carmelo Di Bella",
    "Angelo Massimino",
]

headers = {
    "User-Agent": "WikiCalcioCataniaBot/1.0 (https://localhost:8080; historical encyclopedia)"
}
results = {}
for q in queries:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": q,
            "gsrnamespace": 6,
            "gsrlimit": 8,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|dimensions",
            "iiurlwidth": 1280,
            "format": "json",
        }
    )
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, pinfo in pages.items():
                title = pinfo.get("title", "")
                if not title.lower().endswith((".jpg", ".jpeg", ".png", ".svg")):
                    continue
                ii = pinfo.get("imageinfo", [{}])[0]
                thumb = ii.get("thumburl") or ii.get("url")
                meta = ii.get("extmetadata", {})
                license_name = meta.get("LicenseShortName", {}).get(
                    "value", "Public Domain / CC"
                )
                artist = re.sub(
                    r"<[^>]+>",
                    "",
                    meta.get("Artist", {}).get("value", "Wikimedia Commons"),
                ).strip()
                results[title] = {
                    "url": thumb,
                    "orig_url": ii.get("url"),
                    "license": license_name,
                    "artist": artist,
                    "w": ii.get("width"),
                    "h": ii.get("height"),
                    "query": q,
                }
    except Exception as e:
        print(f"Error on {q}: {e}")

print(f"Found {len(results)} Wikimedia Commons files:")
for k, v in list(results.items()):
    print(f" - {k} ({v['w']}x{v['h']}) [{v['license']}] [{v['query']}] -> {v['url']}")

pathlib.Path("quartz/static/images/commons_manifest.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
)
