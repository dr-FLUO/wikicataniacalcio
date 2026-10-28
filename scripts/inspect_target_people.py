import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open("data/wikimedia_catania_db/wikidata_people.json", encoding="utf-8") as f:
    people = json.load(f)

people_by_name = {p["name"].lower(): p for p in people}

target_names = [
    "Bruno Pizzul", "Alexis Rolín", "Nicola D'Ottavio", "Babú",
    "Generoso Rossi", "Dante Mircoli", "Tomáš Košický", "Marco Romano",
    "Gilberto Pogliano", "Benedetto Stella", "Guilherme Raymundo do Prado",
    "Paolo Dall'Oro", "Renato Miglioli", "Carlo Ravizzoli", "Gyula Mikossy",
    "Giulio Rossi", "Aboubacar Sankharé", "Christian Kanyengele",
    "Pier Luigi Nicoli", "Nello Tedeschini"
]

for name in target_names:
    p = people_by_name.get(name.lower())
    if not p:
        # try fuzzy
        for k, v in people_by_name.items():
            if name.lower() in k or k in name.lower():
                p = v
                break
    print(f"=== {name} ===")
    if p:
        print(f"  QID: {p.get('qid')}, Birth: {p.get('birth_date')} in {p.get('birth_place')}, Country: {p.get('country')}")
        print(f"  Wiki: {p.get('it_wiki_article')}")
        print(f"  Image: {p.get('image_url')}")
    else:
        print("  NOT FOUND in wikidata_people.json")
