import urllib.request
import json
import urllib.parse

def get_page(title):
    url = f"https://it.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(title)}&prop=wikitext|sections&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

d = get_page("Catania Football Club 2026-2027")
if "error" in d:
    print("Error:", d["error"])
elif "parse" in d:
    wt = d["parse"]["wikitext"]["*"]
    print("Page exists! Length:", len(wt))
    print(wt[:500])
else:
    print("Response:", d)
