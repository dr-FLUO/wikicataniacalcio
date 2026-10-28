import requests
import json
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WikiCataniaBot/1.0'
}

queries = {
    "cristiano_lucarelli": "Cristiano Lucarelli",
    "domenico_toscano": "Domenico Toscano",
    "egizio_rubino": "Egizio Rubino",
    "guido_mazzetti": "Guido Mazzetti",
    "claudio_ranieri": "Claudio Ranieri",
    "giancarlo_danova": "Giancarlo Danova",
    "giuseppe_vavassori": "Giuseppe Vavassori",
    "loris_boni": "Loris Boni",
    "roberto_sorrentino": "Roberto Sorrentino (calciatore)",
    "amedeo_biavati": "Amedeo Biavati",
    "nicolo_nicolosi": "Nicolò Nicolosi (calciatore)",
    "stefano_sturaro": "Stefano Sturaro",
    "alessio_castellini": "Alessio Castellini",
    "gabriel_lunetta": "Gabriel Lunetta",
    "marius_adamonis": "Marius Adamonis",
    "adriano_montalto": "Adriano Montalto",
    "alessandro_quaini": "Alessandro Quaini",
    "emmanuele_cicerelli": "Emmanuele Cicerelli",
    "antonino_pulvirenti": "Antonino Pulvirenti",
    "pietro_lo_monaco": "Pietro Lo Monaco",
    "santi_maimone": "Santi Maimone",
    "michele_finocchiaro": "Michele Finocchiaro"
}

results = {}

for key, q in queries.items():
    url = f"https://it.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(q)}&prop=pageimages|extracts&exintro=1&explaintext=1&format=json&pithumbsize=600"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        pages = data.get('query', {}).get('pages', {})
        for pid, pdata in pages.items():
            if pid != "-1":
                thumb = pdata.get('thumbnail', {}).get('source')
                results[key] = {
                    "title": pdata.get('title'),
                    "thumb": thumb,
                    "extract": (pdata.get('extract') or '')[:100]
                }
            else:
                results[key] = {"error": "not found"}
    except Exception as e:
        results[key] = {"error": str(e)}

for k, v in results.items():
    print(f"{k}: {v.get('thumb') or v}")
