import urllib.request
import json
import urllib.parse

# SPARQL query: Get 10 notable players of Calcio Catania (Q2018 or Q114881951) with their birthdate and Wikipedia article
sparql = """
SELECT ?player ?playerLabel ?birthDate ?article WHERE {
  ?player wdt:P54 wd:Q2018 .
  OPTIONAL { ?player wdt:P569 ?birthDate . }
  OPTIONAL {
    ?article schema:about ?player ;
             schema:isPartOf <https://it.wikipedia.org/> .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "it,en". }
}
LIMIT 10
"""

url = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(sparql)
req = urllib.request.Request(url, headers={'User-Agent': 'WikiCalcioCataniaBot/1.0 (test@wikicalciocatania.org)'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

bindings = data.get('results', {}).get('bindings', [])
print(f"Wikidata SPARQL returned {len(bindings)} players:")
for b in bindings:
    name = b.get('playerLabel', {}).get('value')
    bdate = b.get('birthDate', {}).get('value', 'N/A')[:10]
    art = b.get('article', {}).get('value', 'N/A')
    print(f" - {name} (Nato: {bdate}) -> {art}")
