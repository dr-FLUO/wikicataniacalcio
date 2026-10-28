import urllib.request
import json
import re

def clean_team_name(val):
    if not val:
        return ""
    val = re.sub(r"\[\[(?:[^\]\|]+\|)?([^\]]+)\]\]", r"\1", val)
    val = re.sub(r"\{\{Calcio\s*([^\}\|]+)(?:\|[^\}]*)?\}\}", r"\1", val)
    val = re.sub(r"\{\{[^\}]*\}\}", "", val)
    return val.strip().strip("|").strip()

def get_matches(title):
    url = f"https://it.wikipedia.org/w/api.php?action=query&prop=revisions&titles={title}&rvprop=content&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "CataniaWikiBot/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        pages = data["query"]["pages"]
        content = list(pages.values())[0]["revisions"][0]["*"]
    
    blocks = re.findall(r"(\{\{Incontro di club.*?\n\}\})", content, re.DOTALL)
    matches = []
    for b in blocks:
        sq1 = re.search(r"\|\s*Squadra\s*1\s*=\s*(.*?)\n", b, re.IGNORECASE)
        sq2 = re.search(r"\|\s*Squadra\s*2\s*=\s*(.*?)\n", b, re.IGNORECASE)
        turno = re.search(r"\|\s*Turno\s*=\s*(.*?)\n", b, re.IGNORECASE)
        data_m = re.search(r"\|\s*Giornomese\s*=\s*(.*?)\n", b, re.IGNORECASE)
        anno = re.search(r"\|\s*Anno\s*=\s*(.*?)\n", b, re.IGNORECASE)
        p1 = re.search(r"\|\s*Punteggio\s*1\s*=\s*(\d+)", b, re.IGNORECASE)
        p2 = re.search(r"\|\s*Punteggio\s*2\s*=\s*(\d+)", b, re.IGNORECASE)
        if sq1 and sq2:
            s1 = clean_team_name(sq1.group(1))
            s2 = clean_team_name(sq2.group(1))
            t = turno.group(1).strip() if turno else ""
            d = data_m.group(1).strip() if data_m else ""
            a = anno.group(1).strip() if anno else ""
            pt1 = p1.group(1).strip() if p1 else ""
            pt2 = p2.group(1).strip() if p2 else ""
            matches.append({
                "turno": t,
                "data": f"{d} {a}".strip(),
                "sq1": s1,
                "sq2": s2,
                "punteggio": f"{pt1}-{pt2}"
            })
    return matches

if __name__ == "__main__":
    for title in ["Club_Calcio_Catania_1955-1956", "Club_Calcio_Catania_1956-1957", "Calcio_Catania_1982-1983"]:
        res = get_matches(title)
        print(f"=== {title} ({len(res)} matches) ===")
        for m in res:
            print(f"  {m['turno']}: {m['sq1']} vs {m['sq2']} ({m['punteggio']}) - {m['data']}")
        with open(f"data/{title}.json", "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
