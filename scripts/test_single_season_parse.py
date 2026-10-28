import urllib.request
import json
import urllib.parse
import re

def get_wiki_page(title):
    url = f"https://it.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(title)}&prop=wikitext|sections|images|externallinks&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org)'})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode('utf-8'))

data = get_wiki_page("Calcio Catania 1960-1961")
if "parse" in data:
    p = data["parse"]
    print("Title:", p.get("title"))
    print("Sections:", [s["line"] for s in p.get("sections", [])])
    print("Images:", p.get("images", []))
    print("Ext links count:", len(p.get("externallinks", [])))
    wt = p.get("wikitext", {}).get("*", "")
    print("Wikitext length:", len(wt))
